import discord
from discord.ext import commands, tasks
import os
import random
import aiohttp
import io
from datetime import datetime
from myserver import server_on

# Intents
intents = discord.Intents.default()
intents.members = True  # ต้องเปิดใน Discord Dev Console ด้วยนะ

bot = commands.Bot(command_prefix='!', intents=intents)

chat_channel_id = 1362748298858991778
server_channel_id = 1363123342135132351

messages = [
    'มึงเข้ามาแล้วเหรอ? มาทำไม 🤨🔥',
    'มาดิไม่กลัวเลย เดี๋ยวขยี้ให้ดู 😎💥',
    'กูรออยู่, จะหนีไปไหน 🤡',
    'ไหน มึงกล้าพูดแบบนี้กับกูหรอ 😈💬',
    'มึงคิดว่ามากูจะกลัวหรอ? โทษที กูขำ 🤣',
    'มีอะไรจะบอก กูฟังอยู่ 😜👌',
    'มาดิ มาเล่นกับกูหน่อย 🔥',
    'เอ้า!! ทำไมไม่มาต่อสู้บ้าง 😤',
    'เข้ามาดิ!! 😎🔥',
    'เอาดิ ไม่กล้าเหรอ 😏',
    'มีไรก็มาดิครับ 💥',
    'ไหนใครแน่ 😈',
    'โอ้โห คิดว่ากลัวหรอ 🤣',
    'มาเล่นกันหน่อยไหมเพื่อน 😜',
    'ใจถึงพึ่งได้ 🔥',
    'มาท้าให้ได้กูไม่รอ 😤',
    'เล่นกันเถอะ อยากเห็นคนทำตาม 😜',
    'มึงมาทำไม 😏 หรือต้องให้กูท้าอีก? 🔥',
    'มาเล่นกันเถอะ จะได้ดูว่ากูเจ๋งขนาดไหน 😎💥',
    'อยากลองของจริงเหรอ? กูรออยู่ 😈',
    'กล้าเข้ามาเหรอ? กูแค่รอเวลาจัดการ 😈💀',
    'มึงจะหนีไปไหน? 😏🔥 อยู่ตรงนี้แหละ 😜',
    'เอาดิ ไม่กล้าเหรอ? 🤡 มาดูใครเจ๋งกว่า 😎💥',
    'มาเถอะ อยากเห็นว่ามึงจะทำได้ไหม 😈💥',
    'แค่นี้มึงก็คิดจะหยุดแล้วเหรอ? 😏 กูยังไม่เหนื่อยเลย 🔥',
    'เข้ามาเลย กูรออยู่ 😏 อย่าบอกนะว่ากลัว 😈',
    'พูดไปเรื่อยๆ แต่ทำไมไม่กล้ามาเลย 😎🔥',
    'เหยียบมาเหอะ แล้วกูจะโชว์ให้ดูว่าเจ๋งแค่ไหน 😈💥',
    'มึงคิดว่ากลัวหรอ? กูขำ 🤣🔥 มาเลย! 😜',
    'จะให้กูแสดงให้ดูไหม? กูรออยู่ 🔥💥',
    'ไม่ต้องกลัวไป กลัวไปก็ไม่น่าสนุก 😜🔥',
    'กูจะบอกให้มึงรู้เองว่าใครแน่ 🔥😈',
    'ไม่รู้เหรอว่ามึงทำอะไรมันก็ไม่พอสำหรับกู 😏💥',
    'มามิ รอดูหน่อยว่าคุณกล้าไหม 😜🔥',
    'จะวิ่งหนีเหรอ? ทำไมไม่สู้แบบแมนๆ ไปเลย 😈💥',
    'หายไปไหน? กูรอคำท้า 😏🔥',
    'ใครกล้าเข้ามา? หรือจะให้กูเชิญ 😜🔥',
    'มีอะไรอีกไหม? กูพร้อมทุกเวลา 😈💥',
    'คอยดูให้ดี มึงจะได้รู้เองว่าใครเจ๋ง 🔥😎'
]

gifs = [
'https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif',
'https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif',
'https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif',
'https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif',
'https://media.giphy.com/media/3o6ZsY8jv9b3U5ZQyE/giphy.gif',
'https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif',
'https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif',
'https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif',
'https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif',
'https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif',
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    await bot.tree.sync()
    send_random_messages.start()

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="✨welcome")
    if channel:
        await channel.send(f"🎉 welcome {member.mention} To the server!")

@tasks.loop(seconds=30)
async def send_random_messages():
    try:
        chat_channel = bot.get_channel(chat_channel_id)
        server_channel = bot.get_channel(server_channel_id)

        if chat_channel:
            await chat_channel.purge(limit=5)

            random_message = random.choice(messages)

            if not hasattr(send_random_messages, "toggle"):
                send_random_messages.toggle = True

            if send_random_messages.toggle:
                random_gif = random.choice(gifs)
                embed = discord.Embed()
                embed.set_image(url=random_gif)
                await chat_channel.send(content=random_message, embed=embed)
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.imgflip.com/get_memes') as response:
                        if response.status == 200:
                            data = await response.json()
                            if 'data' in data and 'memes' in data['data']:
                                meme = random.choice(data['data']['memes'])
                                async with session.get(meme['url']) as img_response:
                                    if img_response.status == 200:
                                        img_data = await img_response.read()
                                        file = discord.File(io.BytesIO(img_data), 'meme.jpg')
                                        await chat_channel.send(content=random_message, file=file)

            send_random_messages.toggle = not send_random_messages.toggle

        if server_channel:
            await server_channel.purge(limit=3)

            time_now = datetime.utcnow().strftime('%H:%M:%S')
            guild = server_channel.guild
            member_count = guild.member_count

            top_members = sorted(
                [m for m in guild.members if m.joined_at],
                key=lambda m: m.joined_at
            )[:5]

            top_members_list = '\n'.join(
                [f"{i+1}. {member.name} (เข้าร่วม: {member.joined_at.strftime('%Y-%m-%d')})" for i, member in enumerate(top_members)]
            )

            status_message = f"""
**🕒 เวลาปัจจุบัน:** {time_now}
**👥 จำนวนสมาชิกในเซิร์ฟ:** {member_count}

**🏆 สมาชิกที่อยู่ในเซิร์ฟเวอร์นานที่สุด 5 อันดับ:**
{top_members_list}
            """
            await server_channel.send(status_message)

    except Exception as e:
        print(f"❌ Error: {e}")

server_on()

bot.run(os.getenv('TOKEN'))
