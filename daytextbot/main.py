import speech_recognition as sr


def main():
    recognizer = sr.Recognizer()

    with sr.AudioFile("test2.wav") as audio_file:
        audio = recognizer.record(audio_file)

    # Trying to translate speech to text
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Распознано: {text}")
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
