import tkinter as tk
from tkinter import messagebox, filedialog
import settings
import pyperclip
import sys

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Настройки приложения")
        self.geometry("400x300")
        
        self.create_menu()
        self.create_widgets()
        
        try:
            # Проверка доступности pyperclip
            pyperclip.copy("test")
        except pyperclip.PyperclipException:
            messagebox.showerror("Ошибка", "Модуль pyperclip не установлен или не поддерживается в вашей системе.")
            sys.exit(1)

    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить настройки", command=self.save_settings)
        file_menu.add_command(label="Загрузить настройки", command=self.load_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Сбросить настройки", command=self.reset_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        self.config(menu=menubar)

    def create_widgets(self):
        # Здесь создаются основные виджеты вашего приложения
        label = tk.Label(self, text="Основное окно приложения")
        label.pack(pady=20)
        
        # Пример поля для ввода настроек
        self.setting_entry = tk.Entry(self, width=30)
        self.setting_entry.pack(pady=10)
        
        save_btn = tk.Button(self, text="Сохранить значение", command=self.save_setting_value)
        save_btn.pack(pady=5)

    def save_settings(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                settings.save_to_file(file_path)
                messagebox.showinfo("Успех", "Настройки успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")

    def load_settings(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                settings.load_from_file(file_path)
                messagebox.showinfo("Успех", "Настройки успешно загружены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить настройки: {str(e)}")

    def reset_settings(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить настройки к значениям по умолчанию?"):
            try:
                settings.reset_to_defaults()
                messagebox.showinfo("Успех", "Настройки сброшены к значениям по умолчанию")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сбросить настройки: {str(e)}")

    def save_setting_value(self):
        # Пример функции для сохранения конкретного значения
        value = self.setting_entry.get()
        if value:
            try:
                # Здесь должна быть логика сохранения конкретной настройки
                messagebox.showinfo("Успех", f"Значение '{value}' сохранено")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить значение: {str(e)}")
        else:
            messagebox.showwarning("Предупреждение", "Введите значение для сохранения")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
    