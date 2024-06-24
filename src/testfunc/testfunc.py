import discord
from config.server_settings import ServerSettings


async def cleanDefault(guild: discord.Guild):
    await clearRoles(guild)
    await clearChannel(guild)
    await revertAccountSettings(guild)


async def clearRoles(guild: discord.Guild):
    for role in guild.roles:
        if role.name != 'developper' and not role.is_default():
            print(_('Delete role `%(role)s`') % {'role': role.name}, end='')
            try:
                await role.delete()
                print(_('... Succeed.'))
            except (discord.Forbidden, discord.HTTPException) as e:
                print(_('... Failed.'))


async def clearChannel(guild: discord.Guild):
    kBotCategoryName = ServerSettings.getBotCategoryName()
    kBotTextChannelNames = (
        ServerSettings.getBotStatusChannelName(),
        ServerSettings.getBotControlChannelName(),
        ServerSettings.getEntryChannelName(),
        ServerSettings.getSubmitChannelName())

    channels = guild.channels
    for ch in channels:
        if ch.name in kBotTextChannelNames and ch.category.name == kBotCategoryName:
            print(_('Delete channel `%(name)s`') % {'name': ch.name}, end='')
            try:
                await ch.delete()
                print(_('... Succeed.'))
            except (discord.Forbidden, discord.HTTPException) as e:
                print(_('... Failed.'))

    categories = guild.categories
    for cat in categories:
        if cat.name == kBotCategoryName:
            print(_('Delete category `%(name)s`') % {'name': cat.name}, end='')
            try:
                await cat.delete()
                print(_('... Succeed.'))
            except (discord.Forbidden, discord.HTTPException) as e:
                print(_('... Failed.'))


async def revertAccountSettings(guild: discord.guild):
    await guild.me.edit(nick=None)
