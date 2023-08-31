import os
from dotenv import load_dotenv
from . import *
import telegram
from telegram.ext import ApplicationBuilder
import numpy as np
from datetime import datetime

from .description import *
from .register import *
# from .promos import Promos
from .base import Base
from .clients import Clients
from .db import ClientsDB
from . import logger
from collections import defaultdict



load_dotenv()

text_data = static_text()
configs = config()

START_OVER = str(1000)


MASSAGE_GRID = [
    ["Антицеллюлитный", "Лечебный"],
    ["Спортивный", "Меридианный"],
    ["Миофасциальный", "Профилактический"],
    ["Тайский", "Медовый"]
]

MASTER_ID = 355535366 # 408886736 #6046133979 
MASETRS_CHANNEL_ID = os.getenv("MASTERS_CHANNEL_ID")


class Interface(
    Description,
    Register,
    # Promos
):
    (
        #* main 
        ABOUT,
        MASSAGES,
        PRICES,
        REGISTER,
        # TO_REGISTER,
        PROMOTIONS,
        TO_PRICES_INQUIRY,
        APPROVE,
        REJECT,
        *_
    )  = list(map(lambda x: str(x), range(50, 99)))
    
    def __init__(
        self, 
        logger: object,
        app: ApplicationBuilder,
        clients: Clients,
        text_data
    ) -> None:
        self.logger = logger
        self.app = app
        self.clients = clients 
        self.register_store = dict()
        self.messages_id = dict()
        Base.__init__(self, text_data)
        # self._setup_handlers()

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
        new_arr = []
        row = []

        if columns == 1:
            for n, i in enumerate(arr, start=1):
                row.append(i)
                new_arr.append(row)
                row = []
            print(new_arr)
            return new_arr
        
        else:
            rows = len(arr) // columns
            remainder = len(arr) % columns
            total_items = rows * columns + remainder
        
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
            # ("О себе", self.ABOUT),
            ("Виды массажа", self.MASSAGES),
            ("Прейскурант", self.PRICES),
            ("Акции", self.PROMOTIONS),
            ("Записаться", self.REGISTER),
            # ("Заказать звонок", ASK_CALL),
            # ("Подписаться на рассылку акций", MAIL_SALES),
        ]
        btns = self._build_btns(2, to_btns)

        if context.user_data.get(START_OVER):
            print("Start Over")
            client = update.callback_query.from_user
            
            await update.callback_query.edit_message_text(
                text="Что-то еще?",
                reply_markup=btns
            )
        
        else:
            client = update.message.from_user
            await update.message.reply_text(
                "Доброго времени суток! Чем я могу Вам помочь?", 
                reply_markup=btns
            )

        res = self.clients.get_by_tgid(client.id)
            
        if not res:
            self.logger.warning(
                f"New client {client.first_name} <{client.id}> has run a bot\n"
                + "Preparations to add to DB"
            )
            res = self.clients.add_client(client)
            if not res:
                self.logger.error(
                    f"Was not able to add new client <{client.id}> to db "
                )
            res = self.clients.get_by_tgid(client.id)
        
        self.logger.info(
            f"client {client.first_name} <{client.id}> is back to Bot"
        )

        context.user_data[START_OVER] = False
        return self.ALL_ACTIONS    

    async def prices(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        to_btns = [
            ("Назад", self.BACK),
        ]
        btns = self._build_btns(1, to_btns)
        
        massages = self.text_data.get("massages").get("services")
        emoji = self.text_data.get("numerical_emoji")

        prices = ""
        for i in range(len(massages)):
            prices += f"{emoji[i]}   {massages[i]}\n\n"
        
        await update.callback_query.edit_message_text(
            "В настоящее время Вы можете воспользоваться следующими услугами массажа:\n\n"
            + prices,
            reply_markup=btns
        )
        
        return self.TO_PRICES_INQUIRY
        
    
    async def register_to_master(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        **kwargs
    ) -> None:
        print("resending to master")
        
        btns = [[]]
        print("ID info", self.register_store[kwargs.get("id")])
        #* clear dict for user who completed inquiry
        # if not self.register_store[kwargs.get("id")].get("approved"): 
        to_btns = [
            ("❌ Не подтверждено", self.APPROVE),
            ("Отменить", self.REJECT),
        ]
        btns = self._build_btns(1, to_btns)
        # self.register_store[update.message.from_user.id].clear()
        

        await context.bot.send_message(
            MASTER_ID,
            text=f"{'❗ЭТО СТАДИЯ ТЕСТА❗' if configs.get('dev') else ''}"
            + "Мастер Виктор, У Вас новое сообщение\n"
            + f"Сообщение от: *{kwargs.get('name')}*\n"
            + f"Жалоба / Массаж: *{kwargs.get('order')}*\n"
            + f"Предпочтительное время сеанса: *{kwargs.get('time')}*\n"
            + f"Контактный номер телефона: {kwargs.get('phone_number')}\n"
            + "Выберите одно из доступных действий ⬇",
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
            reply_markup=btns
        )

    async def approve(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("CALLED APPROVE", update.callback_query.message.id)

        if not self.messages_id.get(update.callback_query.message.id):
            to_btns = [
                ("✅ Подтверждено", self.APPROVE),
                ("Отменить", self.REJECT),
            ]
            btns = self._build_btns(1, to_btns)

            self.messages_id[update.callback_query.message.id] = {
                "status" : True
            }

            await update.callback_query.edit_message_reply_markup(
                reply_markup=btns
            )

        elif self.messages_id.get(update.callback_query.message.id)\
            and self.messages_id.get(update.callback_query.message.id).get("status"):
            
            to_btns = [
                ("❌ Не подтверждено", self.APPROVE),
                ("Отменить", self.REJECT),
            ]
            btns = self._build_btns(1, to_btns)
            
            self.messages_id[update.callback_query.message.id] = {
                "status" : False
            }
            
            await update.callback_query.edit_message_reply_markup(
                reply_markup=btns
            )

        
        elif self.messages_id.get(update.callback_query.message.id)\
            and not self.messages_id.get(update.callback_query.message.id).get("status"):
            
            to_btns = [
                ("✅ Подтверждено", self.APPROVE),
                ("Отменить", self.REJECT),
            ]
            btns = self._build_btns(1, to_btns)
            
            self.messages_id[update.callback_query.message.id] = {
                "status" : True
            }

            await update.callback_query.edit_message_reply_markup(
                reply_markup=btns
            )
        return self.ALL_ACTIONS


    async def reject(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("CALLED REJECT", update.callback_query.message.id)

        to_btns = [
                ("♻ Восстановить", 1234),
            ]
        btns = self._build_btns(1, to_btns)

        await update.callback_query.edit_message_reply_markup(
            reply_markup=btns
        )
        return self.ALL_ACTIONS


    async def back(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = True
        print("On back is ", context.user_data[START_OVER])

        await self.start(update, context)
        return self.END

    async def home(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        context.user_data[START_OVER] = True
        print("Back to Home ", context.user_data[START_OVER])

        await self.start(update, context)
        return self.ALL_ACTIONS
    
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
 
    async def unknown_command(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        await update.message.reply_text(
            "Извините, но эта команда мне непонятна"
        )
        # return self.END

    async def unknown_message(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        await update.message.reply_text(
            "Извините, но это сообщение мне непонятно"
        )
        # return self.END

    def run(self):

        back = CallbackQueryHandler(self.back, pattern=self.BACK)
        
        register_message_handlers = [
            MessageHandler(
                filters=filters.TEXT\
                    & (~filters.COMMAND)\
                    & (~filters.Regex(r'\d+:\d+'))\
                    & (~filters.Regex(r'^[+789]\d+')), 
                callback=self.register_inquiry_time),
            MessageHandler(filters=filters.Regex(r'\d+:\d+'), callback=self.register_inquiry_phone),
            MessageHandler(
                filters=filters.CONTACT | filters.Regex(r'^[+789]\d+'), 
                callback=self.register_inquiry_finish),
        ]
        
        #! omitted
        # about = ConversationHandler(
        #     entry_points = [CallbackQueryHandler(self.about, pattern=self.ABOUT)],
        #     states = {
        #         self.ABOUT_DESC: [
        #             CallbackQueryHandler(self.experience, pattern=self.EXPERIENCE),
        #             CallbackQueryHandler(self.certificates, pattern=self.CERTIFICATES),
        #             back
        #         ]
        #     },
        #     fallbacks = [
        #         CommandHandler("stop", self.stop),
        #         CallbackQueryHandler(self.finish, pattern=self.FINISH),
        #         ],
        #     allow_reentry=True,
        #     map_to_parent = {
        #         self.END: self.ALL_ACTIONS
        #     }
        # )

        massage_types = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.massages, pattern=self.MASSAGES)],
            states = {
                self.MASSAGES_DESC: [
                    CallbackQueryHandler(self.finish, pattern=self.FINISH),
                    CallbackQueryHandler(
                        self.massage_desc, 
                        pattern=f"{self.SHVZ}|{self.ANTICEL}|{self.SPORT}|{self.CLASSIC}|{self.PROPHYLACTIC}|{self.TAI}|{self.HONEY}"
                    ),
                    back
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=self.FINISH),
                ],
            allow_reentry=True,
            map_to_parent = {
                self.END: self.ALL_ACTIONS
            }
        )

        prices = ConversationHandler(
            entry_points = [
                CallbackQueryHandler(self.prices, pattern=self.PRICES),
            ],
            states = {
                self.TO_PRICES_INQUIRY: [
                    back
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=self.FINISH),
            ],
            allow_reentry=True,
            map_to_parent = {
                self.END: self.ALL_ACTIONS
            }
        )

        register = ConversationHandler(
            entry_points = [
                CallbackQueryHandler(self.register_inquiry, pattern=self.REGISTER),
                CallbackQueryHandler(self.promotions, pattern=self.PROMOTIONS),
            ],
            states = {
                self.TO_REGISTER_INQUIRY: [
                    CallbackQueryHandler(self.register_massage, pattern=self.PICK_MASSAGE),
                    CallbackQueryHandler(self.register_medical_complaints, pattern=self.MEDICAL_COMPLAINTS),
                    *register_message_handlers,
                    back
                ]
            },
            fallbacks = [
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=self.FINISH),
            ],
            allow_reentry=True,
            map_to_parent = {
                self.END: self.ALL_ACTIONS
            }
        )
        
        #! omitted
        # promotions = ConversationHandler(
        #     entry_points = [
        #         CallbackQueryHandler(self.promotions, pattern=self.PROMOTIONS),
        #     ],
        #     states = {
        #         self.PROMOTIONS_INQUIRY: [
        #             *register_message_handlers,
        #             back
        #         ]
        #     },
        #     fallbacks = [
        #         CommandHandler("stop", self.stop),
        #         CallbackQueryHandler(self.finish, pattern=self.FINISH),
        #     ],
        #     allow_reentry=True,
        #     map_to_parent = {
        #         self.END: self.ALL_ACTIONS
        #     }
        # )         

        cv = ConversationHandler(
            entry_points = [CommandHandler("start", self.start)],
            states = {
                self.ALL_ACTIONS: [
                    # about,
                    massage_types,
                    prices,
                    register,
                    CallbackQueryHandler(self.approve, pattern=self.APPROVE),
                    CallbackQueryHandler(self.reject, pattern=self.REJECT),
                    CallbackQueryHandler(self.home, pattern=self.HOME),
                    #* any text in this top-level
                    MessageHandler(
                        filters=filters.TEXT
                            & (~filters.COMMAND),
                        callback=self.unknown_message
                    ),
                    #* any command that does not exists
                    MessageHandler(
                        filters=filters.COMMAND,
                        callback=self.unknown_command
                    ),

                ],                
            },
            fallbacks=[
                CommandHandler("stop", self.stop),
                CallbackQueryHandler(self.finish, pattern=self.FINISH),
                back
            ],
            allow_reentry=True
        )

        self.app.add_handler(cv)

        self.app.run_polling()
        

def run():
    Interface(
        logger=logger(),
        app=build_app(),
        text_data=text_data,
        clients=Clients(
            db=ClientsDB(
                engine=engine()
            )
        )
    ).run()