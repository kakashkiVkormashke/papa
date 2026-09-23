# Батя в дискорде

Бот следит только за каналом `1283109126305611799`.

Для пользователя `498130253038747648` бот отвечает не на каждое сообщение, а после случайного интервала от 10 до 50 его сообщений. После ответа интервал выбирается заново.

Для пользователя `437335754780442646` бот отвечает после каждого третьего сообщения отдельной фразой из списка `SHE_PHRASES` на 70 вариантов. Если в Discord Developer Portal включить `Presence Intent`, бот также напишет `ONLINE_PHRASE` при переходе этого пользователя из offline в online.

`BATYA_PHRASES` — список из 500 уникальных грубых фраз. Бот выбирает случайную строку через `random.choice(BATYA_PHRASES)`.

## Discord

1. Создайте приложение и бота в https://discord.com/developers/applications.
2. На странице Bot включите `Message Content Intent`.
3. Для реакции на появление в сети включите `Presence Intent`. Без него останется fallback: ответ после каждого 3-го сообщения второго пользователя.
4. Пригласите бота с правами `View Channel` и `Send Messages`.
5. Дайте доступ только к нужному каналу, если хотите жестко ограничить поведение.

## Переменные окружения

```text
DISCORD_TOKEN=токен_бота
TARGET_USER_ID=498130253038747648
SECOND_USER_ID=437335754780442646
TARGET_CHANNEL_ID=1283109126305611799
NOZAR_MIN_MESSAGES=10
NOZAR_MAX_MESSAGES=50
SECOND_USER_MESSAGE_INTERVAL=3
ONLINE_PHRASE=пошла нахуй отсюда
```

## Хостинг

Для Bothost используйте ветку `main` и включите собственный `Dockerfile`, если такая настройка есть.

```bash
python -m pip install -r requirements.txt
python -u bot.py
```
