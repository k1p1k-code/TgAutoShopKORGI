# :dog: Telegram Autoshop Korgi
![](https://i.imgur.com/Lzch3s4.jpeg)
**🤖: Данный скрипт создан для авто продаж в телеграмме. С огромным функционалом**

**Присоединяйтеся к телеграмм [каналу](https://t.me/AutoShopKorgi)**
___
# 📋 **Навигация**
* [Начало](#dog-telegram-autoshop-korgi)
* [Цели](#page_with_curl-цели)
* [Установка](#arrow_down-установка)
* [Настройка бота](#wrench-настройка-бота)
  - [Настройка платёжной системы](#credit_card-настройка-платёжной-системы )
  - [Изменение текстов](#green_book-изменение-текстов)
  - [Установка плагина](#electric_plug-установка-плагинов)
* [Туториал по созданию плагинов](/creat_plugin.md) 



# :page_with_curl: Цели
- [x] Выпустить бота
- [ ] Подробнная статистика
- [ ] Изменение надписей кнопок
- [ ] Сделать систему оплаты звездами 
- [ ] Сделать реферальную систему
- [ ] Сделать систему промокодов
- [ ] Улучшить админ меню
- [ ] Оптимизаця

---
# :arrow_down: **Установка**
1. Скачать скриптПерейти в [realese](https://github.com/k1p1k-code/TgAutoShopKORGI/releases) установить AutoShopKorgi.zip 
2. Распокавать в каталоге без латинице 
3. Открыть терминал в детекторе AutoShopByK1p1k
4. Установить зависимости 
``` shell
pip install -r reqments.txt
```
5. Открыть config.py 
заполнить
``` python 
token_bot=''
admin_id=int()
timezone='Europe/Moscow'
```
6. Запустить скрипт 
``` shell 
python main.py
```

## Продвинутый способ запуска

``` python 
#Не заполнять config.py
token_bot=''
admin_id=int()
timezone='Europe/Moscow'
```

Сразу передать через аргументы token_bot, admin_id(пожеланию), timezone(пожеланию)

Если аргумента нет то он береться из config.py

```
python main.py --token_bot 54354353:fdsfsd... 
```


Примеры:
```
python main.py --token_bot 54354353:fdsfsd... --admin_id 432423 --timezone Europe/Moscow 
python main.py --token_bot 54354353:fdsfsd... 
python main.py --token_bot 54354353:fdsfsd...  --admin_id 432423
python main.py --token_bot 54354353:fdsfsd... --timezone Europe/Moscow
python main.py --admin_id 432423 --timezone Europe/Moscow
```
___
# :wrench: **Настройка бота**

## :credit_card: Настройка платёжной системы 
**В боте присутствуют две платёжной системы, со временем будет больше**

1\. Открыть настройки
```/admin``` > ```💳 Способы оплаты```

2\. Выбрать платёжную систему 
**Yoomoney - [создать токен ](https://yoomoney.ru/myservices/new)** ил **Lolz - [создать токен ](https://lolz.live/account/api)**

3\. Вести токен 
Платежная > токен 

4\. Нажать включить/выключить 

## :green_book: Изменение текстов


```/admin``` > ```⚙️ Настройки``` > ```📖 Текста```


## :electric_plug: **Установка плагинов**
**Примечание: плагины имеют больше возможностей чем админ использование плагинов не из [телеграмм канал](https://t.me/AutoShopKorgi), создатель спирта не несёт ответственность.**

1\. Установить плагин можно [здесь](https://t.me/AutoShopKorgi)

2\. Перенести плагин в папку ```plugins```

3\. Запустить скрипт 

4\. Проверить плагин ```/admin``` > ```🧩 Плагины ``` > ```ваш плагин ```(название файла плагина)

Важно: не устанавливать два плагина с одинаковым названием 

