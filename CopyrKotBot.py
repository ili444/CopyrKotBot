# -*- coding: utf-8 -*-
# coding: utf-8
import dbworker, telebot, shelve, random, datetime, urllib, os, json
from kanc import dict2, dict_price
from telebot.types import LabeledPrice
from telebot import types
from datetime import datetime
import urllib.request as urllib2
from urllib.parse import urlparse
from PyPDF2 import PdfFileReader
import os.path
import xlrd
import requests
import pandas as pd
from docx import Document
import zipfile
from pptx import Presentation
from bs4 import BeautifulSoup
from flask import Flask, request



TOKEN = "token"
bot = telebot.TeleBot(TOKEN, threaded=False)


app = Flask(__name__)


class Markup():
    def __init__(self, start_func):
        self.start_func = start_func

    def send_check(self, chat_id, title, description, payload, provider_token, start_parameter, currency, prices,
        provider_data, photo_url, photo_size, photo_width, photo_height):
        URL = f'https://api.telegram.org/bot{TOKEN}/'
        url = URL + (f'sendinvoice?chat_id={chat_id}&title={title}&description={description}&payload={payload}&'
                f'provider_token={provider_token}&start_parameter={start_parameter}&currency={currency}&'
                f'prices={prices}&provider_data={provider_data}&photo_url={photo_url}&photo_size={photo_size}&'
                f'photo_width={photo_width}&photo_height={photo_height}&need_phone_number=True&send_phone_number_to_provider=True')
        requests.get(url)


    def inline_markup(self):
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(types.InlineKeyboardButton("Ч/Б Печать(распечатка)", callback_data='Ч/Б Печать(распечатка)'),
                   types.InlineKeyboardButton("Цветная Печать А4", callback_data='Цветная печать А4'),
                   types.InlineKeyboardButton("Печать фото 10х15", callback_data='Печать фото 10х15'),
                   types.InlineKeyboardButton('А4 Ч/Б двусторонняя', callback_data='А4 Ч/Б двусторонняя'),
                   types.InlineKeyboardButton("Печать на фотобумаге А4 (глянец, матовая)",
                                              callback_data='Печать на фотобумаге'),
                    types.InlineKeyboardButton('Распечатать при мне', callback_data='При мне')
                   )
        return markup


    def call_result(self, chat_id, callback, type_pay):
        number = f'{str(chat_id)}-{mark_up.random_pool()}'
        m, j = mark_up.result_ship(chat_id)
        now = datetime.now()
        today = datetime.today().strftime('%H:%M')
        time_order = f"{now.year}-{now.month}-{now.day}  {today}"
        from_chat_id = -3333306737777
        name = f'{callback.from_user.first_name} {callback.from_user.last_name} @{callback.from_user.username}'
        total_price = mark_up.call_value(chat_id, 'total_price')
        message_id = mark_up.call_value(chat_id, 'message_id')
        bot.edit_message_text(chat_id=callback.from_user.id, message_id=message_id,
                                  text=f'Супер!✅\nТеперь ваш заказ на сумму {str(total_price)} ₽ отправлен Копир-коту!'
                                           f'✅\n\nПозиции заказа:\n\n➕ {j} ₽\n\nЗабрать заказ можете в любое рабочее время по адресу: Проспект Мира 80а, Красноярск (ТЦ АВЕНЮ, 4 этаж)\n\n'
                                           f'Номер вашего заказа - {number}', reply_markup=mark_up.forward())
        bot.send_message(from_chat_id, f'{m}'
                                               f'_________________________________________\n\n'
                                               f'Номер заказа - {number}\n'
                                               f'Время заказа: {time_order}\n'
                                               f'Заказчик: {name}\n'
                                               f'Тип оплаты: {type_pay}\n\n'
                                               f'Итого: {str(total_price)} ₽'
                                 )
        mark_up.forward_file(chat_id, number)
        mark_up.clear_basket(chat_id)


    def call_result2(self, chat_id, message, type_pay):
        number = f'{str(chat_id)}-{mark_up.random_pool()}'
        m, j = mark_up.result_ship(chat_id)
        now = datetime.now()
        today = datetime.today().strftime('%H:%M')
        time_order = f"{now.year}-{now.month}-{now.day}  {today}"
        from_chat_id = -100140673444444
        name = f'{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}'
        total_price = mark_up.call_value(chat_id, 'total_price')
        message_id = mark_up.call_value(chat_id, 'message_id')
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text=f'Супер!✅\nТеперь ваш заказ на сумму {str(total_price)} ₽ отправлен Копир-коту!'
                                           f'✅\n\nПозиции заказа:\n\n➕ {j} ₽\n\nЗабрать заказ можете в любое рабочее время по адресу: Проспект Мира 80а, Красноярск (ТЦ АВЕНЮ, 4 этаж)\n\n'
                                           f'Номер вашего заказа - {number}', reply_markup=mark_up.forward())
        bot.send_message(from_chat_id, f'{m}'
                                               f'_________________________________________\n\n'
                                               f'Номер заказа - {number}\n'
                                               f'Время заказа: {time_order}\n'
                                               f'Заказчик: {name}\n'
                                               f'Тип оплаты: {type_pay}\n\n'
                                               f'Итого: {str(total_price)} ₽'
                                 )
        mark_up.forward_file(chat_id, number)
        mark_up.clear_basket(chat_id)


    def inline_markup2(self):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ Добавить файл", callback_data='добавить'))
        return markup


    def num_copy_markup1(self):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton('1', callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def num_copy_markup3(self):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton('1', callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data='НазадВканц')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data='корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def num_copy_markup2(self, callback, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def clear_basket(self, chat_id):
        with shelve.open('itog.py') as db:
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                del db[dd]


    def clear_basket2(self, chat_id):
        with shelve.open('itog2.py') as db:
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                del db[dd]


    def gen_markup1(self, chat_id, total_price, number_ship):
        markup = types.InlineKeyboardMarkup(True)
        a1 = types.InlineKeyboardButton("Оплата в одно касание", callback_data='now')
        a2 = types.InlineKeyboardButton("Оплатa при получении", callback_data='later')
        a3 = types.InlineKeyboardButton("Оплата переводом Яндекс.Деньги",
                                        url=f'https://money.yandex.ru/transfer?receiver=333333939823&sum={total_price}&success'
                                            f'URL=&quickpay-back-url=https://t.me/copykotbot&shop-host=&label={number_ship}&'
                                            f'targets=№{number_ship}'
                                            '&comment=&origin=form&selectedPaymentType=pc&destination='
                                            'Donate&form-comment=Donate&short-dest=&quickpay-form=shop')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data='назад_корзина')
        markup.add(a1)
        markup.add(a3)
        markup.add(a2)
        markup.add(a4)
        return markup


    def go_basket(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.add(types.InlineKeyboardButton("🛒 В корзину", callback_data='корзина'),
                   types.InlineKeyboardButton("🔃 Изменить примечание ", callback_data='примечания'),
                   types.InlineKeyboardButton("⬅ Назад", callback_data='назад')
                   )
        return markup


    def back(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data='назад')
                   )
        return markup


    def gen_markup2(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.row_width = 2
        markup.add(types.InlineKeyboardButton("🏁 Оформить", callback_data='оформить'),
                   types.InlineKeyboardButton("➕ Добавить", callback_data='добавить'),
                   types.InlineKeyboardButton("❎ Очистить", callback_data='очистить'),
                   types.InlineKeyboardButton("🔃 Изменить", switch_inline_query_current_chat='Изменить')
                   )
        return markup


    def markup_print(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.row_width = 2
        markup.add(types.InlineKeyboardButton("🏁 Отправить", callback_data='отправить'),
                   types.InlineKeyboardButton("➕ Добавить", callback_data='добавить2'),
                   types.InlineKeyboardButton("❎ Очистить", callback_data='очистить2')
                   )
        return markup


    def kancel(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.row_width = 1
        markup.add(types.InlineKeyboardButton("✏ Ручки/Карандаши", switch_inline_query_current_chat='Ручки/Карандаши'),
                   types.InlineKeyboardButton("📁 Папки и Файлы", switch_inline_query_current_chat='Папки и Файлы'),
                   types.InlineKeyboardButton("🗒 Корректирующие средства",
                                              switch_inline_query_current_chat='Корректирующие средства')
                   )
        return markup


    def klava(self, query, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def random_pool(self):
        a = random.randint(1000, 9999)
        return a


    def part_basket(self, chat_id):
        with shelve.open('itog.py') as db:
            l = []
            s = []
            r = []
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                a = db.get(dd)
                r.append(a)
            for line3 in r:
                line2 = ' '.join(line3[:5])
                lin = line3[4]
                s.append(float(lin))
                l.append(line2)
            total_price = sum(s)
            m = ' ₽\n\n➕ '.join(l)
            mark_up.update_key(chat_id, 'total_price', total_price)
        return total_price, m


    def check_basket(self, chat_id):
            with shelve.open('itog.py') as db:
                lst3 = list(db.keys())
                if list(filter(lambda y: str(chat_id) in y, lst3)) == []:
                    bot.send_message(chat_id, 'Ваша корзина пуста!', reply_markup=mark_up.inline_markup2())
                else:
                    total_price, m = mark_up.part_basket(chat_id)
                    bot.send_message(chat_id, 'Ваша корзина :\n\n'
                                              f'➕ {m} ₽.\n\n'
                                              f'Итого: {str(total_price)}  ₽.', reply_markup=mark_up.gen_markup2())


    def basket(self, chat_id, callback):
            with shelve.open('itog.py') as db:
                lst3 = list(db.keys())
                if list(filter(lambda y: str(chat_id) in y, lst3)) == []:
                    bot.send_message(chat_id, 'Ваша корзина пуста!', reply_markup=mark_up.inline_markup2())
                else:
                    total_price, m = mark_up.part_basket(chat_id)
                    if callback.inline_message_id == None:
                        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Ваша корзина :\n\n'
                                               f'➕ {m} ₽.\n\n'
                                               f'Итого: {str(total_price)}  ₽.',
                                          reply_markup=mark_up.gen_markup2())
                    else:
                        bot.edit_message_text(inline_message_id=callback.inline_message_id, text='Вы перешли в корзину!')
                        bot.send_message(chat_id,
                                     text='Ваша корзина :\n\n'
                                          f'➕ {m} ₽.\n\n'
                                          f'Итого: {str(total_price)} ₽.',
                                     reply_markup=mark_up.gen_markup2())


    def result_ship(self, chat_id):
        with shelve.open('itog.py') as db:
            l = []
            r = []
            t = []
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                a = db.get(dd)
                r.append(a)
            for line3 in r:
                line1 = ' '.join(line3[:5])
                line2 = ' '.join(line3[:7])
                l.append(line2)
                t.append(line1)
            m = '_______________________\n\n'.join(l)
            j = ' ₽\n\n➕ '.join(t)
            return m, j


    def forward_file(self, chat_id, number):
        try:
            with shelve.open('itog.py') as db:
                r = []
                lst3 = list(db.keys())
                lst = list((filter(lambda x: str(chat_id) in x, lst3)))  # фильтр на юзера
                for dd in lst:
                    a = db.get(dd)
                    r.append(a)
                for line3 in r:
                    file_id = line3[7]
                    file_name = line3[0]
                    type_print = line3[1]
                    link = (line3[5])[2:-2]
                    channel_id = -333336737368
                    if 'Канцелярия' in type_print:
                        pass
                    elif 'https://api.telegram.org/bot' is not link:
                            urllib2.urlretrieve(link, file_name)
                            files = {'document': open(file_name, 'rb')}
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={str(channel_id)}&caption={number}",
                                          files=files)
                            os.remove(file_name)
                    else:
                        bot.send_document(channel_id, str(file_id), caption=number)
        except Exception as e:
            bot.send_photo(channel_id, str(file_id), caption=number)

    def forward_file2(self, chat_id, number):
        try:
            with shelve.open('itog2.py') as db:
                r = []
                lst3 = list(db.keys())
                lst = list((filter(lambda x: str(chat_id) in x, lst3)))  # фильтр на юзера
                for dd in lst:
                    a = db.get(dd)
                    r.append(a)
                for line3 in r:
                    file_id = line3[2]
                    file_name = line3[0]
                    link = line3[1]
                    channel_id = -1001406737368
                    if 'https://api.telegram.org/bot' is not link:
                            urllib2.urlretrieve(link, file_name)
                            files = {'document': open(file_name, 'rb')}
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={str(channel_id)}",
                                          files=files)
                            os.remove(file_name)
                    else:
                        bot.send_document(channel_id, str(file_id), caption=number)
        except Exception as e:
            bot.send_photo(channel_id, str(file_id), caption=number)


    def gg_basket(self, callback):
        chat_id = callback.from_user.id
        file_name = mark_up.call_value(chat_id, 'file_name')
        type_print = mark_up.call_value(chat_id, 'type_print')
        num = mark_up.call_value(chat_id, 'num')
        num_page = mark_up.call_value(chat_id, 'num_page')
        price_print = mark_up.call_value(chat_id, 'price_print')
        print(num, num_page, price_print)
        link = mark_up.call_value(chat_id, 'link')
        apps = mark_up.call_value(chat_id, 'apps')
        file_id = mark_up.call_value(chat_id, 'file_id')
        with shelve.open('itog.py') as db:
            db[str(chat_id) + ':' + file_name] = [file_name, f' ({type_print}) ',
                                                       (str(num) + ' экз.'),
                                                       (str(num_page) + ' стр.'),
                                                       (str(num_page * num * price_print)),
                                                       ('\n\n' + str(link) + '\n\n'),
                                                       ('Комментарий: \n' + str(apps) + '\n\n'),
                                                        str(file_id)]
        mark_up.update_key(chat_id, 'apps', 'None')


    def new_basket(self, chat_id):
        file_name = mark_up.call_value(chat_id, 'file_name')
        link = mark_up.call_value(chat_id, 'link')
        file_id = mark_up.call_value(chat_id, 'file_id')
        with shelve.open('itog2.py') as db:
            db[str(chat_id) + ':' + file_name] =[file_name, link, file_id]


    def format_pos(self, chat_id):
        mark_up.new_basket(chat_id)
        all_files = mark_up.open_basket(chat_id)
        dbworker.set_state(str(chat_id), '1')
        bot.send_message(chat_id, text='Ваша корзина :\n\n'
                                               f'➕ {all_files}', reply_markup
                                          =mark_up.markup_print())


    def open_basket(self, chat_id):
        with shelve.open('itog2.py') as db:
            s = []
            r = []
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                a = db.get(dd)
                r.append(a)
            for line3 in r:
                files = line3[0]
                s.append(files)
            all_files = '\n\n➕ '.join(s)
        return all_files


    def open_basket2(self, chat_id):
        with shelve.open('itog2.py') as db:
            s = []
            r = []
            lst3 = list(db.keys())
            lst = list((filter(lambda x: str(chat_id) in x, lst3)))
            for dd in lst:
                a = db.get(dd)
                r.append(a)
            for line3 in r:
                files = '\n\n'.join(line3[:2])
                s.append(files)
            all_files = '\n\n+++++++++++++++++++++++\n\n'.join(s)
        return all_files


    def add_kancel(self, callback):
        chat_id = callback.from_user.id
        file_name = mark_up.call_value(chat_id, 'file_name')
        type_print = mark_up.call_value(chat_id, 'type_print')
        num = mark_up.call_value(chat_id, 'num')
        price_print = mark_up.call_value(chat_id, 'price_print')
        mark_up.update_key(chat_id, 'link', 'None')
        link = mark_up.call_value(chat_id, 'link')
        apps = mark_up.call_value(chat_id, 'apps')
        mark_up.update_key(chat_id, 'file_id', 'None')
        file_id = mark_up.call_value(chat_id, 'file_id')
        with shelve.open('itog.py') as db:
            db[str(chat_id) + ':' + file_name] = [file_name, f' ({type_print}) ', (str(num) + ' экз.'),
                                                       ' - ',
                                                       (str(num * price_print)),
                                                       ('\n\n' + str(link) + '\n\n'),
                                                       ('Комментарий: \n' + str(apps) + '\n\n'),
                                                           str(file_id)]


    def callduty(self, price_print, callback):
        chat_id = callback.from_user.id
        type_print = callback.data
        mark_up.update_key(chat_id, 'price_print', price_print)
        mark_up.update_key(chat_id, 'type_print', type_print)


    def inline_plus(self, callback, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def inline_plus_kanc(self, callback, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data='НазадВканц')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data='корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def plus(self, callback, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def plus_kanc(self, callback, num):
        markup = types.InlineKeyboardMarkup()
        a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
        a2 = types.InlineKeyboardButton(str(num), callback_data='jr')
        a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data='НазадВканц')
        a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data='корзина')
        a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
        a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
        markup.add(a1, a2, a3)
        markup.add(a4, a5)
        markup.add(a6)
        markup.add(a7)
        return markup


    def add_knopka(self, id, thumb_url, title, price):
        r1 = types.InlineQueryResultArticle(
            id=id,
            thumb_url=thumb_url,
            title=title,
            description=f'Цена {price} ₽',
            input_message_content=types.InputTextMessageContent(message_text=f"{title}\n\nЦена {price} ₽"
                                                                             f"[\xa0]({thumb_url})"
                                                                , parse_mode='Markdown'),
            reply_markup=mark_up.num_copy_markup3()
        )
        return r1


    def kanc_finish(self, atr):
        r = []
        n_keys = dict2[atr].keys()
        for key1 in n_keys:
            a = dict2[atr].get(key1)
            d = mark_up.add_knopka(
                a['id'], a['thumb_url'], a['title'], a['price']
            )
            r.append(d)
        return r


    def finish_payments(self, chat_id, number_ship):
        m, j = mark_up.result_ship(chat_id)
        from_chat_id = -1001477777777777
        now = datetime.now()
        hours = int(now.hour) + 7
        time_order = str(f"{now.year}-{now.month}-{now.day}  {str(hours)}:{now.minute}")
        type_pay = 'Перевод Яндекс.Деньги'
        name = mark_up.call_value(chat_id, 'info_user')
        total_price = mark_up.call_value(chat_id, 'total_price')
        bot.edit_message_text(chat_id=chat_id, message_id=mark_up.call_value(chat_id, 'message_id'),
                              text=f'Супер! Платёж на сумму {str(total_price)} ₽ получен!✅\nТеперь ваш заказ отправлен Копир-кот!✅\n'
                                   f'\nПозиции заказа:\n\n➕ {j} ₽\n\nЗабрать заказ можете в любое рабочее время по адресу: Проспект Мира 80а, Красноярск (ТЦ АВЕНЮ, 4 этаж)\n\n'
                                   f'Номер вашего заказа - {number_ship}', reply_markup=mark_up.forward())
        bot.send_message(from_chat_id, f'{m}'
                                       f'___________________________\n\n'
                                       f'Номер заказа - {number_ship}\n'
                                       f'Время заказа: {time_order}\n'
                                       f'Заказчик: {name}\n'
                                       f'Тип оплаты: {type_pay}\n\n'
                                       f'Итого: {str(total_price)} ₽.'
                         )
        mark_up.forward_file(chat_id, number_ship)
        mark_up.clear_basket(chat_id)


    def pechat(self, a, price_print, callback):
        chat_id = callback.from_user.id
        mark_up.callduty(price_print, callback)
        num = mark_up.call_value(chat_id, 'num')
        if num != 1:
            markup = mark_up.num_copy_markup2(callback, num)
        else:
            markup = mark_up.num_copy_markup1()
        if callback.inline_message_id == None:
            bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                  text=f'📌 {a} - {str(price_print)} руб/стр.\n\n'
                                       'Выберите кол-во копий:', reply_markup=markup)
        else:
            bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                  text=f'📌 {a} - {str(price_print)} руб/стр.\n\n'
                                       'Выберите кол-во копий:', reply_markup=markup)


    def forward(self):
        markup = types.InlineKeyboardMarkup(True)
        markup.add(types.InlineKeyboardButton("Поделиться ссылкой на бота", url='https://t.me/share/url?url=https%3A//t.me/copykotbot'))
        return markup


    def update_key(self, chat_id, key, value):
        with shelve.open('local_dif.py') as db:
            dictik = (db.get(str(chat_id)))
            dictik.update({str(key): value})
            db[str(chat_id)] = dictik


    def call_value(self, chat_id, key):
        with shelve.open('local_dif.py') as db:
            dictik = db.get(str(chat_id))
            value = dictik.get(key)
            return value


    def start_dif(self, chat_id):
        with shelve.open('local_dif.py') as db:
            db[str(chat_id)] = {'type_print': 'None', 'num': 'None', 'link': 'None', 'file_id': 'None',
                                'file_name': 'None', 'apps': 'None',
                                'num_page': 'None', 'total_price': 'None', 'price_print': 'None', 'info_user': 'None',
                                'message_id': 'None'}


    def len_sub(self):
        with shelve.open('local_dif.py') as db:
            lst3 = list(db.keys())
            return len(lst3)

