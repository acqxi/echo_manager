import datetime as dt
import discord
from discord.ext import commands


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
    async def on_raw_reaction_add( self, rawReactionEventData: discord.RawReactionActionEvent ):
        '''
        判斷標準順序
        1.判斷頻道
        2.判斷訊息
        3.判斷emoji
        4.判斷身分組
        5.執行
        '''
        print( '\non_raw_reaction_add is be called' )  # , {rawReactionEventData}')
        print( F"{self.bot.get_guild( rawReactionEventData.guild_id ).get_member( rawReactionEventData.user_id )}" )

    @commands.command( name="add_reaction", aliases=[ 'ar' ] )
    @commands.has_permissions( administrator=True )
    async def add_reaction( self, ctx: commands.Context, msg: discord.Message, emojis="" ):
        for emoji in emojis.split():
            await msg.add_reaction( emoji )
        await ctx.send( 'reaction added!' )
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove( self, rawReactionEventData ):
        print( '\non_raw_reaction_remove is be called' )  # , {rawReactionEventData}')
        print(
            F"{self.bot.get_guild( rawReactionEventData.guild_id ).get_member( rawReactionEventData.user_id ).display_name}" )


def setup( bot ):
    bot.add_cog( ReactionAddAndRemoveProcess( bot ) )