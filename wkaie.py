# Author: @dare_devil_ex

import json
from telebot import TeleBot as tb

with open("config.json", "r") as f:
    config = json.load(f)
token = config["token"]
_chatID = config["id"]
_from = config["admin"]
bot = tb(token)

class Wkaie:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, f"welcome to place {message.chat}")
        
    @bot.message_handler(content_types=[
        'text', 'photo', 'video', 'voice', 'audio', 'document',
        'location', 'contact', 'animation', 'video_note',
        'venue', 'poll', 'dice', 'sticker'
    ])
    def forward_all(msg):
        print(f"Received: {msg.content_type}")
        try:
            if msg.content_type == 'document':
                bot.send_message(_from, f"{msg.document.file_id}")
            elif msg.content_type == 'photo':
        
                file_id = msg.photo[-1].file_id
                bot.send_message(_from, f"Photo ID: {file_id}")

            elif msg.content_type == 'video':
                bot.send_message(_from, f"Video ID: {msg.video.file_id}")

            elif msg.content_type == 'voice':
                bot.send_message(_from, f"Voice ID: {msg.voice.file_id}")

            elif msg.content_type == 'audio':
                bot.send_message(_from, f"Audio ID: {msg.audio.file_id}")

            elif msg.content_type == 'animation':
                bot.send_message(_from, f"Animation ID: {msg.animation.file_id}")

            elif msg.content_type == 'video_note':
                bot.send_message(_from, f"Video Note ID: {msg.video_note.file_id}")

            elif msg.content_type == 'sticker':
                bot.send_message(_from, f"Sticker ID: {msg.sticker.file_id}")

            elif msg.content_type == 'location':
                bot.send_message(_from, f"Location: {msg.location.latitude}, {msg.location.longitude}")

            elif msg.content_type == 'contact':
                bot.send_message(_from, f"Contact: {msg.contact.first_name} {msg.contact.phone_number}")

            elif msg.content_type == 'venue':
                bot.send_message(_from, f"Venue: {msg.venue.title}, Address: {msg.venue.address}")
                
            else:
                bot.forward_message(_from, msg.chat.id, msg.message_id)
                bot.forward_message(_from, _chatID, msg.message_id)
        except Exception as e:
            print("Error forwarding:", e)
    
    def wkaie():
        print(bot.get_my_name().name, "is ONLINE")
        bot.infinity_polling()


if __name__=="__main__":
    Wkaie.wkaie()