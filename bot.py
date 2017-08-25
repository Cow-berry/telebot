#-*- codimg: utf-8 -*-

import config #в нём лежит ваш токен
import telebot # для работы с телеграмом
import datetime #для работы со временем
from pathlib import Path #для проверки существования файла
import os #для удаления файлов

bot = telebot.TeleBot(config.token)#создаём объект бота

def log(message):
    logfile = open("log.txt", 'a')
    today = datetime.date.today()
    log.write(today.strftime("%d.%m.%Y") + "\n" + message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str( message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
    logfile.close()

@bot.message_handler(commands=["hw"]) # создаём того кто будет перехватывать сообщения с этой командой
def tommorrow_hw(message): # функция обрабатывающая сообщение. message -- объект, который хранит оочень много информации о пользователе, также хранит текст сообщения
    # log = open("log.txt", 'a')# делаю логи всех сообщений с этой командой
    # log.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
    # log.close()
    log(message)
    tommorrowx = datetime.date.today() + datetime.timedelta(days = 1)
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
    # log = open("log.txt", 'a')
    # log.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
    # log.close()
    log(message)
    date = message.text[8:18 ]
    if (date == '') :
        bot.send_message(message.chat.id, "вы не ввели дату в формате dd.mm.yyyy")
    else :
        try:
            hwfile = open(date + "_hw.txt", 'r')
            lines = hwfile.readlines()
            for i in lines:
                bot.send_message(message.chat.id, i)
            hwfile.close()
        except IOError:
            bot.send_message(message.chat.id, "д/з на %s ещё не записывали" %date)

@bot.message_handler(commands=["write"])
def writehw(message):
    log(message)
    if message.chat.id != 310802215:
        access = open("access.txt", 'a')
        access.write(message.chat.first_name +" "+message.chat.last_name + "\nник -- " + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - "+ message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    # log = open("log.txt", 'a')
    # log.write(message.chat.first_name +" "+message.chat.last_name + "\nник -- " + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - "+ message.text + "\n\n")
    # log.close()
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
    if p.is_file():
        hwfile = open(date + "_hw.txt", 'a')
    else:
        hwfile = open(date + "_hw.txt", 'w')
        hwfile.write("Д/з на "+ date + ":\n")
    hwfile.write(hwfin)
    hwfile.close()
    bot.send_message(message.chat.id, "Запись д/з произведена успешно")

@bot.message_handler(commands=["rewri"])
def rewrite(message):
    if message.chat.id != 310802215:
        access = open("access.txt", 'a')
        access.write(message.chat.first_name +" "+message.chat.last_name + "\nник -- " + str(message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - "+ message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    date = message.text[7:17]
    p = Path(date+"_hw.txt")
    if p.is_file():
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), date + '_hw.txt')
        os.remove(path)
    writehw(message)

@bot.message_handler(commands=["wish"])
def wish(message):
    name = message.chat.first_name +" " + message.chat.last_name
    id = str(message.chat.id)
    wish = message.text[6:]
    wishes = open("wishes.txt", 'a')
    wishes.write("имя - " + name + "\n id - " + id + "\nпожелание - " + wish +"\n\n")
    wishes.close()
    bot.send_message(message.chat.id, "Спасибо за пожелание " + message.chat.first_name +". Автор этого бота скоро его прочитает.")

if __name__ == '__main__':#создаю цикл бесконечного ожидания сообщений
    bot.polling()