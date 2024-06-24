import discord
import logging
from typing import Optional, List, Dict
from config.server_settings import ServerSettings


class GuildIsNullError(Exception):
    pass


class AlreadyInitializedError(Exception):
    pass


async def initializeServer(client: discord.Client, message: discord.Message):
    logger = logging.getLogger('initializeServer')
    kBotCategoryName = ServerSettings.getBotCategoryName()
    kBotTextChannelNames = (
        ServerSettings.getBotStatusChannelName(),
        ServerSettings.getBotControlChannelName(),
        ServerSettings.getEntryChannelName(),
        ServerSettings.getSubmitChannelName())
    log_messages: List[str] = []

    try:
        # Starting
        logger.info('Initializing discord server.')
        await message.channel.send(_('Start initializing...'))

        # get guild
        if not message.guild:
            raise AlreadyInitializedError()

        guild: discord.Guild = message.guild
        logger.info('Guild = %s (%s)', guild.name, hex(guild.id))

        # check already exist
        for r in guild.roles:
            if r.name == ServerSettings.getBotAdminRoleName():
                log_messages.append(_("Role `%(name)s` already exists.") % {'name': r.name})
                raise AlreadyInitializedError('Role already exists.', r.name)
        for cat in guild.categories:
            if cat.name == ServerSettings.getBotCategoryName():
                log_messages.append(_("Category `%(name)s` already exists.") % {'name': cat.name})

        # variables
        categories_list: List[discord.CategoryChannel] = guild.categories
        text_channels: List[discord.TextChannel] = guild.text_channels

        # add 'Bot Admin' role
        roles = guild.roles
        for r in roles:
            if r.name == ServerSettings.getBotAdminRoleName:
                break
        else:
            await guild.create_role(
                name=ServerSettings.getBotAdminRoleName(),
                colour=ServerSettings.getBotAdminRoleColour())
            log_messages.append(
                _("Role `%(name)s` has been created.") % {'name': ServerSettings.getBotAdminRoleName()}
            )

        # change 'vemt-bot' role color
        await guild.me.edit(nick='VEMT')

        # create 'bot' category
        for cat in categories_list:
            if cat.name == kBotCategoryName:
                logger.info('Category {} already exists.'.format(cat.name))
                break
        else:
            await guild.create_category(kBotCategoryName)
            logger.info('Category %s has been created.', kBotCategoryName)
            log_messages.append(
                _("Category `%(name)s` has been created.") % {'name': kBotCategoryName}
            )
        # get created 'bot' category
        bot_category = None
        categories_list = guild.categories
        for cat in categories_list:
            if cat.name == kBotCategoryName:
                bot_category = cat
                break
        else:
            logger.fatal('Internal Error. BOT category was not found.')
            return

        # create bot-status, bot-control, entry, submit into BOT category.
        bot_text_channels: List[discord.TextChannel] = bot_category.text_channels

        for target in kBotTextChannelNames:
            for ch in bot_text_channels:
                if target == ch.name:
                    break
            else:
                await bot_category.create_text_channel(target)
                logger.info('Created %s channel.', target)
                log_messages.append(
                    _("Text chat `%(name)s` has been created.") % {'name': format(target)}
                )

    except discord.Forbidden as e:
        logger.exception('Initializing is forbidden.', exc_info=e)
        await message.channel.send(_('BOT does not have permission to do it.'))
        return
    except discord.HTTPException as e:
        logger.exception('Failed to initialize.', exc_info=e)
        return
    except discord.InvalidArgument as e:
        logger.exception('Program error.', exc_info=e)
        await message.channel.send(_('Failed to initialize Discord Server.'))
        return
    else:
        log_messages.insert(0, _('Failed to initialize Discord Server.'))
        await message.channel.send('\n'.join(log_messages))
