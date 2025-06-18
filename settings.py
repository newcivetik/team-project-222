import json
import tkinter as tk
from tkinter import messagebox

class PasswordSettings:
    """
    Класс для хранения настроек генератора паролей.
    """
    DEFAULT_LENGTH = 16
    DEFAULT_USE_LETTERS = True
    DEFAULT_USE_DIGITS = True
    DEFAULT_USE_SYMBOLS = False
    DEFAULT_ALGORITHM = "default"
    DEFAULT_CUSTOM_SETTING = "" # Добавляем настройку для значения из поля ввода

    def __init__(self, length: int = DEFAULT_LENGTH, use_letters: bool = DEFAULT_USE_LETTERS,
                 use_digits: bool = DEFAULT_USE_DIGITS, use_symbols: bool = DEFAULT_USE_SYMBOLS,
                 algorithm: str = DEFAULT_ALGORITHM, custom_setting: str = DEFAULT_CUSTOM_SETTING):  # Добавляем custom_setting
        self.length = length
        self.use_letters = use_letters
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.algorithm = algorithm
        self.custom_setting = custom_setting  # Сохраняем значение из поля ввода

    def __str__(self):
        return (f"Длина: {self.length}, Буквы: {self.use_letters}, "
                f"Цифры: {self.use_digits}, Символы: {self.use_symbols}, Алгоритм: {self.algorithm}, "
                f"Произвольная настройка: {self.custom_setting}")

    def save_to_file(self, filename="settings.json"):
        """
        Сохраняет настройки в файл JSON.
        """
        data = {
            "length": self.length,
            "use_letters": self.use_letters,
            "use_digits": self.use_digits,
            "use_symbols": self.use_symbols,
            "algorithm": self.algorithm,
            "custom_setting": self.custom_setting  # Сохраняем значение из поля ввода
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="settings.json"):
        """
        Загружает настройки из файла JSON.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.length = data.get("length", self.DEFAULT_LENGTH)
                self.use_letters = data.get("use_letters", self.DEFAULT_USE_LETTERS)
                self.use_digits = data.get("use_digits", self.DEFAULT_USE_DIGITS)
                self.use_symbols = data.get("use_symbols", self.DEFAULT_USE_SYMBOLS)
                self.algorithm = data.get("algorithm", self.DEFAULT_ALGORITHM)
                self.custom_setting = data.get("custom_setting", self.DEFAULT_CUSTOM_SETTING) # Загружаем значение из поля ввода

        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл настроек не найден. Используются настройки по умолчанию.")
            self.reset_to_defaults()
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка при чтении файла настроек. Используются настройки по умолчанию.")
            self.reset_to_defaults()

    def reset_to_defaults(self):
        """
        Сбрасывает настройки к значениям по умолчанию.
        """
        self.length = self.DEFAULT_LENGTH
        self.use_letters = self.DEFAULT_USE_LETTERS
        self.use_digits = self.DEFAULT_USE_DIGITS
        self.use_symbols = self.DEFAULT_USE_SYMBOLS
        self.algorithm = self.DEFAULT_ALGORITHM
        self.custom_setting = self.DEFAULT_CUSTOM_SETTING # Сбрасываем значение из поля ввода