mark_up = Markup('ok')


@bot.message_handler(commands=['start', 'reset'])
def handle_start(message):
    chat_id = str(message.from_user.id)
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup1.row('➕ Добавить файл', '🛒 Корзина')
    user_markup1.row('📌 Канцелярия', '📲 Обратная связь')
    name = message.from_user.first_name
    dbworker.set_state(chat_id, '1')
    mark_up.start_dif(chat_id)
    bot.send_message(message.chat.id,
                     f'Приветствую, {name}! Я Копир-кот!\n\nУ нас ты можешь сделать:\n🔹 Ч/Б копии/распечатка А4 - 2,5 руб/стр.'
                     f'\n🔹 А4 Ч/Б двусторонняя - 4 руб/стр.\n🔹 Скан - 2 руб/стр.\n🔹 Цветная распечатка А4 - 20 руб/стр.\n'
                     f'🔹 Печать фото 10х15 - 10 руб/фото.'
                     f'\n🔹 Печать на фотобумаге А4 (глянец, матовая) - 30 руб/стр.'
                     f'\n🔹 Купить канцелярию.\n\nЗаходи в ТЦ АВЕНЮ на 4 этаж!',
                     reply_markup=user_markup1)

@bot.message_handler(commands=['lensub'])
def hand_start(message):
    if message.chat.id == 333377652:
        lensub = mark_up.len_sub()
        bot.send_message(message.chat.id, str(lensub))
    else:
        pass


