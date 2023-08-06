include "converters.pyx"


cdef list_objects_recursive(TDirectory* rdir, objects, vector[TClass*]& classes, path=""):
    cdef TList* keys = rdir.GetListOfKeys()
    if keys == NULL:
        raise IOError("unable to get keys in {0}".format(path))
    cdef TClass* tclass
    cdef vector[TClass*].iterator it
    cdef int nkeys = keys.GetEntries()
    cdef TKey* key
    unique_objects = set()  # multiple cycles of the same key may exist
    directories = list()
    for i in range(nkeys):
        key = <TKey*> keys.At(i)
        clsname = str(key.GetClassName())
        if not classes.empty():
            tclass = GetClass(clsname, True, True)
            if tclass != NULL:
                it = classes.begin()
                while it != classes.end():
                    if tclass.InheritsFrom(deref(it)):
                        unique_objects.add(path + str(key.GetName()))
                        break
                    inc(it)
        else:
            unique_objects.add(path + str(key.GetName()))
        if clsname == "TDirectoryFile":
            directories.append(str(key.GetName()))
    objects.extend(unique_objects)
    # recurse on subdirectories
    for dirname in directories:
        # recursively enter lower directory levels
        list_objects_recursive(<TDirectory*> rdir.Get(dirname),
                               objects, classes,
                               path=path + dirname + "/")


def list_objects(fname, types=None):
    cdef TClass* tclass
    # ROOT owns these pointers
    cdef vector[TClass*] classes
    if types is not None:
        for clsname in types:
            tclass = GetClass(clsname, True, True)
            if tclass == NULL:
                raise ValueError("'{0}' is not a ROOT class".format(clsname))
            classes.push_back(tclass)
    cdef TFile* rfile = Open(fname, 'read')
    if rfile == NULL:
        raise IOError("cannot read {0}".format(fname))
    objects = []
    list_objects_recursive(rfile, objects, classes)
    rfile.Close()
    del rfile
    return objects


def list_trees(fname):
    return list_objects(fname, types=['TTree'])


def list_directories(fname):
    return list_objects(fname, types=['TDirectoryFile'])


def list_structures(fname, tree=None):
    if tree == None:
        # automatically select single tree
        tree = list_trees(fname)
        if len(tree) != 1:
            raise ValueError("multiple trees found: {0}".format(', '.join(tree)))
        tree = tree[0]
    cdef TFile* rfile = Open(fname, 'read')
    if rfile == NULL:
        raise IOError("cannot read {0}".format(fname))
    cdef TTree* rtree = <TTree*> rfile.Get(tree)
    if rtree == NULL:
        raise IOError("tree '{0}' not found in {1}".format(tree, fname))
    structure = get_tree_structure(rtree)
    rfile.Close()
    del rfile
    return structure


def list_branches(fname, tree=None):
    return list(list_structures(fname, tree).keys())


cdef get_branch_structure(TBranch* branch):
    cdef TObjArray* leaves
    cdef TLeaf* leaf
    cdef int ileaf
    leaves = branch.GetListOfLeaves()
    if leaves == NULL:
        raise RuntimeError("branch '{0}' has no leaves".format(branch.GetName()))
    leaflist = []
    for ileaf in range(leaves.GetEntries()):
        leaf = <TLeaf*>leaves.At(ileaf)
        leaflist.append((leaf.GetTitle(), resolve_type(leaf.GetTypeName())))
    if not leaflist:
        raise RuntimeError(
            "leaf list for branch '{0}' is empty".format(
                branch.GetName()))
    return leaflist


cdef get_tree_structure(TTree* tree, branches=None):
    cdef int ibranch
    cdef TBranch* branch
    ret = OrderedDict()
    if branches is not None:
        for branch_name in branches:
            branch = tree.GetBranch(branch_name)
            if branch == NULL:
                continue
            ret[branch.GetName()] = get_branch_structure(branch)
        return ret
    # all branches
    cdef TObjArray* all_branches = tree.GetListOfBranches()
    if all_branches == NULL:
        return ret
    for ibranch in range(all_branches.GetEntries()):
        branch = <TBranch*>(all_branches.At(ibranch))
        ret[branch.GetName()] = get_branch_structure(branch)
    return ret


