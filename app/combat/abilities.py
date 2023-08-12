class Skill:
    def __init__(self):
        self.name = None
        self.description = None
        self.resource_req = None
        self.resource_gen = None
        self.buff = None
        self.debuff = None


    def __repr__(self):
        return f"{self.name}: {self.description}"

class PhysicalAttack(Skill):
    def __init__(self):
        super().__init__()

    @classmethod
    def normal_attack(cls):
        instance = cls
        instance.name = 'Normal Attack'
        instance.description = 'A simple attack with your equipped weapon.' \
                               'Cost nothing to use, but has the lowest damage as well'
        return instance

class Buff:
    def __init__(self):
        self.name = None
        self.description = None
        self.cooldown = None

class Debuff(Buff):
    def __init__(self):
        super().__init__()
