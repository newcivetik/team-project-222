import random
import string

def generate_password(length: int, use_letters: bool, use_digits: bool, use_symbols: bool, algorithm: str = "default") -> str:
    """
    Генерирует случайный пароль заданной длины с использованием указанных наборов символов.
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
        password = ''.join(random.choice(characters) for _ in range(length))
    elif algorithm == "strict":
        chosen_sets = []
        if use_letters:
            chosen_sets.append(string.ascii_letters)
        if use_digits:
            chosen_sets.append(string.digits)
        if use_symbols:
            chosen_sets.append(string.punctuation)

        num_chosen_sets = len(chosen_sets)
        if length < num_chosen_sets:
            raise ValueError("Длина пароля должна быть не меньше количества выбранных наборов символов при использовании strict алгоритма.")

        password_list = [random.choice(s) for s in chosen_sets]
        remaining_length = length - num_chosen_sets
        characters = "".join(chosen_sets)

        for _ in range(remaining_length):
            password_list.append(random.choice(characters))

        random.shuffle(password_list)
        password = ''.join(password_list)
    else:
        raise ValueError("Недопустимый алгоритм генерации пароля.")

    return password