class Heap:
    def __init__(self, keys: list = None, min=True, compare=None):
        self.compare = compare
        # denote whether it's a min heap
        self.min = min
        if keys:
            self.pq = [0] + keys
            self.qp = dict(zip(keys, range(1, len(self.pq))))
            k = len(keys) // 2
            while k >= 1:
                self.__sink(k)
                k -= 1
        else:
            self.pq = [0]
            self.qp = {}

    def insert(self, key):
        self.pq.append(key)
        self.__swim(self.size())

    def pop(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        m = self.pq[1]
        self.__exch(1, self.size())
        self.pq.pop()
        self.__sink(1)
        del self.qp[m]
        return m

    def top(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        return self.pq[1]

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.pq) - 1

    def delete(self, key):
        if key not in self:
            raise ValueError("index is not in the priority queue")
        i = self.qp[key]
        self.__exch(i, self.size())
        self.pq.pop()
        self.__swim(i)
        self.__sink(i)
        del self.qp[key]

    def __contains__(self, item):
        return item in self.qp

    def __compare(self, i, j):
        if self.compare:
            comp = self.compare(self.pq[i], self.pq[j]) > 0
        else:
            comp = self.pq[i] > self.pq[j]
        return comp if self.min else not comp

    def __exch(self, i, j):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def __swim(self, k):
        while k > 1 and self.__compare(k // 2, k):
            self.__exch(k, k // 2)
            k = k // 2

    def __sink(self, k):
        while 2 * k <= self.size():
            j = 2 * k
            if j < self.size() and self.__compare(j, j + 1):
                j += 1
            if not self.__compare(k, j):
                break
            self.__exch(k, j)
            k = j


class IndexHeap:
    def __init__(self, indices: list = None, keys: list = None, min=True, compare=None):
        self.compare = compare
        # denote whether it's a min heap
        self.min = min
        if keys or indices:
            if not (keys and indices):
                raise ValueError('illegal arguments')
            self.pq = [0] + indices
            self.qp = dict(zip(indices, range(1, len(self.pq))))
            self.keys = dict(zip(indices, keys))
            k = len(keys) // 2
            while k >= 1:
                self.__sink(k)
                k -= 1
        else:
            self.pq = [0]
            self.qp = {}
            self.keys = {}

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.pq) - 1

    def pop(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        m = self.pq[1]
        key = self.keys[m]
        self.__exch(1, self.size())
        self.pq.pop()
        self.__sink(1)
        del self.qp[m]
        del self.keys[m]
        return m, key

    def top(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        m = self.pq[1]
        return m, self.keys[m]

    def insert(self, index, key):
        if index in self:
            raise ValueError("index is already in the priority queue")
        self.pq.append(index)
        self.qp[index] = self.size()
        self.keys[index] = key
        self.__swim(self.size())

    def changeKey(self, index, key):
        if index not in self:
            raise ValueError("index is not in the priority queue")
        self.keys[index] = key
        self.__swim(self.qp[index])
        self.__sink(self.qp[index])

    def keyOf(self, index):
        if index not in self:
            raise ValueError("index is not in the priority queue")
        return self.keys[index]

    def delete(self, index):
        if index not in self:
            raise ValueError("index is not in the priority queue")
        i = self.qp[index]
        self.__exch(i, self.size())
        self.pq.pop()
        self.__swim(i)
        self.__sink(i)
        del self.qp[index]
        del self.keys[index]

    def __contains__(self, item):
        return item in self.qp

    def __compare(self, i, j):
        if self.compare:
            comp = self.compare(self.keys[self.pq[i]], self.keys[self.pq[j]]) > 0
        else:
            comp = self.keys[self.pq[i]] > self.keys[self.pq[j]]
        return comp if self.min else not comp

    def __exch(self, i, j):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def __swim(self, k):
        while k > 1 and self.__compare(k // 2, k):
            self.__exch(k, k // 2)
            k = k // 2

    def __sink(self, k):
        while 2 * k <= self.size():
            j = 2 * k
            if j < self.size() and self.__compare(j, j + 1):
                j += 1
            if not self.__compare(k, j):
                break
            self.__exch(k, j)
            k = j
