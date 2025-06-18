import unittest
import password_generator
import settings

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
        password = password_generator.generate_password(10, True, True, True, algorithm="strict")
        self.assertEqual(len(password), 10)
        # Дополнительные проверки:
        # 1. Убедиться, что есть хотя бы одна буква, цифра и символ.
        # 2. Проверить, что длина пароля соответствует заданной.
    def test_settings_save_load(self):
        settings_obj = settings.PasswordSettings(length=20, use_letters=False, use_digits=True, use_symbols=True, algorithm="strict")
        settings_obj.save_to_file("test_settings.json")

        loaded_settings = settings.PasswordSettings()
        loaded_settings.load_from_file("test_settings.json")

        self.assertEqual(settings_obj.length, loaded_settings.length)
        self.assertEqual(settings_obj.use_letters, loaded_settings.use_letters)
        self.assertEqual(settings_obj.use_digits, loaded_settings.use_digits)
        self.assertEqual(settings_obj.use_symbols, loaded_settings.use_symbols)
        self.assertEqual(settings_obj.algorithm, loaded_settings.algorithm)
        import os
        os.remove("test_settings.json") # Clean up after the test

if __name__ == '__main__':
    unittest.main()
