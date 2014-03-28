from abc import ABCMeta, abstractmethod


class Sorter:
    '''
    Abstract sorter class, which provides shared methods being used by
    subclasses.
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod    
    def sort(self, array):
        pass
    
class StraightInsertionSorter(Sorter):
    '''
    Straight insertion sorter
    '''
    def sort(self, array):
        i = 0
        length = len(array)
        while i<length -1:
            k = i
            j = i
            while j<length:
                if array[j]<array[k]:
                    k = j
                j = j + 1
            if k!=i:
                array[k], array[i] = array[i], array[k]
            i = i + 1
            
class StraightSelectionSort(Sorter):
    '''
    Straight selection sorter
    '''
    def sort(self, array):
        i = 0
        length = len(array)
        while i<length -1:
            k = i
            j = i
            while j<length:
                if array[j]<array[k]:
                    k = j
                j = j + 1
            if k!=i:
                array[k], array[i] = array[i], array[k]
            i = i + 1

class BubbleSorter(Sorter):
    '''
    Bubble sorter
    '''
    def sort(self, array):
        length = len(array)
        i = length - 1
        while i>=0:
            j = 1
            while j<=i:
                if array[j-1]>array[j]:
                    array[j-1], array[j] = array[j], array[j-1]
                j = j + 1
            i = i - 1
               
class MergeSorter(Sorter):
    '''
    Merge sorter
    '''
        
    def sort(self, array):
        length = len(array)
        # initialize auxiliary list
        auxiliary_list = [0 for x in range(length)]
        self.__merge_sort(array, auxiliary_list, 0, length - 1)
    
    def __merge_sort(self, array, auxiliary_list, low, high):
        dividedIndex = 0
        if low<high:
            dividedIndex = (low + high) // 2
            self.__merge_sort(array, auxiliary_list, low, dividedIndex)
            self.__merge_sort(array, auxiliary_list, dividedIndex + 1, high)
            self.__merge(array, auxiliary_list, low, dividedIndex, high)
            
    def __merge(self, array, auxiliary_list, low, dividedIndex, high):
        i = low
        j = dividedIndex + 1
        pointer = 0
        while i<=dividedIndex and j<=high:
            if array[i]>array[j]:
                auxiliary_list[pointer] = array[j]
                j = j + 1
            else:
                auxiliary_list[pointer] = array[i]
                i = i + 1
            pointer = pointer + 1
        while i<=dividedIndex:
            auxiliary_list[pointer] = array[i]
            pointer = pointer + 1
            i = i + 1
        while j<=high:
            auxiliary_list[pointer] = array[j]
            pointer = pointer + 1
            j = j + 1
        # copy elements in auxiliary list to the original list
        pointer = 0
        i = low
        while i<=high:
            array[i] = auxiliary_list[pointer]
            i = i + 1
            pointer = pointer + 1
            
class QuickSorter(Sorter):
    '''
    Quick sorter
    '''
    def sort(self, array):
        length = len(array)
        self.__quick_sort(array, 0, length - 1)
    
    def __quick_sort(self, array, low, high):
        if low<high:
            pivotPos = self.__partition(array, low, high)
            self.__quick_sort(array, low, pivotPos - 1)
            self.__quick_sort(array, pivotPos + 1, high)
        
    def __partition(self, array, i, j):
        pivot = array[i]
        while i<j:
            # right side pointer moves to left
            while j>i and array[j]>=pivot:
                j = j - 1
            if i<j:
                array[i] = array[j]
                i = i + 1
            # left side pointer moves to right
            while i<j and array[i]<=pivot:
                i = i + 1
            if i<j:
                array[j] = array[i]
                j = j - 1
        # put the pivot element to the right position
        array[i] = pivot
        return i

class ShellSorter(Sorter):
    '''
    Shell sorter
    '''
    def sort(self, array):
        length = len(array)
        d = length
        while d>1:
            d //= 2
            i = d
            # for each d, execute one pass shell sort
            while i<length:
                tmp = array[i]
                if array[i]<array[i-d]:
                    j = i - d
                    while j>=0 and tmp<array[j]:
                        array[j+d], array[j] = array[j], array[j+d]
                        j = j - d
                    array[j+d] = tmp
                i = i + 1  
                
class HeapSorter(Sorter):
    '''
    Heap sorter
    '''      
    def sort(self, array):
        length = len(array)
        self.__heapify(array)
        i = 0
        while i<length:
            array[0], array[length-1-i] = array[length-1-i], array[0]
            self.__sift_down(array, 0, length-1-i)           
            i = i + 1
    
    def __heapify(self, array):
        length = len(array)
        pos = (length-1) // 2
        i = pos
        while i>=0:
            self.__sift_down(array, i, length)
            i = i - 1
    
    def __sift_down(self, array, s, m):
        tmp = array[s]
        i = 2 * s + 1
        while i<m:
            if i+1<m and array[i]<array[i+1]:
                i = i + 1
            if array[s]<array[i]:
                array[s] = array[i]
                s = i
                i = 2 * s + 1
            else:
                break
            array[s] = tmp
            
            
                            
            
if __name__ == "__main__":
#     sorter = StraightInsertionSorter()
#     sorter = StraightSelectionSort()
#     sorter = BubbleSorter()
#     sorter = MergeSorter()
#     sorter = QuickSorter()
#     sorter = ShellSorter()
    sorter = HeapSorter()
    array = [32, 34, 1, 987, 268, 122]
    sorter.sort(array)
    for i in array:
        print(i)
    
    