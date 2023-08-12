import json
from app.interface.style import Color

color = Color()

class Player:
    def __init__(self):
        self.initialized = False
        self.initialize_class_attributes()

    def __repr__(self):
        """Representation of an instance of a class"""
        return f"\n{color.paint('underline', 'Rouge:')}" \
               f"\nName: {self.name}" \
               f"\nAttack power: {self.attack}" \
               f"\nCritical chance: {self.crit_rate}" \
               f"\nDefense rating: {self.defense}" \
               f"\nHealth: {self.health}\n"

    def initialize_class_attributes(self):
        """This method initializes the proper class attributes from a JSON file"""
        if not self.initialized:
            what_to_load = '/Users/jocokiss/Documents' \
                           '/adventure_game_project/app' \
                           '/classes/class_attributes.json'
        else:
            what_to_load = f"/Users/jocokiss/Documents" \
                           f"/adventure_game_project/app" \
                           f"/saved_games/{self.name}.json"
        with open(what_to_load, 'r') as file:
            class_attributes = json.load(file)

        class_name = self.__class__.__name__
        if class_name in class_attributes:
            attributes = class_attributes[class_name]
            self.__dict__.update(attributes)
            self.initialized = True

    def save_attributes_to_json(self):
        player_file = f"/Users/jocokiss/Documents/adventure_game_project/app/saved_games/{self.name}.json"
        print(player_file)
        with open(player_file, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    # region Properties
    """
    NAME
    """
    @property
    def name(self):
        return self.__dict__.get('name')

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__dict__['name'] = value
        else:
            raise ValueError("Name must be string")


    
    """
    ATTACK
    """
    @property
    def attack(self):
        return self.__dict__.get('attack')
    @attack.setter
    def attack(self, value):
        if value > 0:
            self.__dict__['attack'] = value
        else:
            self.__dict__['attack'] = 0
            print("Player critical rate cannot be negative.")
            
    """
    CRIT RATE
    """
    @property
    def crit_rate(self):
        return self.__dict__.get('crit_rate')
    @crit_rate.setter
    def crit_rate(self, value):
        if value > 0:
            self.__dict__['crit_rate'] = value
        else:
            self.__dict__['crit_rate'] = 0
            print("Player critical rate cannot be negative.")
    
    """
    DEFENSE
    """
    @property
    def defense(self):
        return self.__dict__.get('defense')
    @defense.setter
    def defense(self, value):
        if value > 0:
            self.__dict__['defense'] = value
        else:
            self.__dict__['defense'] = 0
            print("Player defense cannot be negative.")

    """
    HEALTH
    """
    @property
    def health(self):
        return self.__dict__.get('health')
    @health.setter
    def health(self, value):
        if value > 0:
            self.__dict__['health'] = value
        else:
            self.__dict__['health'] = 0
            print("Player health cannot be negative.")

    """
    SEX
    """
    @property
    def sex(self):
        return self.__dict__.get('sex')

    @sex.setter
    def sex(self, value):
        if isinstance(value, str):
            self.__dict__['sex'] = value
        else:
            raise ValueError("Sex must be string")
    
    """
    EXPERIENCE
    """
    @property
    def exp(self):
        return self.__dict__.get('exp')
    @exp.setter
    def exp(self, value):
        if value > 0:
            self.__dict__['exp'] = self.exp + value
            print(f"You gained {value} experience!")
        else:
            raise ValueError("Cannon gain negative experience")
        
    """
    LEVEL
    """
    @property
    def level(self):
        return self.__dict__.get('level')

    @level.setter
    def level(self, value):
        if value:
            self.__dict__['level'] = self.level + 1
            print(f"You leveled up!")
        else:
            raise ValueError("Cannon gain negative experience")

    """
    GOLD BALANCE
    """
    @property
    def gold_balance(self):
        return self.__dict__.get('gold_balance')
    @gold_balance.setter
    def gold_balance(self, value):
        if value > 0:
            self.__dict__['gold_balance'] = self.gold_balance + value
            print(f"You gained {value} gold!")
        else:
            self.__dict__['gold_balance'] = self.gold_balance - value
        
    """
    CRYSTAL BALANCE
    """
    @property
    def crystal_balance(self):
        return self.__dict__.get('crystal_balance')
    @crystal_balance.setter
    def crystal_balance(self, value):
        if value > 0:
            self.__dict__['crystal_balance'] = self.crystal_balance + value
            print(f"You gained {value} crystal!")
        else:
            self.__dict__['crystal_balance'] = self.crystal_balance - value
            
    """
    UPGRADE MATERIALS
    """
    @property
    def upgrade_materials(self):
        return self.__dict__.get('upgrade_materials')

    @upgrade_materials.setter
    def upgrade_materials(self, value):
        if value > 0:
            self.__dict__['upgrade_materials'] = self.upgrade_materials + value
            print(f"You gained {value} crystal!")
        else:
            self.__dict__['upgrade_materials'] = self.upgrade_materials - value

    #endregion

    # region Skills, Buff/Debuff, Cooldowns
    """    
    def load_skills():
        if attacker.skill_cooldown == {} and attacker.status_cooldown == {}:
            for skill in skill_set:
                attacker.skill_cooldown[skill['name']] = 0
                attacker.status_cooldown[skill['name']] = 0

    def buff_gain():
        attacker.buffs_and_debuffs.append(ability['skill_buff'])
        attacker.status_cooldown[ability['name']] = ability["skill_buff_duration"]
        print(f"\n{attacker.name} gained {Color.gold}{ability['skill_buff']}{Color.end_of_modification} "
              f"for {ability['skill_buff_duration']} turn")

    def apply_debuff():
        target.buffs_and_debuffs.append(ability['skill_debuff'])
        target.status_cooldown[ability['name']] = ability["skill_debuff_duration"]
        print(
            f"{attacker.name} applied {Color.red}{ability['skill_debuff']}{Color.end_of_modification} on {target.name}"
            f" for {ability['skill_debuff_duration']} turn")

    def decrease_cooldown():
        for key in attacker.status_cooldown:
            if attacker.status_cooldown[key] <= 0:
                attacker.status_cooldown[key] = 0
                for skill in skill_set:
                    if skill['skill_buff'] in attacker.buffs_and_debuffs and skill['name'] == key:
                        attacker.buffs_and_debuffs.remove(skill['skill_buff'])
                    if skill['skill_debuff'] in attacker.buffs_and_debuffs and skill['name'] == key:
                        attacker.buffs_and_debuffs.remove(skill['skill_debuff'])
            else:
                attacker.status_cooldown[key] -= 1
        for key in attacker.skill_cooldown:
            if attacker.skill_cooldown[key] <= 0:
                attacker.skill_cooldown[key] = 0
            else:
                attacker.skill_cooldown[key] -= 1
                
    """

    # end region

    def __str__(self):
        return str(self.__class__.__name__)

    def __iter__(self):
        attributes = [
            attr for attr in vars(self).items()
            if not attr[0].startswith('__')
        ]
        for attr, value in attributes:
            yield attr, value

    def set_attribute(self, attr, value):
        setattr(self, attr, value)

    def set_name(self):
        name = input("What's your name?: ")
        while not name:
            print("You need to enter a name!")
            name = input("What's your name?: ")
        self.name = name

    def set_sex(self):
        while True:
            sex = input("What's your sex?: ").lower()
            if sex in ['man', 'woman']:
                self.sex = sex
            else:
                print("Invalid sex")

    """
    def he_she(self):
        if self.sex == "Woman":
            return "She"
        return "He"

    def him_her(self):
        if self.sex == "Woman":
            return "her"
        return "him"
        """

