
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
        
    def readNumbers(self, fConvert):
        f = open(self.conf.readIn, 'r')
        for line in f.readlines():
            for num in line.strip().split(self.conf.separator):
                try:
                    self.numbers.append(fConvert(num))
                except:
                    print('Can not be parsed as a number, num=' + num)
    
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
                self.numbers[k], self.numbers[i] = self.numbers[i], self.numbers[k]
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
                    self.numbers[j-1], self.numbers[j] = self.numbers[j], self.numbers[j-1]
                j = j + 1
            i = i - 1
    
    def mergeSort(self ):
        pass
    
    def quickSort(self):
        pass
    
    def shellSort(self):
        pass
    
    def heapSort(self):
        pass
    

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
    sorter.bubbleSort()
    print(sorter.numbers)