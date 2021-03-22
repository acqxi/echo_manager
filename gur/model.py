class MonsterSlime():
    """史萊姆
    生成：
        神對最弱生物的賜福 > 受到第一次傷害不會致死( 50%HP )
    回合內：
        可以左右移動，
        攻擊：
            普通攻擊 (30+30)%ATK 傷害， 發動機率 50%
            特殊攻擊:
                強力攻擊 (100+50)%ATK ，(2 SP) ，發動機率 45%
                史萊姆聯盟 (50 * 史萊姆個數)%ATK ， (3 SP) ，發動機率 5%
        被動：
            複數史萊姆時可以在特定條件 TODO 下為同伴補血( 10%HP )
    回合外：
        受到攻擊有機率(25%)反擊 (30%)DEM
        血量低於50%時閃避機率30%，
    被擊敗：
        有10%機率造成( 150%ATK )傷害 給敵人
        掉落回復道具( 回血果凍( 10%HP ) )
    回合結束：
        掉落 1 exp

    屬性：
        LV: 1~10
        HP: 20 + 5*LV
        SP: 7
        ATK: 10
        DEF: 0
        SPD: 100

    特性：
        種族:史萊姆
        名稱:史萊姆[AA-ZZ]

    文本：
        被生成時:
            自然:[史萊姆隻數]隻野生的史萊姆出現了！
            被召喚:[噗啾*[史萊姆隻數]!]
            復活:[啪嘰*[史萊姆隻數]!]
        退場:
            擊敗:[名稱]扁掉了!
            存活到戰鬥結束:史萊姆慶祝
        行動:
            普通攻擊:biu~
            強力攻擊:biu!!!
            史萊姆聯盟:piu~
            補血:miu~
            反擊:daui~
            閃避:sha!
            移動:NULL
    """


class player():
    """基礎玩家
    特徵:
        姓名
        職業
        種族
        年齡
    
    """


class Turn():
    """回合形成依據
    行動權劃分：
        敏捷倒數為等待時間
    """


class Battle():
    """戰鬥行為生成依據
    
    """