@bot.message_handler(func=lambda message: dbworker.get_current_state(str(message.chat.id)) == 'kanc')
def msg_apps(message):
    try:
        chat_id = message.from_user.id
        type_print = 'Канцелярия'
        mark_up.update_key(chat_id, 'type_print', type_print)
        for y in dict_price.keys():
            if y in message.text:
                mark_up.update_key(chat_id, 'file_name', y)
                mark_up.update_key(chat_id, 'price_print', dict_price.get(y))
            else:
                pass
        dbworker.set_state(str(chat_id), '1')
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: dbworker.get_current_state(str(message.chat.id)) == 'change')
def mseg_apps(message):
    try:
        chat_id = message.from_user.id
        with shelve.open('itog.py') as db:
            lst3 = list(db.keys())
            keys = list((filter(lambda x: str(message.from_user.id) in x, lst3)))
            for dd in keys:
                a = list(db.get(dd))
                if message.text in a[0]:
                    num = a[2]
                    link = a[5]
                    type_print = (a[1])[2:-2]
                    if a[3] == ' - ':
                        num_page = '1'
                    else:
                        num_page = (a[3])[:-4]
                    mark_up.update_key(chat_id, 'file_name', a[0])
                    mark_up.update_key(chat_id, 'price_print', (float(a[4]) / (float(num[:-4]) * float(num_page))))
                    mark_up.update_key(chat_id, 'link', link[2:-2])
                    mark_up.update_key(chat_id, 'type_print', type_print)
                    mark_up.update_key(chat_id, 'num', int(num[0]))
                else:
                    pass
        dbworker.set_state(str(chat_id), '1')
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: dbworker.get_current_state(str(message.chat.id)) == '2')
def msg_appes(message):
    try:
        chat_id = message.from_user.id
        mark_up.update_key(chat_id, 'apps', message.text)
        bot.reply_to(message, 'Добавлю это сообщение в примечание к файлу', reply_markup=mark_up.go_basket())
        dbworker.set_state(str(chat_id), '1')
    except Exception as e:
        print(e)




