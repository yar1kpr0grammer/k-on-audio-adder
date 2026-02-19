import subprocess
from pathlib import Path

BASE_DIR = Path(".")
AUDIO_DIR = BASE_DIR / "RUS Sound" / "[Ancord]"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "_temp"


def ensure_directories():
    """Создать служебные директории если их нет."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    TEMP_DIR.mkdir(exist_ok=True)


def find_videos():
    """Найти подходящие видеофайлы."""
    for video in BASE_DIR.glob("[[]Winter[]] K-On! *.mkv"):
        if "(" not in video.name:
            yield video


def get_audio_for_video(video: Path) -> Path | None:
    """Вернуть путь к аудио для видео или None если нет."""
    audio = AUDIO_DIR / video.with_suffix(".mka").name
    return audio if audio.exists() else None


def convert_audio_to_opus(input_audio: Path, output_audio: Path):
    """Конвертировать аудио в Opus через ffmpeg."""
    print(f"▶ Конвертация в Opus: {input_audio.name}")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_audio),
            "-c:a",
            "libopus",
            "-b:a",
            "192k",
            str(output_audio),
        ],
        check=True,
    )


def mux_audio_with_video(video: Path, audio: Path, output: Path):
    """Добавить аудиодорожку в MKV через mkvmerge."""
    print("   ▶ Mux...")

    subprocess.run(
        [
            "mkvmerge",
            "-o",
            str(output),
            str(video),
            "--language",
            "0:rus",
            "--track-name",
            "0:Ancord",
            "--default-track",
            "0:yes",
            str(audio),
        ],
        check=True,
    )


def process_video(video: Path):
    """Полный пайплайн обработки одного видео."""
    print(f"\n🎬 Обработка: {video.name}")

    audio = get_audio_for_video(video)

    if not audio:
        print("❌ Аудио не найдено")
        return

    temp_audio = TEMP_DIR / f"{video.stem}.opus"
    output_file = OUTPUT_DIR / video.name

    try:
        convert_audio_to_opus(audio, temp_audio)
        mux_audio_with_video(video, temp_audio, output_file)
        print("✅ Готово")
    finally:
        if temp_audio.exists():
            temp_audio.unlink()  # удаляем временный файл


def main():
    ensure_directories()

    for video in find_videos():
        process_video(video)

    print("\n🚀 Все файлы обработаны.")


if __name__ == "__main__":
    main()
