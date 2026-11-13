import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# шаблоны для аппроксимации
def fit_n2(n, c):
    return c * n**2

def fit_nlogn(n, c):
    return c * n * np.log2(np.maximum(n, 1e-10)) # под логарифмом никогда не будет 0

def plot_benchmark_results(results_list: list[dict], target_distribution: str = "Uniform Random"):
    """
    Строит 3 графика (линейный, log-log, fitting) для выбранного распределения (по умолчанию для случайного массива)
    """
    df = pd.DataFrame(results_list) #таблица вместо списка словарей
    df_dist = df[df["Распределение"] == target_distribution] #отбираются строки которые относятся к конкретному распределению
    
    if df_dist.empty:
        print(f"Нет данных для распределения: {target_distribution}")
        return

    # График 1: линейный
    plt.figure(figsize=(10, 6))
    for algo in df_dist["Алгоритм"].unique(): #из таблицы извлекаются данные для конкретной сортировки
        df_algo = df_dist[df_dist["Алгоритм"] == algo]
        plt.errorbar(df_algo["N"], df_algo["Среднее время (с)"], 
                     yerr=df_algo["Отклонение (с)"], label=algo, fmt='-o', capsize=4)
        
    plt.title(f"Время от размера массива (Линейный масштаб) | {target_distribution}") #автоматически подставляется название распределения
    plt.xlabel("Размер массива, N (элементов)")
    plt.ylabel("Время выполнения, T (с)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # График 2: Log-Log
    plt.figure(figsize=(10, 6))
    for algo in df_dist["Алгоритм"].unique():
        df_algo = df_dist[df_dist["Алгоритм"] == algo]
        df_algo = df_algo[df_algo["Среднее время (с)"] > 0]
        plt.errorbar(df_algo["N"], df_algo["Среднее время (с)"], 
                     yerr=df_algo["Отклонение (с)"], label=algo, fmt='-o', capsize=4)
        
    plt.xscale('log') #переключение на логарифмический масштаб
    plt.yscale('log')
    plt.title(f"Время от размера (Log-Log масштаб) | {target_distribution}")
    plt.xlabel("Размер массива, N (элементов)")
    plt.ylabel("Время выполнения, T (с)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # График 3: fitting
    plt.figure(figsize=(10, 6))
    for algo in df_dist["Алгоритм"].unique():
        df_algo = df_dist[df_dist["Алгоритм"] == algo]
        n_vals = df_algo["N"].values
        t_vals = df_algo["Среднее время (с)"].values
        
        p = plt.plot(n_vals, t_vals, 'o', label=f"{algo} (эксп.)")
        color = p[0].get_color()
        
        try:
            if algo in ["merge_sort", "quick_sort", "heap_sort"]:
                popt, _ = curve_fit(fit_nlogn, n_vals, t_vals)
                plt.plot(n_vals, fit_nlogn(n_vals, *popt), '--', color=color, label=f"fit: O(N log N)")
            elif algo in ["insertion_sort", "bubble_sort", "selection_sort", "stupid_sort"]:
                popt, _ = curve_fit(fit_n2, n_vals, t_vals)
                plt.plot(n_vals, fit_n2(n_vals, *popt), '--', color=color, label=f"fit: O(N^2)")
        except Exception as e:
            print(f"Не удалось построить аппроксимацию для {algo}: {e}")

    plt.title(f"Теоретическая аппроксимация (Fitting) | {target_distribution}")
    plt.xlabel("Размер массива, N (элементов)")
    plt.ylabel("Время выполнения, T (с)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
