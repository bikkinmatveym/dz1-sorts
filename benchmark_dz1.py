import time
import random
import statistics 
def generate_data(n: int, distribution_type: str) -> list[int]:
    """
    Генерирует массивы данных с разными распределениями.
    Возвращает 1 массив данных.
    """
    if distribution_type == "Uniform Random": #случайный массив
        return [random.randint(-10000, 10000) for _ in range(n)]
    elif distribution_type == "Sorted": #отсортированный массив
        return list(range(1, n + 1))
    elif distribution_type == "Reversed": # массив, отсортированный в обратном порядке
        return list(range(n, 0, -1))
    elif distribution_type == "Nearly Sorted": #в массиве 5% элементов случайно перемешаны
        arr = list(range(1, n + 1))
        num_swaps = max(1, int(n * 0.05) // 2) # 1 - для очень маленьких массивов
        for _ in range(num_swaps):
            i, j = random.randint(0, n - 1), random.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif distribution_type == "Many Duplicates": #массив с большим количеством повторяющихся элементов
        return [random.choice([1, 2, 3, 4, 5]) for _ in range(n)]

def run_benchmark(sort_func, n_sizes: list[int], repeats: int = 5): #по умолчанию 5 раз тестируется каждая сортировка
    """
    Проводит замеры для одной сортировки.
    Возвращает список словарей со статистикой.
    """
    distributions = [
        "Uniform Random", "Sorted", "Reversed", 
        "Nearly Sorted", "Many Duplicates"
    ]
    
    results = []
    for dist_type in distributions: #перебирает типы массивов
        for n in n_sizes: #перебирает длины массивов

            if sort_func.__name__ == "stupid_sort" and n > 500:
                continue              #stupid sort не тестируется на массивах с длиной больше 500
            
            times = []
            comps = []
            swaps = []
            for seed in range(repeats): 
                # 5 раз тестируется сортировка на различных массивах одной длины и с одинаковым распределением
                random.seed(seed) #каждая сортировка будет получать идентичные массивы
                data = generate_data(n, dist_type)
                data_copy = data.copy() #копируем массив, чтобы каждая сортировка получала на вход неотсортированный
                
                #замер времени
                t_start = time.perf_counter()
                _, cmp_cnt, swap_cnt = sort_func(data_copy) #  "_"  написано тк сам отсортированный массив не нужен
                t_end = time.perf_counter()
                
                times.append(t_end - t_start)
                comps.append(cmp_cnt)
                swaps.append(swap_cnt)
            
            results.append({     #добавляем словарь в список results
                "Алгоритм": sort_func.__name__,
                "Распределение": dist_type,
                "N": n,
                "Среднее время (с)": statistics.mean(times),
                "Отклонение (с)": statistics.stdev(times) if len(times) > 1 else 0.0,
                "Сравнения": int(statistics.mean(comps)),
                "Перезаписи": int(statistics.mean(swaps))
            })
    return results