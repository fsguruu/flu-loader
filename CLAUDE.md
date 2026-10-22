# FentLoader Ultra — Telegram-бот

Telegram-бот (aiogram 3, Python 3.11), який у групах і ЛС ловить посилання на Instagram / TikTok / YouTube Shorts,
завантажує медіа і відповідає відео/каруселлю + окремим аудіо з обкладинкою. Доступ — за одноразовими ключами `FLU_...`.
Плюс розважальні команди (`/gay`, `/dating`, `/cock`, `/pussy`, `/drug`) і `@all` для тегу всіх учасників.

## Запуск

- Прод: сервер AlphaVPS, `git pull && docker compose up -d --build` — піднімає `cobalt-api`
  (self-hosted Cobalt, порт назовні НЕ публікується) і `telegram-bot`.
  `.env` і `bot_msgs_local.py` на сервер кладуться вручну (їх немає в git).
- Локально: `python main.py` з `.venv`. Cobalt (`COBALT_URL`, за замовч. `http://cobalt-api:9000/`) локально недоступний,
  тож перший рівень завантаження впаде і спрацюють fallback-и.
- Тестів і лінтера немає.
- `legacy/` — старий невикористовуваний код (RapidAPI-провайдер, старий Shorts-сервіс), у `.gitignore`. Не імпортувати.

## Змінні оточення (`.env`, ніколи не виводити значення)

`BOT_TOKEN`, `ADMIN_ID`, `APIFY_API_TOKEN`, `FFMPEG_PATH`, `BOT_MODE` (шаблон — `.env.example`).
`COBALT_URL` задається в docker-compose. `RAPIDAPI_KEY` потрібен лише legacy-коду.

## Тексти і режими (prod / local)

- Усі тексти для користувачів — **тільки** в `bot_msgs.py` (prod, англійська, без матів) і `bot_msgs_local.py`
  (local, RU-сленг з матами + весь контент розважальних команд). У коді не хардкодити рядки.
- Імпорт завжди `from messages import msgs` (у `messages.py` вибір за `BOT_MODE`; `IS_LOCAL` — прапорець).
- `bot_msgs_local.py` робить `from bot_msgs import *`, тож відсутній ключ падає на prod-версію.
  Новий ключ додавати в **обидва** файли.
- Розважальні команди (`fun_commands.py`) підключаються лише при `IS_LOCAL`; їх тексти/списки — в `bot_msgs_local.py`.
- `bot_msgs_local.py` у `.gitignore` — на GitHub іде тільки prod.

## Архітектура

```
main.py                     Bot + Dispatcher, middleware, роутери, /start, фоновий cleanup, polling
middlewares/
  outer_middleware.py       OldMessagesFilterMiddleware — відкидає повідомлення, старші за 60 с
  middleware.py             UserTrackerMiddleware (пише учасників груп у БД)
                            AuthMiddleware (пускає: адміна, /start /login /cancel, стан логіну, авторизовані чати)
handlers/                   порядок include_router важливий:
  utility_commands.py       @all; адмін: /newkey(/genkey,/nk,/gk) /timeout(/out) /revive(/rev) /keys /deadkeys /ids
  fun_commands.py           розважальні команди; рандом у generative_functions.py
  auth_user.py              /login [ключ] (FSM LoginState.waiting_for_token), /cancel; у групах — лише адміни чату
  media_handler.py          catch-all @router.message(): витягує URL -> url_validator -> сервіс платформи
services/
  url_validator.py          regex -> "instagram" | "tiktok" | "youtube_shorts" | None
  instagram_service.py      Cobalt -> Apify -> yt-dlp
  tiktok_service.py         tikwm.com API -> Cobalt -> yt-dlp (також обробляє YouTube Shorts)
  telegram_sender.py        send_universal_media(message, wait_msg, media_data) — єдина точка відправки
  utils_service.py          format_caption, is_fake_file, download_temp_file, обкладинки через ffmpeg/Pillow
  cleanup_service.py        фоново видаляє файли з downloads/ старші за 30 хв
  core/                     рушії: cobalt_engine, apify_engine, ytdlp_engine
database/database.py        sqlite3 (data/main.db, у docker — volume ./data), синхронні виклики, нове з'єднання на кожну функцію
messages.py                 вибір набору текстів за BOT_MODE
bot_msgs.py / bot_msgs_local.py  тексти повідомлень (prod EN / local RU-сленг)
```

### Контракт `media_data` (для send_universal_media)

`type` ("video" | "carousel"), `video_path` (локальний файл; .jpg/.png/.webp шле як фото),
`carousel_items` ([{type, url}], ріжеться по 10), `caption` (HTML), `audio_path`, `audio_title`,
`audio_performer`, `avatar_path` (донор обкладинки для аудіо). Відправник сам видаляє файли і через 10 с — `wait_msg`.

### БД

- `bot_keys`: `is_active` = 1 вільний, 0 використаний (чат авторизований), -1 відкликаний (`/timeout`).
  Увага: `used_by_user_id` зберігає **chat_id**, а не user_id — на цьому побудовано `is_chat_authorized`.
- `chat_members` (chat_id, user_id, full_name, username) — для `@all`.

## Конвенції

- Коментарі/докстрінги — мікс RU/UA/EN. Тримайся стилю файлу.
- HTML parse_mode; імена користувачів екрануються через `html.escape`.
- Тимчасові файли — тільки в `downloads/`, завжди прибирати у `finally`.
- Блокуючий yt-dlp — через `asyncio.to_thread` / `run_in_executor`.
- Логування — тільки `logging` (`logger = logging.getLogger(__name__)`), налаштовано в `main.py`. Без `print`.
- Без голих `except:` — мінімум `except Exception:`.

## Відомі проблеми / пастки

- `requirements.txt` — UTF-8. Не перегенеровувати через `pip freeze >` у PowerShell 5 (запише UTF-16).
- `apify_engine` читає `os.getenv` при імпорті — працює, бо `load_dotenv()` викликається раніше (у `messages.py`).
- `instagram_service` і `tiktok_service` мають майже однакові блоки побудови `media_data` — кандидат на рефакторинг.
