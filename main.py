import tkinter as tk
from tkinter import messagebox, filedialog, ttk  # Добавлен ttk для стильных элементов
import settings
import password_generator
import pyperclip
import sys
import string

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор паролей")
        self.geometry("600x450") # Увеличиваем размер окна
        self.settings = settings.PasswordSettings()  # Создаем экземпляр настроек
        self.generated_password = tk.StringVar() # переменная для сгенерированного пароля ПЕРЕМЕСТИЛИ СЮДА

        self.create_menu()
        self.create_widgets()
        self.load_settings_into_gui() # Загружаем настройки в GUI при запуске

        try:
            pyperclip.copy("test")  # Проверка pyperclip при запуске
        except pyperclip.PyperclipException:
            messagebox.showerror("Ошибка", "Модуль pyperclip не установлен или не поддерживается в вашей системе.")
            sys.exit(1)

    def create_menu(self):
        menubar = tk.Menu(self)
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
        # Length label and entry
        length_label = tk.Label(self, text="Длина пароля:")
        length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w") # Используем grid

        self.length_entry = tk.Entry(self, width=5)
        self.length_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.length_entry.insert(0, str(self.settings.length)) # Заполняем значением из настроек

        # Checkbuttons for character sets
        self.use_letters_var = tk.BooleanVar(value=self.settings.use_letters)
        self.use_digits_var = tk.BooleanVar(value=self.settings.use_digits)
        self.use_symbols_var = tk.BooleanVar(value=self.settings.use_symbols)

        letters_check = tk.Checkbutton(self, text="Буквы", variable=self.use_letters_var)
        digits_check = tk.Checkbutton(self, text="Цифры", variable=self.use_digits_var)
        symbols_check = tk.Checkbutton(self, text="Символы", variable=self.use_symbols_var)

        letters_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        digits_check.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        symbols_check.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Algorithm combobox
        algorithm_label = tk.Label(self, text="Алгоритм:")
        algorithm_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.algorithm_combo = ttk.Combobox(self, values=["default", "strict"]) # Используем ttk.Combobox
        self.algorithm_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.algorithm_combo.set(self.settings.algorithm)  # Устанавливаем значение из настроек

        # Custom setting label and entry
        custom_setting_label = tk.Label(self, text="Произвольная настройка:")
        custom_setting_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.custom_setting_entry = tk.Entry(self, width=30)
        self.custom_setting_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.custom_setting_entry.insert(0, self.settings.custom_setting) # Заполняем значением из настроек

        # Generate password button
        generate_btn = tk.Button(self, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.grid(row=4, column=0, columnspan=3, pady=10) # Кнопка во всю ширину

        # Display generated password
        password_label = tk.Label(self, text="Сгенерированный пароль:")
        password_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        password_display = tk.Entry(self, textvariable=self.generated_password, width=40)
        password_display.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        copy_button = tk.Button(self, text="Копировать", command=self.copy_password)
        copy_button.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Layout using grid
        for i in range(6):  # Add some padding to each row
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(1, weight=1) # Allow the entry to expand

    def load_settings_into_gui(self):
        """Загружает настройки из объекта settings в GUI."""
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, str(self.settings.length))
        self.use_letters_var.set(self.settings.use_letters)
        self.use_digits_var.set(self.settings.use_digits)
        self.use_symbols_var.set(self.settings.use_symbols)
        self.algorithm_combo.set(self.settings.algorithm)
        self.custom_setting_entry.delete(0, tk.END)
        self.custom_setting_entry.insert(0, self.settings.custom_setting)

    def save_settings(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Обновляем settings перед сохранением
                self.update_settings_from_gui()
                self.settings.save_to_file(file_path)
                messagebox.showinfo("Успех", "Настройки успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")

    def load_settings(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.settings.load_from_file(file_path)
                self.load_settings_into_gui() # Загружаем настройки в GUI после загрузки из файла
                messagebox.showinfo("Успех", "Настройки успешно загружены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить настройки: {str(e)}")

    def reset_settings(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить настройки к значениям по умолчанию?"):
            try:
                self.settings.reset_to_defaults()
                self.load_settings_into_gui()  # Обновляем GUI после сброса
                messagebox.showinfo("Успех", "Настройки сброшены к значениям по умолчанию")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сбросить настройки: {str(e)}")

    def update_settings_from_gui(self):
        """Сохраняет значения из GUI в объект settings."""
        try:
            self.settings.length = int(self.length_entry.get()) # Преобразуем в int
        except ValueError:
            messagebox.showerror("Ошибка", "Длина пароля должна быть целым числом")
            return False # Возвращаем False, чтобы остановить сохранение, если есть ошибка

        self.settings.use_letters = self.use_letters_var.get()
        self.settings.use_digits = self.use_digits_var.get()
        self.settings.use_symbols = self.use_symbols_var.get()
        self.settings.algorithm = self.algorithm_combo.get()
        self.settings.custom_setting = self.custom_setting_entry.get()

        return True # Возвращаем True, если все прошло успешно

    def generate_password(self):
        """Генерирует пароль на основе текущих настроек."""
        if not self.update_settings_from_gui(): # Сначала обновляем настройки
            return # Если update_settings_from_gui возвращает False, прекращаем выполнение

        try:
            password = password_generator.generate_password(
                self.settings.length,
                self.settings.use_letters,
                self.settings.use_digits,
                self.settings.use_symbols,
                self.settings.algorithm
            )
            self.generated_password.set(password) # Обновляем переменную generated_password
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e)) # Показываем ошибку, если что-то пошло не так

    def copy_password(self):
        """Копирует сгенерированный пароль в буфер обмена."""
        try:
            pyperclip.copy(self.generated_password.get())
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
        except pyperclip.PyperclipException:
            messagebox.showerror("Ошибка", "Не удалось скопировать пароль. Возможно, pyperclip не установлен.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
