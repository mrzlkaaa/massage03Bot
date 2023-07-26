import os
from dotenv import load_dotenv
from . import build_app, static_text
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
text_data = static_text()

ALL_ACTIONS, HOME, END, *_ = list(map(lambda x: str(x), range(5)))
(
    ABOUT_DESC, 
    MASSAGES_DESC, 
    TO_REGISTER,
    PROMOTIONS,
    REGISTER_INQUIRY,
    PROMOTIONS_INQUIRY,
    *_
) = list(map(lambda x: str(x), range(5, 20)))
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
    ON_TEST_TIME,
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
    EXPRESS,
    #* register
    MEDICAL_COMPLAINTS,
    PICK_MASSAGE,
    PICK_PROMOTION,
    #* stoppers
    FINISH,
    BACK,
    STOP,
    *_
)  = list(map(lambda x: str(x), range(500, 600)))

TIME_GRID = [
    ["08:00", "08:30", "09:00"],
    ["09:30", "10:00", "10:30"],
    ["11:00", "11:30", "12:00"],
    ["12:30", "13:00", "13:30"],
    ["14:00", "14:30", "15:00"],
    ["15:30", "16:00", "16:30"],
    ["17:00", "17:30", "18:00"],
    ["18:30", "19:00", "19:30"]
]

MASSAGE_GRID = [
    ["Антицеллюлитный", "Лечебный"],
    ["Спортивный", "Меридианный"],
    ["Миофасциальный", "Профилактический"],
    ["Тайский", "Медовый"]
]

