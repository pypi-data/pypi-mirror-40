
cdef extern from "2to3.h":
    pass 

cdef extern from "util.h":
    cdef void* shift(void*, int)
    void printaddr(void* v)
    cdef cppclass TypeName[T]:
        TypeName()
        const_char* name
    cdef cppclass Vector2Array[T]:
        T* convert(vector[T]* v)
 
cdef extern from "<memory>" namespace "std": 
    cdef cppclass auto_ptr[T]:
        auto_ptr() 
        auto_ptr(T* ptr) 
        reset (T* p)
        T* get()

cdef extern from "Column.h":
    cdef cppclass Column:
        string name
        string type
        Selector* selector
        unsigned_int max_length
        int GetLen()
        int GetCountLen()
        int GetSize()
        void* GetValuePointer()
        const_char* GetTypeName()
    
    cdef cppclass FormulaArrayColumn[T](Column):
        FormulaArrayColumn(string, string, TTreeFormula*)

    cdef cppclass FormulaFixedArrayColumn[T](FormulaArrayColumn):
        FormulaFixedArrayColumn(string, string, TTreeFormula*)

    cdef cppclass FormulaColumn[T](FormulaArrayColumn):
        FormulaColumn(string, string, TTreeFormula*)
    
    cdef cppclass BranchColumn(Column):
        BranchColumn(string, TLeaf*)

cdef extern from "Selector.h":
    cdef cppclass Selector:
        vector[bool] selected
        unsigned_int num_selected
        TTreeFormula* selection
        Selector(TTreeFormula*)

cdef extern from "TreeChain.h":
    cdef cppclass TreeChain:
        TreeChain(TTree*, long_long)
        int Prepare()
        int Next()
        void AddColumn(string, string, BranchColumn*)
        int GetEntry(long_long)
        TTree* fChain
        void AddFormula(TTreeFormula*)
        void AddSelector(Selector*)
        void InitBranches()
        void UpdateSelectors()
