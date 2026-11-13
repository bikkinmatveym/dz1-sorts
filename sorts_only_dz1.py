def stupid_sort(arr: list[int | float]) -> tuple[list[int | float], int, int]:
    comparisons = 0
    writes = 0
    
    i = 0
    #проходим по списку, пока не встретим неотсортированные элементы, потом возвращаемся в начало
    while i < len(arr) - 1:
        comparisons += 1
        #меняем местами неотсортированные элементы
        if arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
            writes += 1
            i = 0
        else:
            i += 1
            
    return arr, comparisons, writes

def insertion_sort(arr: list[int | float]) -> tuple[list[int | float], int, int]:
    comparisons = 0
    writes = 0
    
    for i in range(1, len(arr)):
        #сохраняем элемент в переменную key
        key = arr[i]
        j = i - 1
        #двигаем элементы вправо, если они больше key, пока не дошли до начала списка
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                # cдвигаем элемент вправо
                arr[j + 1] = arr[j]
                writes += 1
                j -= 1
            else:
                break
                
        # помещаем key на нужную позицию
        arr[j + 1] = key
        writes += 1
        
    return arr, comparisons, writes

def merge_sort(arr: list[int | float]) -> tuple[list[int | float], int, int]:
    if len(arr) <= 1:
        return arr, 0, 0
    #разбиваем массив на 2 (рекурсивно)
    mid = len(arr) // 2
    first_half_sorted, comp_1, writes_1 = merge_sort(arr[:mid])
    second_half_sorted, comp_2, writes_2 = merge_sort(arr[mid:])
    #сливаем 2 отсортированных массива в один
    merged_arr, merge_comp, merge_writes = merge(first_half_sorted, second_half_sorted)
    total_comp = comp_1 + comp_2 + merge_comp
    total_writes = writes_1 + writes_2 + merge_writes

    return merged_arr, total_comp, total_writes

#функция сливает 2 массива в 1
def merge(arr_1: list[int | float], arr_2: list[int | float]) -> tuple[list[int | float], int, int]:
    arr_merged = []
    i = j = 0
    comparisons = 0
    writes = 0

    while i < len(arr_1) and j < len(arr_2):
        comparisons += 1
        if arr_1[i] <= arr_2[j]:
            arr_merged.append(arr_1[i])
            i += 1
        else:
            arr_merged.append(arr_2[j])
            j += 1
        writes += 1
    #добавляем в новый массив элемент, оставшийся в одном из старых массивов
    arr_merged.extend(arr_1[i:])
    writes += len(arr_1) - i
    
    arr_merged.extend(arr_2[j:])
    writes += len(arr_2) - j
    
    return arr_merged, comparisons, writes