MASTER_ID = 355535366 # 6046133979


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
    
        to_btns = [
            ("О массажисте Викторе", ABOUT),
            ("Виды массажа", MASSAGES),
            ("Прейскурант", PRICES),
            ("Акции", PROMOTIONS),
            ("Записаться", TO_REGISTER),
            # ("Заказать звонок", ASK_CALL),
            # ("Подписаться на рассылку акций", MAIL_SALES),
        ]
        btns = self._build_btns(2, to_btns)

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

    async def about(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        to_btns = [
            ("Опыт работы", EXPERIENCE),
            ("Сертификаты", CERTIFICATES),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        
        btns = self._build_btns(2, to_btns)
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
        consts = [
            ANTICEL, MEDICAL,
            SPORT, MERIDIAN,
            MIOPHAS, PROPHYLACTIC,
            TAI, HONEY,
            BACK, FINISH
        ]

        lst = [
            *text_data.get("massages").get("massages_list"),
            "Назад", "Завершить"
        ]

        to_btns = list(zip(lst, consts))
        btns = self._build_btns(2, to_btns)
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
        to_btns = [
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, to_btns)

        print(update.callback_query.from_user)
        await update.callback_query.edit_message_text(text="INFO about ")

    async def prices(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        to_btns = [
            ("Записаться", REGISTER),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, to_btns)
        prices = "The price list of services provided by Viktor"
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=prices, reply_markup=btns)
        return ALL_ACTIONS
        
    async def register_to_master(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        **kwargs
    ) -> None:
        print("resending to master")
        reason = kwargs.get('complaints')\
            if kwargs.get('complaints')\
            else text_data.get("massages")\
                .get("mapping")\
                .get(kwargs.get('massage'))  + ' массаж'
        # to_resend = update.message.text
        await context.bot.send_message(
            MASTER_ID,
            text=f"Мастер Виктор, У Вас новое сообщение\n"
            + f"Сообщение от: *{kwargs.get('name')}*\n"
            + f"Жалоба / Массаж: *{reason}*\n"
            + f"Предпочтительное время сеанса: *{kwargs.get('time')}*\n"
            + f"Контактный номер телефона: {kwargs.get('phone_number')}",
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )

    async def promotions(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        to_btns = [
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]

        btns = self._build_btns(1, to_btns)

        self.register_store[update.callback_query.from_user.id] = dict()
         
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to
        
        promotions_list = text_data.get("promotions").get("promotions_list")
        promotions_desc = text_data.get("promotions").get("promotions_desc")
        promotions = ""
        for i in range(len(promotions_list)):
            promotions += promotions_list[i] + "\n".join(promotions_desc[i])
        
        # print(promotions)
        await update.callback_query.edit_message_text(
            "В настоящее время Вы можете воспользоваться следующими акциями:\n\n"
            + promotions,
            reply_markup=btns
        )
        return PROMOTIONS_INQUIRY

    # async def register(
    #     self,
    #     update: Update, 
    #     context: ContextTypes.DEFAULT_TYPE
    # ) -> None:
        
    #     to_btns = [
    #         ("Начать", TO_REGISTER),
    #         ("Назад", HOME),
    #         ("Завершить", FINISH)
    #     ]
    #     btns = self._build_btns(2, to_btns)
        
    #     self.register_store[update.callback_query.from_user.id] = dict()
         
    #     appeal_to = update.callback_query.from_user.first_name
    #     self.register_store[update.callback_query.from_user.id]["name"] = appeal_to

    #     await update.callback_query.answer()
    #     await update.callback_query.edit_message_text(
    #         f"Спасибо за обращение, {appeal_to}.\n"
    #         + "Для завершение процедуры записи, пожалуйста, ответьте на несколько вопросов\n",

    #         reply_markup=btns
            
    #     )
    #     return ALL_ACTIONS
        
    async def register_inquiry(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        to_btns = [
            ("Выбрать вид массажа", PICK_MASSAGE),
            ("У меня медицинские показания", MEDICAL_COMPLAINTS),
            # ("Записаться", ON_TEST_TIME),
            ("Назад", BACK),
            ("Завершить", FINISH)
        ]
        btns = self._build_btns(2, to_btns)
        
        self.register_store[update.callback_query.from_user.id] = dict()
         
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Вас интересует определенный вид массажа?\n",
            reply_markup=btns
            
        )
        

        return REGISTER_INQUIRY

    async def register_medical_complaints(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        # self.register_store[update.message.from_user.id]["complaints"] = update.message.text

        await update.callback_query.edit_message_text(
            "Опишите свои жалобы и беспокойства, пожалуйста 📝",
        )
        return REGISTER_INQUIRY
    
    async def register_massage(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        massages = text_data.get("massages").get("massages_list")
        emoji = text_data.get("numerical_emoji")
        massage_services = ""
        for i in range(len(massages)):
            massage_services += f"{emoji[i]}   {massages[i]}\n\n"
        
        print(massage_services)
        await update.callback_query.edit_message_text(
            "В настоящее время Вам могут быть предоставлены следующие услуги массажа 📋\n\n"
            + massage_services 
            +"Отправьте номер услуги, пожалуйста\n"
            +"Если Вы затрудняетесь сделать выбор, то отправьте 0️⃣\n"
            +"В этом случае мастер проконсультирует Вас и ответит на все Ваши вопросы"
            
        )
        return REGISTER_INQUIRY
    
    async def register_inquiry_time(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        message = update.message.text
        try:
            int(message)
            self.register_store[update.message.from_user.id]["massage"] = message
        except ValueError:
            self.register_store[update.message.from_user.id]["complaints"] = message

        print(self.register_store)
        await update.message.reply_text(
            "Какое время сеанса для Вас наиболее предпочтительно?",
            reply_markup=ReplyKeyboardMarkup(
                TIME_GRID,
                one_time_keyboard = True,
            )
        )
        return REGISTER_INQUIRY

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
            "☎ Пожалуйста, подтвердите отправку контактного номера телефона",
            reply_markup=ReplyKeyboardMarkup(
                [[phone_btn]], 
                one_time_keyboard = True
            )
        )
        return REGISTER_INQUIRY

    def number_correction(
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
        phone_number = self.number_correction(update.message.contact.phone_number)
        self.register_store[update.message.from_user.id]["phone_number"] = phone_number
        await self.register_to_master(
            update,
            context,    
            **self.register_store[update.message.from_user.id]
        )
        await update.message.reply_text(
            "Спасибо 🙏\n"
            + "Ваше обращение зарегистрировано\n"
            + "⏰ Ожидайте звонка для подтверждения записи"
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

    async def home(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = True
        print("Back to Home ", context.user_data[START_OVER])

        await self.start(update, context)
        return ALL_ACTIONS
    
    async def finish(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = False
        await update.callback_query.edit_message_text(
            text="Всего Вам хорошего 👋\n" 
            + "Если Вам что-то будет нужно, вы знаете где меня найти"
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

        back = CallbackQueryHandler(self.back, pattern=BACK)
        register_message_handlers = [
            MessageHandler(filters=filters.TEXT & (~filters.COMMAND) & (~filters.Regex(r'\d+:\d+')), callback=self.register_inquiry_time),
            MessageHandler(filters=filters.Regex(r'\d+:\d+'), callback=self.register_inquiry_phone),
            MessageHandler(filters=filters.CONTACT, callback=self.register_inquiry_finish),
        ]
        about = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.about, pattern=ABOUT)],
            states = {
                ABOUT_DESC: [
                    CallbackQueryHandler(self.experience, pattern=EXPERIENCE),
                    CallbackQueryHandler(self.certificates, pattern=CERTIFICATES),
                    back
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
                    ),
                    back
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
                CallbackQueryHandler(self.register_inquiry, pattern=TO_REGISTER),
                # CallbackQueryHandler(self.ontest, pattern=ON_TEST) #!
            ],
            states = {
                REGISTER_INQUIRY: [
                    CallbackQueryHandler(self.register_massage, pattern=PICK_MASSAGE),
                    CallbackQueryHandler(self.register_medical_complaints, pattern=MEDICAL_COMPLAINTS),
                    *register_message_handlers,
                    back
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
        promotions = ConversationHandler(
            entry_points = [
                CallbackQueryHandler(self.promotions, pattern=PROMOTIONS),
                # CallbackQueryHandler(self.ontest, pattern=ON_TEST) #!
            ],
            states = {
                PROMOTIONS_INQUIRY: [
                    # CallbackQueryHandler(self.register_promotions, pattern=PICK_PROMOTION),
                    *register_message_handlers,
                    back
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
                    promotions,
                    CallbackQueryHandler(self.prices, pattern=PRICES),
                    # CallbackQueryHandler(self.register, pattern=REGISTER),
                    # CallbackQueryHandler(self.ontest, pattern=ON_TEST),
                    CallbackQueryHandler(self.home, pattern=HOME),
                ],                
            },
            fallbacks=[
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=FINISH),
            ],
            allow_reentry=True
        )

        self.app.add_handler(cv)

        self.app.run_polling()
        

def run():
    Massage(app=build_app()).make_pages()