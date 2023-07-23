import os
from dotenv import load_dotenv
from . import build_app
from telegram import (
    Update, InlineKeyboardButton, KeyboardButton,
    KeyboardButtonPollType, ReplyKeyboardMarkup,
    ReplyKeyboardRemove, InlineKeyboardMarkup,   
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, 
    filters, MessageHandler, CallbackQueryHandler,
    ConversationHandler
)
import telegram
import numpy as np
from datetime import datetime

load_dotenv()

ALL_ACTIONS, END = list(map(lambda x: str(x), range(2)))
ABOUT_DESC, MASSAGES_DESC, TO_REGISTER, ON_TEST, *_ = list(map(lambda x: str(x), range(2,15)))
START_OVER = str(100)

(
    START,
    #* main 
    ABOUT,
    MASSAGES,
    PRICES,
    REGISTER,
    TEST,
    ASK_CALL,
    MAIL_SALES,
    #* about
    EXPERIENCE,
    CERTIFICATES,
    #* massages
    ANTICEL,
    MIOPHAS,
    PROPHYLACTIC,
    MERIDIAN,
    MEDICAL,
    SPORT,
    TAI,
    HONEY,
    #* stoppers
    REGISTER_ON_TEST,
    FINISH,
    BACK,
    STOP,
    *_
)  = list(map(lambda x: str(x), range(500, 600)))

MASTER_ID = 6046133979