cdef humanize_bytes(long value, int precision=1):
    abbrevs = (
        (1<<50, 'PB'),
        (1<<40, 'TB'),
        (1<<30, 'GB'),
        (1<<20, 'MB'),
        (1<<10, 'kB'),
        (1, 'bytes'))
    if value == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if value >= factor:
            break
    return '%.*f %s' % (precision, value / float(factor), suffix)


cdef handle_load(int load, bool ignore_index=False):
    if load >= 0:
        return
    if load == -1:
        raise ValueError("chain is empty")
    elif load == -2:
        if ignore_index:
            return
        raise IndexError("tree index in chain is out of bounds")
    elif load == -3:
        raise IOError("cannot open current file")
    elif load == -4:
        raise IOError("cannot access tree in current file")
    raise RuntimeError("the chain is not initialized")


ctypedef cpp_map[string, Selector*] selector_map_type
ctypedef pair[string, Selector*] selector_map_item_type


cdef object tree2array(TTree* tree, branches,
                       string selection, object_selection,
                       start, stop, step,
                       bool include_weight, string weight_name,
                       long cache_size):

    if tree.GetNbranches() == 0:
        raise ValueError("tree has no branches")

    cdef int num_requested_branches = 0
    if branches is not None:
        num_requested_branches = len(branches)
        if num_requested_branches == 0:
            raise ValueError("branches is an empty list")

    cdef long long num_entries = tree.GetEntries()
    cdef long long num_entries_selected = 0
    cdef long long ientry

    cdef TreeChain* chain = new TreeChain(tree, cache_size)
    handle_load(chain.Prepare(), True)

    cdef TObjArray* branch_array = tree.GetListOfBranches()
    cdef TObjArray* leaf_array
    cdef TBranch* tbranch
    cdef TLeaf* tleaf

    cdef Column* col
    cdef Converter* conv

    cdef vector[Column*] columns, columns_tmp
    cdef vector[Converter*] converters, converters_tmp
    # Used to preserve branch order if user specified branches:
    cdef vector[vector['Column*']] column_buckets
    cdef vector[vector['Converter*']] converter_buckets

    # Note: Avoid calling FindBranch for each branch since that results in
    # O(n^2) complexity.

    cdef TTreeFormula* selection_formula = NULL
    cdef TTreeFormula* formula = NULL
    cdef int instance
    cdef bool keep

    cdef bool perform_object_selection = False
    if object_selection:
        perform_object_selection = True
    cdef Selector* selector = NULL
    cdef selector_map_type selector_map
    cdef cpp_map[string, Selector*].iterator selector_map_it

    cdef int ibranch, ileaf, branch_idx = 0
    cdef int num_branches = branch_array.GetEntries()
    cdef unsigned int icol, num_columns

    cdef np.ndarray arr
    cdef void* data_ptr
    cdef int num_bytes
    cdef int entry_size
    cdef bool raise_on_zero_read = False

    cdef char* c_string
    cdef bool shortname
    cdef string column_name
    cdef const_char* branch_name
    cdef const_char* leaf_name
    cdef string branch_title
    cdef int branch_title_size
    cdef char type_code

    cdef object branch_dict = None
    cdef object branch_spec = None
    cdef object branch_defaults = dict()

    if num_requested_branches > 0:
        columns.reserve(num_requested_branches)
        converters.reserve(num_requested_branches)
        column_buckets.assign(num_requested_branches, vector['Column*']())
        converter_buckets.assign(num_requested_branches, vector['Converter*']())
    else:
        columns.reserve(num_branches)
        converters.reserve(num_branches)

    try:
        # Set up the entry selection if present
        if selection.size():
            selection_formula = new TTreeFormula("selection", selection.c_str(), tree)
            if selection_formula == NULL or selection_formula.GetNdim() == 0:
                del selection_formula
                raise ValueError(
                    "could not compile selection expression '{0}'".format(selection))
            # The chain will take care of updating the formula leaves when
            # rolling over to the next tree.
            chain.AddFormula(selection_formula)

        if num_requested_branches > 0:
            branch_dict = dict()
            for idx, branch_spec in enumerate(branches):
                if isinstance(branch_spec, tuple):
                    # branch_spec should be (branch_name, fill_value) or
                    # (branch_name, fill_value, length)
                    if len(branch_spec) == 2:
                        # max_length is implicitly equal to one
                        branch_dict[branch_spec[0]] = (idx, 1)
                    elif len(branch_spec) == 3:
                        if branch_spec[2] < 1:
                            raise ValueError(
                                "truncated length must be greater than zero: {0}".format(branch_spec))
                        branch_dict[branch_spec[0]] = (idx, branch_spec[2])
                    else:
                        raise ValueError(
                            "invalid branch tuple: {0}. "
                            "A branch tuple must contain two elements "
                            "(branch_name, fill_value) or three elements "
                            "(branch_name, fill_value, length) "
                            "to yield a single value or truncate, respectively".format(branch_spec))
                    branch_defaults[branch_spec[0]] = branch_spec[1]
                else:
                    branch_dict[branch_spec] = (idx, 0)
            if len(branch_dict) != num_requested_branches:
                raise ValueError("duplicate branches requested")

        # Set up object selection if present
        # Create reverse lookup dictionary mapping field names to Selectors
        if perform_object_selection:
            for subselection, subselection_branches in object_selection.items():
                if not isinstance(subselection_branches, (list, tuple)):
                    subselection_branches = [subselection_branches]
                formula = new TTreeFormula(subselection, subselection, tree)
                if formula == NULL or formula.GetNdim() == 0:
                    del formula
                    raise ValueError(
                        "the expression '{0}' "
                        "is not valid".format(subselection))
                selector = new Selector(formula)
                chain.AddSelector(selector)
                for subselection_branch in subselection_branches:
                    if selector_map.find(subselection_branch) != selector_map.end():
                        # branch shows up under more than one object selection
                        raise ValueError(
                            "attempting to apply multiple object selections "
                            "on branch or expression '{0}'".format(subselection_branch))
                    selector_map.insert(selector_map_item_type(subselection_branch, selector))

        # Keep track of branches seen in tree and warn of duplicates
        seen_branches = set()

        # Build vector of Converters for branches
        branch_spec = None
        for ibranch in range(num_branches):
            tbranch = <TBranch*> branch_array.At(ibranch)
            branch_name = tbranch.GetName()
            if num_requested_branches > 0:
                if len(branch_dict) == 0:
                    # No more branches to consider
                    break
                try:
                    branch_spec = branch_dict.pop(branch_name)
                except KeyError:
                    # This branch was not selected by the user
                    continue
                branch_idx = branch_spec[0]
            elif branch_name in seen_branches:
                warnings.warn("ignoring duplicate branch named '{0}'".format(branch_name),
                              RuntimeWarning)
                # Ignore duplicate branches
                continue
            else:
                seen_branches.add(branch_name)

            branch_title = string(tbranch.GetTitle())
            branch_title_size = branch_title.size()
            if branch_title_size > 2 and branch_title[branch_title_size - 2] == '/':
                type_code = branch_title[branch_title_size - 1]
            else:
                type_code = '\0'
            leaf_array = tbranch.GetListOfLeaves()
            shortname = leaf_array.GetEntries() == 1

            if perform_object_selection:
                # Find selector for this branch if present
                selector_map_it = selector_map.find(string(branch_name))
                if selector_map_it != selector_map.end():
                    selector = deref(selector_map_it).second
                    # Remove this item from the map to check for branches
                    # present in the object_selection but not in the tree or
                    # any fields of the output array
                    selector_map.erase(selector_map_it)
                else:
                    selector = NULL

            for ileaf in range(leaf_array.GetEntries()):
                tleaf = <TLeaf*> leaf_array.At(ileaf)
                leaf_name = tleaf.GetName()
                conv = get_converter(tleaf, type_code)
                if conv != NULL:
                    # A converter exists for this leaf
                    column_name = string(branch_name)
                    if not shortname:
                        column_name.append(<string> '_')
                        column_name.append(leaf_name)

                    if conv.get_dtypecode() != np.NPY_OBJECT:
                        if selector != NULL:
                            raise TypeError(
                                "attempting to apply selection on column '{0}' "
                                "that is not of type 'object'".format(column_name))
                        # We may not read any bytes for empty arrays
                        # otherwise reading zero bytes can be a sign of a
                        # corrupt ROOT file.
                        raise_on_zero_read = True

                    # Create a column for this branch/leaf pair
                    col = new BranchColumn(column_name, tleaf)
                    col.selector = selector

                    if branch_spec is not None:
                        if branch_spec[1] > 0 and not conv.can_truncate():
                            raise TypeError(
                                "unable to truncate column '{0}' "
                                "of type '{1}'".format(
                                    column_name, resolve_type(tleaf.GetTypeName())))
                        col.max_length = branch_spec[1]

                    if num_requested_branches > 0:
                        column_buckets[branch_idx].push_back(col)
                        converter_buckets[branch_idx].push_back(conv)
                    else:
                        columns.push_back(col)
                        converters.push_back(conv)

                    chain.AddColumn(string(branch_name), string(leaf_name),
                                    <BranchColumn*> col)

                elif num_requested_branches > 0:
                    # User explicitly requested this branch but there is no
                    # converter to handle it
                    raise TypeError(
                        "cannot convert leaf '{0}' of branch '{1}' "
                        "with type '{2}'".format(
                            branch_name, leaf_name,
                            resolve_type(tleaf.GetTypeName())))
                else:
                    # Just warn that this branch cannot be converted
                    warnings.warn(
                        "cannot convert leaf '{0}' of branch '{1}' "
                        "with type '{2}' (skipping)".format(
                            branch_name, leaf_name,
                            resolve_type(tleaf.GetTypeName())),
                        RootNumpyUnconvertibleWarning)

        if num_requested_branches > 0:
            # Attempt to interpret remaining "branches" as expressions
            for expression in branch_dict.keys():
                branch_spec = branch_dict[expression]
                branch_idx = branch_spec[0]
                c_string = expression
                formula = new TTreeFormula(c_string, c_string, tree)
                if formula == NULL or formula.GetNdim() == 0:
                    del formula
                    raise ValueError(
                        "the branch or expression '{0}' "
                        "is not present or valid".format(expression))
                # The chain will take care of updating the formula leaves when
                # rolling over to the next tree.
                chain.AddFormula(formula)

                if perform_object_selection:
                    # Find selector for this expression if present
                    selector_map_it = selector_map.find(expression)
                    if selector_map_it != selector_map.end():
                        selector = deref(selector_map_it).second
                        # Remove this item from the map to check for branches
                        # present in the object_selection but not in the tree or
                        # any fields of the output array
                        selector_map.erase(selector_map_it)
                    else:
                        selector = NULL

                """
                ROOT's definition of "multiplicity":

                   -1: Only one or 0 element(s) per entry
                    0: Only one element per entry
                    1: Variable length array
                    2: Fixed length array (nData is the same for all entries)
                """
                if formula.GetMultiplicity() == 0:
                    # single value per entry
                    if formula.IsInteger(False):
                        col = new FormulaColumn['int'](expression, 'Int_t', formula)
                        conv = find_converter_by_typename('int')
                    else:
                        col = new FormulaColumn['double'](expression, 'Double_t', formula)
                        conv = find_converter_by_typename('double')
                    if selector != NULL:
                        raise TypeError(
                            "attempting to apply selection on column '{0}' "
                            "that is not of type object".format(expression))
                elif formula.GetMultiplicity() == -1 or formula.GetMultiplicity() == 1:
                    # variable number of values per entry
                    if formula.IsInteger(False):
                        col = new FormulaArrayColumn['int'](expression, 'Int_t', formula)
                        conv = get_array_converter('int', '[]')
                    else:
                        col = new FormulaArrayColumn['double'](expression, 'Double_t', formula)
                        conv = get_array_converter('double', '[]')
                    col.selector = selector
                else:
                    # fixed number of values per entry
                    if formula.IsInteger(False):
                        col = new FormulaFixedArrayColumn['int'](expression, 'Int_t', formula)
                        conv = get_array_converter('int', '[{0:d}]'.format(formula.GetNdata()))
                    else:
                        col = new FormulaFixedArrayColumn['double'](expression, 'Double_t', formula)
                        conv = get_array_converter('double', '[{0:d}]'.format(formula.GetNdata()))
                    if selector != NULL:
                        raise TypeError(
                            "attempting to apply selection on column '{0}' "
                            "that is not of type object".format(expression))
                if conv == NULL:
                    # Oops, this should never happen
                    raise AssertionError(
                        "could not find a formula converter for '{0}'. "
                        "Please report this bug.".format(expression))

                if branch_spec[1] > 0 and not conv.can_truncate():
                    raise TypeError(
                        "unable to truncate column '{0}' "
                        "with formula of multiplicity={1:d}".format(
                            expression, formula.GetMultiplicity()))
                col.max_length = branch_spec[1]

                column_buckets[branch_idx].push_back(col)
                converter_buckets[branch_idx].push_back(conv)

            # Flatten buckets into 1D vectors, thus preserving branch order
            for branch_idx in range(num_requested_branches):
                columns.insert(columns.end(),
                               column_buckets[branch_idx].begin(),
                               column_buckets[branch_idx].end())
                converters.insert(converters.end(),
                                  converter_buckets[branch_idx].begin(),
                                  converter_buckets[branch_idx].end())

        elif columns.size() == 0:
            raise RuntimeError("unable to convert any branches in this tree")

        if selector_map.size() > 0:
            raise ValueError(
                "object_selection contains branches that are not "
                "present in the tree or included in the output array")

        # Activate branches used by formulae and columns
        chain.InitBranches()

        # Now that we have all the columns we can
        # make an appropriate array structure
        dtype_fields = []
        for icol in range(columns.size()):
            dtype_fields.append((columns[icol].name, converters[icol].get_dtype(columns[icol])))
        if include_weight:
            dtype_fields.append((weight_name, np.dtype('d')))
        dtype = np.dtype(dtype_fields)

        # Determine indices in slice
        indices = xrange(*(slice(start, stop, step).indices(num_entries)))
        num_entries = len(indices)

        # Initialize the array
        try:
            arr = np.empty(num_entries, dtype=dtype)
        except MemoryError:
            # Raise a more informative exception
            raise MemoryError("failed to allocate memory for {0} array of {1} records with {2} fields".format(
                humanize_bytes(dtype.itemsize * num_entries), num_entries, len(dtype_fields)))

        # Fill default values if we will truncate or impute
        for branch_name, branch_default in branch_defaults.items():
            arr[branch_name].fill(branch_default)

        # Exclude weight column in num_columns
        num_columns = columns.size()

        # Loop on entries in the tree and write the data in the array
        for ientry in indices:
            entry_size = chain.GetEntry(ientry)
            handle_load(entry_size)
            if entry_size == 0 and raise_on_zero_read:
                raise IOError("read failure in current tree or requested entry "
                              "does not exist (branches have different lengths?)")

            # Determine if this entry passes the selection,
            # similar to the code in ROOT's tree/treeplayer/src/TTreePlayer.cxx
            if selection_formula != NULL:
                keep = False
                for instance in range(selection_formula.GetNdata()):
                    if selection_formula.EvalInstance(instance) != 0:
                        keep = True
                        break
                if not keep:
                    continue

            if perform_object_selection:
                # Update object selection vectors
                chain.UpdateSelectors()

            # Copy the values into the array
            data_ptr = np.PyArray_GETPTR1(arr, num_entries_selected)
            for icol in range(num_columns):
                col = columns[icol]
                conv = converters[icol]
                num_bytes = conv.write(col, data_ptr)
                data_ptr = shift(data_ptr, num_bytes)
            if include_weight:
                (<double*> data_ptr)[0] = tree.GetWeight()

            # Increment number of selected entries last
            num_entries_selected += 1

    finally:
        # Delete TreeChain
        del chain
        # Delete Columns
        for icol in range(columns.size()):
            del columns[icol]

    # Shrink the array if we selected fewer than num_entries entries
    if num_entries_selected < num_entries:
        arr.resize(num_entries_selected)

    return arr


