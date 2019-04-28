import telebot
import requests
import pydub
import apiai, json
import time
import threading
import pickle
import sqlite3
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

myQueue = 0
isExit = False
# token = "718686288:AAGsdu8eohZZXRzpsj62CxkY43D3Q9cJ23g" @drunkAndHigh
token = "750812124:AAHwoUR-Uc5C9q8l7aKgqsYgbjC35jcx1ZE"
bot = telebot.TeleBot(token)

# ------------------------------------------ Sta and Tas ---------------------------------
try:
    Sta = open('stuff.dat', 'rb').read()
    if Sta is None:
        Sta = list()
except:
    print("There is no stuff.., I made empty one")
    Sta = list()

try:
    Tas = open('tasks.dat', 'rb').read()
    if Tas is None:
        Tas = list()
except:
    print("There is no such file of tasks' list, so I will make empty one")
    Tas = list()

# ----------------------------------- Classes ------------------------------------

class Number:
    xs = 0
    con = 0
    cur = 0
    ids = 0
    def __init__(self):
        self.xs = 0
        self.con = 0
        self.cur = 0

    def ids(self):
        self.ids += 1
        return self.ids

class BankQueue:
    current = 900
    queue = 910

    def incr_queue(self):
        self.queue += 1

    def take_queue(self, id):
        self.incr_queue()
        str1 = "Номер Вашей очереди: " + str(self.queue)
        str2 = "Сейчас на очереди: " + str(self.current)
        print(str1)
        print(str2)
        bot.send_message(id, str1)
        bot.send_message(id, str2)

        return self.queue

    def incr_current(self):
        self.current += 1

    def live(self, myTurn, id):
        while True:
            self.incr_current()
            self.incr_queue()
            time.sleep(1)

            if self.current == myTurn-2:
                notify(id, "Скоро Ваша очередь \nУ вас номер: "+str(myTurn)+"\nТекущая очередь: "+str(self.current))
                break

class Staff:
    id = 0
    depid = 0
    login = ""
    password = ""
    name = ""
    surname = ""
    age = 0
    role = 0
    tasks = list()
    def __init__(self):
        self.id = 0
        self.depid = 0
        self.login = ""
        self.password = ""
        self.name = ""
        self.surname = ""
        self.age = 0
        self.role = 0
        self.tasks = list()

    def create(self, stuff):
        self.id = stuff.id
        self.depid = stuff.depid
        self.login = stuff.login
        self.password = stuff.password
        self.name = stuff.name
        self.surname = stuff.surname
        self.age = stuff.age
        self.role = stuff.role
        self.tasks = list()

    def setId(self, id):
        self.id = id
    def setDepId(self, depid):
        self.depid = depid
    def setLogin(self, login):
        self.login = login
    def setPassword(self, password):
        self.password = password
    def setName(self, name):
        self.name = name
    def setSurname(self, surname):
        self.surname = surname
    def setAge(self, age):
        self.age = age
    def setRole(self, role):
            self.role = role

    def get_hello(self):
        print('Hello', self.name, self.surname)

class Tasks:
    id = 0
    prior = 0
    depid = 0
    holder_id = 0
    des = ""
    num = 0
    req = 0
    def __init__(self):
        self.id = 0
        self.prior = 0
        self.depid = 0
        self.holder_id = 0
        self.des = ""
        self.num = 0
        self.req = 0

    def get_hello(self):
        print(self.des)

    def setId(self, id):
        self.id = id
    def setHolderId(self, holder_id):
        self.holder_id = holder_id
    def setPrior(self, prior):
        self.prior = prior
    def setDepId(self, depid):
        self.depid = depid
    def setDes(self, des):
        self.des = des
    def setNum(self, num):
        self.num = num
    def setReq(self, req):
        self.req = req



bq = BankQueue()
obj = Number()
newt = Tasks()

# ------------------------------------------ Functions ------------------------------------

# upd = bot.get_updates()
# last_upd = upd[-1]

# print(last_upd.message.json)

def task_buttons(message):
    but_markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Добавить задачу", callback_data="add")
    button2 = telebot.types.InlineKeyboardButton("Удалить задачу", callback_data="delete")
    button3 = telebot.types.InlineKeyboardButton("Выход", callback_data="exit")

    but_markup.add(button1, button2, button3)

    listTasks(message.from_user.id)
    bot.send_message(message.from_user.id, "Выберите действие", reply_markup=but_markup)

