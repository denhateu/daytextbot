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
    await message.answer("Мне лень че то сюда писать, поэтому просто привет!")


@dp.message(F.voice)
async def handle_voice(message: Message):
    voice_file_id = message.voice.file_id

    # Creates directory for voices if not exists
    voices_dir = "voices\\"
    if not os.path.exists(voices_dir):
        os.mkdir(voices_dir)

    source_voice_file_name = f"{voice_file_id}.ogg"
    source_voice_path = f"{voices_dir}{source_voice_file_name}"

    voice_file_name_for_recognize = f"{voice_file_id}.wav"
    recognize_voice_path = f"{voices_dir}{voice_file_name_for_recognize}"

    # Downloading voice file
    voice_file: File = await bot.get_file(voice_file_id)
    await bot.download_file(voice_file.file_path, source_voice_path)

    # Converting ogg to wav
    audio_ogg = AudioSegment.from_file(source_voice_path, format="ogg")
    audio_ogg.export(recognize_voice_path, format="wav")

    # Removing source voice file
    os.remove(source_voice_path)

    recognizer = sr.Recognizer()

    # Gets audio from converted voice file
    with sr.AudioFile(recognize_voice_path) as audio_file:
        audio = recognizer.record(audio_file)

    # Trying to translate speech to text
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        answer = text
    except sr.UnknownValueError:
        answer = "я вообще ничего не понял че там за бормотание в гс"
    except sr.RequestError as e:
        answer = f"какая-то херотень: {e}"

    await message.answer(answer)


@dp.message()
async def other_messages_handler(message: Message):
    await message.answer("а ничо тот факт что мне можно отправлять только голосовые?🙄🙄🙄")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