def root2array_fromfile(fnames, string treename, branches,
                        selection, object_selection, start, stop, step,
                        bool include_weight, string weight_name,
                        long cache_size, bool warn_missing_tree):
    cdef TFile* rfile = NULL
    cdef TTree* tree = NULL
    cdef TChain* chain = new TChain(treename.c_str())
    try:
        for fn in fnames:
            if warn_missing_tree:
                rfile = Open(fn, 'read')
                if rfile == NULL:
                    raise IOError("cannot open file {0}".format(fn))
                tree = <TTree*> rfile.Get(treename.c_str())
                if tree == NULL:
                    # skip this file
                    warnings.warn("tree '{0}' not found in {1}".format(treename, fn),
                                  RuntimeWarning)
                    rfile.Close()
                    del rfile
                    continue
                del tree
                rfile.Close()
                del rfile
            if chain.Add(fn, -1) == 0:
                raise IOError("unable to access tree '{0}' in {1}".format(
                    treename, fn))
        if chain.GetNtrees() == 0:
            raise IOError("none of the input files contain "
                          "the requested tree '{0}'".format(treename))
        ret = tree2array(
            <TTree*> chain, branches,
            selection or '', object_selection,
            start, stop, step,
            include_weight, weight_name, cache_size)
    finally:
        del chain
    return ret


