import pyaudio
import wave

CHUNK = 1024  # Количество кадров за раз
FORMAT = pyaudio.paInt16  # 2 байта на кадр
CHANNELS = 2  # Стерео режим
FRAME_RATE = 44100  # Частота дискретизации
SECONDS = 10  # Продолжительность записи

recorder = pyaudio.PyAudio()  # Создаем объект для PortAudio

# Настройка и открытие аудиопотока для записи
stream = recorder.open(format=FORMAT, channels=CHANNELS, rate=FRAME_RATE,
                       input=True, frames_per_buffer=CHUNK)

frames = []

# Читаем блоки аудио в течение 10 секунд
for i in range(0, int(FRAME_RATE / CHUNK * SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()  # Останавливаем запись
stream.close()  # Закрываем поток
recorder.terminate()  # Освобождаем ресурсы PyAudio

# Сохраняем запись в WAV-файл
with wave.open("output.wav", 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(recorder.get_sample_size(FORMAT))
    wf.setframerate(FRAME_RATE)
    wf.writeframes(b''.join(frames))

print("Запись завершена и сохранена в 'output.wav'")
