
class SorterConf:
    def __init__(self, whichSorter, readIn=None, writeOut=None, 
                 separator=',', topN=None, isAsc=True):
        self.whichSorter = whichSorter
        self.readIn = readIn
        self.writeOut = writeOut
        self.separator = separator
        self.topN = topN
        self.isAsc = isAsc
    
class Sorter:
    
    def __init__(self, conf, data):
        self.conf = conf
        if conf is None or conf.readIn is None or conf.writeOut is None:
            self.numbers = data
        else:
            self.numbers = []
        self.size = len(self.numbers)
        
    '''
        Read numbers from a given file
    '''
    def readNumbers(self, fConvert):
        f = open(self.conf.readIn, 'r')
        for line in f.readlines():
            for num in line.strip().split(self.conf.separator):
                try:
                    self.numbers.append(fConvert(num))
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
            
    
    '''
        Straight insertion sort function
    '''
    def straightInsertionSort(self):
        i = 1
        while i<self.size:
            tmp = self.numbers[i]
            if self.numbers[i]<self.numbers[i-1]: 
                j = i - 1
                while j>=0 and tmp<self.numbers[j]:
                    self.numbers[j+1] = self.numbers[j]
                    j = j - 1
                self.numbers[j+1] = tmp
            i = i + 1 
                
            
    '''
        Straight selection sort function
    '''
    def straightSelectionSort(self ):
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
    
    '''
        Bubble sort function
    '''
    def bubbleSort(self):
        i = self.size - 1
        while i>=0:
            j = 1
            while j<=i:
                if self.numbers[j-1]>self.numbers[j]:
                    self.swap(j-1, j)
                j = j + 1
            i = i - 1
    
    def mergeSort(self ):
        pass
    
    def quickSort(self):
        pass
    
    '''
        Shell sort function
    '''
    def shellSort(self):
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
    
    def heapSort(self):
        pass
    
    def swap(self, i, j):
        self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]


sorters = {
    1 : 'straightInsertionSort',
    2 : 'straightSelectionSort',
    3 : 'bubbleSort',
    4 : 'mergeSort',
    5 : 'quickSort',
    6 : 'shellSort',
    7 : 'heapSort'
}

def sort(self, whichSorter=1):
    pass     
    
        
    
    
    
    
    

if __name__ == '__main__':
    conf = SorterConf(1)
    sorter = Sorter(conf, [9, 1, 7, 7, 4, 0, 3])
#     sorter.straightInsertionSort()
#     sorter.straightSelectionSort()
#     sorter.bubbleSort()
    sorter.shellSort()
    print(sorter.numbers)