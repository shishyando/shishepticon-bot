#!/usr/bin/python3

import configparser
import telebot
import random
import time

config = configparser.ConfigParser()
config.read('config.ini')

bot = telebot.TeleBot(config['CORE']['TOKEN'], parse_mode="HTML")
bot_id = int(config['CORE']['bot_id'])
admin_id = int(config['CORE']['admin_id'])

def check_if_admin(bot, message): # я не захотел реализовывать это через кастомный фильтр потому что тогда я хз как общаться с чуваками которые не админы но просят админскую команду
	chat_id = message.chat.id
	user_id = message.from_user.id
	try:
		chat_member = bot.get_chat_member(chat_id, user_id)
		return chat_member.status in ["creator", "administrator"] or user_id == admin_id
	except Exception as e:
		print("Exception in check_if_admin:")
		print("-" * 10 + '\n' + str(e) + '\n' + "-" * 10)

@bot.message_handler(commands=['help'])
def proc_help(message):
	bot.reply_to(message, """
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
						  """)


@bot.message_handler(commands=['decepticon'])
def proc_decepticon(message):
	total = int(config['DECEPTICONS']['total'])
	if total == 0:
		bot.reply_to(message, "кажется короче автоботы победили ибо деспетиконов я чет не припомню((( ес чо я тож мертв")
		return
	decepticon_id = random.randint(1, total)
	decepticon_photo = open(config['DECEPTICONS'][f'd{decepticon_id}p'], 'rb')
	bot.reply_to(message, config['DECEPTICONS'][f'd{decepticon_id}'])
	bot.send_photo(message.chat.id, decepticon_photo)
	decepticon_photo.close()


@bot.message_handler(commands=['viber'])
def proc_viber(message):
	if random.randint(1, 2) == 1:
		viber_mp4 = open('viber drip car.mp4', 'rb')
	else:
		viber_mp4 = open('viber.gif', 'rb')
	bot.send_video(message.chat.id, viber_mp4)
	viber_mp4.close()


@bot.message_handler(commands=['start'])
def proc_start(message):
	bot.reply_to(message, "оооой ну тут у нас какой-то умный дофига челик главнокомандующий блин да?? сразу старт приказывать нет бы хелп попросить ну-ка иди выйди и зайди нормально")


@bot.message_handler(commands=['leave'])
def proc_leave(message):
	if check_if_admin(bot, message):
		bot.reply_to(message, "ну лан всё я пошел давайте88 и не думайте тут что придет какой-то автобот на белом коне")
		bot.leave_chat(message.chat.id)
	else:
		bot.reply_to(message, "лол ты мне тут не мегатрон чтобы так командовать))")


@bot.message_handler(commands=['promote', 'readonly'])
def proc_promote(message):
	if check_if_admin(bot, message):
		orig_message = message.reply_to_message
		if orig_message is not None:
			try:
				if message.text.startswith('/promote'):
					bot.promote_chat_member(message.chat.id, orig_message.from_user.id,\
															 can_manage_chat=True,\
															 can_delete_messages=True,\
															 can_manage_video_chats=True,\
															 can_restrict_members=True,\
															 can_promote_members=True,\
															 can_change_info=True,\
															 can_invite_users=True,\
															 can_pin_messages=True)
					bot.set_chat_administrator_custom_title(message.chat.id, orig_message.from_user.id, "админ via шишбот")
					bot.reply_to(message, f"лвл ап для @{orig_message.from_user.username}")
				else:
					durations = [int(m) for m in message.text.split() if m.isdigit()]
					if len(durations) != 1:
						bot.reply_to(message, f"ну как бы надо написать ровно одно число – количество минут на которое надо забанить")
					else:
						deadline = time.time() + durations[0] * 60
						try:
							bot.restrict_chat_member(message.chat.id, orig_message.from_user.id, can_send_messages=False, until_date=deadline)
							bot.reply_to(message, f"лвл даун и мут для @{orig_message.from_user.username} на {durations[0]} минут))")
						except Exception as e:
							bot.reply_to(message, f"чет я нарвался конечно боюсь такого мутить((")
			except Exception as e:
				print("-"*10 + '\n' + str(e) + '\n' + "-"*10)
				bot.reply_to(message, "чет не вышло мб я не админ тупо хз")
		else:
			bot.reply_to(message, "ты вобщето не кинул реплай дудень я отказываюсь работать в таких условиях")
	else:
		bot.reply_to(message, "лол ты мне тут не мегатрон чтобы так командовать))")


@bot.message_handler(commands=['chatstat'])
def proc_chatstat(message):
	total = bot.get_chat_member_count(message.chat.id)
	admins = bot.get_chat_administrators(message.chat.id)
	bot.reply_to(message, f"в этом чатике очень мало ({total}) челов и число мегачелов как-то не оч: {len(admins)}\nвот другое дело у нас на Кибертроне")


@bot.message_handler(content_types=["new_chat_members"])
def proc_new_member(message):
	for user in message.new_chat_members:
		print(f"Joined: {user.id}, bot_id: {bot_id}")
		if user.id == bot_id:
			bot.send_message(message.chat.id, "ух здарова челики")
		elif user.is_bot:
			bot.send_message(message.chat.id, f"о привет соплеменник {user.first_name} теперь признавайся автобот или деспетикон??")
		else:
			if random.randint(0, 2) == 2:
				bot.send_message(message.chat.id, f"лол @{user.username} тебе в вайбере пишет дима билан")
				bilan_quiz = open('bilan.png', 'rb')
				bot.send_photo(message.chat.id, bilan_quiz)
				bilan_quiz.close()
			else:
				total = int(config['QUESTIONS']['total'])
				if total > 0:
					qnum = random.randint(1, total)
					bot.send_message(message.chat.id, f"и все-таки @{user.username} ответь: {config['QUESTIONS'][f'q{qnum}']}")


@bot.message_handler(commands=['ban', 'unban'])
def proc_ban(message):
	if check_if_admin(bot, message):
		orig_message = message.reply_to_message
		if orig_message is not None:
			try:
				if message.text.startswith('/unban'):
					res = bot.unban_chat_member(message.chat.id, orig_message.from_user.id, only_if_banned=True)
					bot.reply_to(message, f"разбан для @{orig_message.from_user.username} произойдет сейчас с вероятностью {float(res)}")
				else:
					durations = [int(m) for m in message.text.split() if m.isdigit()]
					if len(durations) != 1:
						bot.reply_to(message, f"ну как бы надо написать ровно одно число – количество дней на которое надо забанить")
					else:
						deadline = time.time() + durations[0] * 86400
						try:
							bot.ban_chat_member(message.chat.id, orig_message.from_user.id, until_date=deadline)
							if durations[0] > 366:
								bot.reply_to(message, f"БАН для @{orig_message.from_user.username} на целые ЭПОХИ")
							else:
								bot.reply_to(message, f"БАН для @{orig_message.from_user.username} на {durations[0]} дней))")
						except Exception as e:
							bot.reply_to(message, f"чет я нарвался конечно боюсь такого мутить((")
			except Exception as e:
				print("Exception in proc_ban:")
				print("-"*10 + '\n' + str(e) + '\n' + "-"*10)
				bot.reply_to(message, "чет не вышло мб я не админ тупо хз")
		else:
			bot.reply_to(message, "ты вобщето не кинул реплай дудень я отказываюсь работать в таких условиях")
	else:
		bot.reply_to(message, "лол ты мне тут не мегатрон чтобы так командовать))")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	if random.randint(1, 100) == 100:
		bot.reply_to(message, "ну ты лол вообще))))))))) за словами бы лучше следил")


bot.infinity_polling()