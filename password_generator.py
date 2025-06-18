
import secrets
import string
import pyperclip  # Установите: pip install pyperclip
import json

# ========= Модуль генерации пароля (password_generator.py) =========
def generate_password(length: int, use_letters: bool, use_digits: bool, use_symbols: bool, algorithm: str = "default") -> str:
    """
    Генерирует случайный пароль заданной длины с использованием указанных наборов символов.

    Args:
        length: Длина пароля (минимум 1).
        use_letters: Использовать ли буквы (a-z, A-Z).
        use_digits: Использовать ли цифры (0-9).
        use_symbols: Использовать ли специальные символы (!@#$%^&*()).
        algorithm: Алгоритм генерации ("default" или "strict").

    Returns:
        Сгенерированный пароль.

    Raises:
        ValueError: Если длина пароля меньше 1 или недопустимый алгоритм.
    """
    if length < 1:
        raise ValueError("Длина пароля должна быть не менее 1.")

    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("Необходимо выбрать хотя бы один набор символов.")

    if algorithm == "default":
        password = ''.join(secrets.choice(characters) for _ in range(length))
    elif algorithm == "strict":
        # Гарантирует наличие хотя бы одного символа из каждого выбранного набора
        password = ""
        if use_letters:
            password += secrets.choice(string.ascii_letters)
        if use_digits:
            password += secrets.choice(string.digits)
        if use_symbols:
            password += secrets.choice(string.punctuation)

        remaining_length = length - len(password)
        if remaining_length > 0:
            password += ''.join(secrets.choice(characters) for _ in range(remaining_length))
        password_list = list(password)
        secrets.shuffle(password_list)  # Перемешиваем, чтобы символы были в случайном порядке
        password = ''.join(password_list)

    else:
        raise ValueError("Недопустимый алгоритм генерации пароля.")

    return password

# ========= Модуль настроек (settings.py) =========
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

# ========= Модуль вывода (main.py или password_generator_app.py) =========
def main():
    """
    Основная функция приложения.
    """
    settings_obj = PasswordSettings()  # Используем настройки по умолчанию
    settings_obj.load_from_file() # Загружаем сохраненные настройки

    print("Генератор паролей")
    print("Настройки по умолчанию:")
    print(settings_obj)

    while True:
        print("\nВыберите действие:")
        print("1. Сгенерировать пароль с текущими настройками")
        print("2. Изменить настройки")
        print("3. Сбросить настройки")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            try:
                password = generate_password(settings_obj.length, settings_obj.use_letters, settings_obj.use_digits, settings_obj.use_symbols, settings_obj.algorithm)
                print("\nСгенерированный пароль:", password)
                try:
                    pyperclip.copy(password)  # Копируем пароль в буфер обмена
                    print("Пароль скопирован в буфер обмена!")
                except pyperclip.PyperclipException:
                    print("Не удалось скопировать пароль в буфер обмена. Установите pyperclip (pip install pyperclip).")

            except ValueError as e:
                print("\nОшибка:", e)
                continue  #Переходим к следующей итерации цикла

            continue_generating = input("Сгенерировать еще один пароль? (y/n): ").lower()
            if continue_generating != 'y':
                break

        elif choice == '2':
            try:
                length = int(input("Введите новую длину пароля: "))
                if length < 1:
                    print("Длина пароля должна быть не менее 1.")
                    continue

                use_letters = input("Использовать буквы? (y/n): ").lower() == 'y'
                use_digits = input("Использовать цифры? (y/n): ").lower() == 'y'
                use_symbols = input("Использовать символы? (y/n): ").lower() == 'y'
                algorithm = input("Выберите алгоритм (default/strict): ").lower()

                settings_obj.length = length
                settings_obj.use_letters = use_letters
                settings_obj.use_digits = use_digits
                settings_obj.use_symbols = use_symbols
                settings_obj.algorithm = algorithm

                print("Настройки обновлены:")
                print(settings_obj)

            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число.")
            except Exception as e:
                print("Произошла ошибка при изменении настроек:", e)
        elif choice == '3':
            settings_obj.reset_to_defaults()
            print("Настройки сброшены к значениям по умолчанию.")
            print(settings_obj)
        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
