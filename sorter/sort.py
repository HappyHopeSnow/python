from abc import abstractmethod, ABCMeta

class SorterConf:
    def __init__(self):
        self.dataInFile = False
        self.readIn = None
        self.writeOut = None
        self.delimeter = ','
        self.topN = None
        self.isAsc = True
        self.container = []
        
    def isDataInFile(self, dataInFile=False):
        self.dataInFile = dataInFile
        
    def setInputFile(self, readIn):
        self.readIn = readIn
        
    def setOutputFile(self, writeOut):
        self.writeOut = writeOut
        
    def isAscOrder(self, isAsc):
        self.isAsc = isAsc
        
    def setTopN(self, topN):
        self.topN = topN
        
    def setDelimeter(self, delimeter):
        self.delimeter = delimeter
        
    def setContainer(self, container):
        self.container = container
        
    
class Sorter:
    '''
    Abstract sorter class, which provides shared methods being used by
    subclasses.
    '''
    __metaclass__ = ABCMeta
    

    def initialize(self, conf):
        if conf is not None:
            self.conf = conf
            if not conf.dataInFile:
                self.numbers = conf.container
            else:
                self.numbers = []
                self.readNumbers()
            self.size = len(self.numbers)

    def __init__(self, conf=None):
        self.initialize(conf)
        
    '''
        Read numbers from a given file
    '''
    def readNumbers(self, fConverter=int):
        f = open(self.conf.readIn, 'r')
        for line in f.readlines():
            for num in line.strip().split(self.conf.separator):
                try:
                    self.numbers.append(fConverter(num))
                except:
                    print('Can not be parsed as a number, num=' + num)
        f.close();
    
    '''
        Write sorted number to a given file
    '''
    def writeSortedNumbers(self):
        f = open(self.conf.writeOut, 'w')
        if self.conf.isAsc== True:
            i = 0
            while i<self.size:
                f.write(self.numbers[i] + self.conf.separator)
            f.write(self.numbers[self.size - 1])    
        else:
            i = self.size - 1
            while i>0:
                f.write(self.numbers[i] + self.conf.separator)
                i = i - 1
            f.write(self.numbers[0])
        f.close() 
    
    @abstractmethod    
    def sort(self):
        pass
    
    def set(self, conf):
        if conf is not None:
            self.initialize(conf)
    
    def swap(self, i, j):
        self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]


class StraightInsertionSorter(Sorter):
    '''
    Straight insertion sorter
    '''
    def sort(self):
        i = 0
        while i<self.size -1:
            k = i
            j = i
            while j<self.size:
                if self.numbers[j]<self.numbers[k]:
                    k = j
                j = j + 1
            if k!=i:
                self.swap(k, i)
            i = i + 1  


class StraightSelectionSort(Sorter):
    '''
    Straight selection sorter
    '''
    def sort(self ):
        i = 0
        while i<self.size -1:
            k = i
            j = i
            while j<self.size:
                if self.numbers[j]<self.numbers[k]:
                    k = j
                j = j + 1
            if k!=i:
                self.swap(k, i)
            i = i + 1
   

class BubbleSorter(Sorter):
    '''
    Bubble sorter
    '''
    def sort(self):
        i = self.size - 1
        while i>=0:
            j = 1
            while j<=i:
                if self.numbers[j-1]>self.numbers[j]:
                    self.swap(j-1, j)
                j = j + 1
            i = i - 1

    
