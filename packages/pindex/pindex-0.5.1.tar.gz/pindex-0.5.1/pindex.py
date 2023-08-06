# -*- coding: utf-8 -*-
'''pindex.py

An awesome tool for indexing matrices.
We propose a new concept “single index” (as in matlab) to index the elements from matrices.
One can alternate exchange python-style index (begin with 0) with matlab-style index (begin with 1)

(Single)Index is treated as a vector.

example
    ind = SingleIndex([1,2,3])  # construct single index
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

'''

import numpy as np


class Arith:
    # interface

    # override + -
    def __add__(self,other):
        pass

    def __radd__(self,other):
        return self+other

    def __neg__(self):
        pass

    def __pos__(self):
        return self

    def __iadd__(self,other):
        return self+other

    def __sub__(self,other):
        return self+(-other)

    def __isub__(self,other):
        return self-other

    def __rsub__(self,other):
        return -self+other

    #override * /
    def __mul__(self,other):
        pass

    def __rmul__(self,other):
        return self*other

    def __imul__(self,other):
        return self*other

    def __truediv__(self,other):
        pass

    def __itruediv__(self,other):
        return self/other

    def __rtruediv__(self,other):
        pass

    def __irtruediv__(self,other):
        return other/other

    # override **
    def __pow__(self,other):
        pass

    def __ipow__(self,other):
        return self**other


def ind2tuple(ind, ns):
    '''single index (int) to multi-index under ns shape of array

    Example:
>>> ind.ind2tuple(7,(3,4))
(1, 2)
>>> ind.ind2tuple(17,(3,4,3))
(2, 1, 1)'''
    dim = len(ns)
    if dim == 0:
        return ()
    if dim == 1:
        return (ind,)
    else:
        d, r = divmod(ind+1, np.prod(ns[:-1]))
        if r == 0:
            return tuple(ind-1 for ind in ns[:-1]) + (d-1,)
        else:
            return ind2tuple(r-1, ns[:-1]) + (d,)


def ind2iter(ind, N=None):
    '''transform index to iterator

    slice to range, int and list to list
    '''
    if isinstance(ind, list):
        return ind
    elif isinstance(ind, slice): # slc is a slice
        a = 0 if ind.start is None else ind.start
        b = N if ind.stop is None else ind.stop # b <= N
        return range(a, b, c) if ind.step else range(a, b)
    else:
        return [ind]


def addind(ind1, ind2):
    '''ind1 + ind2
    ind1, ind2 are int list or range (iter)
    '''
    if isinstance(ind2, int):
        if isinstance(ind1, int):
            return ind1 + ind2
        elif isinstance(ind1, slice):
            return slice(ind1.start + ind2, ind1.stop + ind2, ind1.step)
        else:
            return [a+ind2 for a in ind1]
    elif isinstance(ind2, slice):
        if isinstance(ind1, int):
            return addind(ind2, ind1)
        elif isinstance(ind1, slice):
            return slice(ind1.start+ind2.start, ind1.stop+ind2.stop, (ind1.step if ind1.step is not None else 1)+(ind12.step if ind2.step is not None else 1))
        else:
            return list(map(np.add, ind1, ind2iter(ind2)))
    else:
        if isinstance(ind1, list):
            return list(map(np.add, ind1, ind2))
        else:
            return addind(ind2, ind1)


def mulind(ind, num):
    '''ind * num
    ind is int list or slice, num is int
    '''
    if num == 0:
        return 0
    if isinstance(num, int):
        if isinstance(ind, int):
            return ind1 * num
        elif isinstance(ind, list):
            if num > 0:
                return [num * a for a in ind]
            elif num < 0:
                return [num * a for a in ind[::-1]]
        else:
            if num > 0:
                return slice(num * ind.start, num * ind.stop, num * ind.step if ind.step is not None else num)
            elif num < 0:
                return slice(num * ind.stop, num * ind.start, num * ind.step if ind.step is not None else num)
    elif isinstance(ind, int):
        return ind * num


