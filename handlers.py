# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ContextTypes
# from data import df

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     keyboard = [
#         [InlineKeyboardButton(dish, callback_data=dish) for dish in df['Dish']]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('Please choose a dish:', reply_markup=reply_markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()
#     selected_dish = query.data
#     ingredients = df.loc[df['Dish'] == selected_dish, 'Ingredients'].values[0]
#     context.user_data['selected_dishes'] = context.user_data.get('selected_dishes', []) + [selected_dish]
#     context.user_data['shopping_list'] = context.user_data.get('shopping_list', []) + ingredients
#     await query.edit_message_text(text=f"Selected dish: {selected_dish}\nIngredients: {', '.join(ingredients)}\n\nType /done when you are finished selecting dishes.")

# async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     shopping_list = context.user_data.get('shopping_list', [])
#     if shopping_list:
#         unique_ingredients = list(set(shopping_list))
#         await update.message.reply_text(f"Your shopping list:\n\n{', '.join(unique_ingredients)}")
#     else:
#         await update.message.reply_text("You haven't selected any dishes.")









from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data import df
import os
from PIL import Image
import io

# Функция для изменения размера изображения
def resize_image(image_path, size=(100, 100)):
    img = Image.open(image_path)
    img = img.resize(size, Image.LANCZOS)
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return byte_arr

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = []
    media_group = []

    for index, row in df.iterrows():
        dish = row['Dish']
        image_path = row['Image']

        if os.path.exists(image_path):
            resized_image = resize_image(image_path)
            
            # Добавляем изображение и кнопку в список
            buttons.append(InlineKeyboardButton(f'Select {dish}', callback_data=dish))
            media_group.append((resized_image, dish))

            # Отправляем сообщения по 3 изображения в ряд
            if len(media_group) == 3 or index == len(df) - 1:
                for img, caption in media_group:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=caption)
                media_group = []

                keyboard = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text('Please choose a dish:', reply_markup=reply_markup)
                buttons = []

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_dish = query.data
    ingredients = df.loc[df['Dish'] == selected_dish, 'Ingredients'].values[0]
    context.user_data['selected_dishes'] = context.user_data.get('selected_dishes', []) + [selected_dish]
    context.user_data['shopping_list'] = context.user_data.get('shopping_list', []) + ingredients
    await query.edit_message_text(text=f"Selected dish: {selected_dish}\nIngredients: {', '.join(ingredients)}\n\nType /done when you are finished selecting dishes.")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shopping_list = context.user_data.get('shopping_list', [])
    if shopping_list:
        unique_ingredients = list(set(shopping_list))
        await update.message.reply_text(f"Your shopping list:\n\n{', '.join(unique_ingredients)}")
    else:
        await update.message.reply_text("You haven't selected any dishes.")
