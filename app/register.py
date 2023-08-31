from app import clients
from . import *
from .base import Base

__all__ = ["Register"]

class Register(Base):
    (
        MEDICAL_COMPLAINTS,
        PICK_MASSAGE,
        # PICK_PROMOTION,
        PROMOTIONS_INQUIRY,
        TO_REGISTER_INQUIRY,
        *_
    ) = list(map(lambda x: str(x), range(150, 200)))


    async def promotions(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        to_btns = [
            ("Назад", self.BACK),
            ("Завершить", self.FINISH)
        ]

        btns = self._build_btns(1, to_btns)

        self.register_store[update.callback_query.from_user.id] = dict()
         
        #* name + id
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to
        self.register_store[update.callback_query.from_user.id]["id"] = update.callback_query.from_user.id
        
        emoji = self.text_data.get("numerical_emoji")
        services = self.text_data.get("promotions").get("services")
        desc = self.text_data.get("promotions").get("promotions_desc")

        promotions = ""
        for i in range(len(services)):
            promotions += f"{emoji[i]}   {services[i]}" + '\n'.join(desc[i])
        
        await update.callback_query.edit_message_text(
            "В настоящее время Вы можете воспользоваться следующими акциями:\n\n"
            + promotions,
            reply_markup=btns
        )
        return self.TO_REGISTER_INQUIRY

    async def register_inquiry(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("register")
        to_btns = [
            ("Выбрать вид массажа", self.PICK_MASSAGE),
            ("У меня медицинские показания", self.MEDICAL_COMPLAINTS),
            # ("Записаться", ON_TEST_TIME),
            ("Назад", self.BACK),
            ("Завершить", self.FINISH)
        ]
        
        btns = self._build_btns(2, to_btns)
        
        self.register_store[update.callback_query.from_user.id] = dict()

        #* name + id 
        appeal_to = update.callback_query.from_user.first_name
        self.register_store[update.callback_query.from_user.id]["id"] = update.callback_query.from_user.id
        self.register_store[update.callback_query.from_user.id]["name"] = appeal_to

        
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Вас интересует определенный вид массажа?\n",
            reply_markup=btns
            
        )
    
        return self.TO_REGISTER_INQUIRY

    async def register_medical_complaints(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        # self.register_store[update.message.from_user.id]["complaints"] = update.message.text

        await update.callback_query.edit_message_text(
            "Опишите свои жалобы и беспокойства, пожалуйста 📝",
        )
        return self.TO_REGISTER_INQUIRY
    
    async def register_massage(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        print("called")
        massages = self.text_data.get("massages").get("services")
        emoji = self.text_data.get("numerical_emoji")
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
        return self.TO_REGISTER_INQUIRY
    
    async def register_inquiry_time(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        message = update.message.text
        order = self._validate_order(message)
        
        if not order:
            await update.message.reply_text(
                "К сожалению, совпадений по услугам не найдено.\n"
                + "Попробуйте еще раз"
            )
            
            return self.TO_REGISTER_INQUIRY
        
        
        self.register_store[update.message.from_user.id]["order"] = order

        
        await update.message.reply_text(
            "Какое время сеанса для Вас наиболее предпочтительно?",
            reply_markup=ReplyKeyboardMarkup(
                self.TIME_GRID,
                one_time_keyboard = True,
            )
        )
        return self.TO_REGISTER_INQUIRY

    async def register_inquiry_phone(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        
        self.register_store[update.message.from_user.id]["time"] = update.message.text

        res = self.clients.get_by_tgid(update.message.from_user.id)
    
        if not res.phone_number:
            phone_btn = KeyboardButton(
                "Нажмите сюда, чтобы отправить телефонный номер",
                request_contact=True
                
            )
            await update.message.reply_text(
                "☎ Пожалуйста, подтвердите отправку Ваших контактных данных",
                reply_markup=ReplyKeyboardMarkup(
                    [[phone_btn]], 
                    one_time_keyboard = True
                )
            )
            return self.TO_REGISTER_INQUIRY
        
        self.register_store[update.message.from_user.id]["phone_number"] = "\\" + res.phone_number
        self.register_store[update.message.from_user.id]["approved"] = False 
        
        await self.register_to_master(
            update,
            context,    
            **self.register_store[update.message.from_user.id]
        )

        # self.register_store[update.message.from_user.id].clear()
        await update.message.reply_text(
            "Спасибо 🙏\n"
            + "Ваше обращение зарегистрировано\n"
            + "⏰ Ожидайте звонка для подтверждения записи\n"
            + "Для вызова главного меню отправьте /start",
            reply_markup=ReplyKeyboardRemove()
        )

        return self.END

        

    async def register_inquiry_finish(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            phone_number = self._number_correction(update.message.contact.phone_number)
        except AttributeError:
            phone_number = self._number_correction(update.message.text)
            
        print(phone_number)
        res = self.clients.update(
            update.message.from_user.id, 
            {
                "phone_number": phone_number[1:]
            }
        )

        if not res:
            self.logger.error(
                f"Update operation of client <{update.message.from_user.id}> has failed."
                + f"Phone number {phone_number} was not added to DB"
            )
        else:
            self.logger.info(
                f"Update operation of client <{update.message.from_user.id}> success."
                + f"Phone number {phone_number} has been added to DB"
            )
        self.register_store[update.message.from_user.id]["phone_number"] = phone_number
        self.register_store[update.message.from_user.id]["approved"] = False 

        print(self.register_store)
        await self.register_to_master(
            update,
            context,    
            **self.register_store[update.message.from_user.id]
        )

        await update.message.reply_text(
            "Спасибо 🙏\n"
            + "Ваше обращение зарегистрировано\n"
            + "⏰ Ожидайте звонка для подтверждения записи\n"
            + "Для вызова главного меню отправьте /start",
            reply_markup=ReplyKeyboardRemove()
        )
        
        return self.END

    def _number_correction(
        self,
        string
    ):
        if string.startswith("7"):
            string = "\+" + string
        elif string.startswith("+"):
            string = "\+" + string[1:]
        elif string.startswith("8"):
            string = "\+7" + string[1:]
        elif string.startswith("9"):
            string = "\+7" + string
        
        return string

    def _validate_order(
        self,
        message
    ):
        #* drop spaces
        message = message.strip()
        #* separation of text / int data
        try:
            int(message)
            massage = self.text_data.get("massages")\
                .get("mapping")\
                .get(message)
            promo = self.text_data.get("promotions")\
                .get("mapping")\
                .get(message)
            
            if massage:
                return massage
            elif promo:
                return promo
            else:
                return False

        except AttributeError:

            return message