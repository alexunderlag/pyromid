 # -*- coding: utf8 -*-fg_color
from tkinter import *
import customtkinter
import customtkinter as ctk
import threading
import tkinter as tk
import requests
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from PIL import Image
import sys, os
import time
from CTkTable import *
from datetime import datetime
from CustomTkinterTitlebar import Tk
from CTkToolTip import *
from tkcalendar import Calendar

SERVER_URL = "http://ideal-web.site:5000"
ACTIVE_BTN_COLOR = "#5E2129"  # Можете выбрать нужный вам цвет
DEFAULT_BTN_COLOR = "#DC143C"  # Цвет активной кнопки
HOVER_BTN_COLOR = "#FF2B2B" # Цвет выбранной мышкой кнопки
STANDR_BACK_COLOR = "#2b2b2b"
PLACEHOLDER_COLOR = "#888888"  # Цвет для окна ввода (placeholder_text_color)
NORMAL_TEXT_COLOR = "#000000"  # Цвет для окна ввода (text_color)
WHITE_BACK_COLOR = "#ffffff" # Белый цвет для фона фреймой
GRAY_TEXT_COLOR = "#344767"
def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Октаэдр - заработай миллион")
        self.geometry("1200x750")
        self.frame = Frame(self, root_instance=self)
        self.frame.pack(side=LEFT, fill=Y)
        self.data_updater = DataUpdater()
        self.menu_updater = MenuUpdater()
        self.people_updater = PeopleUpdate()
        self.current_user_balance = 0
        self.auth_user = 0  # Добавлено
        self.toptbar = Toptbar()
        self.toptbar.pack(side=TOP, fill=X)
        self.toptbar2 = Toptbar2(root_instance=self, menu_updater = self.menu_updater,)
        self.toptbar2.pack(side=TOP, fill=X)
        self.rightbar = Rightbar(root_instance=self)
        self.rightbar.pack(side=RIGHT, fill=Y)
        self._frame = None
        self.switch_frame(Main_frame,data_updater=self.data_updater,)

    def switch_frame(self, frame_class,  data_updater=None, people_updater=None):
        new_frame = frame_class(root_instance=self, data_updater=self.data_updater, people_updater = self.people_updater)  # замените None на data_updater
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="left", fill="both", expand=True,)


class DataUpdater:
    def __init__(self):
        self.piramid_data = None
        self.piramid_data2 = None
        thread = threading.Thread(target=self.update_piramid_data_background, daemon=True)
        thread.start()

    def update_piramid_data_background(self):
        while True:
            response = requests.get(f"{SERVER_URL}/get_piramid_data")
            if response.status_code == 200:
                data = response.json()
                self.piramid_data = data['piramid_data']
                self.piramid_data2 = data['piramid_data2']
            else:
                print("Ошибка при получении данных о пирамиде")
                self.piramid_data = None
                self.piramid_data2 = None
            time.sleep(1)  # обновляем каждые 60 секунд
    
    def get_piramid_data(self):
        return self.piramid_data
    
    def get_piramid_data2(self):
        return self.piramid_data2

class PeopleUpdate:
    def __init__(self):
        self.all_users = None
        thread = threading.Thread(target=self.people_updater, daemon=True)
        thread.start()

    def people_updater(self):
        while True:
            response = requests.get(f"{SERVER_URL}/get_all_users")
            if response.status_code == 200:
                data = response.json()
                self.all_users = data['Users']
            else:
                print("Ошибка при получении данных о пирамиде")
                self.all_users = None
            time.sleep(60)  # обновляем каждые 60 секунд
    
    def get_all_users(self):
        return self.all_users
    

class MenuUpdater:
    def __init__(self):
        self.max_user_id = None
        self.max_piramid_id = None
        self.tdays = None
        thread = threading.Thread(target=self.update_menu, daemon=True)
        thread.start()

    def update_menu(self):
        while True:
            response = requests.get(f"{SERVER_URL}/menu_sht")
            if response.status_code == 200:
                data = response.json()
                # Извлекаем и сохраняем значения max_user_id, max_piramid_id и tdays
                self.max_user_id = data.get("max_user_id", 0)
                self.max_piramid_id = data.get("max_piramid_id", 0)
                self.tdays = data.get("tdays", 0)
                # Обновляем тексты кнопок с полученными значениями
            else:
                self.max_user_id = None
                self.max_piramid_id = None
                self.tdays = None
                print("Ошибка при получении данных меню")
            time.sleep(10)
            
    def get_max_user_id(self):
        return self.max_user_id

    def get_max_piramid_id(self):
        return self.max_piramid_id
    
    def get_tdays(self):
        return self.tdays
    
