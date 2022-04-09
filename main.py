import discord
import json
import requests
from discord.ext import commands
from libs import macro

class Cogs:
    safe = [
        'cogs.player',
        'cogs.games',
        'cogs.meme',
        'cogs.nsfw'
    ]


with open("env/configuration.json", 'r') as config:
    data = json.load(config)
    Token = data['Token']
    Prefix = data['Prefix']
    bid = data['bid']
    key = data['key']

bot = commands.Bot(command_prefix=commands.when_mentioned_or(Prefix))
bot.remove_command('help')

for cog in Cogs.safe:
    bot.load_extension(cog)

    def __init__(self, bot):
        self.bot = bot


@bot.event
async def on_ready():
    print('Connected to Hydra: {}'.format(bot.user.name))
    print('Hydra ID: {}'.format(bot.user.id))
    print(f"""READY\nUSER:{bot.user}\nminorities destroyed :sunglasses:""")
    await bot.change_presence(activity=discord.Game(name=f'{Prefix}help || Usef {Prefix}create to start an account!'), status=discord.Status.idle)


@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound)

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=await macro.error(str(error)))

    elif isinstance(error, AssertionError):
        await ctx.send(embed=await macro.error(f"{str(error).replace('AssertionError: ', '')}"))

    elif isinstance(error, IndexError):
        await ctx.send(embed=await macro.error("You need to create an account to use this command! \n Please use ``p!create`` to create an account."))

    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=await macro.error(f"You forgot an argument!\n```{error}```"))
    else:
        await ctx.send(embed=await macro.error(f'Woah there partner. :cowboy: It seems as though you ran into a serious error. \nPlease contact @TheCoddyDay#5100 and DM him the text below, along with the command you used, and how you typed it out.\n```{str(error)}```'))


@bot.command(aliases=['ch',])
async def chat_bot(ctx, uid, *, args):
    msg = args.lower()
    path_ = requests.get(f'http://api.brainshop.ai/get?bid={bid}&key={key}&uid={uid}&msg={msg}')
    path_dic = path_.json()
    chat_send = path_dic['cnt']
    if len(args) == 0:
        await ctx.reply('Please specify something for making conversation with me...')
    
    if len(args) >= 1:
        await ctx.reply(chat_send)

bot.run(Token)
