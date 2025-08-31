# Author: @dare_devil_ex

import json
from telebot import TeleBot as tb, types

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

token = config["token"]
_chatID = config["id"]       # Not directly used
_from = config["admin"]      # Admin to receive content IDs

bot = tb(token)

# Supported content types
SUPPORTED_TYPES = [
    'photo', 'video', 'voice', 'audio', 'document',
    'location', 'contact', 'animation', 'video_note',
    'venue', 'sticker'
]

# Store user -> selected content_type
user_states = {}

class Wkaie:
    @bot.message_handler(commands=['start'])
    def send_welcome(msg):
        bot.reply_to(msg, f"welcome to my place {msg.chat.first_name}")
        
    # Enc and Store
    @bot.message_handler(commands=['store'])
    def handle_send(msg):
        markup = types.InlineKeyboardMarkup()
        for ctype in SUPPORTED_TYPES:
            markup.add(types.InlineKeyboardButton(text=ctype, callback_data=f"select_{ctype}"))
        bot.send_message(msg.chat.id, "Select file type to store", reply_markup=markup)
        
    @bot.message_handler(commands=['store'])
    def handle_send(msg):
        markup = types.InlineKeyboardMarkup()
        for ctype in SUPPORTED_TYPES:
            markup.add(types.InlineKeyboardButton(text=ctype, callback_data=f"select_{ctype}"))
        bot.send_message(msg.chat.id, "Select file type to store", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
    def handle_callback(call):
        ctype = call.data.replace("select_", "")
        user_states[call.from_user.id] = ctype
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"Now send a {ctype}")
        

    @bot.message_handler(content_types=SUPPORTED_TYPES)
    def handle_content(msg):
        user_id = msg.from_user.id

        if user_id not in user_states:
            return

        selected_type = user_states[user_id]

        if msg.content_type != selected_type:
            bot.send_message(msg.chat.id, f"Expected a {selected_type}, but got {msg.content_type}. Try again.")
            return

        file_info = Wkaie.extract_content_id(msg)

        sender = msg.from_user.username or msg.from_user.first_name
        bot.send_message(_from, f"{msg.content_type} from @{sender}:\n`{file_info}`", parse_mode="Markdown")

        bot.send_message(msg.chat.id, f"Here’s your {msg.content_type} ID:\n`{file_info}`", parse_mode="Markdown")

        user_states.pop(user_id)

    def extract_content_id(msg):
        if msg.content_type == 'photo':
            return msg.photo[-1].file_id
        elif msg.content_type == 'video':
            return msg.video.file_id
        elif msg.content_type == 'voice':
            return msg.voice.file_id
        elif msg.content_type == 'audio':
            return msg.audio.file_id
        elif msg.content_type == 'document':
            return msg.document.file_id
        elif msg.content_type == 'animation':
            return msg.animation.file_id
        elif msg.content_type == 'video_note':
            return msg.video_note.file_id
        elif msg.content_type == 'sticker':
            return msg.sticker.file_id
        elif msg.content_type == 'location':
            return f"{msg.location.latitude}, {msg.location.longitude}"
        elif msg.content_type == 'contact':
            return f"{msg.contact.first_name} ({msg.contact.phone_number})"
        elif msg.content_type == 'venue':
            return f"{msg.venue.title}, {msg.venue.address}"
        else:
            return "Unknown content"

    def wkaie():
        print(bot.get_me().first_name, "is ONLINE")
        bot.infinity_polling()


if __name__ == "__main__":
    Wkaie.wkaie()
