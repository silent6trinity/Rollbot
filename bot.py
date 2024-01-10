import discord
from discord.ext import commands

TOKEN = 'TOKEN'
intents = discord.Intents.default()
intents.members = True  # Required to access voice channel members

bot = commands.Bot(command_prefix="/", intents=intents)

async def send_long_message(ctx, message):
    max_characters = 2000
    for i in range(0, len(message), max_characters):
        await ctx.send(f"{message[i:i+max_characters]}")

@bot.command(name='list')
async def list(ctx, role_name: str):
    """Lists all server members with a specific role, matching role names case-insensitively."""
    try:
        # Convert the role_name argument to lowercase
        role_name_lower = role_name.lower()

        # Find the role with a case-insensitive match
        role = next((role for role in ctx.guild.roles if role.name.lower() == role_name_lower), None)

        if role is None:
            await ctx.send(f"Role '{role_name}' not found.")
            return

        members_with_role = [member for member in ctx.guild.members if role in member.roles and not member.bot]
        member_nicknames = sorted([member.nick if member.nick else member.name for member in members_with_role])
        nicknames_string = '\n'.join(member_nicknames)
        await send_long_message(ctx, f"All members of `{role.name}`:\n ```{nicknames_string}```")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name='rollcall')
async def rollcall(ctx, role_name: str = None):
    """Lists members with a specified role who are not in the corresponding voice channel of the text channel, or lists all members in the channel if 'present' is specified."""
    try:
        text_channel_name = ctx.channel.name
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=text_channel_name)

        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            await ctx.send(f"No corresponding voice channel for '{text_channel_name}'.")
            return

        if role_name and role_name.lower() == 'present':
            # List all present members in the voice channel
            present_members = [member.display_name for member in voice_channel.members if not member.bot]
            present_members_string = '\n'.join(sorted(present_members))
            present_count = len(present_members)
            await send_long_message(ctx, f" `{present_count}` Members currently in `{voice_channel.name}` voice channel:\n```{present_members_string}```")
        else:
            if not role_name:
                await ctx.send("Please specify a role name.")
                return

            role_name_lower = role_name.lower()
            role = next((role for role in ctx.guild.roles if role.name.lower() == role_name_lower), None)

            if not role:
                await ctx.send(f"Invalid role '{role_name}'.")
                return

            role_members = [member for member in ctx.guild.members if role in member.roles and not member.bot]
            present_members = [member for member in voice_channel.members if member in role_members and not member.bot]

            # Determine members with the role who are not in the voice channel
            absentees = set(member.display_name for member in role_members) - set(member.display_name for member in present_members)
            
            
            absentees_string = '\n'.join(sorted(absentees))

            # Count of absent and total members
            absent_count = len(absentees)
            total_count = len(role_members)

            await send_long_message(ctx, f"{absent_count}/{total_count} `{role.name}` members currently not present:\n```{absentees_string}```")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

bot.run(TOKEN)
