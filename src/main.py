#!/usr/bin/env python
# coding: utf-8
# (c) 2019 lb-vr WhiteAtelier
import gettext
import logging
import os

import discord

from config import token
from logic import initialize, logger
from testfunc import testfunc

translater = gettext.translation(
    'vemt',
    localedir=os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')),
    fallback=True
)
translater.install()

client = discord.Client()


@client.event
async def on_connect():
    print(_('Connected.'))

"""
@client.event
async def on_ready():
    print('Bot is on ready.')
    channels = client.get_all_channels()
    for ch in channels:
        if ch.name == 'bot-status':
            await ch.send('BOT Started.')
"""


@client.event
async def on_disconnect():
    print(_('Disconnected.'))


@client.event
async def on_message(message):
    if not message.author.bot:
        logging.getLogger().info(
            _('Message received. \n%(message)s\nauthor id = %(id)d')
            % {
                'message': message.content,
                'id': message.author.id
            }
        )

        if message.content.startswith('+'):
            prms = message.content.split()[0].strip(' +\r\n').split(' ')
            if prms[0] == 'close':
                await message.channel.send(_('Bot Closing.'))
                await client.close()
                return
            elif prms[0] == 'clear-role':
                await testfunc.clearRoles(message.guild)
                await message.channel.send(_('Finished %(content)s') % {'content': message.content})
            elif prms[0] == 'clear-ch':
                await testfunc.clearChannel(message.guild)
                await message.channel.send(_('Finished %(content)s') % {'content': message.content})
            elif prms[0] == 'clean':
                await testfunc.cleanDefault(message.guild)
                await message.channel.send(_('Finished %(content)s') % {'content': message.content})
            elif prms[0] == 'init':
                await initialize.initializeServer(client, message)
            else:
                await message.channel.send(
                    _("No command `%(command)s`.") % {'command': prms[0]}
                )

if __name__ == "__main__":
    logger.setupLogger('vemt', logging.INFO, logging.INFO)

    tkn: str = token.loadTokenFromFile()
    if not tkn:
        logging.getLogger().fatal(_('Token string is blank.'))
        exit(-1)

    print(tkn)

    client.run(tkn)
