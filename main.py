import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

intents = disnake.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")
matchmaking_queue = []
active_matches = {}
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='join')
async def join_queue(ctx: Context):
    if ctx.author not in matchmaking_queue and ctx.author not in active_matches:
        matchmaking_queue.append(ctx.author)
        await ctx.send(f'{ctx.author.mention} has joined the matchmaking queue.')
        await try_matchmake(ctx)
    elif ctx.author in matchmaking_queue:
        await ctx.send(f'{ctx.author.mention} is already in the matchmaking queue.')
    else:
        await ctx.send(f'{ctx.author.mention} is already in an active match.')
@bot.command(name='dq')
async def leave_queue(ctx: Context):
    if ctx.author in matchmaking_queue:
        matchmaking_queue.remove(ctx.author)
        await ctx.send(f'{ctx.author.mention} has left the matchmaking queue.')
    elif ctx.author in active_matches:
        opponent = active_matches.pop(ctx.author)
        del active_matches[opponent]
        embed_win = disnake.Embed(title="Match results", description=f"{ctx.author.mention} has forfeited the match. {opponent.mention} wins!", color=0x843c54)
        await ctx.send(embed=embed_win)
    else:
        await ctx.send(f'{ctx.author.mention} is not in the matchmaking queue.')

async def try_matchmake(ctx: Context):
    if len(matchmaking_queue) >= 2:
        player1 = matchmaking_queue.pop(0)
        player2 = matchmaking_queue.pop(0)

        active_matches[player1] = player2
        active_matches[player2] = player1
        match_embed = disnake.Embed(title="Match found!", description=f"{player1.mention} vs {player2.mention}!", color=0x843c54)
        await ctx.send(embed=match_embed)
    



bot.run("YOUR_TOKEN")