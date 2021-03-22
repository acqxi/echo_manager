#%%
import numpy as np
import random as rd


#%%
class Ability():
    """"""

    def __init__(
            self,
            healthPoint: int = 0,
            skillPoint: int = 0,
            attackValue: int = 0,
            defenseValue: int = 0,
            speedValue: int = 0,
            vectorArray: np.ndarray = None,
            abiType: int = 0 ):
        self.va = np.array( vectorArray ) if vectorArray is not None else np.array(
            [ healthPoint, skillPoint, attackValue, defenseValue, speedValue ] )
        self.type = abiType  # 1 to add, 2 to mul

    @property
    def hp( self ):
        return self.va[ 0 ]

    @property
    def sp( self ):
        return self.va[ 1 ]

    @property
    def atkv( self ):
        return self.va[ 2 ]

    @property
    def defv( self ):
        return self.va[ 3 ]

    @property
    def spdv( self ):
        return self.va[ 4 ]

    def __add__( self, other: any ):
        if isinstance( other, Ability ):
            return Ability( vectorArray=[ i if i > 0 else 0 for i in self.va + other.va ] )
        else:
            raise TypeError( f"{other} is belong Ability" )

    def __iadd__( self, other: any ):
        if isinstance( other, Ability ):
            self.va += other.va
            self.va = np.array( [ i if i > 0 else 0 for i in self.va ] )
            return self
        else:
            raise TypeError( f"{other} is belong Ability" )

    def __mul__( self, other: any ):
        if isinstance( other, Ability ):
            return Ability( vectorArray=self.va * other.va )
        else:
            raise TypeError( f"{other} is belong Ability" )

    def __imul__( self, other: any ):
        if isinstance( other, Ability ):
            self.va = self.va * other.va
            return self
        else:
            raise TypeError( f"{other} is belong Ability" )

    def __str__( self ) -> str:
        return f"{self.hp=}\t{self.sp=}\t{self.atkv=}\t{self.defv=}\t{self.spdv=}"


# %%
class Level():
    """"""

    def __init__( self, name: str = "", exprince: int = 0, threshold: list = [] ):
        self.name = name
        self.th = threshold
        self.exp = exprince

    @property
    def lv( self ):
        for lv, e in enumerate( self.th ):
            if self.exp < e:
                return lv + 1

    @property
    def next_exp( self ):
        return self.th[ self.lv - 1 ] - self.exp

    def __add__( self, other ):
        if isinstance( other, ( int, float ) ):
            if ( texp := self.exp + other ) > self.th[ -1 ]:
                raise OverflowError( f"exp over than this need({texp}>{self.th[-1]})" )
            else:
                self.exp = texp

    def __str__( self ) -> str:
        return f"{self.name= }\t{self.exp= }\t{self.lv= }\t{self.th= }"


# %%
class GUI():
    """"""

    ENTITY_TYPE = [ '⬛', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '👹' ]

    def __init__( self ):
        pass

    @staticmethod
    def utfBar( cur: int = 0, max: int = 0 ) -> str:
        component = [ '▉', '▊', '▋', '▍', '▎', '▏', '　' ]

        if cur <= 0:
            return '[　　　　　　　　　　]'
        elif cur == max:
            return '[▉▉▉▉▉▉▉▉▉▉]'
        return "[" + component[ 0 ] * ( cur * 10 // max ) + component[ 6 - (
            ( cur % 10 ) * 6 // 10 ) ] + component[ -1 ] * ( 9 - ( cur * 10 // max ) ) + "]"

    @staticmethod
    def emojiBar( cur: int = 0, max: int = 0, line: int = 5 ) -> str:
        component = {
            5: [ '🟦', '🟩', '🟨', '🟧', '🟥', '⬛' ],
            4: [ '🟦', '🟩', '🟨', '🟥', '⬛' ],
            3: [ '🟦', '🟨', '🟥', '⬛' ],
            2: [ '🟦', '🟥', '⬛' ],
            1: [ '🟦', '⬛' ]
        }[ line ]
        bar_length = 8
        color_count = len( component ) - 1
        if cur <= 0:
            return '[' + '⬛' * bar_length + ']'
        elif cur == max:
            return '[' + '🟦' * bar_length + ']'

        color = color_count - 1 - ( fs := cur * color_count // max )
        le_Sep = ( cur - round( max / color_count * fs ) )
        numbr = le_Sep * bar_length // ( max // color_count )
        bar = component[ color ] * numbr + component[ color + 1 ] * ( bar_length - numbr )

        return '[' + ( bar if bar != '⬛' * bar_length else component[ -2 ] + '⬛' * ( bar_length - 1 ) ) + ']'

    @staticmethod
    def map( entitys: list = [] ) -> str:
        ROW = 5
        COL = 7
        ENTITY_TYPE = GUI.ENTITY_TYPE
        map_list = [ 0 for x in range( ROW * COL ) ]
        for i in entitys:
            map_list[ i[ 1 ] ] = i[ 0 ]
        print( map_list )
        return '\n'.join(
            [ ''.join( [ ENTITY_TYPE[ map_list[ i + j * COL ] ] for i in range( COL ) ] ) for j in range( ROW ) ] )


# %%
class SimpleAvatar():
    """"""

    def __init__( self, name, curAbi: Ability, maxAbi: Ability ):
        self.name = name
        self.ca = curAbi
        self.ma = maxAbi


def Probability( target, pool, other: float = 0 ):
    return rd.randint( 1, 10000 ) < ( target * 10000 // pool ) * ( 1 + other )


# %%
