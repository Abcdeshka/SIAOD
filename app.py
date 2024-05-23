import tkinter as tk
from tkinter import messagebox, ttk
import csv

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсовая работа")
        
        self.label = tk.Label(root, text="Введите имя файла:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)
        
        self.button = tk.Button(root, text="Показать отчет", command=self.show_data)
        self.button.pack(pady=10)
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Создаем табличку
        self.tree = ttk.Treeview(self.frame, columns=("Номер заказа", "Дата заказа", "Название товара", "Категория товара", "Количество продаж", "Цена за единицу", "Общая стоимость"), show='headings')
        self.tree.heading("Номер заказа", text="Номер заказа")
        self.tree.heading("Дата заказа", text="Дата заказа")
        self.tree.heading("Название товара", text="Название товара")
        self.tree.heading("Категория товара", text="Категория товара")
        self.tree.heading("Количество продаж", text="Количество продаж")
        self.tree.heading("Цена за единицу", text="Цена за единицу")
        self.tree.heading("Общая стоимость", text="Общая стоимость")
        
        # Создаем скроллбар
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Размещаем табличку и скроллбар
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def show_data(self):
        name = self.entry.get()
        try:
            with open(f"{name}.csv", encoding='utf-8') as file:
                file_reader = csv.reader(file, delimiter=";")
                total, max_count, max_profit, p_name, c_name, data = solving(file_reader)
                
                # Очистка таблицы перед добавлением новых данных
                for row in self.tree.get_children():
                    self.tree.delete(row)
                
                # Добавление данных в таблицу
                for row in data:
                    self.tree.insert("", tk.END, values=row)
                
                # Показать сообщение с результатами
                messagebox.showinfo("Отчет", f'Общая выручка магазина: {total} рублей\n'
                                             f'Товар, который был продан наибольшее количество раз ({max_count}): \n{c_name}\n'
                                             f'Товар, который принес наибольшую выручку ({max_profit}): \n{p_name}')
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл {name}.csv не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

def solving(file):
    total = max_profit = max_count = 0
    max_p_index = max_c_index = -1
    ht_count = dict()
    ht_profit = dict()
    names = []
    ids = []
    data = []
    
    for row in file:
        if len(row) != 7:
            continue  # Пропустить строки, которые не содержат 7 значений
        
        order_number = row[0]
        order_date = row[1]
        name = row[2]
        category = row[3]
        try:
            count = int(row[4])
            price = float(row[5])
            row_total = float(row[6])
        except ValueError:
            continue
        
        ids.append(order_number)
        names.append(name)
        total += row_total
        data.append((order_number, order_date, name, category, count, price, row_total))

        # Добавляет значения в хеш-таблицу
        if name not in ht_count:
            ht_count[name] = 0
        ht_count[name] += count

        # Добавляет значения в хеш-таблицу
        if name not in ht_profit:
            ht_profit[name] = 0
        ht_profit[name] += count * price
    
    # Ищет товар, принесший большую прибыль
    for name in ht_profit:
        if ht_profit[name] > max_profit:
            max_profit = ht_profit[name]
            max_p_name = name

    # Ищет товар, купленный больше всего раз
    for name in ht_count:
        if ht_count[name] > max_count:
            max_count = ht_count[name]
            max_c_name = name
            
    return total, max_count, max_profit, max_p_name, max_c_name, data

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
