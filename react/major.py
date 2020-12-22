import datetime as dt
from logging import error
from warnings import resetwarnings

import discord
from discord import reaction
from discord.ext import commands

from . import gReactVal

g_dev_limit_rule = {}

g_temp_msg = {}


async def get_msg(
        guild: discord.Guild = None,
        channelID: int = None,
        channel: discord.TextChannel = None,
        msgID: int = None ) -> discord.Message:
    try:
        return g_temp_msg[ msgID ]
    except KeyError:
        if guild is not None and channelID is not None:
            channel = guild.get_channel( channel_id=channelID )
        elif guild is None and channel is None:
            raise Exception( 'guild, channel both None error' )

        msg = await channel.fetch_message( msgID )
        g_temp_msg[ msgID ] = msg
        return msg


def should_remove_reaction():
    return False


class ReactionAddAndRemoveProcess( commands.Cog, name='Calculation Commands' ):
    '''These are the deal with reaction'''

    def __init__( self, bot: commands.Bot ):
        self.bot = bot

    async def cog_check( self, ctx ):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.Cog.listener()
    async def on_raw_reaction_add( self, rRED: discord.RawReactionActionEvent ):  #rRED : rawReactionEventData
        ''''''
        print( '\non_raw_reaction_add is be called' )  # , {rRED}')
        #print( F"{self.bot.get_guild( rRED.guild_id ).get_member( rRED.user_id )}" )

        try:
            react_dict = gReactVal.reactSetInd[ rRED.guild_id ][ rRED.message_id ]
        except KeyError:
            print( 'no co msg' )
            return

        guild = self.bot.get_guild( rRED.guild_id )
        member = guild.get_member( rRED.user_id )

        print( f"{member.display_name} press {rRED.emoji} at msgID:{rRED.message_id}" )

        if should_remove_reaction():  #TODO
            await get_msg( guild, rRED.channel_id, msgID=rRED.message_id ).remove_reaction( rRED.emoji, member )

        try:
            args = react_dict[ str( rRED.emoji ) ]
            if not args[ 2 ]:
                for emoji, relation in react_dict.items():
                    if relation[ 2 ]:
                        continue
                    if relation[ 1 ] in member.roles:
                        await get_msg( guild, rRED.channel_id, msgID=rRED.message_id ).remove_reaction( relation[ 0 ], member )
            await member.add_roles( args[ 1 ] )
        except KeyError:
            print( 'invaild emoji' )
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove( self, rRED ):
        print( '\non_raw_reaction_remove is be called' )  # , {rRED}')
        #print( F"{self.bot.get_guild( rRED.guild_id ).get_member( rRED.user_id ).display_name}" )

        try:
            react_dict = gReactVal.reactSetInd[ rRED.guild_id ][ rRED.message_id ]
        except KeyError:
            print( 'no co msg' )
            return

        guild = self.bot.get_guild( rRED.guild_id )
        member = guild.get_member( rRED.user_id )

        print( f"{member.display_name} press {rRED.emoji} at msgID:{rRED.message_id}" )

        try:
            args = react_dict[ str( rRED.emoji ) ]
            await member.remove_roles( args[ 1 ], reason='unReact msg' )
        except KeyError:
            print( 'invaild emoji' )
            return


def setup( bot ):
    bot.add_cog( ReactionAddAndRemoveProcess( bot ) )
