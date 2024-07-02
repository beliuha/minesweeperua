# Загальний імпорт
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
import asyncio

# Імпорт з app
from app.keyboard import main as kb, geo_kb as geo, p_kb # Клавіатура
from app.google_sheet import sheet # Гугл таблиці
from app.crypto import Crypto # Шифрування
from app.fsm import Feedback # Машина станів

# Налаштування Роутера
router = Router()

# Налаштування шифрування
crypto = Crypto()

# Обробник команди /start
@router.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привіт! Надішліть вашу заявку.", reply_markup=kb)

# Обробник команди 'залишити повідомлення'
@router.message(F.text == 'Залишити повідомлення')
async def feedback_one(message: Message, state: FSMContext):
    photo = []
    await state.set_state(Feedback.location)
    await message.answer('Поділіться з нами геолокацією об\'єкта', reply_markup=geo)

@router.callback_query(Feedback.location, F.data == 'geo-')
async def no_geo(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(location='0.0, 0.0')
    await state.set_state(Feedback.photo)
    await callback.message.answer('Поділіться з нами фото об\'єкта', reply_markup=p_kb)

@router.message(Feedback.location, F.location)
async def get_geo(message: Message, state: FSMContext):
    await state.update_data(location=f'{message.location.latitude}, {message.location.longitude}')
    await state.set_state(Feedback.photo)
    await message.answer('Поділіться з нами фото об\'єкта', reply_markup=p_kb)

@router.callback_query(Feedback.photo, F.data == 'p-')
async def no_photo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(photo='None')
    await state.set_state(Feedback.text)
    await callback.answer()
    await callback.message.answer('Опишіть ситуацію')

@router.message(Feedback.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    # Отримуємо поточні дані стану
    data = await state.get_data()

    # Оновлюємо строку фото
    if 'photo' in data:
        # Додаємо новий file_id до існуючої строки, розділеної комами
        data['photo'] = data['photo'] + ', ' + message.photo[-1].file_id
    else:
        # Ініціалізація ключа 'photo' з першим file_id
        data['photo'] = message.photo[-1].file_id

    # Зберігаємо оновлені дані
    await state.update_data(photo=data['photo'])
    
    # Встановлюємо новий стан, якщо це перше фото
    if await state.get_state() == Feedback.photo:
        await state.set_state(Feedback.text)
        await message.answer('Опишіть ситуацію')

@router.message(Feedback.text, F.text)
async def get_text(message: Message, state: FSMContext):
    await message.answer('Триває обробка...')
    await state.update_data(
        username = message.from_user.username,
        time = datetime.today().strftime('%d.%m.%Y %H:%M:%S'),
        text = message.text
    )

    # Підготовка до шифрування
    data = await state.get_data()
    unencrypted_list = [data['username'], data['time'], data['photo'], data['location'], data['text']]
    print(unencrypted_list)
    encrypted_list = []

    # Шифрування
    await crypto.check_password()
    for o in unencrypted_list:
        if isinstance(o, list):
            new_o = [await crypto.encrypt(str(i)) for i in o]
        else:
            new_o = await crypto.encrypt(o)
        
        encrypted_list.append(new_o)

    # Асинхронне збереження заявки в Google Таблицю
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sheet.sheet1.append_row, [i for i in encrypted_list])

    await state.clear()
    await message.answer("Ваша заявка прийнята!")

# Клавіатура при введенні будь-якої інфи
@router.message(F.text)
async def triger_start(message: Message, state: FSMContext):
    if await state.get_state() == None:
        await message.answer('Залишіть вашу заявку', reply_markup=kb)
