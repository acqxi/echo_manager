import discord
from discord.ext import commands
import sys
import os
import json
import datetime as dt
import asyncio
import logging
import logging.handlers
import pandas as pd
import random as rd

FORMAT = '%(asctime)s %(levelname)s: %(message)s'

logging.basicConfig( level=11, format=FORMAT, stream=sys.stdout )


class player_state():
    '''init state'''

    def __init__( self, name: str = 'p unknown', ethnic: str = '人類', equipment: int = 0, mode: int = 1 ):
        self.name = name
        self.ethnic = ethnic
        self.equipment = equipment

        if False:
            pass
        else:
            self.hp_max = 100

        self.hp = self.hp_max
        self.hp_last = self.hp

    def get_last( self, porp: str ) -> int:
        '''hp mp'''
        if porp == 'hp':
            change = self.hp - self.hp_last
            self.hp_last = self.hp
            return change

    def hp_edit( self, minus: int = 0, plus: int = 0 ) -> str:
        if minus != 0:
            self.hp -= minus
        if plus != 0:
            self.hp += plus
            if self.hp >= self.hp_max:
                self.hp = self.hp_max
                return 'your hp is full\n'


class BattleField():

    inv = { 0: 1, 1: 0 }

    def __init__( self, p1name: str = 'player 1', p2name: str = 'player 2' ):
        self.p1 = player_state( name=p1name )
        self.p2 = player_state( name=p2name )

    def get_data( self, entity: player_state() ) -> ( str, str, str ):

        def graph( now: int, ma: int ):
            component = [ '▉', '▊', '▋', '▍', '▎', '▏', '　' ]
            if now == ma:
                return '[▉▉▉▉▉▉▉▉▉▉]'
            if now <= 0:
                return '[　　　　　　　　　　]'
            return "[" + component[ 0 ] * ( now * 10 // ma ) + component[ 6 - (
                ( now % 10 ) * 6 // 10 ) ] + component[ -1 ] * ( 9 - ( now * 10 // ma ) ) + "]"

        player = f"@{entity.ethnic}\n'{entity.equipment}"
        state = f"HP：{graph(now=entity.hp,ma=entity.hp_max)} {entity.hp}\\{entity.hp_max}\n"
        state += f"MP：{graph(now=0,ma=100)} 0\\1\n"
        state += "State {}"
        hp_change = entity.get_last( 'hp' )
        hp_change = ( '+' if hp_change >= 0 else '' ) + str( hp_change )
        mp_change = '+0'
        this_turn = f"{hp_change} HP\n{mp_change} MP"
        return player, state, this_turn

    def battle( self, p1a: str, p2a: str ) -> ( str, list ):  #a action
        anno, result = '', [ False, '' ]

        p1, p2 = self.p1, self.p2

        #for initiator,recipient in [(self.state[0],self.state[1]),(self.state[1],self.state[0])]:

        if p1a.startswith( 'a' ):
            anno += f"{p1.name} 發起了攻勢，"
            anno += self.attack( assaulter=p1, recipient=p2, attack='' if p1a == 'a' else p1a[ 1: ], defense=p2a )
        elif p2a.startswith( 'a' ):
            anno += f"{p2.name} 發起了攻勢，"
            anno += self.attack( assaulter=p2, recipient=p1, attack='' if p2a == 'a' == 1 else p2a[ 1: ], defense=p1a )

        for player, act in [ ( p1, p1a ), ( p2, p2a ) ]:
            if act.startswith( 'r' ):
                anno += self.recure( user=player, act='' if act == 'r' else act[ 1: ] )

        if p1.hp <= 0 or p2.hp <= 0:
            result = [ True, '雙雙死亡' if p1.hp <= 0 and p2.hp <= 0 else self.who_is_winner() ]

        if anno == '':
            anno = '雙方面面相覷，啥事也沒幹XDD'

        return anno, result

    def who_is_winner( self ):
        if self.p1.hp > self.p2.hp:
            return self.p1.name
        elif self.p1.hp < self.p2.hp:
            return self.p2.name
        else:
            return '平手'

    def recure( self, user: player_state(), act: str ) -> str:
        anno = ''
        mai = '0' if act == '' else act[ 0 ]
        sub = '0' if len( act ) != 2 else act[ 1 ]

        sub = sub

        if mai == '0':  #藥水
            sub_r = rd.randint( 0, 99 )
            sub_r = 3 - [ sub_r % 99, sub_r % 10, sub_r % 2, 0 ].index( 0 )
            anno += f" {user.name} 不慌不忙地從X拉B夢的百寶袋拿出了 {['小回復劑','中回復劑','大回復劑','天使加百列歌頌過的聖水'][sub_r]} 並服用下去 !!\n"
            heal = rd.randint( *[ ( 1, 10 ), ( 10, 20 ), ( 20, 50 ), ( 100, 10**10 ) ][ sub_r ] )
            user.hp_edit( plus=heal )
            return anno + f" {user.name} 回復了 {heal} HP {'!'*(sub_r*2)}\n"
        else:
            return anno + f" {user.name} 一時手忙腳亂，搞的一團糟，HP也沒回到 !!\n"

    def attack( self, assaulter: player_state(), recipient: player_state(), attack: str, defense: str ) -> str:

        a_mai = '0' if attack == '' else attack[ 0 ]
        a_sub = '0' if len( attack ) != 2 else attack[ 1 ]
        a_sub_r = 0

        d_act = defense[ 0 ]
        d_mai = '0' if len( defense ) != 2 else defense[ 1 ]
        d_sub = '0' if len( defense ) != 3 else defense[ 2 ]
        d_sub_r = 0

        normal_damage = [ ( 0, 30 ), ( 25, 70 ), ( 40, 99 ) ]

        anno = ''
        ori_atk = 0
        ori_atk_d = 0

        if a_mai == '0':  # normal attack

            a_sub_r = rd.randint( 0, 2 ) if len( attack ) == 1 else int( a_sub )
            anno += f"他迅速的攻擊 {recipient.name} 的 {['無關緊要的地方','四肢','要害'][a_sub_r%3]} !!\n"
            ori_atk = rd.randint( *normal_damage[ a_sub_r % 3 ] )

            logging.log( 13, f"{ori_atk=}" )
        else:
            anno += "他手忙腳亂的不知道在幹嘛，然後把拳頭打到自己的臉上啦 (hp-1)~~~\n"
            a_sub_r = -1
            ori_atk_d = 1

        if d_act == 'd':
            if d_mai == '0':
                d_sub_r = rd.randint( 0, 2 ) if len( defense ) < 3 else int( d_sub )
                anno += f"{recipient.name} 被突如其來的攻擊嚇到，趕緊將 {['無關緊要的地方','四肢','要害'][d_sub_r%3]} 防禦住 !!\n"

                if a_sub_r == -1:
                    anno += f"攻擊並未到來， {recipient.name} 漂亮的防守了一個寂寞\n"
                elif d_sub_r == a_sub_r:
                    ori_atk = int( ori_atk / ( rd.randint( 20, 40 ) / 10 ) )
                    anno += f"{recipient.name} 漂亮的預測了 {assaulter.name} 的攻擊，化解了一大半傷害\n"
                else:
                    ori_atk = int( ori_atk / ( rd.randint( 10, 20 ) / 10 ) )
                    anno += f"{recipient.name} 失算了，在最後時刻才勘勘將 {assaulter.name} 的攻擊擋下，減少了一小部分的傷害\n"

                recipient.hp_edit( minus=ori_atk )
                return anno + f"最後 {assaulter.name} 對 {recipient.name} 造成了 {ori_atk} 的傷害 !!\n"
        elif d_act == 'a':
            if d_mai == '0':
                d_sub_r = rd.randint( 0, 2 ) if len( defense ) < 3 else int( d_sub )
                anno += f"{recipient.name} 深知攻擊乃是最好的防禦，將攻勢指向了 {assaulter.name} 的 {['無關緊要的地方','四肢','要害'][d_sub_r%3]} !!\n"

            if a_sub_r == -1:
                anno += f"然而 {assaulter.name} 的攻擊並未到來，反而是 {recipient.name} 趁亂擊中 {assaulter.name}\n"
                ori_atk_d += rd.randint( rd.randint( *( normal_damage[ d_sub_r ][ 0 ] + 25, normal_damage[ d_sub_r ][ 1 ] ) ) )
            elif d_sub_r == a_sub_r:
                ori_atk = rd.randint( 1, 99 )
                ori_atk_d = rd.randint( 1, 99 )
                anno += "雙方的攻擊在空中交錯，導致攻擊偏向了其他部位 !!\n"
            else:
                ori_atk_d = rd.randint( *normal_damage[ d_sub_r ] )

            recipient.hp_edit( minus=ori_atk )
            assaulter.hp_edit( minus=ori_atk_d )

            return anno + f"最後 {recipient.name} 受到了{ori_atk} 的傷害， {assaulter.name} 受到了{ori_atk_d} 的傷害 !!\n"
        else:
            recipient.hp_edit( minus=ori_atk )
            return anno + f"面對攻擊 {recipient.name} 沒有做出及時的反應，結實的承受了 {ori_atk} 的傷害 !!!! \n"


class Game( commands.Cog ):
    '''about Game'''

    wait_fight_id = []

    def __init__( self, bot ):
        self.bot = bot
        #self.user_df = pd.DataFrame( { 'hp': 100 } )

    async def cog_check( self, ctx ):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command( name="fight", aliases=[ 'f' ] )
    #@commands.has_permissions( administrator=True )
    async def battle( self, ctx: commands.Context, opponent: discord.Member, turn: int, *actions ):
        fight_id = -1

        interval_time = 5

        #config
        if actions[ -1 ].startswith( '-' ):
            config_set = actions[ -1 ]
            config_item = config_set.split( '-' )[ -1 ].split( '=' )[ 0 ]
            config_value = config_set.split( '=' )[ -1 ]

            if config_item == 'it':
                interval_time = int( config_value )

        for x in range( 10 ):
            if x in self.wait_fight_id:
                continue
            fight_id = x
            self.wait_fight_id.append( x )
            break

        if fight_id == -1:
            await ctx.send( "等待序列已滿" )
            return

        if len( actions ) < turn:
            await ctx.send( f"動作不足 {turn} 個，自動補全為 `防禦(d)`" )
        a = list( actions )
        a.extend( [ 'd' ] * ( turn - len( a ) ) )
        logging.log( 15, f"{a=}" )

        await ctx.send(
            f"請對手在60秒內輸入 **#{fight_id}** 及 { turn} 個反擊動作，並以空格分開，例如\n```fix\n\
            #{fight_id} {' '.join([['a','d','r'][rd.randint(0,2)] for x in range(turn)])}\n```" )
        try:
            response = await self.bot.wait_for(
                'message',
                check=lambda msg: msg.author == opponent and msg.channel == ctx.channel and msg.content.lower().split( ' ' )[
                    0 ] == f"#{fight_id}",
                timeout=60.0 )
        except asyncio.TimeoutError:  #TODO
            await ctx.send( f"戰鬥序列 #{fight_id} 失效" )
            self.wait_fight_id.remove( fight_id )
            return

        op_a = response.content.lower().split( ' ' )[ 1: ]
        logging.log( 15, f"{op_a=}" )
        if len( op_a ) < turn:
            await ctx.send( f"動作不足 {turn} 個，自動補全為 `防禦(d)`" )
        op_a.extend( [ 'd' ] * ( turn - len( op_a ) ) )
        logging.log( 15, f"{op_a=}" )
        this_war_msg = await ctx.send( f'戰鬥開始: {ctx.author.display_name} vs {opponent.display_name}' )

        bf = BattleField( ctx.author.display_name, opponent.display_name )

        for i in range( turn ):
            anno, result = bf.battle( a[ i ], op_a[ i ] )
            await this_war_msg.edit(
                content=anno,
                embed=self.pvp_turn_state_embed(
                    fID=fight_id,
                    describe='this is war!!',
                    p1TurnState=bf.get_data( bf.p1 ),
                    p2TurnState=bf.get_data( bf.p2 ),
                    p1mention=ctx.author.mention,
                    p2mention=response.author.mention,
                    turn=i + 1 ) )
            if result[ 0 ]:
                await ctx.send( f"winner is {result[1]}，戰鬥序列 #{fight_id} 可以再次使用" )
                self.wait_fight_id.remove( fight_id )
                return
            await asyncio.sleep( interval_time )

        await ctx.send( f"winner is {bf.who_is_winner()}，戰鬥序列 #{fight_id} 可以再次使用" )
        self.wait_fight_id.remove( fight_id )
        return

    @staticmethod
    def pvp_turn_state_embed(
        fID: int,
        describe: str,
        p1TurnState: tuple,
        p2TurnState: tuple,
        p1mention: str,
        p2mention: str,
        turn: int,
    ) -> discord.Embed():

        embed = discord.Embed( title=f"#{fID} No.{turn}", description=describe, color=0xa3b4d5, timestamp=dt.datetime.now() )
        #embed.set_author( name=member.display_name, icon_url=member.avatar_url )
        embed.add_field( name='player', value=f"{p1mention}\n```py\n{p1TurnState[ 0 ]}\n```", inline=True )
        embed.add_field( name='state', value=f"```css\n{p1TurnState[ 1 ]}\n```", inline=True )
        embed.add_field( name=f"turn:{turn}", value=f"```diff\n{p1TurnState[ 2 ]}\n```", inline=True )
        embed.add_field( name='player', value=f"{p2mention}\n```py\n{p2TurnState[ 0 ]}\n```", inline=True )
        embed.add_field( name='state', value=f"```css\n{p2TurnState[ 1 ]}\n```", inline=True )
        embed.add_field( name=f"turn:{turn}", value=f"```diff\n{p2TurnState[ 2 ]}\n```", inline=True )
        embed.set_footer( text="Cado" )

        return embed


def setup( bot ):
    bot.add_cog( Game( bot ) )
