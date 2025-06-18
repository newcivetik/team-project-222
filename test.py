import unittest
import password_generator
import settings
import string
import os # Для удаления файла

class TestPasswordGenerator(unittest.TestCase):

    def test_generate_password_valid_length(self):
        password = password_generator.generate_password(10, True, True, True)
        self.assertEqual(len(password), 10)

    def test_generate_password_invalid_length(self):
        with self.assertRaises(ValueError):
            password_generator.generate_password(0, True, True, True)

    def test_generate_password_no_characters(self):
        with self.assertRaises(ValueError):
            password_generator.generate_password(10, False, False, False)

    def test_generate_password_strict_algorithm(self):
        length = 12
        use_letters = True
        use_digits = True
        use_symbols = True
        password = password_generator.generate_password(length, use_letters, use_digits, use_symbols, algorithm="strict")

        self.assertEqual(len(password), length)

        has_letter = any(c in string.ascii_letters for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        self.assertTrue(has_letter, "Пароль должен содержать хотя бы одну букву")
        self.assertTrue(has_digit, "Пароль должен содержать хотя бы одну цифру")
        self.assertTrue(has_symbol, "Пароль должен содержать хотя бы один символ")

    def test_generate_password_strict_algorithm_insufficient_length(self):
        with self.assertRaises(ValueError):
            password_generator.generate_password(2, True, True, True, algorithm="strict")

    def test_generate_password_strict_algorithm_only_letters(self):
        length = 8
        password = password_generator.generate_password(length, True, False, False, algorithm="strict")
        self.assertEqual(len(password), length)
        self.assertTrue(all(c in string.ascii_letters for c in password))  # Убедимся, что все символы - буквы

    def test_settings_save_load(self):
        settings_obj = settings.PasswordSettings(length=20, use_letters=False, use_digits=True, use_symbols=True, algorithm="strict")
        file_path = "test_settings.json"  # Используем переменную для имени файла
        settings_obj.save_to_file(file_path)

        loaded_settings = settings.PasswordSettings()
        loaded_settings.load_from_file(file_path)

        self.assertEqual(settings_obj.length, loaded_settings.length)
        self.assertEqual(settings_obj.use_letters, loaded_settings.use_letters)
        self.assertEqual(settings_obj.use_digits, loaded_settings.use_digits)
        self.assertEqual(settings_obj.use_symbols, loaded_settings.use_symbols)
        self.assertEqual(settings_obj.algorithm, loaded_settings.algorithm)

        # Дополнительная проверка: убедимся, что загруженные настройки действительно отличаются от дефолтных.
        default_settings = settings.PasswordSettings()
        self.assertNotEqual(loaded_settings.length, default_settings.length) #хотя бы один параметр должен отличаться

        os.remove(file_path) # Clean up after the test

if __name__ == '__main__':
    unittest.main()