def root2array_fromtree(tree, branches, selection, object_selection,
                        start, stop, step,
                        bool include_weight, string weight_name,
                        long cache_size):
    cdef TTree* rtree = <TTree*> PyCObject_AsVoidPtr(tree)
    return tree2array(
        rtree, branches,
        selection or '', object_selection,
        start, stop, step,
        include_weight, weight_name, cache_size)


cdef TTree* array2tree(np.ndarray arr, string name='tree', TTree* tree=NULL) except *:
    cdef vector[NP2ROOTConverter*] converters
    cdef NP2ROOTConverter* cvt
    cdef vector[int] roffsetarray
    cdef int roffset
    cdef unsigned int icol
    cdef unsigned int num_cols
    cdef SIZE_t arr_len = arr.shape[0]
    cdef SIZE_t idata
    cdef void* source = NULL
    cdef void* thisrow = NULL
    cdef bool own_tree = False

    if tree == NULL:
        own_tree = True
        tree = new TTree(name.c_str(), name.c_str())

    try:
        fieldnames = arr.dtype.names
        fields = arr.dtype.fields

        # Determine the structure
        for icol in range(len(fieldnames)):
            fieldname = fieldnames[icol]
            # roffset is an offset of particular field in each record
            dtype, roffset = fields[fieldname]
            cvt = find_np2root_converter(tree, fieldname, dtype)
            if cvt != NULL:
                roffsetarray.push_back(roffset)
                converters.push_back(cvt)
            else:
                warnings.warn("converter for {!r} is not "
                              "implemented (skipping)".format(dtype))

        # Fill the data
        num_cols = converters.size()
        for idata in range(arr_len):
            thisrow = np.PyArray_GETPTR1(arr, idata)
            for icol in range(num_cols):
                roffset = roffsetarray[icol]
                source = shift(thisrow, roffset)
                converters[icol].fill_from(source)

        # Need to update the number of entries in the tree to match
        # the number in the branches since each branch is filled separately.
        tree.SetEntries(-1)

    except:
        if own_tree:
            del tree
        raise

    finally:
        for icol in range(converters.size()):
            del converters[icol]

    tree.ResetBranchAddresses()
    return tree


def array2tree_toCObj(arr, name='tree', tree=None):
    cdef TTree* intree = NULL
    cdef TTree* outtree = NULL
    if tree is not None:
        intree = <TTree*> PyCObject_AsVoidPtr(tree)
    outtree = array2tree(arr, name=name, tree=intree)
    return PyCObject_FromVoidPtr(outtree, NULL)


def array2root(arr, filename, treename='tree', mode='update'):
    cdef TFile* rfile = Open(filename, mode)
    if rfile == NULL:
        raise IOError("cannot open file {0}".format(filename))
    if not rfile.IsWritable():
        raise IOError("file {0} is not writable".format(filename))
    # If a tree with that name exists, we want to update it
    cdef TTree* tree = <TTree*> rfile.Get(treename)
    tree = array2tree(arr, name=treename, tree=tree)
    tree.Write(treename, kOverwrite)
    del tree
    rfile.Close()
    del rfile
