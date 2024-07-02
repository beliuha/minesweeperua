from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Залишити повідомлення")]], 
        resize_keyboard=True, input_field_placeholder='Оберіть пункт меню', one_time_keyboard=True
)

geo_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ні, я не хочу', callback_data='geo-')]
    ]
)

p_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ні, я не хочу', callback_data='p-')]
    ]
)