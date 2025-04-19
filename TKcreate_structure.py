import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, BooleanVar

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

class StructureGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор структуры проекта")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TCheckbutton', background='#f0f0f0')
        
        self.create_structure_var = BooleanVar(value=True)
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        create_template_btn = ttk.Button(
            button_frame, 
            text="Создать/Обновить структуру", 
            command=self.create_or_update_structure
        )
        create_template_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        analyze_project_btn = ttk.Button(
            button_frame, 
            text="Анализировать существующий проект", 
            command=self.analyze_project
        )
        analyze_project_btn.pack(side=tk.LEFT)
        
        create_structure_cb = ttk.Checkbutton(
            main_frame,
            text="Создать структуру папок и файлов автоматически",
            variable=self.create_structure_var,
            onvalue=True,
            offvalue=False
        )
        create_structure_cb.pack(pady=(0, 10), anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='white',
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_or_update_structure(self):
        """Основная функция для создания/обновления структуры"""
        target_dir = filedialog.askdirectory(title="Выберите целевую директорию")
        if not target_dir:
            return
        
        structure_file = os.path.join(target_dir, "structure.txt")
        structure_content = ""
        
        # Если файл существует и не пустой - читаем из него
        if os.path.exists(structure_file) and os.path.getsize(structure_file) > 0:
            try:
                with open(structure_file, 'r', encoding='utf-8') as f:
                    structure_content = f.read()
                self.status_var.set(f"Используется существующий файл: {structure_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл structure.txt: {str(e)}")
                return
        else:
            # Создаем новый файл с шаблоном по умолчанию
            structure_content = DEFAULT_STRUCTURE
            try:
                with open(structure_file, 'w', encoding='utf-8') as f:
                    f.write(DEFAULT_STRUCTURE)
                self.status_var.set(f"Создан новый файл шаблона: {structure_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать файл structure.txt: {str(e)}")
                return
        
        # Отображаем содержимое в текстовом поле
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, structure_content)
        
        # Если выбран чекбокс, создаем структуру
        if self.create_structure_var.get():
            try:
                self.create_actual_structure(target_dir, structure_content)
                messagebox.showinfo(
                    "Успех", 
                    f"Структура проекта успешно {'создана' if not os.path.exists(structure_file) else 'обновлена'} в {target_dir}"
                )
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать структуру: {str(e)}")
    
    def create_actual_structure(self, base_dir, structure_content):
        """Создает реальную структуру папок и файлов"""
        lines = structure_content.split('\n')
        current_path = []
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            indent_level = 0
            for char in line:
                if char in ['│', '├', '└', ' ', '─']:
                    indent_level += 1
                else:
                    break
            indent_level = indent_level // 4

            while len(current_path) > indent_level:
                current_path.pop()

            clean_line = line.replace('├──', '').replace('└──', '').replace('│', '').strip()
            if not clean_line:
                continue

            current_path.append(clean_line)
            full_path = os.path.join(base_dir, *current_path)

            if '.' in clean_line and not clean_line.endswith('/'):
                folder_path = os.path.dirname(full_path)
                if folder_path and not os.path.exists(folder_path):
                    os.makedirs(folder_path, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8'):
                    pass
            else:
                dir_path = full_path.rstrip('/')
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
    
    def analyze_project(self):
        """Анализирует существующий проект и создает файл с его структурой"""
        project_dir = filedialog.askdirectory(title="Выберите папку проекта")
        
        if not project_dir:
            return
        
        try:
            structure = self.generate_project_structure(project_dir)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, structure)
            
            save_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt")],
                initialfile="project_structure.txt",
                title="Сохранить структуру проекта"
            )
            
            if save_file:
                with open(save_file, 'w', encoding='utf-8') as f:
                    f.write(structure)
                self.status_var.set(f"Структура проекта сохранена в {save_file}")
                messagebox.showinfo("Успех", "Структура проекта успешно сохранена!")
            else:
                self.status_var.set("Структура проекта сгенерирована, но не сохранена")
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проанализировать проект: {str(e)}")
    
    def generate_project_structure(self, directory, prefix=''):
        """Рекурсивно генерирует структуру проекта в виде дерева"""
        items = os.listdir(directory)
        items.sort()
        
        structure = []
        pointers = ['├── ', '└── ']
        
        for i, item in enumerate(items):
            full_path = os.path.join(directory, item)
            
            if i == len(items) - 1:
                pointer = pointers[1]
            else:
                pointer = pointers[0]
            
            if os.path.isdir(full_path):
                structure.append(f"{prefix}{pointer}{item}/")
                new_prefix = prefix + ('    ' if i == len(items) - 1 else '│   ')
                structure.append(self.generate_project_structure(full_path, new_prefix))
            else:
                structure.append(f"{prefix}{pointer}{item}")
        
        return '\n'.join(structure)

if __name__ == '__main__':
    root = tk.Tk()
    app = StructureGeneratorApp(root)
    
    window_width = 800
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()