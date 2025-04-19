import os

DEFAULT_STRUCTURE = """my_bot/
├── bot.py
├── config.py
├── handlers/
│   ├── __init__.py
│   ├── subscription_handler.py
│   ├── payment_handler.py
│   └── usage_handler.py
├── utils/
│   └── data_manager.py
└── data/
    └── user_12345.json
"""

def create_structure_from_tree(file_path):
    # Читаем структуру из файла
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Если файл пустой, записываем в него структуру по умолчанию
    if not lines:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_STRUCTURE)
        lines = DEFAULT_STRUCTURE.split('\n')

    # Список для текущего пути
    current_path = []

    for line in lines:
        clean_line = line.strip()

        if not clean_line:  # Пропускаем пустые строки
            continue

        # Определяем уровень вложенности по количеству отступов
        indent_level = 0
        for char in line:
            if char in ['│', '├', '└', ' ', '─']:
                indent_level += 1
            else:
                break
        indent_level = indent_level // 4  # Примерное преобразование в уровень вложенности

        # Поддерживаем правильную вложенность
        while len(current_path) > indent_level:
            current_path.pop()  # Убираем из пути, если переходим на уровень выше

        # Убираем символы дерева
        clean_line = line.replace('├──', '').replace('└──', '').replace('│', '').strip()

        # Пропускаем строки, которые содержат только символы дерева
        if not clean_line:
            continue

        # Добавляем текущую строку в путь
        current_path.append(clean_line)

        # Строим полный путь
        full_path = os.path.join(*current_path)

        # Логируем, что обрабатываем файл/папку
        print(f"Обрабатываем: {clean_line} -> полный путь: {full_path}")

        # Если это файл (есть точка в названии и не заканчивается на /), то создаем файл
        if '.' in clean_line and not clean_line.endswith('/'):
            folder_path = os.path.dirname(full_path)  # Получаем путь к папке

            # Логируем создание папки
            if folder_path and not os.path.exists(folder_path):
                print(f"Создаем папку: {folder_path}")
                os.makedirs(folder_path, exist_ok=True)  # Создаем папку, если ее нет

            # Логируем создание файла
            print(f"Создаем файл: {full_path}")
            with open(full_path, 'w', encoding='utf-8') as f:
                pass  # Создаем пустой файл

        # Если это папка, создаем ее
        else:
            # Удаляем возможный слеш в конце (для папок)
            dir_path = full_path.rstrip('/')
            if not os.path.exists(dir_path):
                print(f"Создаем папку: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)

    print("✅ Структура успешно создана.")

def ensure_structure_file(file_path):
    # Если файла нет или он пустой, создаем/заполняем его
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_STRUCTURE)
        print(f"Файл {file_path} был создан/обновлен со структурой по умолчанию.")
        return True
    return False

if __name__ == '__main__':
    structure_file = 'structure.txt'
    
    # Проверяем и при необходимости создаем/обновляем файл структуры
    file_created = ensure_structure_file(structure_file)
    
    # Если файл только что создан, выводим сообщение
    if file_created:
        print(f"Файл {structure_file} был создан. Структура проекта теперь будет автоматически создана.")
    
    # Всегда создаем структуру из файла (даже если он только что создан)
    create_structure_from_tree(structure_file)