@bot.message_handler(content_types=['text', 'document', 'photo'])
def msg_hand(message):
    try:
        chat_id = message.from_user.id
        info_user = f'{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}'
        mark_up.update_key(chat_id, 'info_user', info_user)
        num = 1
        mark_up.update_key(chat_id, 'num', num)
        if message.text == '📌 Канцелярия':
            bot.send_message(chat_id, 'Добро пожаловать в канцелярию ..', reply_markup=mark_up.kancel())
            type_print = 'Канцелярия'
            mark_up.update_key(chat_id, 'type_print', type_print)
        if message.text == '📲 Обратная связь':
            bot.send_contact(chat_id, phone_number=333336886, first_name='Екатерина')
            bot.send_location(chat_id, 56.012386, 92.8707427)
            bot.send_message(chat_id, 'Адрес: Проспект Мира 80а, Красноярск (ТЦ АВЕНЮ, 4 этаж)\n'
                                      'Пн - Сб 10:00 - 19:00\nВс - выходной')
        if message.content_type == 'photo':
            file_id = (message.json).get('photo')[0].get('file_id')
            mark_up.update_key(chat_id, 'file_id', file_id)
            file_info = bot.get_file(file_id)
            link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
            mark_up.update_key(chat_id, 'link', link)
            file_name = file_id[:10] + '.png'
            mark_up.update_key(chat_id, 'file_name', file_name)
            if dbworker.get_current_state(str(chat_id)) == 'add_file':
                mark_up.format_pos(chat_id)
            else:
                bot.send_message(message.from_user.id, 'Вы добавили файл:\n\n'
                                                  f'💾 {file_name}\n\n'
                                                  'Внимание❗\nЕсли Вы хотите, чтобы файл(ы) были распечатаны при Вашем присутствии, то выберите'
                                                  ' услугу - "Распечатать при мне"\n\n'
                                                  'Выберите услугу:', reply_markup=mark_up.inline_markup())
        if message.content_type == 'document':
            file_id = message.document.file_id
            mark_up.update_key(chat_id, 'file_id', file_id)
            file_info = bot.get_file(file_id)
            link = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
            mark_up.update_key(chat_id, 'link', link)
            file_name = message.document.file_name
            mark_up.update_key(chat_id, 'file_name', file_name)
            if dbworker.get_current_state(str(chat_id)) == 'add_file':
                mark_up.format_pos(chat_id)
            elif file_name.endswith('.ppt') or file_name.endswith('.doc') or file_name.endswith('.xls'):
                bot.send_message(chat_id, text='Внимание❗\nФайлы формата - .doc,  .xls,  .ppt,\n'
                                                'печатаются при Вашем присутствии')
                mark_up.format_pos(chat_id)
            else:
                bot.send_message(message.chat.id, 'Вы добавили файл:\n\n'
                                                  f'💾 {file_name}\n\n'
                                                  'Внимание❗\nЕсли Вы хотите, чтобы файл(ы) были распечатаны при Вашем присутствии, то выберите'
                                                  ' услугу - "Распечатать при мне"\n\n'
                                                  'Выберите услугу:', reply_markup=mark_up.inline_markup())
        if 'http' in message.text:
            if 'no_preview' or 'psv4.userapi.com' in message.text:
                url = message.text
                result = urllib.request.urlopen(url)
                file_name = os.path.basename(urllib.parse.urlparse(result.url).path)
                mark_up.update_key(chat_id, 'file_name', file_name)
                mark_up.update_key(chat_id, 'link', url)
                if dbworker.get_current_state(str(chat_id)) == 'add_file':
                    mark_up.format_pos(chat_id)
                elif file_name.endswith('.ppt') or file_name.endswith('.doc') or file_name.endswith('.xls'):
                    bot.send_message(chat_id, text='Внимание❗\nФайлы формата - .doc,  .xls,  .ppt,\n'
                                                'печатаются при Вашем присутствии')
                    mark_up.format_pos(chat_id)
                else:
                    bot.send_message(message.chat.id, 'Вы добавили файл:\n\n'
                                                  f'💾 {file_name}\n\n'
                                                  'Внимание❗ Если Вы хотите, чтобы файл(ы) были распечатаны при Вашем присутствии, то выберите'
                                                  ' услугу - "Распечатать при мне"\n\n'
                                                  'Выберите услугу:', reply_markup=mark_up.inline_markup())
            else:
                bot.reply_to(message, '❗По этой ссылку я скачать файл не смогу - нужна ссылка на скачивание❗\n\n'
                                      'Пример формата ссылок из VK:\n\n'
                                      '📎 https://vk.com/doc81064057_483314359?hash=406d1e781b028f5265&dl=HAYTANRUGA2TO:'
                                      '1544379753:9642c332b34e71d369&api=1&no_preview=1\n\n'
                                      '📎 https://psv4.userapi.com/c848036/u81064057/docs/d16/3bc44478b397/Skhema_Kriolita.pdf'
                                      '?extra=P2VMpQXtPHssvjwo2YAeVlvWK86Ox-cjjWcM3yJDZlb1eMN-EpsOJ8gh3yFbFkHeisDyZXP'
                                      '-Yci9uxQqf2IpI6fcSUZAhw02RKOfVvGAbEEmCLsG4_PGgCChuAhqArcnrySY_2kgDI9Y32_XuD6Kjkg',
                             reply_markup=mark_up.inline_markup2())
        if message.text == '➕ Добавить файл':
            bot.send_message(chat_id,
                             text=
                             '❗Отправьте, пожалуйста, ссылку на файл, фотографию или сам файл, который нужно распечатать❗\n\n'
                             'Поддерживаю форматы:\n\n'
                             '✅pdf, docx, pptx, xlsx\n✅frw, cdw, dwg\n✅png, jpeg')
        if message.text == '🛒 Корзина':
            mark_up.check_basket(chat_id)
    except Exception as e:
        if e == 'HTTP Error 404: Not Found':
            bot.reply_to(message,
                         'Ой, ошибка❗\nНичего не нашел по этой ссылке, попробуйте скинуть ссылку на файл по-другому')
        bot.send_message(481077652, str(e))


