"""
blocklist.py

Этот файл содержит черный список JWT-токенов. Он будет импортирован приложением \
и ресурсом выхода из системы, чтобы токены могли быть добавлены в черный список, \
когда пользователь выходит из системы.
"""

BLOCKLIST = set()
