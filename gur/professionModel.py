from .lowLevel import Level


class ProfessionBase():
    """"""


class professionBasic1( ProfessionBase ):
    """
    villager
    - 特徵
        - 等級上限 : 10
        - 種族限制 : 無
        - 前置職業 : 無
        - 職業經驗冪 :  3 5 8 13 21 34 55 89 144 233
    - 職業技能
        - ( 1 ) 被動 → 探測怪物屬性( 只能得到名稱等級)
            - [ 玩家名稱 ]發現了敵人 !
        - ( 2 )村民蓄力直拳 80% ATK 1 SP
            - [ 玩家名稱 ]用力揍了[敵人名稱]一拳 !
        - ( 5 )基礎包紮 回復 10 * P.LV % P.HP (2 SP)
            - [ 玩家名稱 ]用拙劣的包紮技巧稍稍治療了[隊友名稱] !
        - ( 10 )村民KTV  場上村民總等級大於15 全體P.ATK 翻5倍 兩回合 ( 5 SP)
            - [ 玩家名稱 ]突然唱起兩隻老虎，場上鄉愁的村民氣勢大增！
    - 職業屬性 P.S
        - HP:  10 * LV
        - SP:   2 + LV
        - ATK:  10
        - DEF:  0
        - SPD:  0
    """

    name = '村民'
    max_lv = 10
    th = [ 3, 5, 8, 13, 21, 34, 55, 89, 144, 233 ]

    def __init__( self, age ):
        self.lvm = Level( name=self.name, threshold=self.th )
