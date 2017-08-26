# -*- codimg: utf-8 -*-

import config  # в нём лежит ваш токен
import telebot  # для работы с телеграмом
import datetime  # для работы со временем
import time
from pathlib import Path  # для проверки существования файла
import os  # для удаления файлов

bot = telebot.TeleBot(config.token)  # создаём объект бота


def log(message):
    logfile = open("log.txt", 'a')
    today = datetime.date.today()
    logfile.write(
        time.strftime("%d.%m.%Y  %H:%M:%S", time.localtime(time.time())) + "\n" + message.chat.first_name + " " + message.chat.last_name + "\nник -- "
        + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - "+ message.text + "\n\n")
    logfile.close()

def write_file(name, text):
    file = open(name, 'w')
    file.write(text)
    file.close()


def add_file(name, text):
    file = open(name, 'a')
    file.write(text)
    file.close()

def is_autor(id):
    if id == config.id:
        return True
    else:
        return False

@bot.message_handler(commands=["hw"])  # создаём того кто будет перехватывать сообщения с этой командой
def tommorrow_hw(message):  # функция обрабатывающая сообщение. message -- объект, который хранит оочень много информации о пользователе, также хранит текст сообщения
    log(message)
    tommorrowx = datetime.date.today() + datetime.timedelta(days=1)
    tommorrow = tommorrowx.strftime("%d.%m.%Y")
    try:
        hwfile = open(tommorrow + "_hw.txt", 'r')
        lines = hwfile.readlines()
        for i in lines:
            bot.send_message(message.chat.id, i)
        hwfile.close()
    except IOError:
        bot.send_message(message.chat.id, "д/з на завтра ещё не записывали")


@bot.message_handler(commands=["hwdate"])
def date_hw(message):
    log(message)
    date = message.text[8:18]
    if (date == ''):
        bot.send_message(message.chat.id, "вы не ввели дату в формате dd.mm.yyyy")
    else:
        try:
            hwfile = open(date + "_hw.txt", 'r')
            lines = hwfile.readlines()
            for i in lines:
                bot.send_message(message.chat.id, i)
            hwfile.close()
        except IOError:
            bot.send_message(message.chat.id, "д/з на %s ещё не записывали" % date)


@bot.message_handler(commands=["write"])
def writehw(message):
    log(message)
    autor = is_autor(message.chat.id)
    if not (autor):
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    text = message.text
    date = text[7:17]
    hw = text[18:]
    split = hw.split("\\n")
    hwfin = ''
    for i in split:
        hwfin = hwfin + i + "\n"
    if (date == ''):
        bot.send_message(message.chat.id, "Вы не ввели дату в формате dd.mm.yyyy")
        return
    if hwfin == '':
        bot.send_message(message.chat.id, "Вы не ввели дз")
        return
    p = Path(date + "_hw.txt")
    if not (p.is_file()):
        hwfin = "Д/з на " + date + ":\n" + hwfin
    add_file(date + "_hw.txt", hwfin)
    bot.send_message(message.chat.id, "Запись д/з произведена успешно")


@bot.message_handler(commands=["rewri"])
def rewrite(message):
    autor = is_autor(message.chat.id)
    if not(autor):
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    date = message.text[7:17]
    p = Path(date + "_hw.txt")
    write_file(date + "_hw.txt", "Д/з на " + date + ":\n")
    writehw(message)


@bot.message_handler(commands=["wish"])
def wish(message):
    name = message.chat.first_name + " " + message.chat.last_name
    id = str(message.chat.id)
    wish = message.text[6:]
    wishes = open("wishes.txt", 'a')
    wishes.write("имя - " + name + "\n id - " + id + "\nпожелание - " + wish + "\n\n")
    wishes.close()
    bot.send_message(message.chat.id, "Спасибо за пожелание " + message.chat.first_name + ". Автор этого бота скоро его прочитает.")


@bot.message_handler(commands=["info"])
def info(message):
    log(message)
    id = message.chat.id
    infofile = open("info.txt", 'r')
    lines = infofile.readlines()
    if lines == []:
        bot.send_message(id, "На данный момент нет никакой важной информации.")
        return
    for i in lines:
        if i != '':
            bot.send_message(id, i)
    infofile.close()


@bot.message_handler(commands=["info_remove"])
def remove_info(message):
    autor = is_autor(message.chat.id)
    if not (autor):
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    log(message)
    write_file("info.txt", '')
    bot.send_message(message.chat.id, "Информацияя успешно удалена")


@bot.message_handler(commands=["info_add"])
def add_info(message):
    autor = is_autor(message.chat.id)
    if not (autor):
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    log(message)
    infotext = message.text[10:]
    split = infotext.split("\\n")
    infofin = ''
    for i in split:
        infofin = infofin + i + "\n"
    add_file("info.txt", infofin)
    bot.send_message(message.chat.id, "Информация записана успешно")


if __name__ == '__main__':  # создаю цикл бесконечного ожидания сообщений
    bot.polling()
