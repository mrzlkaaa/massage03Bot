from os import terminal_size
from . import *
from .base import Base

__all__ = ["Description"]

#* massages


class Description(Base):
    (
        EXPERIENCE,
        CERTIFICATES,
        SHVZ,
        ANTICEL,
        MIOPHAS,
        PROPHYLACTIC,
        MERIDIAN,
        MEDICAL,
        CLASSIC,
        SPORT,
        TAI,
        HONEY,
        EXPRESS,
        ABOUT_DESC, 
        MASSAGES_DESC, 
        *_
    ) = list(map(lambda x: str(x), range(100, 149)))

    async def about(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        to_btns = [
            ("Опыт работы", self.EXPERIENCE),
            ("Сертификаты", self.CERTIFICATES),
            ("Назад", self.BACK),
            ("Завершить", self.FINISH)
        ]
        
        btns = self._build_btns(2, to_btns)
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="BLABLABLA", reply_markup=btns)
        
        return self.ABOUT_DESC
    
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
    
    #! turns to error 
    async def massages(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        consts = [
            self.SHVZ, self.ANTICEL,
            self.SPORT, self.CLASSIC,
            self.PROPHYLACTIC,
            self.TAI, self.HONEY,
            self.BACK, self.FINISH
        ]
        
        lst = [
            *self.text_data.get("massages").get("list"),
            "Назад", "Завершить"
        ]

        to_btns = list(zip(lst, consts))
        btns = self._build_btns(2, to_btns)
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=\
            "Пожалуйста, ознакомьтесь с перечнем видов массажа", 
            reply_markup=btns)

        return self.MASSAGES_DESC

    async def massage_desc(
        self,
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        
        await update.callback_query.answer()
        massage_id = update.callback_query.data
        to_btns = [
            ("Назад", self.BACK),
            ("Завершить", self.FINISH)
        ]
        btns = self._build_btns(2, to_btns)

        print(update.callback_query.from_user)
        await update.callback_query.edit_message_text(
            text="Массаж шейно-воротниковой зоны - это процедура, направленная на улучшение кровообращения, расслабление мышц и устранение напряжения в области шеи и верхней части спины. Массажист применяет различные техники, такие как разминание, растяжение и давление, чтобы снять накопившееся напряжение и спазмы. Этот вид массажа особенно эффективен для тех, кто страдает от болей в шее, головных болей, ограниченности движений или сидячего образа жизни. Комбинирование массажа шейно-воротниковой зоны с другими методами релаксации, такими как ароматерапия, может усилить его положительное действие на организм. В результате процедуры, клиент чувствует снятие напряжения, улучшение подвижности шейных позвонков и общее ощущение расслабления."
        )