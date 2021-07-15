#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Экспорт эмодзи с гильдий Discord. Возможен экспорт как статичных эмодзи (в .png), так и эспорт анимированных эмодзи (в .gif)
import asyncio
import discord
import sys, os
import requests
from progress.bar import IncrementalBar
from discord.ext import commands

try:
    bot = discord.Client()

    @bot.event
    async def on_ready():
        print(f"Авторизован в {bot.user.name}")
        guild = bot.get_guild(int(sys.argv[2]))
        print(f"Определена гильдия: {guild.name}")
        print(f"Найдено {len(guild.emojis)} эмодзи. Начало экспорта...")
        path_to_folder = f"./{guild.name} - {guild.id}" # Папка в формате: NAME - ID
        if not os.path.exists(path_to_folder):
            os.mkdir(path_to_folder) # Создание папки
        bar = IncrementalBar('Экспортировано эмодзи', max = len(guild.emojis)) # Определение ProgressBar
        for emoji in guild.emojis:
            emj = bot.get_emoji(emoji.id)
            url = emj.url_as(format=None,
                            static_format='png')
            r = requests.get(emj.url)
            file = str(url).partition('s/')[2] # Получение имени файла
            with open(f'{path_to_folder}/{file}', 'wb') as f: # Сохранение эмодзи в файл
                f.write(r.content)
            bar.next()
        bar.finish()
        print(f"\033[32mЗавершён экспорт {len(guild.emojis)} эмодзи\033[0m")
        print("Выход из аккаунта...")
        await bot.close()

    bot.run(sys.argv[1],bot=False) # Авторизация в селфбота
except Exception as err:
    print(f"\033[31mОшибка. Укажите аргументы в правильной последовательности или проверьте их. <Token> <GuildID>\033[0m")
    raise err
