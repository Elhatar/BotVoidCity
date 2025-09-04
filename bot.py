#Imports
import discord
from discord.ext import commands
import random
import os
import json

#Constants
CHAR_DIR = "characters"
new_line = '\n'

skills = {
"АТЛ":"СИЛ",
"ВЫН":"ТЕЛ",
"СТК":"ТЕЛ",
"ЛВРК":"ЛВК",
"СКР":"ЛВК",
"АКР":"ЛВК",
"ВНИМ":"ИНТ",
"ПРОН":"ИНТ",
"ВЫСЛ":"ИНТ",
"БИНТ":"ИНТ",
"КОНЦ":"РАС",
"АНАЛИНТ":"ИНТ",
"АНАЛУЧ":"УЧН",
"ЗГРД":"ИНТ",
"ЖИВ":"ИНТ",
"КОМПИНТ":"ИНТ",
"КОМПУЧ":"УЧН",
"ИНФ":"ИНТ",
"НАУ":"УЧН",
"ДЕД":"ИНТ",
"ЭЛЕК":"УЧН",
"ВЗРВ":"УЧН",
"МАСК":"ИНТ",
"ППОМ":"ИНТ",
"ПАРМ":"УЧН",
"ИМПЛ":"УЧН",
"ОБМ":"ХАР",
"УБЕЖ":"ХАР",
"ВЫСТ":"ХАР"
}

#Intents
intents = discord.Intents.default()
intents.message_content = True
#Prefix
bot = commands.Bot(command_prefix='!', intents=intents) 

#Logic
def get_char_path(user_id: int):
    """Путь к JSON файлу персонажа по ID пользователя"""
    return os.path.join(CHAR_DIR, f"{user_id}.json")

def load_character(user_id: int):
    """Загружает файл персонажа"""
    path = get_char_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_character(user_id: int, data: dict):
    """Сохраняет данные персонажа"""
    os.makedirs(CHAR_DIR, exist_ok=True)
    path = get_char_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#Commands
##Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong')
    await ctx.send(random.SystemRandom().randint(1, 12))

##Show stats
@bot.command()
async def show(ctx):
    """Показывает полные характеристики вашего персонажа"""
    char = load_character(ctx.author.id)
    if char:
        await ctx.send(
            f"**{char['имя']}**\n"
            f"Сила: {char['сила']}\n"
            f"Ловкость: {char['ловкость']}\n"
            f"Телосложение: {char['телосложение']}"
        )
    else:
        await ctx.send("У тебя пока нет персонажа!")

##Roll stat
@bot.command()
async def roll(ctx, stat, skill=None):
    """Проверка выбранной характеристики/навыка. Для навыка испульзуйте !roll <id навыка> н"""
    char = load_character(ctx.author.id)
    if char:
        if char["Счётчик рассудка"] == 0:
            mindBonus = 0
        if char["Счётчик рассудка"] in range(1, 5):
            mindBonus = 1
        if char["Счётчик рассудка"] in range(6, 14):
            mindBonus = 2
        if char["Счётчик рассудка"] == 15:
            mindBonus = 3
        if char["Счётчик рассудка"] in range(-1, -5):
            mindBonus = -1
        if char["Счётчик рассудка"] in range(-6, -14):
            mindBonus = -2
        if skill is None and stat in char:
            if stat != "УДЧ":
                roll = random.SystemRandom().randint(1, 12)
                result = char[stat] + roll + mindBonus
                await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat]} + {mindBonus} = {result}")
            else:
                roll = random.SystemRandom().randint(1, 100)
                result = char[stat] + roll + mindBonus
                await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat]} + {mindBonus} = {result}")
        elif stat in char:
            if stat != "ХИР":
                roll = random.SystemRandom().randint(1, 12)
                result = char[stat] + char[skills[stat]] + roll + mindBonus
                await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat] + char[skills[stat]]} + {mindBonus} = {result}")
            else:
                roll = random.SystemRandom().randint(1, 12)
                result = char[stat] + char["ИНТ"] + char["УЧН"] + roll + mindBonus
                await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat] + char["ИНТ"] + char["УЧН"]} + {mindBonus} = {result}")
        else:
            pass

