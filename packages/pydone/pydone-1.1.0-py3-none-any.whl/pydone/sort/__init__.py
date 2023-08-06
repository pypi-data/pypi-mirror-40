def help():
    print('use sort.bubble() sort.insertion(), sort.quick(), sort.quicklc()')

def bubble():
    print('''
def bubble_sort(A):
    inorder = False
    while not inorder:
        inorder = True
        for i in range(len(A)-1):
            if A[i] > A[i+1]:
                A[i],A[i+1] = A[i+1],A[i]
                inorder = False
    return A
        ''')

def insertion():
    print('''
def insertion_sort(A):
   for i in range(1,len(A)): # A[0] sorted
       inserting = A[i]
       while i > 0 and A[i-1] > inserting:
           A[i] = A[i-1]
           A[i-1] = inserting
           i -= 1
   return A
        ''')

def quick():
    print('''
def quicksort(array):
    if array == []: # terminating condition
        return []
    else:
        pivot = array[0]
        less = []
        great = []
        for i in array[1:]: # from 2nd to last
            if i < pivot:
                less.append(i)
            else:
                great.append(i)
    return quicksort(less) + [pivot] + quicksort(great)
        ''')

def quicklc():
    print('''
    def quicksort(elements):
        if len(elements) == 0: # terminating condition
            return []
        else:
            return quicksort([i for i in elements[1:] if i < elements[0]]) + [elements[0]] + quicksort([i for i in elements[1:] if i >= elements[0]])
        ''')
