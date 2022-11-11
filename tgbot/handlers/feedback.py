from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot import config
from tgbot.keyboards.reply import cancel_button
from tgbot.misc.states import Stages


async def feedback_command(message: Message):
    await message.answer('📝 Здесь вы можете написать свой отзыв о боте, '
                         'предложить какие-либо изменения, попросить о помощи или '
                         'сообщить об ошибках. Разработчики обязательно заметят ваше сообщение.\n\n'
                         '<i>Гадости тоже можете написать)</i>', reply_markup=cancel_button)
    await Stages.feedback.set()


def register_feedback_command(dp: Dispatcher):
    dp.register_message_handler(feedback_command, Command('feedback'))


async def send_report(message: Message, state: FSMContext):
    admins = message.bot.get('config').tg_bot.admin_ids
    main_admin = admins[0]

    username = message.from_user.username
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    report = message.text
    await message.bot.send_message(chat_id=main_admin,
                                   text=f'Пользователь {username} отправил фидбек!\n\n'
                                        f'ID: {user_id}\n'
                                        f'Полное имя: {full_name}\n\n'
                                        f'Текст сообщения:\n\n'
                                        f'<i>{report}</i>')

    await message.answer('🫶 Спасибо за обратную связь!')

    await state.reset_state(with_data=False)


def register_send_report(dp: Dispatcher):
    dp.register_message_handler(send_report, state=Stages.feedback)


def register_all_feedback(dp):
    register_feedback_command(dp)
    register_send_report(dp)
