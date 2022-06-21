import re
from random import choice
from getpass import getpass
from discord.ext.commands import Bot
from zork import Zork

ZORK_SAVE = 'zork.pickle'

USE_GPT2 = True

if USE_GPT2:
    from aitextgen import aitextgen
    ai = aitextgen()
    print("Loaded model")

bot = Bot('/')
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_thread_create(thread):
    print('joined thread', thread.name)
    await thread.join()

@bot.event
async def on_thread_join(thread):
    print('joined thread', thread.name)
    await thread.join()

@bot.event
async def on_thread_update(thread):
    print('joined thread', thread.name)
    await thread.join()


last_prompt = ""
@bot.listen()
async def on_message(message):
    global last_prompt
    if message.author == bot.user:
        return

    content = re.sub('<@[0-9]+>', '', message.content).strip()
    author = re.sub('#[0-9]+', '', str(message.author)).strip()

    print(f'listened to "{message.author}: {message.content}"')

    if message.mentions == [bot.user] and USE_GPT2:
        prompt = f'Q: {content}\nA: '
        last_prompt = prompt
        print("prompt", prompt)
        try:
            reply = ai.generate(temperature=0.85, return_as_list=True, prompt=prompt, max_length=100)[0][len(prompt)-1:].split('\n')[0]
            print("reply", reply)
            await message.reply(reply)
        except: pass

@bot.command()
async def tryagain(ctx):
    try:
        reply = ai.generate(temperature=0.95, return_as_list=True, prompt=last_prompt, max_length=100)[0][len(last_prompt)-1:].split('\n')[0]
        await ctx.send(reply)
    except: pass

zork_sessions = {}
@bot.command()
async def zork(ctx):
    print('zork!')
    player_id = str(ctx.author.id)
    if not zork_sessions.get(player_id):
        zork_sessions[player_id] = zork = Zork('***Welcome to Adam\'s Dungeon!***', '''***Welcome to Adam's Dungeon!***
This dungeon is essentially just Zork plugged into my bot to work in Discord.
I hope you enjoy it!
*-- Adam McDaniel*''', './zork')
        await ctx.send(f'*{ctx.author.name} wants to play Zork!*')
        await ctx.reply('\n'.join(zork.read()))

    else:
        command = str(ctx.message.content)[5:].strip()
        print('command', command)
        zork: Zork = zork_sessions[player_id]
        print(zork)
        if zork:
            if command == 'quit':
                zork_sessions.pop(player_id)
                await ctx.reply(f'*{ctx.author} quit the game.*')
            elif command == 'save':
                await ctx.reply(choice([
                    "That would require good coding and foresight.",
                    "No can do, buckaroo",
                    "I'm not sure how to save this game.",
                    "I don't know how!",
                    "That's a bit too advanced for me.",
                    "Huh? I don't know what you're talking about.",
                    "Sorry, I can't.",
                ]))
            elif command != '':
                zork.write(command)
                await ctx.reply('\n'.join(zork.read()))
            else:
                await ctx.reply(f'*{ctx.author} did nothing.*')

bot.run(getpass('Enter your bot\'s token: '))