class Massage:
    def __init__(
        self, 
        app: ApplicationBuilder 
    ) -> None:
        self.app = app
        self.register_store = dict()
        # self._setup_handlers()

    def _conversation_setup(
        self,
        entry,
        states,
        fallbacks
    ):
        return ConversationHandler(
            entry_points = entry,
            states = states,
            fallbacks = fallbacks,
            allow_reentry=True
        )

    def _setup_handlers(
        self,
        handler: str,
        callback_str: str,
        filters: None | object = None,
        iscommand:bool = False
        
    ):
        #! under dev
        #* LIST of handlers:
        #*  about:
        #*      conversation start with /about 
        #*      (can be implemented via button) command
        #*      Other stuff implemented via buttons:
        #*          experience - 
        #*          rewards - 
        #*          fallback - 
        #*  services:
        #*      conversation start with /services
        #*      (can be implemented via button) command
        #*      Here is a set of links (buttons) to navigate
        #*      to get more info about each type of massage provided
        #*      by master. Each page with massage description consists of 
        #*      price info and register button:
        #*          type1 - 
        #*          type2 - 
        #*          typeN -
        #*          fallback -     

        method = getattr(telegram.ext, handler)
        callback = getattr(self, callback_str)
        if iscommand:
            return method(
                command=callback_str,
                callback=callback,
            )
        
        return method( 
            callback=callback
        )
    
    def _build_btns(
        self,
        columns: int,
        data: list,
        # callback_data: list
    ):
        # if callback_data is None:
        #     callback_data = data
        
        keyboard = []
        for i in data:
            keyboard.append(
                InlineKeyboardButton(i[0], callback_data=i[1])
            )
        keyboard = self._reshaper(keyboard, columns)

        return InlineKeyboardMarkup(keyboard)

    def _reshaper(
        self, 
        arr, 
        columns: int
    ):
        rows = len(arr) // columns
        remainder = len(arr) % columns
        total_items = rows * columns + remainder
        new_arr = []
        row = []

        for n, i in enumerate(arr, start=1):
            row.append(i)
            if n % columns == 0 and n != 1:
                new_arr.append(row)
                row = []

        
        if remainder:
            new_arr.append(arr[-remainder:])
        
        return new_arr
    
    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
    
        welcome = [
            ("О массажисте Викторе", ABOUT),
            ("Виды массажа", MASSAGES),
            ("Прейскурант", PRICES),
            ("Тестовый экспресс-массаж", ON_TEST),
            ("Записаться", REGISTER),
            ("Заказать звонок", ASK_CALL),
            ("Подписаться на рассылку акций", MAIL_SALES),
        ]
        # welcome_callback_data = [
        #     "about", "massage", "prices", "/register",
        #     "/test", "/askcall"
        # ]
        btns = self._build_btns(2, welcome)

        if context.user_data.get(START_OVER):
            print("Start Over")
            
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                text="Что-то еще?",
                reply_markup=btns
            )
        
        else:
            await update.message.reply_text(
                "Привет, дорогой друг! Чем я могу помочь?", 
                reply_markup=btns
            )
        context.user_data[START_OVER] = False
        return ALL_ACTIONS 

    # async def go(
    #     self,
    #     update: Update, 
    #     context: ContextTypes.DEFAULT_TYPE
    # ):
    #     val = update.message.reply_text(
    #             "HELLOOOOOO",
    #             reply_markup=ReplyKeyboardMarkup(
    #             [["1", "2", "3"], ["4", "5", "6"], ["7", "8 ", "9"], ["END"]],
    #             one_time_keyboard = False,
    #             input_field_placeholder="Choose any"
    #         )
    #     )

    async def about(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        prices = [
            ("Опыт работы", EXPERIENCE),
            ("Сертификаты", CERTIFICATES),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        
        btns = self._build_btns(2, prices)
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="BLABLABLA", reply_markup=btns)
        
        return ABOUT_DESC
        
    async def experience(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("Called experience")
        return 

    async def certificates(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("Called certificates")
        return 

    async def massages(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        massages = [
            ("Антицеллюлитный", ANTICEL),
            ("Лечебный", MEDICAL),
            ("Спортивный", SPORT),
            ("Меридианный", MERIDIAN),
            ("Миофасциальный", MIOPHAS),
            ("Профилактический", PROPHYLACTIC),
            ("Тайский", TAI),
            ("Медовый", HONEY),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, massages)
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="all massages", reply_markup=btns)

        return MASSAGES_DESC

    async def massage_desc(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        await update.callback_query.answer()
        massage_id = update.callback_query.data
        massage_desc = [
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, massage_desc)

        print(update.callback_query.from_user)
        await update.callback_query.edit_message_text(text="INFO about ")

    async def prices(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        prices = [
            ("Записаться", REGISTER),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, prices)
        prices = "The price list of services provided by Viktor"
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=prices, reply_markup=btns)
        
    async def register_to_master(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        **kwargs
    ) -> None:
        print("resending to master")
        # to_resend = update.message.text
        await context.bot.send_message(
            MASTER_ID,
            text=f"Мастер Виктор, У Вас новое сообщение\n"
            + f"Сообщение от: *{kwargs.get('name')}*\n"
            + f"Жалоба на: *{kwargs.get('complaints')}*\n"
            + f"Предпочтительное время сеанса: *{kwargs.get('time')}*\n"
            + f"Контактный номер телефона: {kwargs.get('phone_number')}",
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )
    
    async def register(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        self.register_store[update.callback_query.from_user.id] = dict()
         
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            f"Спасибо за обращение, {appeal_to}.\nДля завершение процедуры записи, пожалуйста, ответьте на несколько вопросов\n"
            + "Какие у Вас жалобы?"
        )
        # await self.resend_to_master(update, context)

        
        return TO_REGISTER

    async def on_test(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        on_test = [
            ("Записаться", REGISTER),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, on_test)
        self.register_store[update.callback_query.from_user.id] = dict()
         
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            f"Спасибо за обращение, {appeal_to}.\n"
            + "Позвольте подробнее рассказать про тестовый экспресс-массаж шейно-воротниковой зоны\n" 
            + "Такой массаж направлен на снятие усталости с мышц спины и шеи, что положительно влияет на качество сна\n"
            + "Длительность сеанса не более 10 минут. Стоимость 250 рублей",
            reply_markup=btns
        )
        return TO_REGISTER

    def _make_time_grid(
        self,
        # from_,
        # to_
    ) -> None:
        # print(datetime.strptime(time_str, "%H:%M").hour)
        time_grid = [
            ["08:00", "08:30", "09:00"],
            ["09:30", "10:00", "10:30"],
            ["11:00", "11:30", "12:00"],
            ["12:30", "13:00", "13:30"],
            ["14:00", "14:30", "15:00"],
            ["15:30", "16:00", "16:30"],
            ["17:00", "17:30", "18:00"],
            ["18:30", "19:00", "19:30"]
        ]
        return time_grid

    async def register_inquiry_time(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        self.register_store[update.message.from_user.id]["complaints"] = update.message.text

        await update.message.reply_text(
            "Какое предпочтительное время для сеанса?",
            reply_markup=ReplyKeyboardMarkup(
                self._make_time_grid(),  # replace to time shcedule
                one_time_keyboard = True,
            )
        )
        return TO_REGISTER
    
    async def register_inquiry_phone(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        # time_str = update.message.text
        self.register_store[update.message.from_user.id]["time"] = update.message.text

        phone_btn = KeyboardButton(
            "Отправить телефонный номер",
            request_contact=True
            # one_time_keyboard = False,
        )
        await update.message.reply_text(
            "Введите контактный номер телефона",
            reply_markup=ReplyKeyboardMarkup(
                [[phone_btn]], 
                one_time_keyboard = True
            )
        )
        return TO_REGISTER

    def check_number_correction(
        self,
        string
    ):
        if string.startswith("7"):
            string = "\+" + string
        elif string.startswith("+"):
            string = "\+" + string[1:]
        
        return string

    async def register_inquiry_finish(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        phone_number = self.check_number_correction(update.message.contact.phone_number)
        self.register_store[update.message.from_user.id]["phone_number"] = phone_number
        await self.register_to_master(
            update,
            context,    
            **self.register_store[update.message.from_user.id]
        )
        await update.message.reply_text(
            "Спасибо, Ваше обращение зарегистрировано."
            + "Ожидайте звонка для подтверждения записи"
        )
        
        return ALL_ACTIONS

    async def back(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = True
        print("On back is ", context.user_data[START_OVER])

        await self.start(update, context)
        return END
    
    async def finish(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = False
        await update.callback_query.edit_message_text(
            text="Всего Вам хорошего. Если Вам что-то будет нужно, вы знаете где меня найти"
        )

    async def stop(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        context.user_data[START_OVER] = False
        await update.message.reply_text(
            "Всего Вам хорошего. Если Вам что-то будет нужно, вы знаете где меня найти"
        )
 
    def make_pages(self):

        about = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.about, pattern=ABOUT)],
            states = {
                ABOUT_DESC: [
                    CallbackQueryHandler(self.experience, pattern=EXPERIENCE),
                    CallbackQueryHandler(self.certificates, pattern=CERTIFICATES),
                    CallbackQueryHandler(self.back, pattern=BACK)
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=FINISH),
                ],
            allow_reentry=True,
            map_to_parent = {
                END: ALL_ACTIONS
            }
        )

        massage_types = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.massages, pattern=MASSAGES)],
            states = {
                MASSAGES_DESC: [
                    CallbackQueryHandler(self.finish, pattern=FINISH),
                    CallbackQueryHandler(
                        self.massage_desc, 
                        pattern=f"{ANTICEL}|{MEDICAL}|{MERIDIAN}|{SPORT}|{MIOPHAS}|{PROPHYLACTIC}|{TAI}|{HONEY}"
                    )
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=FINISH),
                ],
            allow_reentry=True,
            map_to_parent = {
                END: ALL_ACTIONS
            }
        )
        register = ConversationHandler(
            entry_points = [
                CallbackQueryHandler(self.register, pattern=REGISTER),
                CallbackQueryHandler(self.on_test, pattern=ON_TEST)
                # CallbackQueryHandler(self.register_on_test, pattern=REGISTER_ON_TEST),
            ],
            states = {
                TO_REGISTER: [
                    CallbackQueryHandler(self.finish, pattern=FINISH),
                    MessageHandler(filters=filters.TEXT & (~filters.COMMAND) & (~filters.Regex(r'\d+:\d+')), callback=self.register_inquiry_time),
                    MessageHandler(filters=filters.Regex(r'\d+:\d+'), callback=self.register_inquiry_phone),
                    MessageHandler(filters=filters.CONTACT, callback=self.register_inquiry_finish)
                    
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=FINISH),
                ],
            allow_reentry=True,
            map_to_parent = {
                END: ALL_ACTIONS
            }
        )

        cv = ConversationHandler(
            entry_points = [CommandHandler("start", self.start)],
            states = {
                ALL_ACTIONS: [
                    about,
                    massage_types,
                    register,
                    # CallbackQueryHandler(self.about, pattern="about"),
                    CallbackQueryHandler(self.prices, pattern=PRICES),
                    # CallbackQueryHandler(self.on_test, pattern=ON_TEST),
                    # CallbackQueryHandler(self.back, pattern="back")
                ],                
            },
            fallbacks=[
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=FINISH),
            ],
            allow_reentry=True
        )

        self.app.add_handler(cv)
        # for i in pages:
        #     page = self._setup_handlers(*i) 
        #     self.app.add_handler(page)

        self.app.run_polling()
        

def run():
    Massage(app=build_app()).make_pages()