from gur.lowLevel import Ability, SimpleAvatar


class SkillBase():
    """"""

    def __init__( self, name, spExertion ):
        self.name = name
        self.spe = spExertion


class NorSigAtk( SkillBase ):
    """"""

    def __init__( self, name, spExertion, text, cause: Ability ):
        super().__init__( name, spExertion )
        self.cause = cause
        self.text = text

    def active( self, raider: SimpleAvatar, target: SimpleAvatar ) -> tuple[ Ability, str ]:
        anno = self.text.replace( '[ 玩家名稱 ]', f"[ {raider.name} ]" ).replace( '[ 目標名稱 ]', f"[ {target.name} ]" )
        if self.cause.type == 1:
            return ()