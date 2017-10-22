# -*- codimg: utf-8 -*-

import logging
import config  # в нём лежит ваш токен
import telebot  # для работы с телеграмом
import datetime  # для работы со временем
import time
from pathlib import Path  # для проверки существования файла
from telebot import types # для крутых клавиатур

bot = telebot.TeleBot(config.token)  # создаём объект бота
helpmess = ["/hw =>дз на завтра если оно есть", "/hwsub - дз на определённый предмет. Просто введите эту команду, дальше станет понятно, что делать",
"/hwdate [дата в формате dd.mm.yyyy d-day, m-month, y-year] =>  дз на определённую дату если оно есть",
"/allhw  =>вся актуальную домашку",
"/timetable   =>всё известное расписание",
"/wish [текст пожелания] => автор бота прочтёт её",
"/info  => важная организационная информация",
"/help => список всех этих команд"]

def read_file(name):
        try:
            file = open(name, 'r')
        except Exception as e:
            logging.error(e)
        ls = file.readlines()
        l = ''
        for i in ls:
            l += i
        file.close()
        return l


def log(message):
    logfile = open("log.txt", 'a')
    today = datetime.date.today()
    logfile.write(
        time.strftime("%d.%m.%Y  %H:%M:%S", time.localtime(time.time())) + "  " + str(message.chat.id) + "  " + message.chat.first_name + " " + message.chat.last_name + "  "
        + str(message.chat.username) + "  " + message.text + "\n")
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
    if (id == config.id) or (id == config.kesha_id) or (id == config.gosha_id):
        return True
    else:
        return False

@bot.message_handler(commands=["hw"])  # создаём того кто будет перехватывать сообщения с этой командой
def tommorrow_hw(message):  # функция обрабатывающая сообщение. message -- объект, который хранит оочень много информации о пользователе, также хранит текст сообщения
    log(message)
    tommorrowx = datetime.date.today() + datetime.timedelta(days=1)
    if datetime.date.isoweekday(datetime.date.today()) == 6 :
        tommorrowx = tommorrowx + datetime.timedelta(days=1)
    tommorrow = tommorrowx.strftime("%d.%m.%Y")
    try:
        hw = read_file(tommorrow + "_hw.txt")
        bot.send_message(message.chat.id, hw)
    except Exception as e:
        bot.send_message(message.chat.id, "Дз на завтра не записано")
        logging.error(e)


@bot.message_handler(commands=["hwdate"])
def date_hw(message):
    log(message)
    date = message.text[8:18]
    if (date == ''):
        bot.send_message(message.chat.id, "вы не ввели дату в формате dd.mm.yyyy")
    else:
        try:
            hw = read_file(date+"_hw.txt")
            bot.send_message(message.chat.id, hw)
        except IOError:
            bot.send_message(message.chat.id, "д/з на %s ещё не записывали" % date)
        except Exception as e:
            logging.error(e)


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

@bot.message_handler(commands=['remove_hw'])
def rm_hw (message):
     autor = is_autor(message.chat.id)
     if not(autor):
         access = open("access.txt", 'a')
         access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
             message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
         access.close()
         bot.send_message(message.chat.id, "Отказано в доступе")
         return
     date = message.text[11:21]
     write_file(date+"_hw.txt", '')
     bot.send_message(message.chat.id, "ДЗ на "+date+" успешно удалено.")
    
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
    wishes.write(time.strftime("%d.%m.%Y  %H:%M:%S", time.localtime(time.time())) + "\n" + "имя - " + name + "\n id - " + id + "\nпожелание - " + wish + "\n\n")
    wishes.close()
    bot.send_message(message.chat.id, "Спасибо за пожелание " + message.chat.first_name + ". Автор этого бота скоро его прочитает.")
    bot.send_message(config.id, "Пришло пожелание от " + name + " : " + wish)


@bot.message_handler(commands=["info"])
def info(message):
    log(message)
    id = message.chat.id
    infox = read_file("info.txt")
    if infox != '':
                                                                                                                                                       bot.send_message(message.chat.id, infox)

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

@bot.message_handler(commands=["send"])
def send (message):
    autor = is_autor(message.chat.id)
    if not (autor):
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        bot.send_message(message.chat.id, "Отказано в доступе")
        return
    log(message)
    text = message.text
    id = text[6:15]
    mes = text[16:] 
    try:
        bot.send_message(id, mes)
    except Exception:
        bot.send_message(message.chat.id, "возможно вы ввели несуществующий id")

@bot.message_handler(commands=["timetable"])
def timetable (message):
    log(message)
    timetablef = open("timetable.txt", 'r')
    lines = timetablef.readlines()
    for i in lines:
        if i == '':
            bot.send_message(message.chhat.id, '.')
        else:
            bot.send_message(message.chat.id, i)
    timetablef.close()

@bot.message_handler(commands=["allhw"])
def all_hw(message):
    log(message)
    allhwf = open("allhw.txt", 'r')
    lines = allhwf.readlines()
    text = ''
    for i in lines:
        text += i
    bot.send_message(message.chat.id, text)
    allhwf.close()

@bot.message_handler(commands=["help"])
def help(message):
    id = message.chat.id
    log(message)
    for i in helpmess:
        bot.send_message(id, i)

@bot.message_handler(commands=["hwsub"])
def hwsub(message):
    log(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    try:
        subfile = open("subjects.txt", 'r')
    except Exception as e:
        logging.error(e)
        return
    subs = subfile.readlines()
    keyboard.add(*[types.KeyboardButton(name) for name in subs])
    sent = bot.send_message(message.chat.id, 'По какому предмету?', reply_markup=keyboard)
    subfile.close()
    bot.register_next_step_handler(sent, hwsent)

def hwsent(message):
    log(message)
    try:
        subfile = open(message.text + ".txt", 'r')
    except Exception as e:
        logging.error(e)
        return
    sub = subfile.readlines()
    newsub = ''
    for i in sub:
        newsub += i
    bot.send_message(message.chat.id, newsub)
    subfile.close()

@bot.message_handler(commands = ["duty"])
def duty(message):
    log(message)
    dutyf = open("duty.txt", 'r')
    lines = dutyf.readlines()
    linesx = ''
    for i in lines:
        linesx += i
    bot.send_message(message.chat.id, linesx)
    dutyf.close()

@bot.message_handler(commands=["konspekt"])
def konspekt(message):
    log(message)
    konspektf = open("konspekt.zip", 'rb')
    bot.send_document(message.chat.id, konspektf)
    konspektf.close()

@bot.message_handler(commands=["all"])
def send_all(message):
    log(message)
    if not (is_autor(message.chat.id)) :
        bot.send_message(message.chat.id, "Отказано в доступе")
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        return
    text = message.text
    if text.startswith('/all') :
        text = text[4:]
    idesf = open("id.txt", 'r')
    id = idesf.readlines()
    idesf.close()
    if text == "":
        return
    for i in id :
        bot.send_message(i, text)

@bot.message_handler(commands = ["i"])
def important(message):
    log(message)
    if not (is_autor(message.chat.id)):
        bot.send_message(message.chat.id, "Отказано в доступе")
        access = open("access.txt", 'a')
        access.write(message.chat.first_name + " " + message.chat.last_name + "\nник -- " + str(
            message.chat.username) + "\nid - " + str(message.chat.id) + "\nтекст - " + message.text + "\n\n")
        access.close()
        return
    message.text = "    появилась важная информация"
    send_all(message)

while True:
    try:
        bot.polling()
        time.sleep(1)
    except Exception as e:
        logging.error(e)
        time.sleep(1)