class MergeSorter(Sorter):
    '''
    Merge sorter
    '''
    def __init__(self, conf=None):
        super(MergeSorter, self).__init__(conf)
        
    def sort(self):
        # initialize auxiliary list
        self.auxList = [0 for x in range(self.size)]
        self.mergeSort(0, self.size - 1)
    
    def mergeSort(self, low, high):
        dividedIndex = 0
        if low<high:
            dividedIndex = (low + high) / 2
            self.mergeSort(low, dividedIndex)
            self.mergeSort(dividedIndex + 1, high)
            self.merge(low, dividedIndex, high)
            
    def merge(self, low, dividedIndex, high):
        i = low
        j = dividedIndex + 1
        pointer = 0
        while i<=dividedIndex and j<=high:
            if self.numbers[i]>self.numbers[j]:
                self.auxList[pointer] = self.numbers[j]
                j = j + 1
            else:
                self.auxList[pointer] = self.numbers[i]
                i = i + 1
            pointer = pointer + 1
        while i<=dividedIndex:
            self.auxList[pointer] = self.numbers[i]
            pointer = pointer + 1
            i = i + 1
        while j<=high:
            self.auxList[pointer] = self.numbers[j]
            pointer = pointer + 1
            j = j + 1
        # copy elements in auxiliary list to the original list
        pointer = 0
        i = low
        while i<=high:
            self.numbers[i] = self.auxList[pointer]
            i = i + 1
            pointer = pointer + 1
            
    
class QuickSorter(Sorter):
    '''
    Quick sorter
    '''
    def sort(self):
        self.quickSort(0, self.size - 1)
    
    def quickSort(self, low, high):
        if low<high:
            pivotPos = self.partition(low, high)
            self.quickSort(low, pivotPos - 1)
            self.quickSort(pivotPos + 1, high)
        
    def partition(self, i, j):
        pivot = self.numbers[i]
        while i<j:
            # right side pointer moves to left
            while j>i and self.numbers[j]>=pivot:
                j = j - 1
            if i<j:
                self.numbers[i] = self.numbers[j]
                i = i + 1
            # left side pointer moves to right
            while i<j and self.numbers[i]<=pivot:
                i = i + 1
            if i<j:
                self.numbers[j] = self.numbers[i]
                j = j - 1
        # put the pivot element to the right position
        self.numbers[i] = pivot
        return i

class ShellSorter(Sorter):
    '''
    Shell sorter
    '''
    def sort(self):
        d = self.size
        while d>1:
            d /= 2
            i = d
            # for each d, execute one pass shell sort
            while i<self.size:
                tmp = self.numbers[i]
                if self.numbers[i]<self.numbers[i-d]:
                    j = i - d
                    while j>=0 and tmp<self.numbers[j]:
                        self.swap(j+d, j)
                        j = j - d
                    self.numbers[j+d] = tmp
                i = i + 1

    
class HeapSorter(Sorter):
    '''
    Heap sorter
    '''      
    def sort(self):
        self.heapify()
        i = 0
        while i<self.size:
            self.swap(0, self.size-1-i) 
            self.siftDown(0, self.size-1-i)           
            i = i + 1
    
    def heapify(self):
        pos = (self.size-1) / 2
        i = pos
        while i>=0:
            self.siftDown(i, self.size)
            i = i - 1
    
    def siftDown(self, s, m):
        tmp = self.numbers[s]
        i = 2 * s + 1
        while i<m:
            if i+1<m and self.numbers[i]<self.numbers[i+1]:
                i = i + 1
            if self.numbers[s]<self.numbers[i]:
                self.numbers[s] = self.numbers[i]
                s = i
                i = 2 * s + 1
            else:
                break
            self.numbers[s] = tmp


class SorterFactory:
    '''
        Manage Sorter implementation classes, as well as instances
    '''
    instances = {
        1 : StraightInsertionSorter(),
        2 : StraightSelectionSort(),
        3 : BubbleSorter(),
        4 : MergeSorter(),
        5 : QuickSorter(),
        6 : ShellSorter(),
        7 : HeapSorter()
    }
    
    @classmethod 
    def getInstance(cls, sorterType):
        instance = cls.instances.get(sorterType, None)
        if instance is not None:
            return instance
        else:
            raise BaseException('Unknown sorter type: ' + sorterType)


if __name__ == '__main__':
    data = [9, 1, 7, 7, 4, 0, 3, 8]
    conf = SorterConf()
    conf.setContainer(data)
    sorter = SorterFactory.getInstance(4)
    sorter.set(conf);
    sorter.sort()
    print(sorter.numbers)
