from abc import abstractmethod, ABCMeta

class SorterConf:
    '''
    Sorter configuration object.
    '''
    def __init__(self):
        self.is_data_in_file = False
        self.file_in = None
        self.file_out = None
        self.delimeter = ','
        self.top_n = None
        self.is_asc_order = True
        self.container = []
        self.f_converter = int
        
    
class Sorter:
    '''
    Abstract sorter class, which provides shared methods being used by
    subclasses.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, conf=None):
        self.__initialize(conf)
        
    def __initialize(self, conf):
        if conf:
            self.conf = conf
            if not conf.is_data_in_file:
                self.numbers = conf.container
            else:
                self.numbers = []
                self.__read_numbers()
            self.length = len(self.numbers)
    
    '''
        Read numbers from a given file
    '''
    def __read_numbers(self, f_converter=int):
        try:
            f = open(self.conf.file_in, 'r')
        except:
            raise IOError('Error to open file: ' + self.conf.file_in)
        for line in f.readlines():
            for num in line.strip().split(self.conf.delimeter):
                try:
                    self.numbers.append(f_converter(num))
                except:
                    print('Can not be parsed as a number, num=' + num)
        f.close()
        
    def output(self):
        if self.conf.is_data_in_file:
            self.__write_sorted_numbers()
        else:
            self.__print_container()
            
    def __print_container(self):
        num_cnt = self.__get_actual_top_n()
        if self.conf.is_asc_order:
            print(self.numbers[:num_cnt])
        else:
            print(list(reversed(self.numbers))[:num_cnt])
    
    '''
        Write sorted number to a given file
    '''
    def __write_sorted_numbers(self):
        f = open(self.conf.file_out, 'w')
        # count of numbers being returned 
        num_cnt = self.__get_actual_top_n()
        if self.conf.is_asc_order == True:
            i = 0
            while i<num_cnt-1:
                f.write(str(self.numbers[i]) + self.conf.delimeter)
                i = i + 1
            f.write(str(self.numbers[num_cnt - 1]))    
        else:
            i = self.length - 1
            cnt = 0
            while i>=0 and cnt<num_cnt-1:
                cnt = cnt + 1
                f.write(str(self.numbers[i]) + self.conf.delimeter)
                i = i - 1
            f.write(str(self.numbers[i - 1]))
        f.close() 
    
    def __get_actual_top_n(self):
        num_cnt = self.length
        if self.conf.top_n and self.conf.top_n<self.length:
            num_cnt = self.conf.top_n
        return num_cnt
    
    @abstractmethod    
    def sort(self):
        pass
    
    def set_conf(self, conf):
        if conf:
            self.__initialize(conf)
    
    def swap(self, i, j):
        self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]


class StraightInsertionSorter(Sorter):
    '''
    Straight insertion sorter
    '''
    def sort(self):
        i = 0
        while i<self.length -1:
            k = i
            j = i
            while j<self.length:
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
        while i<self.length -1:
            k = i
            j = i
            while j<self.length:
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
        i = self.length - 1
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
        self.__auxiliary_list = [0 for x in range(self.length)]
        self.__merge_sort(0, self.length - 1)
    
    def __merge_sort(self, low, high):
        dividedIndex = 0
        if low<high:
            dividedIndex = (low + high) // 2
            self.__merge_sort(low, dividedIndex)
            self.__merge_sort(dividedIndex + 1, high)
            self.__merge(low, dividedIndex, high)
            
    def __merge(self, low, dividedIndex, high):
        i = low
        j = dividedIndex + 1
        pointer = 0
        while i<=dividedIndex and j<=high:
            if self.numbers[i]>self.numbers[j]:
                self.__auxiliary_list[pointer] = self.numbers[j]
                j = j + 1
            else:
                self.__auxiliary_list[pointer] = self.numbers[i]
                i = i + 1
            pointer = pointer + 1
        while i<=dividedIndex:
            self.__auxiliary_list[pointer] = self.numbers[i]
            pointer = pointer + 1
            i = i + 1
        while j<=high:
            self.__auxiliary_list[pointer] = self.numbers[j]
            pointer = pointer + 1
            j = j + 1
        # copy elements in auxiliary list to the original list
        pointer = 0
        i = low
        while i<=high:
            self.numbers[i] = self.__auxiliary_list[pointer]
            i = i + 1
            pointer = pointer + 1
            
    
class QuickSorter(Sorter):
    '''
    Quick sorter
    '''
    def sort(self):
        self.__quick_sort(0, self.length - 1)
    
    def __quick_sort(self, low, high):
        if low<high:
            pivotPos = self.__partition(low, high)
            self.__quick_sort(low, pivotPos - 1)
            self.__quick_sort(pivotPos + 1, high)
        
    def __partition(self, i, j):
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
        d = self.length
        while d>1:
            d //= 2
            i = d
            # for each d, execute one pass shell sort
            while i<self.length:
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
        self.__heapify()
        i = 0
        while i<self.length:
            self.swap(0, self.length-1-i) 
            self.__sift_down(0, self.length-1-i)           
            i = i + 1
    
    def __heapify(self):
        pos = (self.length-1) // 2
        i = pos
        while i>=0:
            self.__sift_down(i, self.length)
            i = i - 1
    
    def __sift_down(self, s, m):
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
    __instances = {
        1 : StraightInsertionSorter(),
        2 : StraightSelectionSort(),
        3 : BubbleSorter(),
        4 : MergeSorter(),
        5 : QuickSorter(),
        6 : ShellSorter(),
        7 : HeapSorter()
    }
    
    @classmethod 
    def get_instance(cls, sorter_type):
        instance = cls.__instances.get(sorter_type, None)
        template = 'Sorter detail: TYPE = {0}, CLASS = {1}'
        if instance:
            fmt = template.format(sorter_type, instance.__class__.__name__)
            print(fmt)
            return instance
        else:
            raise ValueError('Unknown sorter type: ' + sorter_type)

