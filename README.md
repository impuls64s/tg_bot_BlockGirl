# Телеграмм бот BlockGirl

### О боте:

Если вашей девушке не хватает внимания, то просто запустите бота.
Бот предназначен для блокировки девушки, чтобы  вы могли уделить время любимым играм.
В функционал бота входит 4 кнопки:
* __Флирт с джентельменом__ - бот присылает игривые сообщения и стикер с джентельменом.
* __Получить комплимент__ -  бот одаривает вашу девушку комлиментами прикрепляя ее фотографию.
* __Покажи фотку__ - присылает рандомную фотографию из папки images.
* __Викторина__ - вопросы с 4 вариантами ответа, при успешном прохождение, придется делать подарок.


### Настройки:

* __photos__ - папка которую нужно заполнить неудачными фотографиями.
* __.env__ - необходимо получить токен в тг канале @BotFather. Там же настраивается профиль.
```
API_TOKEN = твой токен тут
PHOTOS_DIRECTORY = photos # директория с фотографиями
```
* __texts__ - текста ответных сообщений, вопросы и ссылки на стикеры.


### Установка и запуск:
```
$ git clone https://github.com/impuls64s/tg_bot_BlockGirl.git
$ cd tg_bot_BlockGirl
$ pip install -r requirements.txt
$ pyton bot.py - запуск бота
$ Ctrl + C - остановка бота
```