def stream_audio_file(speech_file, chunk_size=1024):

    # Chunk audio file
    with open(speech_file, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data

def client(message):
    print("You are a client")
def stuff(message):
    print("You are a stuff")


def new_id(lis):
    df = 1

    while (True):
        c = True
        for dc in lis:
            if dc.id == df:
                c = False
        if c:
            return df
        df = df + 1


'''with open('staff.dat', "rb") as file: 
Sta = pickle.load(file) 
with open('tasks.dat', "rb") as file: 
Tas = pickle.load(file)'''

def admin(message):
    print("You are an admin")

    # for admin

    log = "admin"
    pas = "admin"
    x = False
    # try:
    #     Sta = open('stuff.dat', 'rb').read()
    #     if Sta is None:
    #         Sta = list()
    # except:
    #     Sta = list()

    # for s in Sta:
    #     if s.login == log and s.password == pas and s.role == 1:
    #         obj.cur = s
    #         x = True
    #         break
    # if x:
    #     resp = '!!!There is no such admin!!!'
    # if not x:
    #     fin = list()
    #     for t in Tas:
    #         if t.depid == obj.cur.depid:
    #             fin.append(t)
    #     fin.sort()
    #     fin.reverse()
    # for f in fin:
    #     print()

    task_buttons(message)


def listTasks(myId):
    tasks = []
    try:
        with open("tasks.dat", "rb") as f:
            tasks = pickle.load(f)
            print(type(tasks))
            print(tasks)
            for t in tasks:
                bot.send_message(myId, str(t.id) + " " + t.des)
    except:
        print("There is no any task")
        bot.send_message(myId, "There is no any task")


@bot.callback_query_handler(func= lambda callback: True)
def manage_task(callback):

    if callback.data == "add":
        newt = Tasks()
        print("Enter name of the task")
        bot.send_message(callback.from_user.id, "Enter name of the task")
        obj.xs = 1
        obj.count = 0

    elif callback.data == "delete":
        obj.xs = 2
        obj.count = 0
        print("Enter id of deleting task")
        bot.send_message(callback.from_user.id, "Enter id of deleting task")
    else:
        obj.xs = 0
        obj.count = 0
        bot.send_message(callback.from_user.id, "I am hearing you...")
        return


def notify(id, info):
    bot.send_message(id, info)


def bus_bus_ticket(busid, seats):
    print("Bus: " + str(busid))
    bseats = []

    conn = sqlite3.connect("citybusdb.sqlite3")
    cursor = conn.cursor()
    get_schedule = "SELECT id FROM 'Citybus1_schedule' where bus_id = {}".format(busid)
    cursor.execute(get_schedule)
    sid = cursor.fetchone() #schedule id

    for s in seats:
        check_query = "select ocu from 'Citybus1_ticket' where sch_id = {} and id = {}".format(sid, s)
        ocu = cursor.execute(check_query)
        if ocu[0] == 1:
            bseats.append(s)

    for s in seats:
        book_ticket = "update 'Citybus1_ticke t' set ocu = 1 where sch_id = {} and id = {}".format(sid, s)
        cursor.execute(book_ticket)
        conn.commit()

    cursor.close()
    conn.close()

    if len(bseats) > 0:
        return (bseats, sid)
    else:
        return (None, sid)


def get_seats(schid):
    conn = sqlite3.connect("citybusdb.sqlite3")
    cursor = conn.cursor()

    get_query = "select id, ocu from 'Citybus1_ticket' where sch_id = {}".format(schid)

    cursor.execute(get_query)
    ss = cursor.fetchall()

    cursor.close()
    conn.close()
    return ss


def get_tickets():
    global uid
    conn = sqlite3.connect("citybusdb.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Citybus1_ticket' where hol_id = {}".format(uid))
    tickets = cursor.fetchall()
    new_tickets = []
    for t in tickets:
        global sched
        cursor.execute("select * from 'Citybus1_schedule' where id = {}".format(t[4]))
        sched = cursor.fetchone()
        data = {
            "sid": t[1],
            "source": sched[1],
            "destination": sched[2],
            "ltime": sched[3],
            "atime": sched[4],
            "driver": sched[7],
            "bus": sched[6]
        }
        new_tickets.append(data)

    return new_tickets


def get_driver(drid):
    conn = sqlite3.connect("citybusdb.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Citybus1_driver' where id = {}".format(drid))
    driver = cursor.fetchone()
    drive = {
        "name": driver[3],
        "surname": driver[4],
        "age": driver[5],
        "dr_class": driver[6]
    }
    return drive


def get_bus(busid):
    conn = sqlite3.connect("citybusdb.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'Citybus1_bus' where id = {}".format(busid))
    bus = cursor.fetchone()
    drive = {
        "id": bus[0],
        "mark": bus[2],
        "year": bus[4],
        "seats": bus[5],
    }
    return drive


def get_schedule():
    return
#     conn = sqlite3.connect("citybusdb.sqlite3")
#     cursor = conn.cursor()
#
#     cursor.execute("select * from 'Citybus1_schedule' where id = {}".format(t[4]))
#     sched = cursor.fetchone()
#     new_sched = {
#         "id": sched[0],
#         "source": sched[1],
#         "destination": sched[2],
#         "bus": sched[6],
#         "driver": sched[7],
#     }
#     cursor.close()
#     conn.close()
#
#     return new_sched

# -------------------------------------------  Decorators ------------------------------------------

@bot.message_handler(commands = ["schedule"])
def handle_schedule(message):
    listTasks(message.from_user.id)


@bot.message_handler(commands = ["tasks"])
def handle_task(message):
    task_buttons(message)

@bot.message_handler(commands = ["start"])
def handle_start(message):
    bot.send_message(message.from_user.id, "welcome")
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

    user_markup.row("/Client")
    user_markup.row("/Stuff")
    user_markup.row("/Admin")
    print(user_markup)
    bot.send_message(message.from_user.id, "Вы кто?: ", reply_markup=user_markup)

@bot.message_handler(content_types = ["commands"])
def handle_command(message):
    print("That's the command")
    but_markup = telebot.types.ReplyKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Add Task")
    button2 = telebot.types.InlineKeyboardButton("Delete Task")
    but_markup.add(button1, button2)
    bot.send_message(message.from_user.id, "Выберите действие", reply_markup=but_markup)


@bot.message_handler(content_types = ["text"])
def handle_command(message):
    print("text2")

    if obj.xs == 1:
        if obj.count == 0:
            des = message.text
            newt.setDes(des)
            obj.count += 1
            bot.send_message(message.from_user.id, "Enter required number of performed tasks")
        elif obj.count == 1:
            fer = int(message.text)
            newt.setReq(fer)
            obj.count += 1
            bot.send_message(message.from_user.id, "Enter priority as digit(1(lowest priority)-10(highest priority))")
        elif obj.count == 2:
            prior = int(message.text)
            newt.setPrior(prior)
            obj.count += 1
            bot.send_message(message.from_user.id, "Is this for special person?(enter answer and id of holder)")
        elif obj.count == 3:
            obj.cur = None
            text = message.text
            if text.lower().find('yes') != -1 or text.lower() == "y":
                textList = text.split(" ")
                zip = int(textList[1])
                newt.setHolderId(zip)
                newt.setNum(0)
                newt.setId(obj.ids())
                Tas.append(Tasks().create(newt))
            else:
                for z in Sta:
                    id = new_id(Sta)
                    if z.depid == obj.cur.depid:
                        newt.setDepId(0)
                        newt.setNum(0)
                        newt.setId(id)
                        newt.setHolderId(0)
                        Tas.append(Tasks().create(newt))
            with open('tasks.dat', "wb") as file:
                pickle.dump(Tas, file)
            task_buttons(message)

    elif obj.xs == 2:
        dele = int(message.text)
        for t in Tas:
            if t.id == dele:
                Tas.remove(t)
        with open('tasks.dat', "wb") as file:
            pickle.dump(Tas, file)
        task_buttons(message)

    else:
        if message.text == "/Client":
            client(message)

        elif message.text == "/Stuff":
            stuff(message)

        elif message.text == "/Admin":
            admin(message)

        elif message.text.lower() == "займи мне место":
            myQueue = bq.take_queue(message.from_user.id)
            t1 = threading.Thread(target=bq.live, args=(myQueue, message.from_user.id))
            t1.start()

        elif message.text.lower() == "покажи водителя":
            driver = get_driver()
            bot.send_message(message.from_user.id, "Driver:")
            bot.send_message(message.from_user.id, "name: {}".format(driver['name']))
            bot.send_message(message.from_user.id, "surname: {}".format(driver['surname']))
            bot.send_message(message.from_user.id, "age: {}".format(driver['age']))
            bot.send_message(message.from_user.id, "Driver class: {}".format(driver['dr_class']))

        elif message.text.lower() == "покажи мои билеты":
            mytickets = get_tickets()
            for t in mytickets:
                bot.send_message(message.from_user.id, "Booked seat:{}".format(t['sid']))
                bot.send_message(message.from_user.id, "source: {}".format(t['source']))
                bot.send_message(message.from_user.id, "destination: {}".format(t['destination']))
                bot.send_message(message.from_user.id, "leaving time: {}".format(t['ltime']))
                bot.send_message(message.from_user.id, "arrival time: {}".format(t['atime']))
                bot.send_message(message.from_user.id, "Driver: {}".format(t['driver']))
                bot.send_message(message.from_user.id, "Bus: {}".format(t['bus']))

        elif message.text.lower() == "покажи автобус":
            bus = get_bus()
            bot.send_message(message.from_user.id, "Bus:{}".format(bus['id']))
            bot.send_message(message.from_user.id, "Mark: {}".format(bus['mark']))
            bot.send_message(message.from_user.id, "Year: {}".format(bus['year']))
            bot.send_message(message.from_user.id, "Amount of seats: {}".format(bus['seats']))

        elif message.text.lower() == "покажи расписание":
            schedule = get_schedule()
            myQueue = bq.take_queue(message.from_user.id)
            bot.send_message(message.from_user.id, "Schedule")
            bot.send_message(message.from_user.id, "id:{}".format(schedule['id']))
            bot.send_message(message.from_user.id, "source: {}".format(schedule['source']))
            bot.send_message(message.from_user.id, "destination: {}".format(schedule['destination']))
            bot.send_message(message.from_user.id, "Bus: {}".format(schedule['bus']))
            bot.send_message(message.from_user.id, "Driver: {}".format(schedule['driver']))

        elif message.text.lower().find("купи билеты") is not -1 or message.text.lower().find("купить билеты") is not -1:
            msg = message.text.lower()
            global busid
            busid = 0
            seats = []
            isFirst = True
            for str in msg.split():
                if str.isdigit():
                    if isFirst:
                        busid = int(str)
                        break
                    else:
                        seats.append(int(str))

            bseats, sid = bus_bus_ticket(busid, seats)
            if bseats is None:
                print("Life is good")
                bot.send_message(chat_id=message.from_user.id, text="Дело сделано!")
            else:
                str = "Unfortunately, these seats are occupied already: "
                for bs in bseats:
                    str += bs + " "
                if len(seats) > len(bseats):
                    str += "But I have booked the rest"
                bot.send_message(chat_id= message.from_user.id, text= str)

            msg = "Here are the seats of bus: {}\n".format(busid)
            ss = get_seats(sid)
            for s in range(0, len(ss)):
                key = False
                if s[0] == 1:
                    key = True
                msg += "id: {} booked: {}\n".format(s[0], key)

            bot.send_message(chat_id=message.from_user.id, text=msg)

        else:
            # bot.send_message(message.from_user.id, message.text)

            request = apiai.ApiAI('b9c84a1d9d2d4626884a0033964085d4').text_request()  # Токен API к Dialogflow
            request.lang = 'ru'  # На каком языке будет послан запрос
            request.session_id = 'AIYAv1'  # ID Сессии диалога (нужно, чтобы потом учить бота)
            request.query = message.text  # Посылаем запрос к ИИ с сообщением от юзера...
            responseJson = json.loads(request.getresponse().read().decode('utf-8'))
            response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
            # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
            if response:
                bot.send_message(chat_id= message.from_user.id, text=response)
            else:
                bot.send_message(chat_id=message.from_user.id, text='Я Вас не совсем поняла!')

@bot.message_handler(content_types = ["document"])
def handle_command(message):
    print("prishel document2")

@bot.message_handler(content_types = ["audio"])
def handle_command(message):
    print("Audio")

@bot.message_handler(content_types = ["photo"])
def handle_command(message):
    print("Photo2")

@bot.message_handler(content_types = ["voice"])
def handle_command(message):
    print("Voice has been got")

    ogg_file = 'voice.oga'
    wav_file = 'voice.wav'
    # ogg_file = 'C:\\Users\\user\\Desktop\\bot\\voice recog\\voice.ogg'
    # wav_file = os.path.splitext(ogg_file)[0] + '.wav'

    bot.send_message(message.from_user.id, "голосовое сообщение обрабатывается...")

    vid = message.voice.file_id
    v_file = bot.get_file(vid)

    # downloading arrived voice file from telegram
    url = "https://api.telegram.org/file/bot" + token + "/" + v_file.file_path
    r = requests.get(url, allow_redirects=True)
    open(ogg_file, 'wb').write(r.content)

    # print(type(v_file))
    # print(v_file)

    headers = {
        'Authorization': 'Bearer KRIV3WV2U373FT3NCZEVVGLWV47M5RAG',
        'Content-Type': 'audio/wav',
        'Transfer-encoding': 'chunked'
    }

    # converting from ogg to wav
    sound = pydub.AudioSegment.from_ogg(ogg_file)
    sound.export(wav_file, format='wav')

    # recognizing the audio
    data = stream_audio_file(wav_file)
    response = requests.post('https://api.wit.ai/speech?v=2010307', headers=headers, data=data)
    print("successful")


    json_resp = response.json()
    print(json_resp)
    # bot.send_message(message.from_user.id, json['_text'])
    text = json_resp['_text'].lower()

    if text == "займи мне место":
        myQueue = bq.take_queue(message.from_user.id)
        t1 = threading.Thread(target=bq.live, args=(myQueue, message.from_user.id))
        t1.start()
    else:
        request = apiai.ApiAI('b9c84a1d9d2d4626884a0033964085d4').text_request()  # Токен API к Dialogflow
        request.lang = 'ru'  # На каком языке будет послан запрос
        request.session_id = 'AIYAv1'  # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = json_resp['_text']  # Посылаем запрос к ИИ с сообщением от юзера...
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response:
            bot.send_message(message.from_user.id, response)
        else:
            bot.send_message(message.from_user.id, 'Я Вас не совсем поняла!')


# ----------------------------------------------------

    # from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    # import apiai, json
    # updater = Updater(token='750812124:AAHwoUR-Uc5C9q8l7aKgqsYgbjC35jcx1ZE') # Токен API к Telegram
    # dispatcher = updater.dispatcher
    # Обработка команд
    # def startCommand(bot, update):
    #     bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
    # def textMessage(bot, update):
        # request = apiai.ApiAI('b9c84a1d9d2d4626884a0033964085d4').text_request() # Токен API к Dialogflow
        # request.lang = 'ru' # На каком языке будет послан запрос
        # request.session_id = 'AIYAv1' # ID Сессии диалога (нужно, чтобы потом учить бота)
        # request.query = json['_text'] # Посылаем запрос к ИИ с сообщением от юзера...
        # responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        # response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        # if response:
        #     bot.send_message(chat_id=update.message.chat_id, text=response)
        # else:
        #     bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем поняла!')
    # Хендлеры
    # start_command_handler = CommandHandler('start', startCommand)
    # text_message_handler = MessageHandler(Filters.text, textMessage)
    # Добавляем хендлеры в диспетчер
    # dispatcher.add_handler(start_command_handler)
    # dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    # updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    # updater.idle()

# ----------------------------------------------------


#
# while True:
#     try:
#         bot.polling(none_stop=True, interval=0)
#
#     except Exception as e:
#         logger.error(e)  # или просто print(e) если у вас логгера нет,
#         # или import traceback; traceback.print_exc() для печати полной инфы
#         time.sleep(15)

bot.polling(none_stop= True, interval=0)
