import discord
from discord.ext import commands
import asyncio
import datetime as dt


class DevCommands( commands.Cog, name='Developer Commands' ):
    '''These are the developer commands'''

    def __init__( self, bot ):
        self.bot = bot

    async def cog_check( self, ctx ):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id == self.bot.author_id

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=[ 'rl' ]  # Aliases for the command.
    )
    async def reload( self, ctx: commands.Context, cog: str ):
        '''
        Reloads a cog.
        '''
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension( cog )
                self.bot.load_extension( cog )
            await ctx.send( 'Done', delete_after=360 )
            await ctx.message.delete( delay=360 )
        if cog in extensions:
            self.bot.unload_extension( cog )  # Unloads the cog
            self.bot.load_extension( cog )  # Loads the cog
            await ctx.send( 'Done', delete_after=360 )  # Sends a message where content='Done'
            await ctx.message.delete( delay=360 )
        else:
            await ctx.send( 'Unknown Cog' )  # If the cog isn't found/loaded.

    @commands.command( name="unload", aliases=[ 'ul' ] )
    async def unload( self, ctx: commands.Context, cog: str ):
        '''
        Unload a cog.
        '''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send( "Cog is not loaded!" )
            return
        self.bot.unload_extension( cog )
        await ctx.send( f"`{cog}` has successfully been unloaded." )

    @commands.command( name="load" )
    async def load( self, ctx: commands.Context, cog: str ):
        '''
        Loads a cog.
        '''
        try:

            self.bot.load_extension( cog )
            await ctx.send( f"`{cog}` has successfully been loaded." )

        except commands.errors.ExtensionNotFound:
            await ctx.send( f"`{cog}` does not exist!" )

    @commands.command( name="listcogs", aliases=[ 'lc' ] )
    async def listcogs( self, ctx: commands.Context ):
        '''
        Returns a list of all enabled commands.
        '''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join( [ str( cog ) for cog in self.bot.extensions ] )
        base_string += "\n```"
        await ctx.send( base_string )

    #@commands.Cog.listener()
    #async def on_command_error( self, ctx: commands.Context, error ):
    #    await ctx.send( error )

    @commands.command( name="register", aliases=[ 'reg' ] )
    async def register( self, ctx: commands.Context ):
        slepp_time = 10
        await ctx.send( '請輸入辨識碼', delete_after=600 )
        await asyncio.sleep( slepp_time )
        await ctx.send( '辨識碼錯誤，請確認後重新輸入', delete_after=600 )
        await asyncio.sleep( slepp_time )
        await ctx.send( '辨識碼正確，系統已激活.', delete_after=600 )
        await asyncio.sleep( slepp_time )
        await ctx.send( '已設定有警報時提及所有人', delete_after=600 )
        await asyncio.sleep( slepp_time )
        await ctx.send( '生成網站動態連結中...', delete_after=600 )
        await asyncio.sleep( slepp_time )
        await ctx.send( '連結如下: http://192.168.154.122/setting/tagger?pasw=a1b35ac1d61f46a131c\n關閉網頁後連結將失效', delete_after=600 )
        await asyncio.sleep( slepp_time )
        embed = discord.Embed( title="#0000 No.00017", description='毫米波雷達資訊', color=0xa3b4d5, timestamp=dt.datetime.now() )
        #embed.set_author( name=member.display_name, icon_url=member.avatar_url )
        embed.add_field( name='mmWave Sensor Number', value="```py\n0000\n```", inline=True )
        embed.add_field( name='state', value="```css\nno detect\n```", inline=True )
        embed.add_field( name='point change', value="```diff\n+4\n```", inline=True )
        embed.add_field( name='camera state', value='off', inline=True )
        embed.add_field( name='daily alert count', value='0', inline=True )
        embed.add_field( name='Opti', value='NO', inline=True )
        embed.set_footer( text="Cado" )
        await ctx.send( '目前資訊', embed=embed, delete_after=600 )
        await asyncio.sleep( slepp_time )
        embed = discord.Embed(
            title='功能說明', description='以下為主要功能，呼叫此頁面請使用`c!feature`', color=0xa3b4d5, timestamp=dt.datetime.now() )
        #embed.set_author( name=member.display_name, icon_url=member.avatar_url )
        embed.add_field( name='`c!register`', value='註冊', inline=False )
        embed.add_field( name='`c!setting`', value='群組設定', inline=False )
        embed.add_field( name='`c!STATS`', value="毫米波雷達資訊", inline=False )
        embed.add_field( name='`c!camera on/off`', value='手動開關攝影機', inline=False )
        embed.add_field( name='`c!website`', value='生成網頁操作介面連結', inline=False )
        embed.add_field( name='`c!alert on/off`', value='開關警報，若關閉將不警告', inline=False )
        embed.set_footer( text="Cado" )
        await ctx.send( '目前開放功能', embed=embed, delete_after=600 )

    @commands.command( name="atme", aliases=[ 'a' ] )
    async def atme( self, ctx: commands.Context, msg: str ):
        await asyncio.sleep( 5 )
        embed = discord.Embed(
            title='已經於12.24開始錄影',
            description='雷達偵測到可疑目標，已開啟攝相機進行錄影',
            color=0xa3b4d5,
            timestamp=dt.datetime.now(),
        )
        embed.set_image( url='https://upload.cc/i1/2020/10/02/xPLg2K.png' )
        await ctx.send( msg, embed=embed )


def setup( bot ):
    bot.add_cog( DevCommands( bot ) )
