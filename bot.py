import os
import re
from telethon import TelegramClient, events
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
ALLOWED_IDS = os.getenv("ALLOWED_IDS", "*")

if ALLOWED_IDS == "*":
    ALLOWED_IDS = None
else:
    ALLOWED_IDS = list(map(int, ALLOWED_IDS.split(",")))

class Yuki:
    def __init__(self, api_id: int, api_hash: str, allowed_ids: list[int], download_dir: str = "cache"):
        self.client = TelegramClient(device_model="PC", system_version="Windows 11", session="yuki-bot", api_id=api_id, api_hash=api_hash)
        self.allowed_ids = allowed_ids
        self.download_dir = download_dir
        self.prefixes = ["!", "/"]
        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'geo_bypass': True,
            'cookiefile': './cookies.txt',
            'progress_hooks': [self._progress_hook],
        }
        os.makedirs(self.download_dir, exist_ok=True)
        self.current_status_message = None
        self.video_meta = {}

        self.client.on(events.NewMessage)(self._handle_new_message)

    async def start(self):
        print("🚀 Запуск yuki-bot...")
        async with self.client:
            try:
                user = await self.client.get_me()
                print(f"✅ Успешный вход в аккаунт Telegram. Имя: @{user.username}, ID: {user.id}")
            except Exception as e:
                print(f"❌ Не удалось войти в аккаунт Telegram: {e}")
                return
            await self.client.run_until_disconnected()


    async def _handle_new_message(self, event: events.NewMessage.Event):
        if self.allowed_ids is not None and event.sender_id not in self.allowed_ids:
            return

        if any(event.text.startswith(f"{prefix}скачать") or event.text.startswith(f"{prefix}download") for prefix in self.prefixes):
            command_parts = event.text.split(maxsplit=1)
            if len(command_parts) >= 2 and self._is_youtube_url(command_parts[1]):
                await self._process_download_command(event, command_parts[1])
            else:
                await event.reply("❌ **Укажите корректную ссылку на YouTube.**")

    async def _process_download_command(self, event: events.NewMessage.Event, video_url: str):
        await event.delete()
        self.current_status_message = await event.reply("⏳ **Получение данных...**")

        video_file_path = None

        try:
            video_info = await self._get_video_info(video_url)
            if video_info['duration'] > 900:
                await self._update_status_message("❌ **Видео больше 15 минут.**")
                return

            video_file_path = await self._download_video(video_url)
            await self._update_status_message("⚙️ **Обработка видео...**")
            await self._update_status_message("📤 **Отправка видео...**")
            await self.client.send_file(
                event.chat_id, video_file_path, caption=self._format_video_metadata()
            )
            await self._update_status_message("✅ **Загрузка завершена**")
        except Exception as error:
            await self._update_status_message(f"❌ **Ошибка:** {error}")
        finally:
            if video_file_path and os.path.exists(video_file_path):
                os.remove(video_file_path)

            if self.current_status_message:
                try:
                    await self.current_status_message.delete()
                except Exception:
                    pass

    async def _get_video_info(self, video_url: str):
        video_info = {}
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_info['duration'] = info.get('duration', 0)
        return video_info

    async def _download_video(self, video_url: str) -> str:
        """
        Загрузка видео с помощью yt-dlp асинхронно.
        """
        video_file_path = ""

        with YoutubeDL(self.ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=True)
            video_file_path = ydl.prepare_filename(video_info)

            self.video_meta = {
                "title": video_info.get("title", "Неизвестно"),
                "uploader": video_info.get("uploader", "Неизвестно"),
                "url": video_info.get("webpage_url", video_url),
                "resolution": f"{video_info.get('width')}x{video_info.get('height')}" if video_info.get('width') and video_info.get('height') else "Неизвестно"
            }

        return video_file_path

    def _progress_hook(self, data):
        """
        Хук для отслеживания прогресса загрузки.
        """
        if data['status'] == 'finished':
            self.client.loop.create_task(
                self._update_status_message("✅ **Загрузка завершена**")
            )

    async def _update_status_message(self, new_text: str):
        """
        Обновление текущего сообщения статуса с новым текстом.
        """
        if self.current_status_message:
            try:
                await self.current_status_message.edit(new_text)
            except Exception:
                pass

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Убирает символы, которые могут ломать гиперссылки.
        """
        return re.sub(r'[()\[\]]', '', name)

    def _format_video_metadata(self) -> str:
        """
        Формирование метаданных для окончательной надписи к видео.
        """
        title = self.video_meta.get("title", "Неизвестно")
        sanitized_title = self.sanitize_name(title)
        uploader = self.video_meta.get("uploader", "Неизвестно")
        url = self.video_meta.get("url", None)
        resolution = self.video_meta.get("resolution", "Неизвестно")

        return (
            f"📄 **Название:** [{sanitized_title}]({url})\n"
            f"✍️ **Автор:** {uploader}\n"
            f"🖼 **Качество:** {resolution}\n\n"
            f"❤️ yuki-bot by @riktikdev"
        )

    @staticmethod
    def _is_youtube_url(url: str) -> bool:
        """
        Проверяет, является ли ссылка URL YouTube.
        """
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|.+\?v=)?[a-zA-Z0-9_-]{11}|https://www\.youtube\.com/shorts/[a-zA-Z0-9_-]+'
        )
        return bool(youtube_regex.match(url))

if __name__ == "__main__":
    try:
        if not API_ID or not API_HASH:
            raise ValueError("Не указаны `API_ID` или `API_HASH` в переменных окружения.")

        bot = Yuki(api_id=API_ID, api_hash=API_HASH, allowed_ids=ALLOWED_IDS)
        bot.client.loop.run_until_complete(bot.start())
    except (KeyboardInterrupt, SystemExit):
        print("\nОстановка работы скрипта...")
    except Exception as error:
        print(f"Произошла ошибка: {error}")