##Roll stat with advantage
@bot.command()
async def adv(ctx, stat, skill=None):
    """Проверка выбранной характеристики/навыка с преимуществом"""
    char = load_character(ctx.author.id)
    if char:
        if char["Счётчик рассудка"] == 0:
            mindBonus = 0
        if char["Счётчик рассудка"] in range(1, 5):
            mindBonus = 1
        if char["Счётчик рассудка"] in range(6, 14):
            mindBonus = 2
        if char["Счётчик рассудка"] == 15:
            mindBonus = 3
        if char["Счётчик рассудка"] in range(-1, -5):
            mindBonus = -1
        if char["Счётчик рассудка"] in range(-6, -14):
            mindBonus = -2
        for i in range(2):
            if skill is None and stat in char:
                if stat != "УДЧ":
                    roll = random.SystemRandom().randint(1, 12)
                    result = char[stat] + roll + mindBonus
                    await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat]} + {mindBonus} = {result}")
                else:
                    roll = random.SystemRandom().randint(1, 100)
                    result = char[stat] + roll + mindBonus
                    await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat]} + {mindBonus} = {result}")
            elif stat in char:
                if stat != "ХИР":
                    roll = random.SystemRandom().randint(1, 12)
                    result = char[stat] + char[skills[stat]] + roll + mindBonus
                    await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat] + char[skills[stat]]} + {mindBonus} = {result}")
                else:
                    roll = random.SystemRandom().randint(1, 12)
                    result = char[stat] + char["ИНТ"] + char["УЧН"] + roll + mindBonus
                    await ctx.send(f"**{char['имя']}** {new_line}Проверка {stat}: {roll} + {char[stat] + char["ИНТ"] + char["УЧН"]} + {mindBonus} = {result}")
            else:
                pass
 
            
#Get damage
@bot.command()
async def damage(ctx, num, typ):
    """Получить по лицу/Вылечиться. Использование !damage <значение> <ТИП>. Типы: РЕЖ (режущий), КОЛ (колющий), ДРОБ (дробящий), ХИЛ (лечение)"""
    char = load_character(ctx.author.id)
    if char:
        num = int(num)
        if typ in ["РЕЖ", "КОЛ", "ДРОБ", "ХИЛ"]:
            if typ != "ХИЛ":
                result = num * char[typ]
                char["ХП"] = char["ХП"] - round(result)
                if char["ХП"] <= 0:
                    char["ХП"] = 0
                await ctx.send(f"**{char['имя']}** {new_line}Получено урона {round(result)} ({round(result, 2)}) {new_line}Текущее здоровье: {char["ХП"]} из {char["Макс ХП"]}")
            else:
                char["ХП"] = char["ХП"] + num
                if char["ХП"] >= char["Макс ХП"]:
                    char["ХП"] = char["Макс ХП"]
                await ctx.send(f"**{char['имя']}** {new_line}Здоровья восстановлено {num} {new_line}Текущее здоровье: {char["ХП"]} из {char["Макс ХП"]}")
            save_character(ctx.author.id, char)
        else:
            pass

##Add mind
@bot.command()
async def sanity(ctx, num):
    """Добавить значение к счётчику рассудка. Использование !mindadd <значение>"""
    char = load_character(ctx.author.id)
    if char:
        char["Счётчик рассудка"] = char["Счётчик рассудка"] + int(num)
        if char["Счётчик рассудка"] >= 15:
            char["Счётчик рассудка"] = 15
        await ctx.send(f"**{char['имя']}** {new_line}Текущий рассудок: {char["Счётчик рассудка"]}")
        save_character(ctx.author.id, char)