class Frame(customtkinter.CTkFrame):
    def __init__(self, master, root_instance,**kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.home_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/home.png")), size=(25, 25))  
        self.about_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/about.png")), size=(25, 25))
        self.contacts_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/contacts.png")), size=(25, 25))
        self.loteray_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/loteray.png")), size=(25, 25))
        self.profile_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/profile.png")), size=(25, 25))
        self.pyrammid_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/pyrammid.png")), size=(25, 25))
        self.rules_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/rules.png")), size=(25, 25))
        self.configure(corner_radius=0, fg_color="#2b2b2b",border_width=0)
        self.left_menu = customtkinter.CTkFrame(self)
        self.left_menu.configure(corner_radius=0, fg_color="transparent",border_width=0)
        self.left_menu.pack(side=TOP, pady=(0,0))
        self.logotype = customtkinter.CTkLabel(self.left_menu, text="Октаэдр", text_color="#f3f3f3", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logotype.pack( padx=50, pady=(20,60))
        # Создаем список с информацией о кнопках
        self.buttons_info = [
            {"text": "Главная", "image" : self.home_image, "command": lambda: self.root_instance.switch_frame(Title_frame),},
            {"text": "Правила",  "image" : self.rules_image,"command": lambda: self.root_instance.switch_frame(MainRules)},
            {"text": "Профиль",  "image" : self.profile_image,"command": lambda: self.root_instance.switch_frame(Main_frame1)},
            {"text": "Пирамиды", "image" : self.pyrammid_image, "command": lambda: self.root_instance.switch_frame(Main_frame)},
            {"text": "Лотерея",  "image" : self.loteray_image,"command": "login"},
            {"text": "Контакты", "image" : self.contacts_image, "command": "login"},
            {"text": "О нас",  "image" : self.about_image,"command": "login"},
        ]
        for button_info in self.buttons_info:
            self.button = customtkinter.CTkButton(
                self.left_menu,
                text=button_info["text"],
                image=button_info["image"],
                command=button_info["command"],
                font=customtkinter.CTkFont(size=13, weight="bold"),
                corner_radius=4,
                text_color="#f3f3f3",
                fg_color="transparent",
                hover_color="#ffffff",
            )
            self.button.pack(anchor="w", padx=20, pady=(10, 15)) 

class Rightbar(customtkinter.CTkFrame):
    def __init__(self, root_instance, master=None, current_user_balance=0, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.pack(side=RIGHT)
        self.current_user_balance = current_user_balance  # Добавлено
        self.configure(corner_radius=0, fg_color="#2b2b2b",)
        self.auth_frame = customtkinter.CTkFrame(self)
        self.auth_frame.pack( padx=(0,20),pady=(5,5))
        self.auth_frame.configure(corner_radius=10, fg_color="#ffffff", border_width=1, border_color="#edeeef",)
        self.login_entry = customtkinter.CTkEntry(self.auth_frame,fg_color="#ffffff",placeholder_text_color=GRAY_TEXT_COLOR,border_color="#e9aede",border_width=1, placeholder_text="Логин")
        self.login_entry.pack(padx=10, pady=(10, 0))
        self.pass_entry = customtkinter.CTkEntry(self.auth_frame, fg_color="#ffffff",placeholder_text_color=GRAY_TEXT_COLOR,border_color="#e9aede",border_width=1, placeholder_text="Пароль", show="*")
        self.pass_entry.pack(padx=10, pady=(5, 5))
        self.login_btn = customtkinter.CTkButton(self.auth_frame, text='Войти', fg_color=DEFAULT_BTN_COLOR, hover_color=HOVER_BTN_COLOR, text_color="#ffffff",command=self.login)
        self.login_btn.pack(padx=10, pady=(5, 0))
        self.register_btn =  customtkinter.CTkButton(self.auth_frame, text='Регистрация', fg_color=DEFAULT_BTN_COLOR, hover_color=HOVER_BTN_COLOR, command=lambda: self.root_instance.switch_frame(Registration_Frame))
        self.register_btn.pack(padx=10, pady=(10, 10))
        self.second_frame = customtkinter.CTkFrame(self)
        self.second_frame.configure(corner_radius=10,fg_color="#ffffff",border_width=1, border_color="#edeeef", )
        self.balance_label = create_label(self.second_frame, f"Баланс: {current_user_balance}р.", 7, 0)  # Добавлено
        self.logo_label2 = create_label(self.second_frame, "Профиль", 0, 0, sticky="s", padx=10, pady=(10, 0))
        self.logo_Text1 = create_label(self.second_frame, '', 1, 0,sticky="s", pady=(0,0))
        self.logo_Text = create_label(self.second_frame, '', 2, 0,pady=(0, 0))
        self.logo_Text3 = create_label(self.second_frame, '', 3, 0)
        self.logo_Text4 = create_label(self.second_frame, '', 4, 0)
        self.profil_email = create_label(self.second_frame, '', 6, 0, padx=10,)
        self.cal_btn5 = create_button(self.second_frame, 'Пополнить баланс',  self.open_balance_window, 8, 0, padx=20, pady=(10, 5))
        self.btn_exit = create_button(self.second_frame, 'Выйти', self.logout, 9, 0, padx=20, pady=(10, 5))

    def login(self):
        login = self.login_entry.get()
        password = self.pass_entry.get()
        
        response = requests.post(f"{SERVER_URL}/login", json={"login": login, "password": password})
        data = response.json()
        
        if response.status_code == 400:
            CTkMessagebox(title="Ошибка", message=data['message'], icon="cancel")
        else:
            self.is_logged_in = True
            user_info = data['user']
            balance = user_info["balance"]
            nikname = user_info["login"]
            lname = user_info["lname"]
            fname = user_info["fname"]
            city = user_info["city"]
            mobile = user_info["mobile"]
            email = user_info["email"]
            self.update_profile(nikname, fname, lname, city, mobile, email, balance)
            self.auth_frame.pack_forget()
            self.second_frame.pack(ipadx=5,ipady=10,padx=20,pady=5,)
            self.logged_in_username = login
            self.root_instance.auth_user = 1
            if self.root_instance._frame is not None:
                self.root_instance._frame.destroy()
            self.root_instance.switch_frame(Main_frame)
            CTkMessagebox(title="Успешно", message="Успешная авторизация")
    def update_frame(self, new_balance):
        print(f"Updating balance to {new_balance}р.")
        self.balance_label.configure(text=f"Баланс: {new_balance}р.")

    # def open_registration_window(self):
    #     registration_window = Registration(master=self)
    #     registration_window.grab_set()

    def logout(self):
        self.logged_in_username = None
        self.is_logged_in = False
        self.user_info = None
        self.second_frame.pack_forget()
        self.auth_frame.pack(padx=(0,20),pady=(5,5))
        self.root_instance.auth_user = 0
        if self.root_instance._frame is not None:
            self.root_instance._frame.destroy()
        self.root_instance.switch_frame(Main_frame)

    def open_balance_window(self):
        logged_in_login = self.logged_in_username
        self.balance_window = Balanceup(logged_in_login, self)

    def update_profile(self, nikname, fname, lname, city, mobile, email, balance):
        self.logo_label2.configure(text_color=GRAY_TEXT_COLOR,)
        self.logo_Text.configure(text=f"Никнейм: {nikname}",text_color=GRAY_TEXT_COLOR,)
        self.logo_Text1.configure(text=f"{fname} {lname}",text_color=GRAY_TEXT_COLOR,)
        self.logo_Text3.configure(text=f"Город: {city }",text_color=GRAY_TEXT_COLOR,)
        self.logo_Text4.configure(text=f"Номер: {mobile}",text_color=GRAY_TEXT_COLOR,)
        self.profil_email.configure(text=f"Email: {email}",text_color=GRAY_TEXT_COLOR,)      
        self.balance_label.configure(text=f"Баланс: {balance}р.",text_color=GRAY_TEXT_COLOR,)

class Toptbar(customtkinter.CTkFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(corner_radius=0, fg_color="#2b2b2b")
        self.not_register = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.not_register.pack(side=TOP, anchor="ne",padx=20)

        self.message = customtkinter.CTkLabel(self, text = 'Добро пожаловать в закрытую бета версию')
        self.message.configure (fg_color= 'transparent', text_color="#f3f3f3" ,font=customtkinter.CTkFont(size=10))
        self.message.x_limit = 1024
        self.message.move = 1
        self.message.delay = 30
        self.message.place(x=155)
        self.message.after(15, self.move)
        self.update_menu()

    def update_menu(self):
        response = requests.get(f"{SERVER_URL}/advertup")
        if response.status_code == 200:
            data = response.json()
            newstoday = data.get("newstoday", 0)
            self.update_newstoday_button(newstoday)
        else:
            print("Ошибка при получении данных о пирамиде")

    def update_newstoday_button(self, newstoday):
        self.message.configure(text=f'{newstoday}')

    def move(self):   
        if self.message.winfo_x() + self.message.move >= self.message.x_limit or self.message.winfo_x() + self.message.move < 0:
            self.message.move = -self.message.move
        self.message.place(x=self.message.winfo_x() + self.message.move)
        self.message.after(self.message.delay, self.move)

class Toptbar2(customtkinter.CTkFrame):
    def __init__(self,root_instance, menu_updater, master=None, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.menu_updater = menu_updater  
        self.memb_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/member.png")), size=(50, 50))
        self.money_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/money.png")), size=(50, 50))
        self.pyramid_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/pyramid.png")), size=(50, 50))
        self.time_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/time.png")), size=(50, 50))
        self.configure(corner_radius=0, fg_color="#2b2b2b",)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        self.folowerrs_btn = customtkinter.CTkButton(self, text='', anchor="w", compound="right", command=lambda: self.root_instance.switch_frame(People_frame), font=customtkinter.CTkFont(size=12), corner_radius=10, text_color=GRAY_TEXT_COLOR, fg_color="#ffffff", border_width=1, border_color="#edeeef", hover_color="#ffffff")        
        self.folowerrs_btn.grid(row=0, column=0, sticky="ew", padx=(25,20), pady=(20, 20))
        self.folowerrs_btn.configure(corner_radius=10,border_width=1, border_color="#edeeef", fg_color="#ffffff")
        self.follower_text= customtkinter.CTkLabel(self.folowerrs_btn, text='Нас уже:',text_color=GRAY_TEXT_COLOR, fg_color="transparent",font=customtkinter.CTkFont(size=11,),anchor=S)
        self.follower_text.grid(sticky=SW,row=0, column=0,padx=10, pady=3)
        self.follower_text2 = customtkinter.CTkLabel(self.folowerrs_btn, text='',text_color=GRAY_TEXT_COLOR,fg_color="transparent", font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.follower_text2.grid(sticky=NW,row=1, column=0, padx=10,columnspan=2,pady=3)
        self.follloer_image = customtkinter.CTkLabel(self.folowerrs_btn, text='',text_color=GRAY_TEXT_COLOR,image=self.memb_image, font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.follloer_image.grid(sticky=E,row=0, column=3, padx=(30,0),rowspan=2)
        self.follower_text.bind("<Button-1>", lambda  event=None: self.root_instance.switch_frame(People_frame))
        self.follower_text2.bind("<Button-1>", lambda event=None: self.root_instance.switch_frame(People_frame))
        self.follloer_image.bind("<Button-1>", lambda event=None: self.root_instance.switch_frame(People_frame))
        self.tooltip_user = CTkToolTip(self.folowerrs_btn, delay=0.5, message="Показать всех пользователей", corner_radius=5)
        self.tooltip_user1 = CTkToolTip(self.follower_text, delay=0.5, message="Показать всех пользователей")
        self.tooltip_user2 = CTkToolTip(self.follower_text2, delay=0.5, message="Показать всех пользователей")
        self.tooltip_user3 = CTkToolTip(self.follloer_image, delay=0.5, message="Показать всех пользователей")
        self.money_btn = customtkinter.CTkButton(self, text='', anchor="w", compound="right", command="self.some_command", font=customtkinter.CTkFont(size=12), corner_radius=10, text_color=GRAY_TEXT_COLOR, fg_color="#ffffff", border_width=1, border_color="#edeeef", hover_color="#ffffff")
        self.money_btn.configure(corner_radius=10,border_width=1, border_color="#edeeef", fg_color="#ffffff")
        self.money_btn.grid(row=0, column=1, sticky="ew", padx=0, pady=(20, 20))
        self.money_text= customtkinter.CTkLabel(self.money_btn, text='Сняли денег:',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=11,),anchor=S)
        self.money_text.grid(sticky=SW,row=0, column=0,padx=10,pady=3)
        self.money_text2 = customtkinter.CTkLabel(self.money_btn, text='0 рублей',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.money_text2.grid(sticky=NW,row=1, column=0, padx=10,columnspan=2,pady=3)
        self.money_image = customtkinter.CTkLabel(self.money_btn, text='',text_color=GRAY_TEXT_COLOR,image=self.money_image, font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.money_image.grid(sticky=E,row=0, column=3, padx=(30,0),rowspan=2)

        self.witdraw = customtkinter.CTkButton(self, text='', anchor="w", compound="right", command=lambda: self.root_instance.switch_frame(Main_frame), font=customtkinter.CTkFont(size=12), corner_radius=10, text_color=GRAY_TEXT_COLOR, fg_color="#ffffff", border_width=1, border_color="#edeeef", hover_color="#ffffff")
        self.witdraw.configure(corner_radius=10,border_width=1, border_color="#edeeef", fg_color="#ffffff")
        self.witdraw.grid(row=0, column=2, sticky="ew", padx=(20,0), pady=(20, 20))
        self.witdraw_text= customtkinter.CTkLabel(self.witdraw, text='Для игры доступны:',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=11,),anchor=S)
        self.witdraw_text.grid(sticky=SW,row=0, column=0,padx=10,pady=3)
        self.witdraw_text2 = customtkinter.CTkLabel(self.witdraw, text='0 рублей',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.witdraw_text2.grid(sticky=NW,row=1, column=0, padx=10,columnspan=2,pady=3)
        self.witdraw_image = customtkinter.CTkLabel(self.witdraw, text='',text_color=GRAY_TEXT_COLOR,image=self.pyramid_image,font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.witdraw_image.grid(sticky=E,row=0, column=3, padx=(30,0),rowspan=2)
        self.witdraw_text.bind("<Button-1>", lambda  event=None: self.root_instance.switch_frame(Main_frame))
        self.witdraw_text2.bind("<Button-1>", lambda event=None: self.root_instance.switch_frame(Main_frame))
        self.witdraw_image.bind("<Button-1>", lambda event=None: self.root_instance.switch_frame(Main_frame))

        self.days = customtkinter.CTkButton(self, text='', anchor="w", compound="right", command="self.yet_another_command", font=customtkinter.CTkFont(size=12), corner_radius=10, text_color=GRAY_TEXT_COLOR, fg_color="#ffffff", border_width=1, border_color="#edeeef", hover_color="#ffffff")
        self.days.configure(corner_radius=10,border_width=1, border_color="#edeeef", fg_color="#ffffff")
        self.days.grid(row=0, column=3, sticky="ew", padx=20, pady=(20, 20))
        self.days_text= customtkinter.CTkLabel(self.days, text='Мы уже работаем:',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=11,),anchor=S)
        self.days_text.grid(sticky=SW,row=0, column=0,padx=10,pady=3)
        self.days_text2 = customtkinter.CTkLabel(self.days, text='',text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.days_text2.grid(sticky=NW,row=1, column=0, padx=10,columnspan=2,pady=3)
        self.days_image = customtkinter.CTkLabel(self.days, text='',text_color=GRAY_TEXT_COLOR,image=self.time_image,font=customtkinter.CTkFont(size=12,weight="bold"),anchor=N)
        self.days_image.grid(sticky=E,row=0, column=3, padx=(30,0),rowspan=2)
        self.init_ui()

    def init_ui(self):
        self.follower_text2.configure(text=f"{self.menu_updater.get_max_user_id()} участников")
        self.witdraw_text2.configure(text=f"{self.menu_updater.get_max_piramid_id()} пирамиды")
        self.days_text2.configure(text=f"{self.menu_updater.get_tdays()} дней")

class Main_frame(customtkinter.CTkFrame):
    def __init__(self, root_instance, data_updater, people_updater, master=None, **kw):
        super().__init__(master, **kw)
        self.data_updater = data_updater
        self.people_updater = people_updater
        self.root_instance = root_instance
        self.pyramid_selection_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.pyramid_selection_frame.pack(fill="x", padx=25, pady=(20, 10))
        self.popular_pyramids_btn = customtkinter.CTkButton(self.pyramid_selection_frame, text="Самые популярные", command=self.display_popular_pyramids)
        self.popular_pyramids_btn.pack(side="left", padx=5)

        self.fast_pyramids_btn = customtkinter.CTkButton(self.pyramid_selection_frame, text="Быстрые", command=self.display_fast_pyramids)
        self.fast_pyramids_btn.pack(side="left", padx=5)

        self.normal_pyramids_btn = customtkinter.CTkButton(self.pyramid_selection_frame, text="Обычные", command=self.display_normal_pyramids)
        self.normal_pyramids_btn.pack(side="left", padx=5)

        self.long_pyramids_btn = customtkinter.CTkButton(self.pyramid_selection_frame, text="Долгие", command=self.display_long_pyramids)
        self.long_pyramids_btn.pack(side="left", padx=5)
        self.button_state_p1 = tk.NORMAL if self.root_instance.auth_user == 1 else tk.DISABLED
        self.button_state_p2 = DEFAULT_BTN_COLOR if self.root_instance.auth_user == 1 else ACTIVE_BTN_COLOR
        self.create_ui()
        self.update_ui()
    def display_popular_pyramids(self):
        # Logic to display popular pyramids
        pass

    def display_fast_pyramids(self):
        # Logic to display fast pyramids
        pass

    def display_normal_pyramids(self):
        # Logic to display normal pyramids
        pass

    def display_long_pyramids(self):
        # Logic to display long pyramids
        pass
    def create_ui(self):
        self.pyramid_one = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        self.pyramid_one.pack(side="top", anchor="nw", padx=25, pady=(20, 10))
        self.logo_Textp1 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_Textp1.grid(row=0, column=1, padx=0, pady=(10, 5))
        self.logo_Textp2 = customtkinter.CTkLabel(self.pyramid_one, text="", text_color=GRAY_TEXT_COLOR,font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp2.grid(row=1, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp3 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp3.grid(row=2, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.logo_Textp4 = customtkinter.CTkLabel(self.pyramid_one, text="", text_color=GRAY_TEXT_COLOR,font=customtkinter.CTkFont(size=12, weight="bold"))
        # self.logo_Textp4.grid(row=3, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp5 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp5.grid(row=4, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.logo_Textp6 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        # self.logo_Textp6.grid(row=5, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp7 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp7.grid(row=6, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.ost_time = customtkinter.CTkLabel(self.pyramid_one, text="", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.ost_time.grid(row=7, column=1, padx=0, pady=(10, 5))
        self.progressbar = customtkinter.CTkProgressBar(self.pyramid_one, orientation="horizontal",height=20,determinate_speed=0.013,width=300)
        self.progressbar.grid(row=8, column=1, padx=15, pady=(15, 5),sticky="ew",)
        self.progressbar.start()
        self.button_p1 = customtkinter.CTkButton(self.pyramid_one, text="Депозит", command=lambda: self.root_instance.switch_frame(Deposit_Frame), state=self.button_state_p1, fg_color=self.button_state_p2, hover_color=HOVER_BTN_COLOR)
        self.button_p1.grid(row=9, column=1,sticky="e",pady=(10,15),padx=15)

        self.pyramid_two = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        self.pyramid_two.pack(side="top", anchor="nw", padx=25, pady=(20, 10))
        self.logo_Textp11 = customtkinter.CTkLabel(self.pyramid_two, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_Textp11.grid(row=0, column=1, padx=0, pady=(10, 5))
        self.logo_Textp22 = customtkinter.CTkLabel(self.pyramid_two, text="", text_color=GRAY_TEXT_COLOR,font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp22.grid(row=1, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp33 = customtkinter.CTkLabel(self.pyramid_two, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp33.grid(row=2, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.logo_Textp4 = customtkinter.CTkLabel(self.pyramid_one, text="", text_color=GRAY_TEXT_COLOR,font=customtkinter.CTkFont(size=12, weight="bold"))
        # self.logo_Textp4.grid(row=3, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp55 = customtkinter.CTkLabel(self.pyramid_two, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp55.grid(row=4, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.logo_Textp6 = customtkinter.CTkLabel(self.pyramid_one, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        # self.logo_Textp6.grid(row=5, column=1, padx=30, pady=(0, 0),sticky="w")
        self.logo_Textp77 = customtkinter.CTkLabel(self.pyramid_two, text="",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_Textp77.grid(row=6, column=1, padx=30, pady=(0, 0),sticky="w")
        # self.ost_time = customtkinter.CTkLabel(self.pyramid_one, text="", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.ost_time.grid(row=7, column=1, padx=0, pady=(10, 5))
        self.progressbar2 = customtkinter.CTkProgressBar(self.pyramid_two, orientation="horizontal",height=20,width=300)
        self.progressbar2.grid(row=8, column=1, padx=15, pady=(15, 5),sticky="ew",)
        self.button_p2 = customtkinter.CTkButton(self.pyramid_two, text="Депозит", command='Deposit', state=self.button_state_p1, fg_color=self.button_state_p2, hover_color=HOVER_BTN_COLOR)
        self.button_p2.grid(row=9, column=1,sticky="e",pady=(10,15),padx=15)

    def update_ui(self):
        # Обновление данных для pyramid_one
        self.piramid_data = self.data_updater.get_piramid_data()
        self.progress_value = self.piramid_data['progress']
        self.minstavka =  self.piramid_data['minstavka']
        self.logo_Textp1.configure(text=f"{self.piramid_data['name']}")
        self.logo_Textp2.configure(text=f"Баланс: {self.piramid_data['balance']}")
        self.logo_Textp3.configure(text=f"Участников: {self.piramid_data['participants']} (Последний: {self.piramid_data['lastuser']})")
        # self.logo_Textp4.configure(text=f"Последний: {self.piramid_data['lastuser']}")
        self.logo_Textp5.configure(text=f"Минимальный шаг: {self.piramid_data['minshag']} + {self.piramid_data['balance']} ({self.minstavka})")
        # self.logo_Textp6.configure(text=f"Дата начала: {self.piramid_data['start_date']}")
        self.logo_Textp7.configure(text=f"Осталось:{round(self.piramid_data['seconds_left'])} секунд.",text_color=GRAY_TEXT_COLOR)
        # self.logo_Textp7.configure(text=f"Осталось:{round(self.data_updater.seconds_left)} секунд. ({self.piramid_data['end_date']})",text_color=GRAY_TEXT_COLOR)

        self.progressbar.set(self.progress_value)

        self.piramid_data2 = self.data_updater.get_piramid_data2()
        self.progress_value2 = self.piramid_data2['progress']
        self.minstavka2 =  self.piramid_data2['minstavka']
        self.logo_Textp11.configure(text=f"{self.piramid_data2['name']}")
        self.logo_Textp22.configure(text=f"Баланс: {self.piramid_data2['balance']}")
        self.logo_Textp33.configure(text=f"Участников: {self.piramid_data2['participants']} (Последний: {self.piramid_data2['lastuser']})")
        # self.logo_Textp44.configure(text=f"Последний: {self.piramid_data2['lastuser']}")
        self.logo_Textp55.configure(text=f"Минимальный шаг: {self.piramid_data2['minshag']} + {self.piramid_data2['balance']} ({self.minstavka2})")
        # self.logo_Textp66.configure(text=f"Дата начала: {self.piramid_data2['start_date']}")
        self.logo_Textp77.configure(text=f"Осталось:{round(self.piramid_data2['seconds_left'])} секунд.",text_color=GRAY_TEXT_COLOR)
        self.progressbar2.set(self.progress_value2)

        # self.ost_time.configure(text=f"Осталось:{round(self.data_updater.seconds_left)} секунд")
        # Планируем следующее обновление
        self.after(1000, self.update_ui)

class Title_frame(customtkinter.CTkFrame):
    def __init__(self, root_instance, data_updater,people_updater=None, master=None, **kw):
        super().__init__(master, **kw)
        self.data_updater = data_updater 
        self.people_updater = people_updater
        self.root_instance = root_instance
        self.configure(corner_radius=0, fg_color=STANDR_BACK_COLOR,)
        self.textbox = customtkinter.CTkTextbox(master=self, width=90,fg_color=STANDR_BACK_COLOR, font=customtkinter.CTkFont(size=20, weight="bold",) )
        self.textbox.pack(fill="both", expand=True, padx=15,pady=(0,20))
        self.textbox.insert("0.0", "Добро пожаловать, это бета тест)))" * 50)
    
class People_frame(ctk.CTkFrame):
    def __init__(self,root_instance, data_updater, people_updater, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(corner_radius=0, fg_color="#2b2b2b",)
        self.pack(fill="both", expand=True, )
        
        self.usersframe = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.usersframe.pack(fill="x")
        
        self.scrollframe = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color="#ffffff")
        self.scrollframe.pack(fill="both", expand=True, padx=25, pady=(20, 10))
        self.root_instance = root_instance
        self.people_updater = people_updater
        self.data_updater = data_updater

        self.init_ui()

    def convert_users_to_table_data(self, users):
        table_data = [["Имя", "Фамилия", "Баланс", "Дата регистрации", "Профиль"]]  # Replace "Email" with "Дата регистрации"
        
        for user in users:
            action_btn = self.create_action_button(user)
            row = [user['fname'], user['lname'], user['balance'], user['date_register'], action_btn]  # Use 'date_register' instead of 'email'
            table_data.append(row)
        
        return table_data

    def create_action_button(self, user):
        return "Посмотреть"
    
    def init_ui(self):
        # Добавляем кнопки для фильтрации пользователей
        self.all_users_btn = ctk.CTkButton(self.usersframe, text="Все пользователи", command=self.display_all_users)
        self.all_users_btn.grid(row=0, column=0, sticky="ew", padx=(25,5))

        self.top_100_btn = ctk.CTkButton(self.usersframe, text="Топ 100", command=self.display_top_100)
        self.top_100_btn.grid(row=0, column=1, sticky="ew", padx=5)

        self.top_10_btn = ctk.CTkButton(self.usersframe, text="Топ 10", command=self.display_top_10)
        self.top_10_btn.grid(row=0, column=2, sticky="ew", padx=5)

        self.new_users_btn = ctk.CTkButton(self.usersframe, text="Новые пользователи", command=self.display_new_users)
        self.new_users_btn.grid(row=0, column=3, sticky="ew", padx=(5,25))
        self.usersframe.grid_columnconfigure(0, weight=1)
        self.usersframe.grid_columnconfigure(1, weight=1)
        self.usersframe.grid_columnconfigure(2, weight=1)
        self.usersframe.grid_columnconfigure(3, weight=1)
        self.display_all_users()

    def reset_button_colors(self):
        """Сбрасывает цвета всех кнопок к исходному состоянию."""
        self.all_users_btn.configure(fg_color=ACTIVE_BTN_COLOR, hover_color=HOVER_BTN_COLOR)
        self.top_100_btn.configure(fg_color=ACTIVE_BTN_COLOR, hover_color=HOVER_BTN_COLOR)
        self.top_10_btn.configure(fg_color=ACTIVE_BTN_COLOR, hover_color=HOVER_BTN_COLOR)
        self.new_users_btn.configure(fg_color=ACTIVE_BTN_COLOR, hover_color=HOVER_BTN_COLOR)

    def display_all_users(self):
        self.reset_button_colors()
        self.all_users_btn.configure(fg_color=DEFAULT_BTN_COLOR)
        users = self.people_updater.get_all_users()
        
        # Сортировка пользователей по балансу в порядке убывания
        users.sort(key=lambda x: x['balance'], reverse=True)
        
        self.update_table_data(users)

    def display_top_100(self):
        self.reset_button_colors()
        self.top_100_btn.configure(fg_color=DEFAULT_BTN_COLOR)
        users = self.people_updater.get_all_users()
        users.sort(key=lambda x: x['balance'], reverse=True)
        self.update_table_data(users[:100])

    def display_top_10(self):
        self.reset_button_colors()
        self.top_10_btn.configure(fg_color=DEFAULT_BTN_COLOR)
        users = self.people_updater.get_all_users()
        users.sort(key=lambda x: x['balance'], reverse=True)
        self.update_table_data(users[:10])

    def display_new_users(self):
        self.reset_button_colors()
        self.new_users_btn.configure(fg_color=DEFAULT_BTN_COLOR)
        
        users = self.people_updater.get_all_users()
        
        # Сортировка пользователей по дате регистрации в порядке убывания
        users.sort(key=lambda x: datetime.strptime(x['date_register'], '%Y-%m-%d'), reverse=True)
        
        # Обновляем таблицу данными о новых пользователях
        self.update_table_data(users)

    def update_table_data(self, users):
        table_data = self.convert_users_to_table_data(users)
        rows = len(table_data)
        columns = len(table_data[0])

        # Удалите старую таблицу, если она существует
        for widget in self.scrollframe.winfo_children():
            widget.destroy()

        # Создаем новую таблицу
        self.table = CTkTable(self.scrollframe, row=rows, column=columns, values=table_data,command=self.cell_clicked)
        self.table.pack(expand=True, fill="both", padx=5, pady=5)
    def open_user_profile(self, login):
        # Отправка POST-запроса на сервер и получение данных пользователя
        data = {"lname": login}
        response = requests.post(f"{SERVER_URL}/get_user_info", json=data)
        print(data)
        if response.status_code == 200:
            user_data = response.json()
            self.root_instance.switch_frame(UserProfile, user_data=user_data)  # Переключение на экран UserProfile и передача данных
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить информацию о пользователе")

    def cell_clicked(self, cell):
        # проверьте, является ли столбец ячейки столбцом "Посмотреть"
        if cell["column"] == 4:  # если "Посмотреть" это пятая колонка
            user_login = self.table.get(cell["row"], 0)  # предположим, что login хранится в первой колонке
            self.open_user_profile(user_login)
class Deposit_Frame(ctk.CTkFrame):
    def __init__(self, root_instance, data_updater, people_updater, master=None, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.configure(corner_radius=0, fg_color="#2b2b2b",)
        self.pack(fill="both", expand=True)
        self.label = customtkinter.CTkLabel(self, text="Введите данные")
        self.label.grid(row=0, column=1,pady=(10, 10), columnspan=2)

class Registration_Frame(ctk.CTkFrame):
    def __init__(self, root_instance, data_updater, people_updater, master=None, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.ava_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/ava.png")), size=(35, 35))  
        self.pass_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/pass.png")), size=(35, 35))  
        self.email_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/email.png")), size=(35, 35))  
        self.fname_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/fname.png")), size=(35, 35))  
        self.city_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/city.png")), size=(35, 35))  
        self.mobile_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/mobile.png")), size=(35, 35)) 
        self.birthday_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/birthday.png")), size=(35, 35))  
        self.promocode_image = customtkinter.CTkImage(light_image=Image.open(resource("./icons/promocode.png")), size=(35, 35))  
        self.configure(corner_radius=0, fg_color="#2b2b2b",)
        self.pack(fill="both", expand=True)
        self.frame_reg = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.frame_reg.pack(fill="both", expand=True, padx=25, pady=(5, 15))
        self.label = customtkinter.CTkLabel(self.frame_reg, text="Введите данные",text_color=GRAY_TEXT_COLOR)
        self.label.grid(row=0, column=0,pady=(10, 10), columnspan=3)
        

        self.login_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.login_frame.grid(row=1, column=1, pady=(10, 0))
        self.ava_image_label = customtkinter.CTkLabel(self.login_frame, text="",image=self.ava_image,compound="left", fg_color="transparent")
        self.ava_image_label.grid(sticky="n",row=0,rowspan=3, column=1,padx=5,pady=5,)  # Размещаем в верхней части, но ниже, чем label
        self.reg_user = customtkinter.CTkEntry(self.login_frame, placeholder_text="Логин", text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_user.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.login_frame.columnconfigure(2, minsize=250)

        self.reg_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_frame.grid(row=2, column=1, pady=(10, 0))
        self.reg_pass = customtkinter.CTkEntry(self.reg_frame, placeholder_text="Пароль",show="*",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_pass.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.pass_image_label = customtkinter.CTkLabel(self.reg_frame, text="",image=self.pass_image,compound="left", fg_color="transparent")
        self.pass_image_label.grid(sticky="n",row=0, column=1,padx=5,pady=5,) 
        self.reg_frame.columnconfigure(2, minsize=250)
        
        self.reg_frame_pass = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_frame_pass.grid(row=3, column=1, pady=(10, 0))
        self.reg_passdub = customtkinter.CTkEntry(self.reg_frame_pass, placeholder_text="Повтор пароля",show="*",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_passdub.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.pass_image_label = customtkinter.CTkLabel(self.reg_frame_pass, text="",image=self.pass_image,compound="left", fg_color="transparent")
        self.pass_image_label.grid(sticky="n",row=0, column=1,padx=5,pady=5,) 
        self.reg_frame_pass.columnconfigure(2, minsize=250)

        self.reg_email_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_email_frame.grid(row=4, column=1, padx=20, pady=(10, 0))
        self.reg_email_image_label = customtkinter.CTkLabel(self.reg_email_frame, text="",image=self.email_image,compound="left", fg_color="transparent")
        self.reg_email_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.reg_email = customtkinter.CTkEntry(self.reg_email_frame, placeholder_text="Email",text_color=GRAY_TEXT_COLOR, font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_email.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.reg_email_frame.columnconfigure(2, minsize=250)

        self.reg_fname_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_fname_frame.grid(row=5, column=1, padx=20, pady=(10, 0))
        self.reg_fname_image_label = customtkinter.CTkLabel(self.reg_fname_frame, text="",image=self.fname_image,compound="left", fg_color="transparent")
        self.reg_fname_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.reg_fname = customtkinter.CTkEntry(self.reg_fname_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Имя", font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_fname.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.reg_fname_frame.columnconfigure(2, minsize=250)
        
        self.reg_lname_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_lname_frame.grid(row=6, column=1, padx=20, pady=(10, 0))
        self.reg_lname_image_label = customtkinter.CTkLabel(self.reg_lname_frame, text="",image=self.fname_image,compound="left", fg_color="transparent")
        self.reg_lname_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.reg_lname = customtkinter.CTkEntry(self.reg_lname_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Фамилия", font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_lname.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.reg_lname_frame.columnconfigure(2, minsize=250)

        self.reg_city_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_city_frame.grid(row=1, column=2, padx=20, pady=(10, 0))
        self.reg_city_image_label = customtkinter.CTkLabel(self.reg_city_frame, text="",image=self.city_image,compound="left", fg_color="transparent")
        self.reg_city_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.reg_city = customtkinter.CTkEntry(self.reg_city_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Город", font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_city.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.reg_city_frame.columnconfigure(2, minsize=250)

        self.phone_var = tk.StringVar(value="Телефон") 
        self.reg_mobile_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.reg_mobile_frame.grid(row=2, column=2, padx=20, pady=(10, 0))
        self.reg_mobile_image_label = customtkinter.CTkLabel(self.reg_mobile_frame, text="",image=self.mobile_image,compound="left", fg_color="transparent")
        self.reg_mobile_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.reg_mobile = customtkinter.CTkEntry(self.reg_mobile_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Телефон",textvariable=self.phone_var, font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.reg_mobile.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.reg_mobile_frame.columnconfigure(2, minsize=250)
        self.reg_mobile.bind('<KeyRelease>', self.on_phone_key_release)
        self.reg_mobile.bind('<FocusIn>', self.on_phone_focus_in)
        self.reg_mobile.bind('<KeyRelease>', self.on_phone_key_release)
        self.phone_started = False
        self.dates = ['1','2', '3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.months = ['Январь','Февраль', 'Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
        self.variable = StringVar()
        self.variable.set(self.dates[30])
        self.birthday_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.birthday_frame.grid(row=3, column=2, padx=20, pady=(10, 0))
        self.birthday_image_label = customtkinter.CTkLabel(self.birthday_frame, text="",image=self.birthday_image,compound="left", fg_color="transparent")
        self.birthday_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.birthday = customtkinter.CTkEntry(self.birthday_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Дата рождения", font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.birthday.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.birthday_frame.columnconfigure(2, minsize=250)
        self.promocode_frame = ctk.CTkFrame(self.frame_reg, fg_color=WHITE_BACK_COLOR ,corner_radius=15,)
        self.promocode_frame.grid(row=4, column=2, padx=20, pady=(10, 0))
        self.promocode_image_label = customtkinter.CTkLabel(self.promocode_frame, text="",image=self.promocode_image,compound="left", fg_color="transparent")
        self.promocode_image_label.grid(sticky="n",row=0, column=0,padx=5,pady=5,) 
        self.promocode = customtkinter.CTkEntry(self.promocode_frame,text_color=GRAY_TEXT_COLOR, placeholder_text="Промокод", font=customtkinter.CTkFont(size=12,weight="bold"),fg_color="transparent", border_width=0)
        self.promocode.grid(row=0, column=2, columnspan=2, padx=(0,5), pady=(10,5), sticky="ew")
        self.promocode_frame.columnconfigure(2, minsize=250)
        self.reg_btn =  customtkinter.CTkButton(self.frame_reg, text='Зарегистрировать', command=self.register)
        self.reg_btn.grid(row=11, column=2,pady=(10, 10))

    def on_phone_focus_in(self, event):
        content = self.phone_var.get()
        if content == "Телефон":
            self.phone_var.set("+7")
            self.reg_mobile.icursor(2)  # Устанавливает курсор после "+7"
            self.phone_started = True  
            
    def on_phone_key_release(self, event):
        content = self.phone_var.get()
        
        # Удаляем все нецифровые символы, кроме первых двух (для "+7")
        cleaned_content = "+7" + ''.join([char for char in content[2:] if char.isdigit()])
        
        if content != cleaned_content:
            self.phone_var.set(cleaned_content)
            return

        if content == "":
            if not self.phone_started:
                self.phone_var.set("Телефон")
            else:
                self.phone_var.set("+7")
                self.reg_mobile.icursor(2)
        else:
            if content == "Телефон":
                return
                
            content = self.phone_var.get()
            
            # Если пользователь начал вводить номер, мы добавляем +7
            if len(content) == 1 and content.isdigit():
                self.phone_var.set("+7" + content)
                self.reg_mobile.icursor(3)
            elif not content.startswith("+7") and content != '':
                self.phone_var.set("+7" + content[1:])
                self.reg_mobile.icursor(3)
            elif len(content) > 12:
                self.phone_var.set(content[:12])


    def register(self):
        phone_content = self.phone_var.get()
        response = requests.post(f"{SERVER_URL}/register", json={
            "login":self.reg_user.get(),
            "email": self.reg_email.get(),
            "password": self.reg_pass.get(),
            "password_dub": self.reg_passdub.get(),
            "fname": self.reg_fname.get(),
            "lname": self.reg_lname.get(),
            "city": self.reg_city.get(),
            "mobile": self.reg_mobile.get(),
            "promocode":  self.promocode.get()
        })

        # Handling the response
        data = response.json()
        if response.status_code == 400:
            messagebox.showerror("", data['message'])
        else:
            messagebox.showinfo("Регистрация успешно завершена", data['message'])
            if self.root_instance._frame is not None:
                self.root_instance._frame.destroy()
            self.root_instance.switch_frame(Main_frame)

class MainRules(customtkinter.CTkFrame):
    def __init__(self, root_instance, data_updater,people_updater=None, master=None, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.data_updater = data_updater 
        self.people_updater = people_updater 
        self.configure(corner_radius=0, fg_color="#ffffff",border_width=5, border_color="#000000")
        rules1 = "Для того, чтобы играть в лотерею Мечталлион, нужно зарегистрировать чек. Правила лотереи говорят, что оформить чек можно на официальном сайте акции или приобретя бумажный билет у партнеров конкурса. При обращении в «Почту России» можно купить билет в одном чеке. При покупке в сетях магазинов «Магнит», «Дикси» и «Красное и Белое» нужно приобрести 3 лотерейных билета в одном чеке. Важно, чтобы все билеты на Мечталлион были куплены в России.Следующий этап – зарегистрироваться на официальном сайте лотереи. Это обязательное условие проведения акции. Согласно правилам, участвовать могут только совершеннолетние лица, являющиеся гражданами РФ, постоянно проживающие на территории России и являющиеся налоговыми резидентами. Для этого нужно создать личный кабинет на сайте и указать имя и адрес электронной почты, приняв пользовательское соглашение. Без регистрации участие в акции Мечталлион будет невозможным."

        self.textbox1 = customtkinter.CTkTextbox(master=self, font=customtkinter.CTkFont(size=20, weight="bold",))
        self.textbox1.pack(fill='both',padx=5,pady=5,expand=True, )
        self.textbox1.insert("0.0", rules1)

class UserProfile(customtkinter.CTkFrame):
    def __init__(self, root_instance, data_updater,people_updater=None, master=None, **kw):
        super().__init__(master, **kw)
        self.root_instance = root_instance
        self.data_updater = data_updater 
        self.people_updater = people_updater 
        self.configure(corner_radius=0, fg_color="#ffffff",border_width=5, border_color="#000000")
        self.textbox1 = customtkinter.CTkTextbox(master=self, font=customtkinter.CTkFont(size=20, weight="bold",))
        self.textbox1.pack(fill='both',padx=5,pady=5,expand=True, )


class MainTitle(customtkinter.CTkFrame):
    def __init__(self, data_updater,root_instance, people_updater=None, master=None, **kw):
        super().__init__(master, **kw)
        self.data_updater = data_updater 
        self.people_updater = people_updater 
        self.root_instance = root_instance
        self.configure(corner_radius=0, fg_color="#242438",border_width=1, border_color="#000000")
        self.logo_Textp11 = customtkinter.CTkLabel(self, text='Добро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловатьДобро пожаловать', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_Textp11.grid(row=0, column=1, padx=0, pady=(10, 5),columnspan=2)

# class Registration(customtkinter.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("380x300")
#         self.title("Окно регистрации")


class Balanceup(customtkinter.CTkToplevel):
    def __init__(self, login, rightbar_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Здесь login - это имя пользователя, переданное при создании окна
        self.login = login
        self.rightbar_instance = rightbar_instance
        self.window = customtkinter.CTkFrame(self, corner_radius=0)
        self.title("Пополнение баланса")
        self.my_valid = self.window.register(validate) 
        self.label = customtkinter.CTkLabel(self, text="Введите цельную сумму в рублях")
        self.label.grid(row=0, column=1,padx=10,pady=(10, 10), columnspan=2)
        self.reg_user = customtkinter.CTkEntry(self, placeholder_text="Сумма",validate = 'key', validatecommand = (self.my_valid,'%S'))
        self.reg_user.grid(row=1, column=1, padx=20, pady=(10, 10))
        self.btn_balance =  customtkinter.CTkButton(self, text='Пополнить', command=self.clicked)
        self.btn_balance.grid(row=2, column=1, padx=20, pady=(10, 10))

    def clicked(self):
        # Определите переменные nikname и balance
        nikname = self.login
        balance = self.reg_user.get()  # получите сумму из self.reg_user

        # Отправка запроса на сервер
        if balance == '' or balance == "0":
            CTkMessagebox(title="Ошибка", message="Введите цельную сумму в рублях", icon="cancel")
        else:
            response = requests.post(f"{SERVER_URL}/update_balance", json={"login": nikname, "balance": balance})
            # Обработка ответа
            if response.status_code == 200:
                response_data = response.json()
                messagebox.showinfo("Успешно", response_data["message"])
                new_balance = response_data.get("new_balance")
                if new_balance is not None:
                    self.rightbar_instance.update_frame(new_balance)
                
                self.close()  # Закрыть окно пополнения баланса
            else:
                messagebox.showerror("Ошибка", "Произошла ошибка при пополнении баланса")
    def close(self):
        self.destroy()
        
def create_label(parent, text, row, column, padx=10, pady=(0, 0), sticky="w"):
    label = customtkinter.CTkLabel(parent, text=text, font=customtkinter.CTkFont(size=12, weight="bold"), width=70)
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return label

def create_button(parent, text, command, row, column,padx=0, pady=(0, 0),sticky="w", ):
    button = customtkinter.CTkButton(parent, text=text, command=command,  fg_color=DEFAULT_BTN_COLOR, hover_color=HOVER_BTN_COLOR)
    button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return button
def validate(u_input): # callback function
    return u_input.isdigit()

if __name__ == "__main__":
    root = Root()
    # root.overrideredirect(1)
    root.mainloop()
