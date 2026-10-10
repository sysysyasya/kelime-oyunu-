import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents) oyunlar = {}
kullanilanlar = {}
son_kelime = {}

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.command()
async def baslat(ctx):
    oyunlar[ctx.channel.id] = True
    kullanilanlar[ctx.channel.id] = set()
    son_kelime[ctx.channel.id] = None
    await ctx.send("Kelime zinciri başladı! İlk kelimeyi yazın.")

@bot.command()
async def bitir(ctx):
    oyunlar[ctx.channel.id] = False
    await ctx.send("Oyun bitti!")

@bot.command()
async def sifirla(ctx):
    kullanilanlar[ctx.channel.id] = set()
    son_kelime[ctx.channel.id] = None
    await ctx.send("Kullanılan kelimeler sıfırlandı.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    if message.content.startswith("!"):
        return
    kanal = message.channel.id
    if not oyunlar.get(kanal, False):
        return
    kelime = message.content.strip().casefold()
    if not kelime.isalpha() or kelime.endswith("ğ"):
        await message.delete()
        return
    if not all(harf in "abcçdefgğhıijklmnoöprsştuüvyz" for harf in kelime):
        await message.delete()
        return
    if kelime in kullanilanlar.setdefault(kanal, set()) or not kelime_listesinde(kelime):
        await message.delete()
        return
    onceki = son_kelime.get(kanal)
    if onceki and kelime[0] != onceki[-1]:
        await message.delete()
        return
    kullanilanlar[kanal].add(kelime)
    son_kelime[kanal] = kelime
    await message.add_reaction("💚")

def kelime_listesinde(kelime):
    try:
        with open("kelimeler.txt", encoding="utf-8") as f:
            return kelime in {satir.strip().casefold() for satir in f if satir.strip()}
    except FileNotFoundError:
        return False

bot.run(os.environ["DISCORD_TOKEN"])
