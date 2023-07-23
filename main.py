   



# async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends a predefined poll"""
#     questions = ["Good", "Really good", "Fantastic", "Great"]
#     message = await context.bot.send_poll(
#         update.effective_chat.id,
#         "How are you?",
#         questions,
#         is_anonymous=False,
#         allows_multiple_answers=True,
#     )

# async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Ask user to create a poll and display a preview of it"""
#     # using this without a type lets the user chooses what he wants (quiz or poll)
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="1"),
#             InlineKeyboardButton("Option 2", callback_data="2"),
#             InlineKeyboardButton("Option 3", callback_data="3")
#         ],
#         # [InlineKeyboardButton("Option 3", callback_data="3")],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)

# async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # user = update.message.from_user
    
#     # await update.message.reply_text(
#     #     "I see! Please send me a photo of yourself, "
#     #     "so I know what you look like, or send /skip if you don't want to.",
#     #     reply_markup=ReplyKeyboardRemove(),
#     # )

#     photo_file = update.message
#     await context.bot.send_photo(
#         update.effective_chat.id,
#         "media/1.jpg"
#     )


async def unknown(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Извините, не понял команду."
    )

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#     print(query)
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")


# if __name__ == '__main__':

    
    # application = ApplicationBuilder()\
    #     .token(os.getenv("TOKEN"))\
    #     .build()


    
    # application.add_handler(poll_handler)
    # application.add_handler(preview_handler)
    # application.add_handler(photo_handler)

    # application.add_handler(btn1_handler)

    # application.add_handler(unknown_handler)
    
    # application.run_polling()