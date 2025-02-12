from pyrogram import Client, filters
from pyrogram.types import Message
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import os
import re
import pymongo
import time
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import config

# Configuration for Spoiler Mode
SPOILER = config.SPOILER_MODE
slangf = 'slang_words.txt'

# Read slang words from a text file
with open(slangf, 'r') as f:
    slang_words = set(line.strip().lower() for line in f)

# Initialize the Bot with provided credentials from the config
Bot = Client(
    "antinude",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# Load the pre-trained NSFW detection model
model_name = "AdamCodd/vit-base-nsfw-detector"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# NSFW detection function
async def check_nsfw_image(image_path):
    try:
        # Open image and preprocess
        image = Image.open(image_path)
        inputs = feature_extractor(images=image, return_tensors="pt")

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=-1).item()

        return predicted_class == 1  # 1 means NSFW, 0 means safe
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

# Handler for '/start' command
@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply("""
ʜɪ ᴛʜᴇʀᴇ! ɪ'ᴍ ᴛʜᴇ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ ɢᴜᴀʀᴅɪᴀɴ ʙᴏᴛ. 
ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ᴀɴᴅ ꜱᴀꜰᴇ ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ. 
ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴍᴀɪɴ ꜰᴇᴀᴛᴜʀᴇꜱ ɪ ᴏꜰꜰᴇʀꜱ::

• **ɪᴍᴀɢᴇ ꜰɪʟᴛᴇʀɪɴɢ:** ɪ ᴄᴀɴ ᴀʟsᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ᴘᴏʀɴᴏɢʀᴀᴘʜɪᴄ ᴏʀ ɴꜱꜰᴡ ɪᴍᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ
• **ᴡᴏʀᴅ ꜱʟᴀɴɢɪɴɢ:** ɪ ᴄᴀɴ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ [ɢᴀᴀʟɪ-ꜱʟᴀɴɢꜰᴜʟ] ᴍᴇꜱsᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ. 
ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ, ꜱɪᴍᴘʟʏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ-ᴄʜᴀᴛꜱ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ , ᴛʜᴀɴᴋs ꜰᴏʀ ᴜꜱɪɴɢ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ-ɢᴜᴀʀᴅɪᴀɴ! 
ʟᴇᴛ's ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜱᴀꜰᴇ ᴀɴᴅ ʀᴇsᴇᴄᴛꜰᴜʟ. ᴘᴏᴡᴇʀᴇᴅ ʙʏ @BillaSpace/@Heavenwaala
""")

# image processing function
@Bot.on_message(filters.group & filters.photo)
async def image(bot: Client, message: Message):
    sender = await bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges is not None  # Correct admin check

    if not isadmin:
        try:
            photo = message.photo
            print(f"Downloading image with file ID: {photo.file_id}")

            # Download the image locally
            file_path = await bot.download_media(photo.file_id)
            print(f"Image downloaded to: {file_path}")

            # Check if the image is NSFW
            nsfw = await check_nsfw_image(file_path)

            if nsfw:
                name = message.from_user.first_name
                await message.delete()
                
                # Send NSFW warning message
                await message.reply(
                    f"⚠️ **Warning**: **{name}** sent an NSFW image, and it has been deleted by the Billa.",
                    quote=True
                )

                if config.SPOILER:  # Ensure SPOILER flag is defined in config
                    await message.reply_photo(
                        file_path,
                        caption=f"**⚠️ Warning** (NSFW detected)\n**{name}** sent an NSFW image.",
                        has_spoiler=True
                    )

            # Optionally, delete the file after processing
            os.remove(file_path)

        except Exception as e:
            print(f"Error processing image: {e}")  # Debugging

# Handler for text messages containing slang
@Bot.on_message(filters.group & filters.text)
async def slang(bot, message):
    sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges
    if not isadmin:
        sentence = message.text
        sent = re.sub(r'\W+', ' ', sentence)
        isslang = False
        for word in sent.split():
            if word.lower() in slang_words:
                isslang = True
                await message.delete()
                sentence = sentence.replace(word, f'||{word}||')
        
        if isslang:
            name = message.from_user.first_name
            msgtxt = f"""{name} ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ᴅᴜᴇ ᴛᴏ ᴛʜᴇ ᴘʀᴇꜱᴇɴᴄᴇ ᴏꜰ ɪɴᴀᴘᴘʀᴏꜱʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ[ɢᴀᴀʟɪ/ꜱʟᴀɴɢꜰᴜʟ ᴡᴏʀᴅꜱ]. ʜᴇʀᴇ ɪꜱ ᴀ ᴄᴇɴꜱᴏʀᴇᴅ ᴠᴇʀꜱɪᴏɴ ᴏꜰ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ:

{sentence}
            """

            if SPOILER:
                await message.reply(msgtxt)

# Run the bot
Bot.run()
