import os
import sys
import logging
import asyncio
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.file import File
import speech_recognition as sr
from pydub import AudioSegment


# Gets token from environment
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("Соси")


@dp.message(F.voice)
async def handle_voice(message: Message):
    voice_file_id = message.voice.file_id
    source_voice_file_name = f"{voice_file_id}.ogg"
    voice_file_name_for_recognize = f"{voice_file_id}.wav"

    # Downloading voice file
    voice_file: File = await bot.get_file(voice_file_id)
    await bot.download_file(voice_file.file_path, source_voice_file_name)

    # Converting ogg to wav
    audio_ogg = AudioSegment.from_file(source_voice_file_name, format="ogg")
    audio_ogg.export(voice_file_name_for_recognize, format="wav")

    # Removing source voice file
    os.remove(source_voice_file_name)

    recognizer = sr.Recognizer()

    # Gets audio from converted voice file
    with sr.AudioFile(voice_file_name_for_recognize) as audio_file:
        audio = recognizer.record(audio_file)

    # Trying to translate speech to text
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        answer = text
    except sr.UnknownValueError:
        answer = "Не удалось распознать речь"
    except sr.RequestError as e:
        answer = f"Ошибка: {e}"

    await message.answer(answer)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
