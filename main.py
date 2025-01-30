from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import config
import re
import os

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

# NSFW check function using aiohttp (asynchronous)
async def check_nsfw_image(image_url):
    url = "https://nsfw3.p.rapidapi.com/v1/results"
    payload = {
        "url": image_url,
        "strictness": "1.0"
    }
    headers = {
        "x-rapidapi-key": config.NSFW_API_KEY,  # Use the API key from config
        "x-rapidapi-host": "nsfw3.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Asynchronous HTTP request using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            # Handle the response
            if response.status == 200:
                data = await response.json()  # Async way to get JSON response
                nsfw = data.get("data", {}).get("is_nsfw", False)
                return nsfw
            else:
                print(f"Eʀʀᴏʀ Wɪᴛʜ Aᴘɪ ʀᴇǫᴜᴇsᴛ: {response.status}")
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

# Image processing function
@Bot.on_message(filters.group & filters.photo)
async def image(bot: Client, message: Message):
    sender = await bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges is not None  # Correct admin check

    if not isadmin:
        try:
            # Directly access the photo object (PhotoSize)
            photo = message.photo
            print(f"Downloading image with file ID: {photo.file_id}")

            # Get the file information
            file_info = await bot.get_file(photo.file_id)
            if file_info.file_path:
                file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_info.file_path}"

                # Check if the image is NSFW
                print(f"Checking NSFW for image: {file_url}")  # Debugging
                nsfw = await check_nsfw_image(file_url)

                if nsfw:
                    name = message.from_user.first_name
                    await message.delete()

                    if config.SPOILER:  # Ensure SPOILER flag is defined in config
                        await message.reply_photo(
                            file_url,
                            caption=f"""**⚠️ Warning** (NSFW ᴅᴇᴛᴇᴄᴛᴇᴅ)
**{name}** Sᴇɴᴛ A Nᴜᴅᴇ/NSFW Pʜᴏᴛᴏ""",
                            has_spoiler=True
                        )

        except Exception as e:
            print(f"Eʀʀᴏʀ ᴘʀᴏᴄᴇssɪɴɢ ɪᴍᴀɢᴇ: {e}")  # Debugging


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
            msgtxt = f"""{name} ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ᴅᴜᴇ ᴛᴏ ᴛʜᴇ ᴘʀᴇꜱᴇɴᴄᴇ ᴏꜰ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ[ɢᴀᴀʟɪ/ꜱʟᴀɴɢꜰᴜʟ ᴡᴏʀᴅꜱ]. ʜᴇʀᴇ ɪꜱ ᴀ ᴄᴇɴꜱᴏʀᴇᴅ ᴠᴇʀꜱɪᴏɴ ᴏꜰ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ:
                
{sentence}
            """
            if SPOILER:
                await message.reply(msgtxt)

# Run the bot
Bot.run()