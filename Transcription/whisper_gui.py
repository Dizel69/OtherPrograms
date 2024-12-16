import whisper
import ttkbootstrap as ttk  # Используем ttkbootstrap
from ttkbootstrap.constants import *  # Для управления стилями
from tkinter import filedialog, messagebox, simpledialog
from threading import Thread
from docx import Document  # Для сохранения в .docx

# Глобальная модель Whisper
model = None

# Словарь описаний моделей
MODEL_DESCRIPTIONS = {
    "tiny": "Очень быстрая, но низкая точность.",
    "base": "Быстрая, средняя точность.",
    "small": "Медленнее, но высокая точность.",
    "medium": "Высокая точность, медленная.",
    "large": "Наивысшая точность, очень медленная."
}

# Функция загрузки модели
def load_model(model_name="large"):
    global model
    model = whisper.load_model(model_name)

# Функция транскрибации
def transcribe_audio(file_path, language):
    try:
        if model is None:
            raise RuntimeError("Модель еще загружается. Подождите.")
        result = model.transcribe(file_path, language=language)
        return format_text(result["text"])
    except Exception as e:
        return f"Ошибка: {e}"

# Функция автоформатирования текста
def format_text(text):
    sentences = text.split(".")
    formatted_text = "\n\n".join(sentence.strip() + "." for sentence in sentences if sentence)
    return formatted_text

# Обработчик выбора файла
def select_file():
    file_path = filedialog.askopenfilename(
        title="Выберите аудиофайл",
        filetypes=(
            ("Аудиофайлы", "*.mp3 *.wav *.m4a *.ogg"),
            ("Все файлы", "*.*")
        ),
    )
    if file_path:
        entry_file_path.delete(0, END)
        entry_file_path.insert(0, file_path)

# Сохранение сразу в DOCX
def save_transcription(text):
    save_path = filedialog.asksaveasfilename(
        title="Сохраните результат",
        defaultextension=".docx",
        filetypes=(("Документ Word", "*.docx"), ("Все файлы", "*.*"))
    )

    if save_path:
        doc = Document()
        doc.add_heading("Результат транскрибации", level=1)
        doc.add_paragraph(text)
        doc.save(save_path)
        messagebox.showinfo("Успех", "Файл сохранён как DOCX!")
    else:
        messagebox.showwarning("Ошибка", "Файл не был сохранён!")

# Обработчик кнопки "Распознать"
def recognize_audio():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showwarning("Ошибка", "Выберите файл для распознавания!")
        return

    selected_language = language_selector.get().split(" - ")[0]

    btn_recognize.config(state=DISABLED)
    text_result.delete(1.0, END)
    text_result.insert(END, "Распознаю текст...\n")

    def process():
        transcription = transcribe_audio(file_path, selected_language)
        text_result.delete(1.0, END)
        text_result.insert(END, transcription)
        if transcription and "Ошибка" not in transcription:
            save_transcription(transcription)
        btn_recognize.config(state=NORMAL)

    Thread(target=process).start()

# Обработчик переключения темы
def change_theme():
    selected_theme = theme_selector.get()
    root.style.theme_use(selected_theme)

# Обработчик для полноэкранного режима
def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Обработчик для выбора модели
def select_model():
    selected = model_selector.get().split(" - ")[0]
    text_result.delete(1.0, END)
    text_result.insert(END, f"Загружаю модель {selected}...\n")
    Thread(target=lambda: load_model(selected)).start()

# Создаём интерфейс
root = ttk.Window(themename="superhero")
root.title("Whisper GUI - Распознавание аудио в текст")
root.geometry("800x600")
root.minsize(600, 400)

# Поле для ввода пути к файлу
frame_file = ttk.Frame(root)
frame_file.pack(pady=10, padx=10, fill=X)

label_file = ttk.Label(frame_file, text="Путь к аудиофайлу:", font=("Arial", 12))
label_file.pack(side=LEFT, padx=5)

entry_file_path = ttk.Entry(frame_file, width=50, font=("Arial", 12))
entry_file_path.pack(side=LEFT, padx=5, fill=X, expand=True)

btn_browse = ttk.Button(
    frame_file,
    text="Обзор",
    command=select_file,
    bootstyle="success",
    padding=8
)
btn_browse.pack(side=LEFT, padx=5)

# Выбор языка
language_selector = ttk.Combobox(
    root,
    values=["ru - Русский", "en - Английский", "de - Немецкий", "es - Испанский"],
    state="readonly",
    font=("Arial", 10),
)
language_selector.set("ru - Русский")
language_selector.pack(pady=10)

# Кнопка распознавания
btn_recognize = ttk.Button(
    root,
    text="Распознать",
    command=recognize_audio,
    bootstyle="primary",
    padding=10
)
btn_recognize.pack(pady=10)

# Поле для вывода текста
label_result = ttk.Label(root, text="Результат транскрибации:", font=("Arial", 12))
label_result.pack(anchor=W, padx=10)

text_result = ttk.Text(root, wrap=WORD, font=("Arial", 12))
text_result.pack(pady=5, padx=10, fill=BOTH, expand=True)

# Панель для выбора модели
frame_options = ttk.Frame(root)
frame_options.pack(pady=10, padx=10, fill=X)

model_selector = ttk.Combobox(
    frame_options,
    values=[f"{key} - {value}" for key, value in MODEL_DESCRIPTIONS.items()],
    state="readonly",
    font=("Arial", 10),
)
model_selector.set("large - Наивысшая точность, очень медленная.")
model_selector.pack(side=LEFT, padx=5)

btn_load_model = ttk.Button(
    frame_options,
    text="Выбрать модель",
    command=select_model,
    style="info.TButton",
    padding=5,
)
btn_load_model.pack(side=LEFT, padx=5)

# Панель переключения темы в правом нижнем углу
frame_theme = ttk.Frame(root)
frame_theme.pack(side=BOTTOM, anchor=SE, padx=10, pady=10)

theme_label = ttk.Label(frame_theme, text="Тема:")
theme_label.pack(side=LEFT)

theme_selector = ttk.Combobox(
    frame_theme,
    values=root.style.theme_names(),
    state="readonly",
    font=("Arial", 10)
)
theme_selector.set(root.style.theme_use())
theme_selector.pack(side=LEFT, padx=5)

btn_change_theme = ttk.Button(
    frame_theme,
    text="Сменить",
    command=change_theme
)
btn_change_theme.pack(side=LEFT, padx=5)

# Запуск основного цикла
root.mainloop()
