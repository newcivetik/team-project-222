import json

class PasswordSettings:
    """
    Класс для хранения настроек генератора паролей.
    """
    def __init__(self, length: int = 16, use_letters: bool = True, use_digits: bool = True, use_symbols: bool = False, algorithm: str = "default"):
        self.length = length
        self.use_letters = use_letters
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.algorithm = algorithm # Добавляем алгоритм

    def __str__(self):
        return (f"Длина: {self.length}, Буквы: {self.use_letters}, "
                f"Цифры: {self.use_digits}, Символы: {self.use_symbols}, Алгоритм: {self.algorithm}")

    def save_to_file(self, filename="settings.json"):
        """
        Сохраняет настройки в файл JSON.
        """
        with open(filename, "w") as f:
            json.dump(self.__dict__, f)  # Сохраняем все атрибуты объекта в JSON

    def load_from_file(self, filename="settings.json"):
        """
        Загружает настройки из файла JSON.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.length = data.get("length", self.length)
                self.use_letters = data.get("use_letters", self.use_letters)
                self.use_digits = data.get("use_digits", self.use_digits)
                self.use_symbols = data.get("use_symbols", self.use_symbols)
                self.algorithm = data.get("algorithm", self.algorithm)
        except FileNotFoundError:
            print("Файл настроек не найден. Используются настройки по умолчанию.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла настроек. Используются настройки по умолчанию.")

    def reset_to_defaults(self):
        """
        Сбрасывает настройки к значениям по умолчанию.
        """
        self.length = 16
        self.use_letters = True
        self.use_digits = True
        self.use_symbols = False
        self.algorithm = "default"
