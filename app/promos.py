from . import *
from .base import Base

# class Promos(Base):

#     PROMOTIONS_INQUIRY = 201

#     async def promotions(
#         self,
#         update: Update, 
#         context: ContextTypes.DEFAULT_TYPE
#     ) -> None:

#         to_btns = [
#             ("Назад", self.BACK),
#             ("Завершить", self.FINISH)
#         ]

#         btns = self._build_btns(1, to_btns)

#         self.register_store[update.callback_query.from_user.id] = dict()
         
#         appeal_to = update.callback_query.from_user.first_name
#         self.register_store[update.callback_query.from_user.id]["name"] = appeal_to
        
#         promotions_list = self.text_data.get("promotions").get("promotions_list")
#         promotions_desc = self.text_data.get("promotions").get("promotions_desc")
#         promotions = ""
#         for i in range(len(promotions_list)):
#             promotions += promotions_list[i] + "\n".join(promotions_desc[i])
        
#         # print(promotions)
#         await update.callback_query.edit_message_text(
#             "В настоящее время Вы можете воспользоваться следующими акциями:\n\n"
#             + promotions,
#             reply_markup=btns
#         )
#         return self.TO_REGISTER