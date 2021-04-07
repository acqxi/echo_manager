import asyncio
import enum
import random as rd
from typing import List, Tuple, Union

import discord
from discord.ext import commands

RANDOM_VALUE = 15
MONSTER_TIME = 3


class Monster():
    """"""

    def __init__( self, name='enemyA', hp=100 ):
        self.name = name
        self.hp = hp
        self.sp = 0

    def is_alive( self ):
        return self.hp > 0

    def action( self, command: str ) -> Tuple[ bool, int ]:
        if command == 'a':
            return True, rd.randint( 1, RANDOM_VALUE * MONSTER_TIME )
        elif command == 'r':
            return True, -1 * rd.randint( 1, RANDOM_VALUE )
        else:
            return False, 0


class Player():
    """"""

    def __init__( self, userObj: discord.Member, name, hp=100, sp=15 ):
        self.uo = userObj
        self.name = name
        self.hp = hp
        self.sp = sp

    def action( self, command: str ) -> Tuple[ bool, int ]:
        if command == 'a':
            return True, rd.randint( 1, RANDOM_VALUE )
        elif command == 'r':
            if self.sp < 4:
                return False, 1
            self.sp -= 4
            return True, -1 * rd.randint( 1, RANDOM_VALUE )
        else:
            return False, 0

    def is_alive( self ):
        return self.hp > 0


class Battle():
    """"""

    def __init__( self, our: List[ Player ], enemy: List[ Monster ] ):
        self.our = our
        self.ene = enemy
        self.who_win = None
        self.our_loss = 0
        self.ene_loss = 0

    def kia( self ) -> str:  #killed in action
        anno = ''
        for entity in self.our:
            if not entity.is_alive():
                self.our.remove( entity )
                anno += f"[{entity.name}] 傷重不治，死時血量:{entity.hp}\n"

        for entity in self.ene:
            if not entity.is_alive():
                self.ene.remove( entity )
                anno += f"[{entity.name}] 傷重不治，死時血量:{entity.hp}\n"

        return anno

    @property
    def is_gameover( self ) -> Union[ str, bool ]:
        if not self.our:
            self.who_win = '魔物'
            return True
        elif not self.ene:
            self.who_win = '我們'
            return True
        else:
            return False

    def __iter__( self ):
        return self

    def __next__( self ) -> Tuple[ List[ Union[ Player, Monster ] ], str ]:
        anno = self.kia()

        if self.is_gameover:
            raise StopIteration
        return self.our + self.ene, anno

    def send_damege( self, attacker: Union[ Player, Monster ], taker: Union[ Player, Monster ], action: str ) -> str:
        succ, dhp = attacker.action( action )
        if not succ:
            return [ '', f"[{attacker.name}]錯估了自己的SP存量，發動技能失敗。" ][ dhp ]

        taker.hp -= dhp

        if taker in self.our:
            self.our_loss += dhp
        else:
            self.ene_loss += dhp

        act_int = { 'a': 0, 'r': 1 }[ action ]
        val_int = { 'a': dhp, 'r': -1 * dhp }[ action ]
        return f"[{attacker.name}]對[{taker.name}]使用了[{['攻擊]，使其損失','治癒]，使其回復'][act_int] + str( val_int )}血量。"


class RPG( commands.Cog ):
    """"""

    def __init__( self, bot: commands.Bot ) -> None:
        super().__init__()
        self.bot = bot

    def cog_check( self, ctx ):
        return super().cog_check( ctx )

    @commands.command( name='rpg' )
    async def rpg( self, ctx: commands.Context, *args: str ):
        players_list_obj = [ ctx.author ]

        if args:
            print( args )
            for arg in args:
                if arg.startswith( '<@' ):
                    print( 'a person' )
                    players_list_obj.append( ctx.guild.get_member( eval( arg.strip( '<@!>' ) ) ) )

        if len( players_list_obj ) > 1:
            players_list_str = ' 、 '.join( [ member.mention for member in players_list_obj ] )
            players_list_set = set( players_list_obj )
            players_acc_set = set()
            head_msg = await ctx.send( f"請問玩家 {players_list_str} 是否要與玩家 {ctx.author.mention} 玩RPG，是請按⭕反應本段文字，30秒內未反應則邀請失效" )
            [ await head_msg.add_reaction( emoji ) for emoji in [ '⭕', '❌' ] ]
            for player in players_list_set:
                try:
                    reaction, user = await self.bot.wait_for(
                        event='reaction_add',
                        check=lambda r, u: u in players_list_set.difference( players_acc_set ) and r.emoji in [ '⭕', '❌' ] and r
                        .message == head_msg,
                        timeout=30 )
                except asyncio.TimeoutError as e:
                    await head_msg.edit( content=f"玩家{ctx.author.mention}向玩家{players_list_str}發起的戰鬥邀請失效{e}" )
                    return
                if reaction.emoji == '⭕':
                    players_acc_set.add( user )
                else:
                    await head_msg.edit( content=f"玩家{ctx.author.mention}向玩家{players_list_str}發起的戰鬥邀請被拒絕" )
                    return

        battle = Battle(
            our=[ Player( player, name=player.nick, hp=100 ) for player in players_list_obj ], enemy=[ Monster() ] )
        for entities, anno in battle:

            await ctx.send(
                anno + '\n'.join(
                    [ f"實體( {id} )=>名字：{v.name[:3]+v.name[-3:]:^5}，hp：{v.hp}，sp：{v.sp}" for id, v in enumerate( entities ) ] ) )
            anno2 = ''
            for entity in entities:
                if isinstance( entity, Player ):
                    await ctx.send( f"輪到[{ entity.uo.mention }]決定攻擊動作。", delete_after=30 )
                    try:
                        response_msg: discord.Message = await self.bot.wait_for(
                            event='message', check=lambda msg: msg.author == entity.uo, timeout=30 )
                    except asyncio.TimeoutError:
                        continue

                    r_args: Tuple[ str ] = response_msg.content.split()
                    if r_args[ 0 ] not in [ 'a', 'r' ]:
                        #await response_msg.delete()
                        anno2 += entity.uo.mention + '放棄了此次攻擊\n'
                        continue
                    if not r_args[ 1 ].isnumeric() or eval( r_args[ 1 ] ) not in range( len( entities ) ):
                        #await response_msg.delete()
                        anno2 += entity.uo.mention + '放棄了此次攻擊\n'
                        continue
                    anno2 += battle.send_damege(
                        attacker=entity, taker=entities[ eval( r_args[ 1 ] ) ], action=r_args[ 0 ] ) + '\n'
                    #await response_msg.delete()
                elif isinstance( entity, Monster ):
                    num_of_alive_p = len( [ e for e in entities if isinstance( e, Player ) ] )
                    anno2 += battle.send_damege(
                        attacker=entity, taker=entities[ rd.randint( 0, num_of_alive_p - 1 ) ], action='a' ) + '\n'

            await ctx.send( anno2 )

        await ctx.send( f"[ {battle.who_win} ]獲得了最終的勝利\n我方承受了{ battle.our_loss }點傷害，並造成了敵方{ battle.ene_loss }點傷害。" )


def setup( bot: commands.Bot ):
    bot.add_cog( RPG( bot=bot ) )
