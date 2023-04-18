#!/usr/bin/python3

import configparser
from aiogram import Bot, Dispatcher, types
import random
import time
import asyncio

config = configparser.ConfigParser()
config.read('config.ini')
bot_id = int(config['CORE']['bot_id'])
admin_id = int(config['CORE']['admin_id'])
bot = Bot(token=config['CORE']['TOKEN'], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
help_message = """
ну че здарова))
Я умею в эти команды:
/help
/start
/leave чтобы я ливнул из чата
/promote чтобы повысить кого-то (кинь в ответ на сообщение челика)
/readonly X чтобы кинуть кого-то в ридонли на X минут (тоже в ответ на сообщение челика) 
/chatstat сколько человек и сколько админов
/viber )))))
/decepticon >:)
"""


async def check_if_admin(cur_bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        chat_member = await cur_bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ["creator", "administrator"] or user_id == admin_id
    except Exception as e:
        print("Exception in check_if_admin:")
        print("-" * 10 + '\n' + str(e) + '\n' + "-" * 10)


@dp.message_handler(commands=['help'])
async def proc_help(message):
    await message.reply(help_message)


@dp.message_handler(commands=['decepticon'])
async def proc_decepticon(message):
    total = int(config['DECEPTICONS']['total'])
    if total == 0:
        await message.reply("кажется короче автоботы победили ибо деспетиконов я чет не припомню((( ес чо я тож мертв")
        return
    decepticon_id = random.randint(1, total)
    decepticon_photo = open(config['DECEPTICONS'][f'd{decepticon_id}p'], 'rb')
    await message.reply(config['DECEPTICONS'][f'd{decepticon_id}'])
    await bot.send_photo(message.chat.id, decepticon_photo)
    decepticon_photo.close()


@dp.message_handler(commands=['viber'])
async def proc_viber(message):
    if random.randint(1, 2) == 1:
        viber_mp4 = open('resources/viber_drip_car.mp4', 'rb')
    else:
        viber_mp4 = open('resources/viber.gif', 'rb')  # так задумано, чтобы гифка вечно грузилась
    await bot.send_video(message.chat.id, viber_mp4)
    viber_mp4.close()


@dp.message_handler(commands=['start'])
async def proc_start(message):
    await message.reply(
        "оооой ну тут у нас какой-то умный дофига челик главнокомандующий блин да?? сразу старт приказывать нет бы "
        "хелп попросить ну-ка иди выйди и зайди нормально")


@dp.message_handler(commands=['leave'])
async def proc_leave(message):
    if await check_if_admin(bot, message):
        await message.reply("ну лан всё я пошел давайте88 и не думайте тут что придет какой-то автобот на белом коне")
        await bot.leave_chat(message.chat.id)
    else:
        await message.reply("лол ты мне тут не мегатрон чтобы так командовать))")


@dp.message_handler(commands=['promote', 'readonly'])
async def proc_promote(message):
    if await check_if_admin(bot, message):
        orig_message = message.reply_to_message
        if orig_message is not None:
            try:
                if message.text.startswith('/promote'):
                    success = await bot.promote_chat_member(message.chat.id, orig_message.from_user.id,
                                                            can_manage_chat=True, can_delete_messages=True,
                                                            can_manage_video_chats=True, can_restrict_members=True,
                                                            can_promote_members=True, can_change_info=True,
                                                            can_invite_users=True, can_pin_messages=True)
                    await bot.set_chat_administrator_custom_title(message.chat.id, orig_message.from_user.id,
                                                                  "админ via шишбот")
                    if success:
                        await message.reply(f"лвл ап для @{orig_message.from_user.username}")
                    else:
                        await message.reply(f"не получилось сделать лвл ап для @{orig_message.from_user.username}")
                else:
                    durations = [int(m) for m in message.text.split() if m.isdigit()]
                    if len(durations) != 1:
                        await message.reply(
                            f"ну как бы надо написать ровно одно число – количество минут на которое надо "
                            f"забанить")
                    else:
                        deadline = time.time() + durations[0] * 60
                        deadline = int(deadline)
                        try:
                            await bot.restrict_chat_member(message.chat.id, orig_message.from_user.id,
                                                           can_send_messages=False, until_date=deadline)
                            await message.reply(
                                f"лвл даун и мут для @{orig_message.from_user.username} на {durations[0]} минут))")
                        except Exception as e:
                            await message.reply(f"чет я нарвался конечно боюсь такого мутить((")
            except Exception as e:
                print("-" * 10 + '\n' + str(e) + '\n' + "-" * 10)
                await message.reply("чет не вышло мб я не админ тупо хз")
        else:
            await message.reply("ты вобщето не кинул реплай дудень я отказываюсь работать в таких условиях")
    else:
        await message.reply("лол ты мне тут не мегатрон чтобы так командовать))")


@dp.message_handler(commands=['chatstat'])
async def proc_chatstat(message):
    total = await bot.get_chat_member_count(message.chat.id)
    admins = await bot.get_chat_administrators(message.chat.id)
    await message.reply(
        f"в этом чатике очень мало ({total}) челов и число мегачелов как-то не оч: {len(admins)}\nвот другое дело у "
        f"нас на Кибертроне")


@dp.message_handler(content_types=["new_chat_members"])
async def proc_new_member(message):
    for user in message.new_chat_members:
        print(f"Joined: {user.id}, bot_id: {bot_id}")
        if user.id == bot_id:
            await bot.send_message(message.chat.id, "ух здарова челики")
        elif user.is_bot:
            await bot.send_message(message.chat.id,
                                   f"о привет соплеменник {user.first_name} теперь признавайся автобот или деспетикон??")
        else:
            if random.randint(0, 2) == 2:
                await bot.send_message(message.chat.id, f"лол @{user.username} тебе в вайбере пишет дима билан")
                bilan_quiz = open('resources/bilan.png', 'rb')
                await bot.send_photo(message.chat.id, bilan_quiz)
                bilan_quiz.close()
            else:
                total = int(config['QUESTIONS']['total'])
                if total > 0:
                    qnum = random.randint(1, total)
                    await bot.send_message(message.chat.id,
                                           f"и все-таки @{user.username} ответь: {config['QUESTIONS'][f'q{qnum}']}")


@dp.message_handler(commands=['ban', 'unban'])
async def proc_ban(message):
    if await check_if_admin(bot, message):
        orig_message = message.reply_to_message
        if orig_message is not None:
            try:
                if message.text.startswith('/unban'):
                    res = bot.unban_chat_member(message.chat.id, orig_message.from_user.id, only_if_banned=True)
                    await message.reply(
                        f"разбан для @{orig_message.from_user.username} произойдет сейчас с вероятностью {float(res)}")
                else:
                    durations = [int(m) for m in message.text.split() if m.isdigit()]
                    if len(durations) != 1:
                        await message.reply(
                            f"ну как бы надо написать ровно одно число – количество дней на которое надо забанить")
                    else:
                        deadline = time.time() + durations[0] * 86400
                        deadline = int(deadline)
                        try:
                            await bot.ban_chat_member(message.chat.id, orig_message.from_user.id, until_date=deadline)
                            if durations[0] > 366:
                                await message.reply(f"БАН для @{orig_message.from_user.username} на целые ЭПОХИ")
                            else:
                                await message.reply(
                                    f"БАН для @{orig_message.from_user.username} на {durations[0]} дней))")
                        except Exception as e:
                            await message.reply(f"чет я нарвался конечно боюсь такого мутить((")
            except Exception as e:
                print("Exception in proc_ban:")
                print("-" * 10 + '\n' + str(e) + '\n' + "-" * 10)
                await message.reply("чет не вышло мб я не админ тупо хз")
        else:
            await message.reply("ты вобщето не кинул реплай дудень я отказываюсь работать в таких условиях")
    else:
        await message.reply("лол ты мне тут не мегатрон чтобы так командовать))")


@dp.message_handler(content_types='text')
async def echo_all(message):
    random_value = random.randint(1, 500)

    if random_value == 500:
        await message.reply("ну ты лол вообще))))))))) за словами бы лучше следил")
    elif random_value == 499:
        await message.reply("базар братанчик дело говоришь")


@dp.message_handler(content_types='photo')
async def echo_photos(message):
    random_value = random.randint(1, 100)
    if random_value == 100:
        await message.reply("да уж фоточки у тебя не оч)0)((9")
    elif random_value == 99:
        await message.reply("ляя кефтеме какие бархатные фотки ай")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