@bot.inline_handler(func=lambda query: True)
def inline_query(query):
    try:
        chat_id = query.from_user.id
        dbworker.set_state(str(chat_id), 'kanc')
        if query.query == 'Ручки/Карандаши':
            r = mark_up.kanc_finish(atr='pens')
            bot.answer_inline_query(query.id, r, cache_time=0, is_personal=True)
        if query.query == 'Папки и Файлы':
            r = mark_up.kanc_finish(atr='files')
            bot.answer_inline_query(query.id, r, cache_time=0, is_personal=True)
        if query.query == 'Корректирующие средства':
            r = mark_up.kanc_finish(atr='corection')
            bot.answer_inline_query(query.id, r, cache_time=0, is_personal=True)
        if query.query == 'Изменить':
            with shelve.open('itog.py') as db:
                r = []
                lst3 = list(db.keys())
                keys = list((filter(lambda x: str(query.from_user.id) in x, lst3)))
                for dd in keys:
                    a = list(db.get(dd))
                    default = 'https://pp.userapi.com/c845218/v845218058/cd929/DMHxsJvNO6s.jpg'
                    num = a[2]
                    markup = types.InlineKeyboardMarkup()
                    a1 = types.InlineKeyboardButton("-", callback_data=u'-1')
                    a2 = types.InlineKeyboardButton(str(num[:-4]), callback_data='jr')
                    a3 = types.InlineKeyboardButton("+", callback_data=u'+1')
                    if a[1] == 'Канцелярия':
                        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'НазадВканц')
                    else:
                        a4 = types.InlineKeyboardButton("⬅ Назад", callback_data=u'назад1')
                    a5 = types.InlineKeyboardButton("🛒 Корзина", callback_data=u'корзина')
                    a6 = types.InlineKeyboardButton("📝 Примечания", callback_data=u'примечания')
                    a7 = types.InlineKeyboardButton("❌ Удалить позицию", callback_data=u'удалить позицию')
                    markup.add(a1, a2, a3)
                    markup.add(a4, a5)
                    markup.add(a6)
                    markup.add(a7)
                    input_content = types.InputTextMessageContent(message_text=f"{a[0]}\n\n")
                    r2 = types.InlineQueryResultArticle(id=a[0],
                                                        thumb_url=default, title=a[0],
                                                        description=f'{a[1]}\n{a[2]}\n{a[4]} ₽',
                                                        input_message_content=input_content, reply_markup=markup)
                    r.append(r2)
                dbworker.set_state(str(chat_id), 'change')
                bot.answer_inline_query(query.id, r, cache_time=0, is_personal=True)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: call == '+1' or '-1')