##Add inspiration
@bot.command()
async def insp(ctx, num):
    """Добавить значение к количеству вдохновений. Использование !inspadd <значение>"""
    char = load_character(ctx.author.id)
    if char:
        char["Счётчик вдохновений"] = char["Счётчик вдохновений"] + int(num)
        if char["Счётчик вдохновений"] >= 3:
            char["Счётчик вдохновений"] = 3
        await ctx.send(f"**{char['имя']}** {new_line}Количество вдохновений: {char["Счётчик вдохновений"]}")
        save_character(ctx.author.id, char)

#Print mind/inspiration
#Print mind
@bot.command()
async def get(ctx, value):
    """Посмотреть значение рассудка/количество вдохновений/здоровья. Использование !get <стат>. s - рассудок, i - вдохновения, hp - здоровье"""
    char = load_character(ctx.author.id)
    if value == "s":
        await ctx.send(f"**{char['имя']}** {new_line}Текущий рассудок: {char["Счётчик рассудка"]}")
    if value == "i":
        await ctx.send(f"**{char['имя']}** {new_line}Количество вдохновений: {char["Счётчик вдохновений"]}")

##Roll dice
@bot.command()
async def dice(ctx, num):
    """Бросток куба. Использование - !dice <значение> (Например, !dice 6 - это бросок D6"""
    char = load_character(ctx.author.id)
    result = random.SystemRandom().randint(1, int(num))
    await ctx.send(f"**{char['имя']}** {new_line}Бросок d{num}: {result}")

##Rolls list
@bot.command()
async def tab(ctx):
    """Таблица возможных проверок"""
    await ctx.send(
    "Характеристики:"  + '\n' +
    "СИЛ - Сила" + '\n' +
    "ЛВК - Ловкость" + '\n' +
    "ТЕЛ - Телосложение" + '\n' +
    "ОРЖ - Оружин" + '\n' +
    "ТМП - Темп" + '\n' +
    "УДЧ - Удача" + '\n' +
    "СКО - Скорость" + '\n' +
    "РЕФ - Реакция" + '\n' +
    "ИНТ - Интеллект" + '\n' +
    "УЧН - Учёность" + '\n' +
    "ХАР - Харизма" + '\n' +
    "РАС - Рассудок" + '\n' +
    "АТЛ - Атлетика" + '\n' +
    "ВЫН - Выносливость" + '\n' +
    "СТК - Стойкость" + '\n' +
    "ЛВРК - Ловкость рук" + '\n' +
    "СКР - Скрытность" + '\n' +
    "АКР - Акробатика" + '\n' +
    "ВНИМ - Внимание" + '\n' +
    "ПРОН - Проницательность" + '\n' +
    "ВЫСЛ - Выслеживание" + '\n' +
    "БИНТ - Боевой интелект" + '\n' +
    "КОНЦ - Концентрация" + '\n' +
    "АНАЛИНТ - Анализ от Интеллекта" + '\n' +
    "АНАЛУЧ - Анализ от Учёности" + '\n' +
    "ЗГРД - Знание города" + '\n' +
    "ЖИВ - Обращение с животными" + '\n' +
    "КОМПИНТ - Композиция от Интеллекта" + '\n' +
    "КОМПУЧ - Композиция от Учёности" + '\n' +
    "ИНФ - Поиск информации" + '\n' +
    "НАУ - Наука" + '\n' +
    "ДЕД - Дедукция" + '\n' +
    "ЭЛЕК - Электроника" + '\n' +
    "ВЗРВ - Взрывчатка" + '\n' +
    "МАСК - Маскировка" + '\n' +
    "ППОМ - Первая помощь" + '\n' +
    "ПАРМ - Парамедик" + '\n' +
    "ХИР - Хирургия" + '\n' +
    "ИМПЛ - Импланты" + '\n' +
    "ОБМ - Обман" + '\n' +
    "УБЕЖ - Убеждение" + '\n' +
    "ВЫСТ - Выступление"
)

#Run bot
bot.run('TOKEN')
