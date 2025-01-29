from pyrogram import Client, filters
import requests
import config
import re

SPOILER = config.SPOILER_MODE
slangf = 'slang_words.txt'

with open(slangf, 'r') as f:
    slang_words = set(line.strip().lower() for line in f)

Bot = Client(
    "antinude",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# NSFW check function
def check_nsfw_image(image_url):
    url = "https://nsfw3.p.rapidapi.com/v1/results"
    payload = {
        "url": image_url,
        "strictness": "1.0"
    }
    headers = {
        "x-rapidapi-key": "68ac1982e7msha9d496d4e35ffe3p15e79ajsn130cc87e6bb9",
        "x-rapidapi-host": "nsfw3.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        nsfw = data.get("data", {}).get("is_nsfw", False)
        return nsfw
    else:
        print(f"Error with API request: {response.status_code}")
        return False

# Handler for image messages
@Bot.on_message(filters.group & filters.photo)
async def image(bot, message):
    sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges
    if not isadmin:
        # Get the file ID and file path using the Telegram API
        file_info = await bot.get_file(message.photo.file_id)
        
        # Generate a publicly accessible URL
        image_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_info.file_path}"
        
        # Call the NSFW check function with the Telegram image URL
        nsfw = check_nsfw_image(image_url)

        if nsfw:
            name = message.from_user.first_name
            await message.delete()
            if SPOILER:
                await message.reply_photo(image_url, caption=f"""**ᴡᴀʀɴɪɴɢ ⚠️** (nude photo)
                **{name}** ꜱᴇɴᴛ ᴀ ɴᴜᴅᴇ/ɴꜱꜰᴡ ᴘʜᴏᴛᴏ""", has_spoiler=True)

# Slang detection handler
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
            msgtxt = f"""{name} ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ᴅᴜᴇ ᴛᴏ ᴛʜᴇ ᴘʀᴇꜱᴇɴᴄᴇ ᴏꜰ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ[ɢᴀᴀʟɪ/ꜱʟᴀɴɢꜰᴜʟ ᴡᴏʀᴅꜱ]. ʜᴇʀᴇ ɪꜱ ᴀ ᴄᴇɴꜱᴏʀᴇᴅ ᴠᴇʀꜱɪᴏɴ ᴏꜰ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ:
                
{sentence}
            """
            if SPOILER:
                await message.reply(msgtxt)

Bot.run()