def callback_query_handler(callback):
    try:
        if callback:
            chat_id = callback.from_user.id
            num = mark_up.call_value(chat_id, 'num')
            if callback.data == 'При мне':
                mark_up.new_basket(chat_id)
                all_files = mark_up.open_basket(chat_id)
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Ваша корзина :\n\n'
                                               f'➕ {all_files}', reply_markup
                                          =mark_up.markup_print())
            if callback.data == 'удалить позицию':
                if callback.inline_message_id == None:
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Позиция удалена', reply_markup
                                          =mark_up.inline_markup2())
                else:
                    bot.edit_message_text(inline_message_id=callback.inline_message_id, text='Позиция удалена')
                file_name = mark_up.call_value(chat_id, 'file_name')
                with shelve.open('itog.py') as db:
                    del db[str(chat_id) + ':' + file_name]
                mark_up.check_basket(chat_id)
            if callback.data == '+1':
                num += 1
                mark_up.update_key(chat_id, 'num', num)
                if callback.inline_message_id == None:
                    markup = mark_up.plus(callback, num)
                    bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id,
                                                  reply_markup=markup)
                else:
                    if mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                        markup = mark_up.inline_plus_kanc(callback, num)
                    else:
                        markup = mark_up.inline_plus(callback, num)
                    bot.edit_message_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=markup)
            if callback.data == '-1':
                num -= 1
                if num < 1:
                    num = 1
                if callback.inline_message_id == None:
                    markup = mark_up.plus(callback, num)
                    bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id,
                                                  reply_markup=markup)
                else:
                    if mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                        markup = mark_up.inline_plus_kanc(callback, num)
                    else:
                        markup = mark_up.inline_plus(callback, num)
                    bot.edit_message_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=markup)
                mark_up.update_key(chat_id, 'num', num)
            if callback.data == 'назад1':
                file_name = mark_up.call_value(chat_id, 'file_name')
                if callback.inline_message_id == None:
                    if mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                        markup = mark_up.kancel()
                    else:
                        markup = mark_up.inline_markup()
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text=f'Выберите услугу:\n\n'
                                               f'💾 {file_name}',
                                          reply_markup=markup)
                else:
                    bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                          text=f'Выберите услугу:\n\n'
                                               f'💾 {file_name}',
                                          reply_markup=mark_up.inline_markup())
            if callback.data == 'НазадВканц':
                if callback.inline_message_id == None:
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text=f'Добро пожаловать в канцелярию ..',
                                          reply_markup=mark_up.kancel())
                else:
                    bot.send_message(chat_id,
                                     text=f'Добро пожаловать в канцелярию ..',
                                     reply_markup=mark_up.kancel())
            if callback.data == 'корзина':
                file_name = (mark_up.call_value(chat_id, 'file_name')).lower()
                url = mark_up.call_value(chat_id, 'link')
                if mark_up.call_value(chat_id, 'type_print') != 'Канцелярия':
                    urllib2.urlretrieve(url, file_name)
                    if file_name.endswith('.docx'):
                        document = Document(file_name)
                        document.save(f'{file_name}1.zip')
                        zf = zipfile.ZipFile(f'{file_name}1.zip')
                        f = zf.open('docProps/app.xml').read()
                        soup = BeautifulSoup(f, 'xml')
                        num_page = soup.find('Pages').next_element
                        mark_up.update_key(chat_id, 'num_page', int(num_page))
                        os.remove(f'{file_name}1.zip')
                    if file_name.endswith('.pdf'):
                        input1 = PdfFileReader(open(file_name, "rb"))
                        num_page = input1.getNumPages()
                        mark_up.update_key(chat_id, 'num_page', int(num_page))
                    format1 = ['.frw', '.cdw', '.png', 'jpeg', '.dwg', '.dwt' '.gif', '.txt', '.mp4', '.jpg']
                    for y in format1:
                        if y == file_name[-4:]:
                            num_page = 1
                            mark_up.update_key(chat_id, 'num_page', num_page)
                        else:
                            pass
                    if file_name.endswith('.doc'):
                        num_page = 0
                        mark_up.update_key(chat_id, 'num_page', num_page)
                    if file_name.endswith('.pptx'):
                        filename = os.path.abspath(file_name)
                        np = Presentation(filename)
                        num_page = len(np.slides)
                        mark_up.update_key(chat_id, 'num_page', int(num_page))
                    if file_name.endswith('.xlsx'):
                        xl = pd.ExcelFile(os.path.abspath(file_name))
                        num_page = len(xl.sheet_names)
                        mark_up.update_key(chat_id, 'num_page', int(num_page))
                    mark_up.gg_basket(callback)
                    os.remove('/home/deployproject/' + file_name)
                elif mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                    mark_up.add_kancel(callback)
                total_price, m = mark_up.part_basket(chat_id)
                if callback.inline_message_id == None:
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Ваша корзина :\n\n'
                                               f'➕ {m} ₽.\n\n'
                                               f'Итого: {str(total_price)}  ₽.',
                                          reply_markup=mark_up.gen_markup2())
                else:
                    bot.edit_message_text(inline_message_id=callback.inline_message_id, text='Вы перешли в корзину!')
                    bot.send_message(chat_id,
                                     text='Ваша корзина :\n\n'
                                          f'➕ {m} ₽.\n\n'
                                          f'Итого: {str(total_price)}  ₽.',
                                     reply_markup=mark_up.gen_markup2())
            if callback.data == 'примечания':
                file_name = mark_up.call_value(chat_id, 'file_name')
                if callback.inline_message_id == None:
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Идём дальше! Напишите примечания к данному файлу ..\n\n'
                                               f'➕ {file_name}', reply_markup=mark_up.back())
                else:
                    bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                          text='Идём дальше! Напишите примечания к данному файлу ..\n\n'
                                               f'➕ {file_name}', reply_markup=mark_up.back())
                dbworker.set_state(str(chat_id), '2')
            if callback.data == 'оформить':
                number_ship = f'{str(chat_id)}-{mark_up.random_pool()}'
                total_price = mark_up.call_value(chat_id, 'total_price')
                markup = mark_up.gen_markup1(chat_id, total_price, number_ship)
                mark_up.update_key(chat_id, 'message_id', callback.message.message_id)
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                      text='Внимание❗\nЕсли кол-во страниц, заявленных ботом в корзине, '
                                           'не совпадает с действительным кол-ом страниц в Вашем заказе, то рекомендуется выбрать "Оплата при получении"\n\n'
                                           '"Оплата в одно касание" возможна при сумме заказа не менее 65 ₽.\n'
                                           'Если сумма заказа меньше, то Вы можете воспользоваться "Оплата переводом Яндекс.Деньги"\n\n'
                                           'Выберите тип оплаты :', reply_markup=markup)
            if callback.data == 'очистить':
                mark_up.clear_basket(chat_id)
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                      text='Ваша корзина очищена!', reply_markup=mark_up.inline_markup2())
            if callback.data == 'добавить':
                num = 1
                mark_up.update_key(chat_id, 'num', num)
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                      text='❗Отправьте, пожалуйста, ссылку на файл или сам файл, который нужно распечатать❗\n\n'
                                           'Поддерживаю форматы:\n\n'
                                           '✅pdf, docx, pptx, xlsx\n✅frw, cdw, dwg\n✅png, jpeg')
            if callback.data == 'добавить2':
                dbworker.set_state(str(chat_id), 'add_file')
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                      text='❗Отправьте, пожалуйста, ссылку на файл или сам файл, который нужно распечатать❗\n\n')
            if callback.data == 'отправить':
                number = f'{str(chat_id)}-{mark_up.random_pool()}'
                j = mark_up.open_basket(chat_id)
                m = mark_up.open_basket2(chat_id)
                now = datetime.now()
                today = datetime.today().strftime('%H:%M')
                time_order = f"{now.year}-{now.month}-{now.day}  {today}"
                from_chat_id = -100140666666666666
                type_pay = 'Распечатать при мне'
                name = f'{callback.from_user.first_name} {callback.from_user.last_name} @{callback.from_user.username}'
                bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                      text=f'Супер!✅\nТеперь ваш заказ отправлен Копир-коту!'
                                           f'✅\n\nПозиции заказа:\n\n➕ {j} ₽\n\nЗабрать заказ можете в любое рабочее время по адресу: Проспект Мира 80а, Красноярск (ТЦ АВЕНЮ, 4 этаж)\n\n'
                                           f'Номер вашего заказа - {number}', reply_markup=mark_up.forward())
                bot.send_message(from_chat_id, f'{m}'
                                               f'_________________________________________\n\n'
                                               f'Номер заказа - {number}\n'
                                               f'Время заказа: {time_order}\n'
                                               f'Заказчик: {name}\n'
                                               f'Тип оплаты: {type_pay}\n\n'
                                 )
                mark_up.forward_file2(chat_id, number)
                mark_up.clear_basket2(chat_id)
            if callback.data == 'очистить2':
                mark_up.clear_basket2(chat_id)
                bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                      text='Ваша корзина очищена!', reply_markup=mark_up.inline_markup2())
            if callback.data == 'назад_корзина':
                mark_up.basket(chat_id, callback)
            if callback.data == 'назад':
                dbworker.set_state(str(chat_id), '1')
                if callback.inline_message_id == None:
                    if mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                        markup = mark_up.plus_kanc(callback, num)
                    else:
                        markup = mark_up.plus(callback, num)
                    bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                                          text='Хорошо, выберите кол-во копий:', reply_markup=markup)
                else:
                    if mark_up.call_value(chat_id, 'type_print') == 'Канцелярия':
                        markup = mark_up.inline_plus_kanc(callback, num)
                    else:
                        markup = mark_up.inline_plus(callback, num)
                    bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                          text='Хорошо, выберите кол-во копий:', reply_markup=markup)
            if callback.data == 'Ч/Б Печать(распечатка)':
                mark_up.pechat(a='Ч/Б копии/распечатка А4', price_print=2.5, callback=callback)
            if callback.data == 'Печать фото 10х15':
                mark_up.pechat(a='Печать фото 10х15', price_print=10.0, callback=callback)
            if callback.data == 'Цветная печать А4':
                mark_up.pechat(a='Цветная распечатка А4', price_print=20.0, callback=callback)
            if callback.data == 'А4 Ч/Б двусторонняя':
                price_print = 2.0
                mark_up.callduty(price_print, callback)
                num = mark_up.call_value(chat_id, 'num')
                if num != 1:
                    markup = mark_up.num_copy_markup2(callback, num)
                else:
                    markup = mark_up.num_copy_markup1()
                if callback.inline_message_id == None:
                    bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                          text='📌 А4 Ч/Б двусторонняя - 4 руб/стр.\n\n'
                                               'Выберите кол-во копий:', reply_markup=markup)
                else:
                    bot.edit_message_text(inline_message_id=callback.inline_message_id,
                                          text='📌 А4 Ч/Б двусторонняя - 4 руб/стр.\n\n'
                                               'Выберите кол-во копий:', reply_markup=markup)
            if callback.data == 'Печать на фотобумаге':
                mark_up.pechat(a='Печать на фотобумаге А4 (глянец, матовая)', price_print=30.0, callback=callback)
            if callback.data == "later":
                mark_up.call_result(chat_id, callback, type_pay='Оплата при получении')
            if callback.data == 'now':
                with shelve.open('itog.py') as db:
                    r = []
                    l = []
                    lst3 = list(db.keys())
                    lst = list((filter(lambda x: str(chat_id) in x, lst3)))
                    for dd in lst:
                        a = list(db.get(dd))
                        r.append(a)
                    for line3 in r:
                        line2 = ' '.join(line3[:5])
                        l.append(line2)
                    m = ' ₽\n✅ '.join(l)
                price = mark_up.call_value(chat_id, 'total_price')
                price1 = float(price) * 100
                #prices = [LabeledPrice(label=f'Стоимость заказа ', amount=int(price1))]
                number_ship = f'{str(chat_id)} - {str(mark_up.random_pool())}'
                mark_up.update_key(chat_id, 'number_ship', number_ship)
                title = f'№: {number_ship}'
                provider_data = json.dumps({"receipt":{
                                "items":[
                                        {
                                            "description": number_ship,
                                            "quantity": "1.00",
                                            "amount": {
                                            "value": str(price)+"0",
                                            "currency": "RUB"
                                                                },
                                            "vat_code": 1
                                                }]}}, ensure_ascii=False)
                if price1 > 6569.0:
                    mark_up.send_check(chat_id,
                                     provider_token='3955555552:LIVE:33333',
                                     start_parameter='true',
                                     title=title,
                                     description=f'✅ {m}  ₽',
                                     payload='test',
                                     currency='RUB',
                                     prices=json.dumps([{'label': 'Стоимость заказа ', 'amount': int(price1)}], ensure_ascii=False),
                                     provider_data=provider_data ,
                                     photo_url='https://pp.userapi.com/c845218/v845218058/cd929/DMHxsJvNO6s.jpg',
                                     photo_height=512,
                                     photo_width=512,
                                     photo_size=512
                                     )
                else:
                    bot.answer_callback_query(callback.id, "Сумма заказа должна быть не менее 65 ₽")
            bot.answer_callback_query(callback.id, " ")
    except KeyError as a:
        chat_id = callback.from_user.id
        if str(chat_id) in a:
            mark_up.check_basket(chat_id)
        else:
            bot.send_message(chat_id,
                         text='Отправьте, пожалуйста, ссылку на файл или сам файл, который нужно распечатать\n\n'
                              'Поддерживаю форматы:\n\n'
                              '✔pdf, docx, pptx, xlsx\n✔frw, cdw, dwg\n✔png, jpeg')
        bot.send_message(481077652, str(a))
    except Exception as e:
        chat_id = callback.from_user.id
        if e == 'expected string or bytes-like object' or chat_id:
            mark_up.check_basket(chat_id)
        bot.send_message(481077652, str(e))



@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Проблемы с картой"
                                                " повторите платеж позже.")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    try:
        chat_id = message.from_user.id
        mark_up.call_result2(chat_id, message, type_pay='Банк. перевод')
    except Exception as e:
        print(e)

@app.route('/{}'.format(TOKEN), methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

@app.route('/{}'.format('PAYMENTS'), methods=['POST'])
def Check_Payments():
    try:
        chat_id = int((request.form['label'])[:-5])
        number_ship = request.form['label']
        total_price1 = float(request.form['amount'])
        total_price2 = (float(mark_up.call_value(chat_id, 'total_price')) * 0.98)
        if total_price1 >= total_price2:
            mark_up.finish_payments(chat_id, number_ship)
        else:
            mark_up.finish_payments(chat_id, number_ship)
        return 'HTTP 200 OK', 200
    except Exception as e:
        return 'HTTP 200 OK', 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://deployproject.pythonanywhere.com/{}".format(TOKEN))
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