class SingleIndex(Arith):
    '''single index: int, list, slice
    '''
    def __init__(self, value, N=None):
        """
        Arguments:
            value {int|list|slice} -- index
            N -- the bound
        
        Raises:
            TypeError -- [description]
        """

        if isinstance(value, (int, list, slice)):
            self.value = value
        else:
            raise TypeError('args should be of int, slice, list(of ints)')


    def isa(self, T):
        return isinstance(self.value, T)

    def __add__(self, other):
        return SingleIndex(addind(self.value, other.value if isinstance(other, SingleIndex) else other))

    def __mul__(self, num):
        return SingleIndex(mulind(self.value, num))

    def __neg__(self):
        return -1 * self

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'Single Index: %s' % self

    def isempty(self, N=None):
        """True if it is an empty index, such as []
        
        Keyword Arguments:
            N {int} -- the bound of index (default: {None})
        
        Returns:
            bool -- True if it is empty
        """
        if self.isa(int):
            return False
        elif self.isa(list):
            return self.value == []
        else:
            a, b, c = self.value.start, self.value.stop, self.value.step
            if c is None or c > 0:
                if a is None or a == 0:
                    return b is None or -N < b < 0 or b > 0
                elif a > 0:
                    return b is None or b > a or b < 0 and b + N > a
                else:
                    return b is None or b > a + N or b < 0 and b > a
            else:
                if a is None or a == N - 1:
                    return b is None or -N <= b < -1 or b < N - 1
                elif a > 0:
                    return b is None or b < a or b < 0 and b + N < a
                else:
                    return b is None or b < a + N or b < 0 and b < a

    def max(self, N=None):
        """Get the maximum in the index
        
        Keyword Arguments:
            N {int} -- the bound of the index (default: {None})
        
        Returns:
            int
        """
        if self.isa(int):
            return self.value
        elif self.isa(list):
            return max(self.value)
        else:
            a, b, c = self.value.start, self.value.stop, self.value.step
            if c is None or c > 1:
                b = N - 1 if b is None else b - 1
                if c == 1:
                    return b
                else:
                    r = mod(b - a, c)
                    return b - r
            else:
                return N - 1 if a is None else a


    def min(self, N=None):
        """Get the minimum in the index
        
        See also .max
        """
        if self.isa(int):
            return self.value
        elif self.isa(list):
            return min(self.value)
        else:
            a, b, c = self.value.start, self.value.stop, self.value.step
            if c is None or c > 1:
                return 0 if a is None else a
            else:
                b = 0 if b is None else b + 1
                if c == -1:
                    return b
                else:
                    r = mod(a - b, -c)
                    return b - r


    def __call__(self, x):
        # self(x) == x[self]
        if isinstance(x, (str, tuple, list)):
            if self.isa((int, slice)):
                return x[self.value]
            else:
                return [x[k] for k in self.value]
        elif isinstance(x, np.ndarray):
            ns = x.shape
            if self.isa(int):
                return x[ind2tuple(self.value, ns)]
            elif self.isa(slice):
                return [x[ind2tuple(k, ns)] for k in ind2iter(self.value)]
            else:
                return [x[ind2tuple(k, ns)] for k in self.value]

    def assign(self, x, v):
        # self.assing(x, v) <=> x[self] = v
        if isinstance(x, (str, tuple, list)):
            if self.isa((int, slice)):
                x[self.value] = v
            else:
                for k in self.value:
                    x[k] = v
        elif isinstance(x, np.ndarray):
            ns = x.shape
            if self.isa(int):
                x[ind2tuple(self.value, ns)] = v
            elif self.isa(slice):
                for k in ind2iter(self.value):
                    x[ind2tuple(k, ns)] = v
            else:
                for k in self.value:
                    x[ind2tuple(k, ns)] = v


    def py2matlab(self):
        # python style to matlab style
        if self.isa(int):
            self.value -= 1
        elif self.isa(slice):
            a, b, c = self.value.start, self.value.stop, self.value.step
            if c is None or c > 0:  # a <= b
                self.value = slice(a-1 if a else None, None if b == 0 else b, c)
            elif c < 0: # a >= b
                self.value = slice(a-1 if a else None, None if b == 1 or b is None else b-2, c)
        else:
            self.value = [v - 1 for v in self.value]


    def matlab2py(self):
        # matlab style to python style; inverse of py2matlab
        if self.isa(int):
            self.value += 1
        elif self.isa(slice):
            a, b, c = self.value.start, self.value.stop, self.value.step
            if c is None or c > 0:
                if a is not None:
                    a += 1
            else:
                if a is not None:
                    a += 1
                if b is not None:
                    b += 2
            self.value = slice(a, b, c)
        else:
            self.value = [v + 1 for v in self.value]



class Index(Arith, np.ndarray):
    '''Multi-index, array of SingleIndex
    1D Multi-index is identified with SingleIndex

    Example:
    Index([1,2,3]) == Index(([1,2,3],))  # works as SingleIndex([1,2,3])
    Index(([1,2], 3, slice(1,4)))
    '''
    def __new__(cls, args):
        if isinstance(args, (int, list, slice)):
            # 1-dim index is equiv. to single index
            return super(Index, cls).__new__(cls, shape=1, dtype=SingleIndex, buffer=np.array(SingleIndex(args)))
        elif isinstance(args, tuple):
            return super(Index, cls).__new__(cls, shape=len(args), dtype=SingleIndex, buffer=np.array([SingleIndex(a) for a in args]))
        else:
            raise TypeError('args should be of int, slice, list(of ints), tuple')


    @property
    def dim(self):
        return len(self)

    def __call__(self, array):
        # self(x) == x[self]
        if len(self) == 1:
            return self[0](array)
        else:
            if isinstance(array, np.ndarray):
                return np.array([self[1:](a) for a in array[self[0].value]])
            else:
                return np.array([self[1:](a) for a in self[0](array)])

    def assign(self, array, v):
        if len(self) == 1:
            self[0].assign(array, v)
        else:
            for k, a in enumerate(self[0](array)):
                self[1:].assign(a, v[k])

    def __add__(self, other):
        if isinstance(other, int):
            return Index(tuple(a + other for a in self))
        else:
            return Index(map(np.add, self, other))

    def __neg__(self):
        return Index(map(lambda x:-x, self))

    def __mul__(self,other):
        if np.isscalar(other):
            return Index(map(lambda x:x*other, self))
        else:
            return Index(map(np.add, self, other))

    def __str__(self):
        return ','.join(map(str, self))

    def __repr__(self):
        return 'Multi-Index: %s' % self

    def minInd(self):
        # minimal index
        m = tuple(a.min() for a in self)
        return Index(m)

    def maxInd(self):
        # minimal index
        m = tuple(a.max() for a in self)
        return Index(m)

    def min_(self, *others):
        return Index(tuple(min(min(other.minInd()[k] for other in others), self.minInd()[k]) for k in range(self.dim)))

    def max_(self, *others):
        return Index(tuple(max(max(other.maxInd()[k] for other in others), self.maxInd()[k]) for k in range(self.dim)))

    def py2matlab(self):
        for ind in self:
            ind.py2matlab()

    def matlab2py(self):
        for ind in self:
            ind.matlab2py()


def irange(minInd, maxInd):
    # interval index
    # irange([1,1],[3,4]) == index(([1,2], [1,2,3]))
    return Index(tuple(slice(a, b) for a, b in zip(minInd, maxInd)))


