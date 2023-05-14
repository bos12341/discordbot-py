from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('-버튼'):
        # remove the prefix and get the url
        url = message.content[4:].strip()

        # create the button
        button = discord.Button(label='클릭', url=url)

        # generate an embed with the button
        embed = discord.Embed(title='클릭하세요', description='')
        embed.add_field(name='\u200b', value=f'{button}')

        # send the message
        await message.channel.send(embed=embed)
    
    if message.content.startswith('-인증'):
        if message.channel.id != 1099558481519980658: # 지정된 채널의 ID를 입력해주세요
            await message.channel.send("인증은 지정된 채널에서만 가능합니다.")
            return

        embed = discord.Embed(title='인증하기', description='일회용 인증')
        embed.add_field(name="",value="이모지 클릭" ,inline=False)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('✅')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("시간이 초과되었습니다.")
        else:
            role = discord.utils.get(message.guild.roles, id=1090595156220182528) # 지급할 역할 ID를 입력해주세요
            await user.add_roles(role)
            await message.channel.send(f'{message.author.mention}, 인증이 완료되었습니다.')
            
    if message.content.startswith('-프사'):
        try:
            # 명령어 뒤에 입력한 유저 ID를 추출
            user_id = int(message.content.split()[1])
            user = await client.fetch_user(user_id)

            # 해당 유저의 프로필 사진 URL과 멘션을 출력
            await message.channel.send(f"{user.avatar_url}")
            await message.channel.send(f"{user.mention}")
        
        # 유효하지 않은 유저 ID를 입력한 경우
        except:
            await message.channel.send("올바른 유저 ID를 입력해주세요.")


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
