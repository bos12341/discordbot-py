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
async def on_message(message):
    if message.author == client.user:
        return

    # 저장할 파일 경로와 이름 설정
    file_path = 'saved_messages.txt'

    # 메시지 내용 가져와서 파일에 저장
    with open(file_path, 'a') as file:
        file.write(f'{message.author.name}: {message.content}\n')

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
