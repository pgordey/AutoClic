import pyautogui
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
from pynput import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Автокликер")
        
        self.coordinates = []  # Список для хранения координат кликов
        self.markers = []  # Список для хранения меток
        self.running = False  # Флаг для управления состоянием автокликера
        
        self.label = tk.Label(root, text="Автокликер")  # Создаем метку для заголовка
        self.label.pack(pady=10)  # Добавляем метку в окно с отступом
        
        # Кнопка для добавления позиции клика
        self.add_btn = tk.Button(root, text="Добавь точку куда кликать (Ctrl+A)", command=self.add_position)
        self.add_btn.pack(pady=5)  # Добавляем кнопку в окно с отступом
        
        # Кнопка для запуска автокликера
        self.start_btn = tk.Button(root, text="Начать кликать (Ctrl+S)", command=self.start_clicking)
        self.start_btn.pack(pady=20)  # Добавляем кнопку в окно с отступом
        
        # Кнопка для остановки автокликера
        self.stop_btn = tk.Button(root, text="Перестать кликать (Ctrl+X)", command=self.stop_clicking)
        self.stop_btn.pack(pady=5)  # Добавляем кнопку в окно с отступом
        
        # Метка для отображения списка координат
        self.pos_label = tk.Label(root, text="")
        self.pos_label.pack(pady=10)  # Добавляем метку в окно с отступом
        
        # Ползунок для установки задержки между кликами
        self.delay_scale = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Задержка между кликами (сек)")
        self.delay_scale.pack(pady=10)
        self.delay_scale.set(1)  # Установка задержки по умолчанию на 1 секунду
        
        # Установка окна поверх всех окон
        self.root.attributes('-topmost', True)
        
        # Привязка горячих клавиш с использованием pynput
        listener = keyboard.GlobalHotKeys({
            '<ctrl>+a': self.add_position,  # Привязка Ctrl+A для добавления позиции клика
            '<ctrl>+s': self.start_clicking,  # Привязка Ctrl+S для запуска автокликера
            '<ctrl>+x': self.stop_clicking  # Привязка Ctrl+X для остановки автокликера
        })
        listener.start()  # Запуск прослушивателя горячих клавиш
    
    def add_position(self):
        # Получаем текущие координаты курсора
        pos = pyautogui.position()
        # Добавляем координаты в список
        self.coordinates.append(pos)
        # Обновляем текст метки для отображения новых координат
        self.pos_label.config(text=f"Positions: {self.coordinates}")
        
        # Создаем маленькое окно для метки
        marker = tk.Toplevel(self.root)
        marker.geometry(f"10x10+{pos[0]}+{pos[1]}")
        marker.overrideredirect(True)  # Убираем заголовок окна
        marker.attributes('-topmost', True)
        marker.configure(bg='red')  # Устанавливаем цвет фона для метки
        self.markers.append(marker)
    
    def start_clicking(self):
        # Проверяем, есть ли координаты для кликов
        if not self.coordinates:
            # Показать предупреждение, если координаты не заданы
            messagebox.showwarning("No Positions", "Add at least one position first!")
            return
        # Устанавливаем флаг запуска автокликера
        self.running = True
        # Запускаем функцию кликов в отдельном потоке
        self.thread = Thread(target=self.click_loop)
        self.thread.start()
    
    def stop_clicking(self):
        # Сбрасываем флаг запуска автокликера
        self.running = False
        # Ожидаем завершения потока, если он существует
        if hasattr(self, 'thread'):
            self.thread.join()
        # Удаление всех меток с экрана
        for marker in self.markers:
            marker.destroy()
        self.markers.clear()
    
    def click_loop(self):
        # Получаем задержку между кликами
        delay = self.delay_scale.get()
        # Бесконечный цикл для выполнения кликов
        while self.running:
            # Проходим по всем координатам в списке
            for pos in self.coordinates:
                # Проверяем, не остановлен ли автокликер
                if not self.running:
                    break
                # Выполняем клик по текущим координатам
                pyautogui.click(pos)
                # Задержка между кликами
                time.sleep(delay)

if __name__ == "__main__":
    root = tk.Tk()  # Создаем главное окно
    app = AutoClicker(root)  # Создаем экземпляр автокликера
    root.mainloop()  # Запускаем главный цикл обработки событий
