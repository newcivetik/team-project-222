import secrets
import string

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