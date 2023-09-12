import os
import pytube
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, TextClip
from rich.console import Console
import shutil

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def download_audio(youtube_url, output_path):
    try:
        yt = pytube.YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=output_path)
    except pytube.exceptions.PytubeError as e:
        console.print(f"Ошибка при скачивании аудио: {e}", style="bold red")
        return False
    return True

def convert_to_mp3(input_video, output_mp3):
    try:
        video = VideoFileClip(input_video)
        audio = video.audio
        audio.write_audiofile(output_mp3, codec='mp3')
    except Exception as e:
        console.print(f"Ошибка при конвертации в MP3: {e}", style="bold red")
        return False
    return True

def add_text_overlay(input_video, output_video):
    try:
        video = VideoFileClip(input_video)
        txt_clip = TextClip("MUSIC", fontsize=70, color='red')
        txt_clip = txt_clip.set_duration(video.duration)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video.duration)
        video = video.set_duration(video.duration)
        video = video.set_audio(txt_clip)
        video.write_videofile(output_video, codec='libx264', audio_codec='aac')
    except Exception as e:
        console.print(f"Ошибка при добавлении текстового оверлея: {e}", style="bold red")
        return False
    return True

def main():
    clear_console()  # Очистить консоль при запуске

    while True:
        # Текст для добавления между "music" и "================"
        additional_text = "|  \/  || | | |/ ___| |_ _| / ___|  |\n| |\/| || | | |\___ \  | | | |      |\n| |  | || |_| | ___) | | | | |___   |\n|_|  |_| \___/ |____/ |___| \____|  |\n"

        separator = "=" * 36
        styled_text = f"[red]{separator}\n{additional_text}{separator}[/red]"
        console.print(styled_text, end="\n")

        youtube_url = input("Введите URL YouTube видео (или 'q' для выхода): ")

        if youtube_url.lower() == 'q':
            break  # Выход из программы

        output_dir = "output"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        mp3_output = os.path.join(output_dir, "audio.mp3")
        if download_audio(youtube_url, mp3_output):
            console.print(f"Аудио сохранено в: [cyan]{mp3_output}[/cyan]")

        # Удаляем только файл web_video.mp4
        video_output_path = os.path.join(output_dir, "web_video.mp4")

if __name__ == "__main__":
    main()
