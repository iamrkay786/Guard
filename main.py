from pyrogram import Client, filters
import requests
import re
import config

url = "https://nsfw3.p.rapidapi.com/v1/results"
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

#-----------------------------------------------------------------

@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply("""ʜɪ ᴛʜᴇʀᴇ! ɪ'ᴍ ᴛʜᴇ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ ɢᴜᴀʀᴅɪᴀɴ ʙᴏᴛ. ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ᴀɴᴅ ꜱᴀꜰᴇ ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ. ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴍᴀɪɴ ꜰᴇᴀᴛᴜʀᴇꜱ ɪ ᴏꜰꜰᴇʀꜱ::
• **ɪᴍᴀɢᴇ ꜰɪʟᴛᴇʀɪɴɢ:** ɪ ᴄᴀɴ ᴀʟꜱᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ᴘᴏʀɴᴏɢʀᴀᴘʜɪᴄ ᴏʀ ɴꜱꜰᴡ ɪᴍᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ
• **ᴡᴏʀᴅ ꜱʟᴀɴɢɪɴɢ:** ɪ ᴄᴀɴ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ [ɢᴀᴀʟɪ-ꜱʟᴀɴɢꜰᴜʟ] ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ. 
ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ, ꜱɪᴍᴘʟʏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ-ᴄʜᴀᴛꜱ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴜꜱɪɴɢ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ-ɢᴜᴀʀᴅɪᴀɴ! ʟᴇᴛ'ꜱ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜱᴀꜰᴇ ᴀɴᴅ ʀᴇꜱᴘᴇᴄᴛꜰᴜʟ. ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Heavenwaala/@BillaSpace""")

#-----------------------------------------------------------------

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

    # Send the POST request
    response = requests.post(url, data=payload, headers=headers)
    
    # Handle the response
    if response.status_code == 200:
        data = response.json()
        nsfw = data.get("data", {}).get("is_nsfw", False)
        return nsfw
    else:
        print("Error with API request:", response.status_code)
        return False

#-----------------------------------------------------------------

@Bot.on_message(filters.group & filters.photo)
async def image(bot, message):
    sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges
    if not isadmin:
        # Download the image
        x = await message.download()
        
        # You can either upload the image to a server or use the Telegram file URL
        image_url = "https://storage.googleapis.com/api4ai-static/samples/nsfw-1.jpg"  # Replace this with the actual image URL if needed
        
        # Call the NSFW check function
        nsfw = check_nsfw_image(image_url)

        if nsfw:
            name = message.from_user.first_name
            await message.delete()
            if SPOILER:
                await message.reply_photo(x, caption=f"""**ᴡᴀʀɴɪɴɢ ⚠️** (nude photo)
                **{name}** ꜱᴇɴᴛ ᴀ ɴᴜᴅᴇ/ɴꜱꜰᴡ ᴘʜᴏᴛᴏ""", has_spoiler=True)

#-----------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------

Bot.run()