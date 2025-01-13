import discord
from discord.ext import commands

# Function to securely load the token and prefix
def get_token_and_prefix():
    token = input("Enter your bot token: ")
    prefix = input("Enter your bot prefix: ")  # Fixed: Ensure you are getting the prefix
    return token, prefix  # Return both token and prefix

# Display banner function
def display_banner():
    banner_text = """
         /$$$$$$$  /$$                     /$$             /$$   /$$           /$$                          
| $$__  $$| $$                    | $$            | $$$ | $$          | $$                          
| $$  \\ $$| $$  /$$$$$$  /$$$$$$$ | $$   /$$      | $$$$| $$ /$$   /$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$$$$$$ | $$ |____  $$| $$__  $$| $$  /$$/      | $$ $$ $$| $$  | $$| $$  /$$/ /$$__  $$ /$$__  $$
| $$__  $$| $$  /$$$$$$$| $$  \\ $$| $$$$$$/       | $$  $$$$| $$  | $$| $$$$$$/ | $$$$$$$$| $$  \\__/
| $$  \\ $$| $$ /$$__  $$| $$  | $$| $$_  $$       | $$\\\\  $$$| $$  | $$| $$_  $$ | $$_____/| $$      
| $$$$$$$/| $$|  $$$$$$$| $$  | $$| $$ \\\\  $$      | $$ \\\\  $$|  $$$$$$/| $$ \\\\  $$|  $$$$$$$| $$      
|_______/ |__/ \\\\_______/|__/  |__/|__/  \\\\__/      |__/  \\\\__/ \\\\______/ |__/  \\\\__/ \\\\_______/|__/      
"""
    print(banner_text)

# Bot setup
def main():
    # Securely load token and prefix
    token, prefix = get_token_and_prefix()

    # Set up intents
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    # Initialize bot
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    bot.remove_command("help")

    # Event for when the bot is ready
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print(f'Bot ID: {bot.user.id}')
        print('--- Ready for servers ---\n')
        display_banner()

    # Commands
    @bot.command()
    async def ban(ctx, member: discord.Member):
        try:
            await member.ban()
            await ctx.send(f'Banned {member.name}')
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members.")
        except discord.HTTPException:
            await ctx.send("Failed to ban the member.")

    @bot.command()
    async def kick(ctx, member: discord.Member):
        try:
            await member.kick()
            await ctx.send(f'Kicked {member.name}')
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick members.")
        except discord.HTTPException:
            await ctx.send("Failed to kick the member.")
    
    @bot.command()
    async def create_channel(ctx, name):
        try:
            guild = ctx.guild
            await guild.create_text_channel(name)
            await ctx.send(f'Created channel: {name}')
        except discord.Forbidden:
            await ctx.send("I don't have permission to create channels.")
        except discord.HTTPException:
            await ctx.send("Failed to create the channel.")
    
    @bot.command()
    async def delete_roles(ctx):
        try:
            guild = ctx.guild
            for role in guild.roles:
                if role.name != "@everyone":
                    await role.delete()
            await ctx.send('Deleted all roles (except @everyone).')
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete roles.")
        except discord.HTTPException:
            await ctx.send("Failed to delete the roles.")

    # Add more commands as needed...

    # Run the bot
    bot.run(token)

if __name__ == "__main__":
    main()