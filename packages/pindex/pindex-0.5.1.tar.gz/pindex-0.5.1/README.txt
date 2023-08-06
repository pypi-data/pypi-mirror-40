Introduction
=============

Abstract
----------
An awesome tool for indexing matrices. propose a new concept “single index” (as in matlab) to index the elements from matrices. exchange python-style index(begin with 0) with matlab-style index(begin with 1)

Keywords
----------
Index, Matrix, Single Index, Style of Index


New feature: 

    1. fix some bugs

Feature:

    1. propose single index
    2. change to (back from) matlab-style index
    3. arithmetic of the index


Content
=========

Classes::

    SingleIndex: wrapper of int, list, slice
    Index: array of SingleIndex


Interface::

    Arith: arithmetic of index


function::

    irange: interval-like index


Grammar
=========

Basic grammar
-------------

import::

    import pindex   # python for index

Example::

    ind = SingleIndex([1,2,3])  # construct a single index
    s = ind('helloworld')   # index(array) == array[index]
    print(s)
    
    A = np.array([[1,2,6],[3,4,5]])
    B = ind(A)
    print(B)    # index matrix with single index as in matlab

    ind.py2matlab()        # change to matlab style
    s = ind('helloworld')
    print(s)  # output: hel

    ind = Index([1,2,3])    # for 1dim array, Index == SingleIndex
    ss = ind('helloworld')
    print(ss)

    ind = Index(([1,2],[3,4]))  # construct multi-index
    try:
        ss = ind(['hello', 'world'])
        print(ss)
    except:
        ind.py2matlab()
        ss = ind(['hello', 'world'])
        print(ss)


Attention::

    ind = SingleIndex([1,2,3])
    A = [[1,2,6],[3,4,5]]
    B = ind(A)  # pindex.py thinks A is a list (of lists, with length 2) instead of matrix
    ind = Index(([0,1],[0,1]))   # this is ok, since you use multi-index

