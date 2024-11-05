import fade
import discord
import asyncio
import datetime
import os
import ctypes
import re
import sys
import time
from colorama import Fore, Style, init

sys.stdout.reconfigure(encoding='utf-8')

def set_window_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

set_window_title("          🌟  cimientos  🌟               ")

text = '''



                                ▄▄· ▪  • ▌ ▄ ·. ▪  ▄▄▄ . ▐ ▄ ▄▄▄▄▄      .▄▄ · 
                               ▐█ ▌▪██ ·██ ▐███▪██ ▀▄.▀·•█▌▐█•██  ▪     ▐█ ▀. 
                               ██ ▄▄▐█·▐█ ▌▐▌▐█·▐█·▐▀▀▪▄▐█▐▐▌ ▐█.▪ ▄█▀▄ ▄▀▀▀█▄
                               ▐███▌▐█▌██ ██▌▐█▌▐█▌▐█▄▄▌██▐█▌ ▐█▌·▐█▌.▐▌▐█▄▪▐█
                               ·▀▀▀ ▀▀▀▀▀  █▪▀▀▀▀▀▀ ▀▀▀ ▀▀ █▪ ▀▀▀  ▀█▄▀▪ ▀▀▀▀ 
                                     ▄▄·  ▄ .▄▄▄▄ . ▄▄· ▄ •▄ ▄▄▄ .▄▄▄
                                    ▐█ ▌▪██▪▐█▀▄.▀·▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
                                    ██ ▄▄██▀▐█▐▀▀▪▄██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄
                                    ▐███▌██▌▐▀▐█▄▄▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
                                    ·▀▀▀ ▀▀▀ · ▀▀▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀


                                         xfsc on discord <3

'''

faded_text = fade.greenblue(text)

for line in faded_text.splitlines():
    for char in line:
        print(char, end='', flush=True) 
        time.sleep(0.01)
    print()

init(autoreset=True)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

async def check_token_and_get_info():
    while True:
        token_to_check = input(f"{Fore.CYAN}                    Ingresa el token del bot: {Style.RESET_ALL}")

        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        try:
            @client.event
            async def on_ready():
                print(f"\n{Fore.MAGENTA}                    El bot está listo y pertenece a los siguientes servidores:{Style.RESET_ALL}")
                for guild in client.guilds:
                    print(f"{Fore.GREEN}                    - {guild.name}{Style.RESET_ALL} (ID: {Fore.CYAN}{guild.id}{Style.RESET_ALL})")
                    member_count = guild.member_count
                    print(f"  {Fore.YELLOW}                    Miembros: {member_count}{Style.RESET_ALL}")

                    boost_count = guild.premium_subscription_count
                    if boost_count:
                        print(f"  {Fore.LIGHTMAGENTA_EX}                    Boosts: {boost_count}{Style.RESET_ALL} 🚀")
                    else:
                        print(f"  {Fore.RED}                    Boosts: ❌{Style.RESET_ALL}")

                    if guild.text_channels:
                        try:
                            invite = await guild.text_channels[0].create_invite()
                            print(f"  {Fore.BLUE}                    Invitación: {invite.url}{Style.RESET_ALL}")
                        except discord.Forbidden:
                            print(f"  {Fore.RED}                    No tengo permisos para crear una invitación en este servidor.{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.RED}                    No hay canales de texto disponibles para crear una invitación.{Style.RESET_ALL}")

                save_info_to_txt(client.user.name, client.guilds, token_to_check)
                print(f"{Fore.LIGHTYELLOW_EX}                    [ > ] ¿Le gustaría chequear otro token? (Y/N): {Style.RESET_ALL}")
                response = await asyncio.to_thread(input)
                if response.upper() != 'Y':
                    await client.close()
                    return

                await client.close()

            await client.start(token_to_check)

        except discord.LoginFailure:
            print(f"{Fore.RED}                    Error de inicio de sesión: el token no es válido.{Style.RESET_ALL}")
            await asyncio.sleep(5)

def save_info_to_txt(bot_name, guilds, token):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logs_folder = "logs"
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    sanitized_bot_name = sanitize_filename(bot_name)
    file_name = os.path.join(logs_folder, f"{sanitized_bot_name}_info_{current_time}.txt")

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("Información del bot:\n")
        file.write(f"Nombre del bot: {bot_name}\n")
        file.write(f"Token del bot: {token}\n")
        file.write("Servidores:\n")

        for guild in guilds:
            file.write(f"- {guild.name} (ID: {guild.id})\n")
            member_count = guild.member_count
            file.write(f"  Miembros: {member_count}\n")
            boost_count = guild.premium_subscription_count
            if boost_count:
                file.write(f"  Boosts: {boost_count}\n")
            else:
                file.write(f"  Boosts: False\n")

if __name__ == "__main__":
    asyncio.run(check_token_and_get_info())
