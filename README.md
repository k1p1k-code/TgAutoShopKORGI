# :dog: Telegram Autoshop Korgi
![](https://i.imgur.com/Lzch3s4.jpeg)
**🤖: Данный скрипт создан для авто продаж в телеграмме. С огромным функционалом**

**Присоединяйтеся к телеграмм [каналу](https://t.me/AutoShopKorgi)**
___
# 📋 **Навигация**
* [Начало](#dog-telegram-autoshop-korgi)
* [Установка](#arrow_down-установка)
* [Настройка бота](#wrench-настройка-бота)
  - [Установка плагина](#electric_plug-установка-плагинов)
  -  [Настройка платёжной системы](#credit_card-настройка-платёжной-системы )
* [Туториал по созданию плагинов](/creat_plugin.md) 


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
Заполнить
``` python 
token='токен от бота'
admin_id='телеграмм айди админа'
```
6. Запустить скрипт 
``` shell 
python3 app.py
```
___
# :wrench: **Настройка бота**
## :electric_plug: **Установка плагинов**
**Примечание: плагины имеют больше возможностей чем админ использование плагинов не из [телеграмм канал](https://t.me/AutoShopKorgi), создатель спирта не несёт ответственность.**

1\. Установить плагин можно [здесь](https://t.me/AutoShopKorgi)

2\. Перенести плагин в папку ```plugins```

3\. Запустить скрипт 

4\. Проверить плагин ```/admin``` > ```🧩 Плагины ``` > ```ваш плагин ```(название файла плагина)

Важно: не устанавливать два плагина с одинаковым названием 

## :credit_card: Настройка платёжной системы 
**В боте присутствуют две платёжной системы, со временем будет больше**

1\. Открыть настройки
```/admin``` > ```💳 Способы оплаты```

2\. Выбрать платёжную систему 
**Yoomoney - [создать токен ](https://yoomoney.ru/myservices/new)**
**Lolz - [создать токен ](https://lolz.live/account/api)**

3\. Вести токен 
Платежная > токен 

4\. Нажать включить/выключить 
