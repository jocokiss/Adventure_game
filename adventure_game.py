"""
2:  Spend gold for upgrading weapon and gear(do not
    exist yet) DONE, GEAR UPDATE REMAINS

3: Add some kind of base ability set for enemies, +specials for bigger ones and bosses

4: Add more abilities and some sort of healing

    ---INGAME CURRENCY, AND ARMOR UPGRADE REMAINS.---

"""

<<<<<<< HEAD
#NEW BRANCH
=======
#EZT KÉNE ÁTRAKNI
>>>>>>> master

import json
import random
from collections import defaultdict

player_stats = {"name": None,
                "class": None,
                "sex": None,
                "experience": 0,
                "level": 0,
                "gold_balance": 0,
                "crystal_balance": 0,
                "upgrade_materials": 0,
                "damage": 0,
                "crit": 0,
                "defense": 0,
                "health": 0}


class Color:
    pink = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    gold = '\033[93m'
    red = '\033[91m'
    end_of_modification = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


class Player:
    def __init__(self, name, sex, attack, crit, defense, health):
        self.name = name
        self.sex = sex
        self.attack = attack
        self.defense = defense
        self.critical_chance = crit

        self.max_health = health
        self.health = health

        self.buffs_and_debuffs = []
        self.status_cooldown = {}
        self.skill_cooldown = {}

        self.info = None
        self.inventory = None
        self.equipment = None

    def he_she(self):
        if self.sex == "Woman":
            return "She"
        else:
            return "He"

    def him_her(self):
        if self.sex == "Woman":
            return "her"
        else:
            return "him"

    def info_inventory_or_equipment(self, info_inventory_or_equipment):
        with open(player_json_file, "r") as f:
            player = json.load(f)

            """
            player_info = player["Player info"]
            player_inventory = player["Player inventory"]
            player_equipment = player["Player equipment"]
            """

        if info_inventory_or_equipment == "info":
            self.info = player["Player info"]
            return self.info

        if info_inventory_or_equipment == "inventory":
            self.inventory = player["Player inventory"]
            return self.inventory

        if info_inventory_or_equipment == "equipment":
            self.equipment = player["Player equipment"]
            return self.equipment


class Rouge(Player):
    def __init__(self, name, sex, attack, crit, defense, health):
        super().__init__(name, sex, attack, crit, defense, health)
        self.combo_points = {'count': 0}
        self.max_health = health

    def add_combo_points(self, points_to_add):
        self.combo_points['count'] += points_to_add
        if self.combo_points['count'] >= 5:
            self.combo_points['count'] = 5


class Enemy(Player):
    def __init__(self, name, sex, attack, crit, defense, health):
        super().__init__(name, sex, attack, crit, defense, health)
        self.critical_chance = crit
        self.max_health = health

        self.buffs_and_debuffs = []
        self.status_cooldown = {}
        self.skill_cooldown = {}


def new_game_or_load():
    new_or_load = input("Would you like to start a New game or Load an existing one? N/L:  ").lower()
    if new_or_load == "n":
        new_character = character_creation()
        return new_character
    if new_or_load == "l":
        while True:
            save_file = input("\nPlease type in the name of your saved character: ")
            saved_game = save_file + ".json"
            try:
                with open(saved_game, "r") as file:
                    player_save_game = json.load(file)
                    return player_save_game
            except FileNotFoundError:
                print("No saved game with this name found")
                continue


def character_creation():
    player_stats_copy = player_stats

    warrior = Player(" ", " ", 12, 10, 30, 200)
    rouge = Player(" ", " ", 10, 30, 20, 160)
    print(f"\nChoose your class!\n"
          f"{Color.underline}{Color.bold}Warrior:{Color.end_of_modification}\n"
          f"\nAttack power: {warrior.attack}"
          f"\nCritical chance: {warrior.critical_chance}"
          f"\nDefense rating: {warrior.defense}"
          f"\nHealth: {warrior.health}\n"
          f"\n{Color.underline}{Color.bold}Rouge:{Color.end_of_modification}\n"
          f"\nAttack power: {rouge.attack}"
          f"\nCritical chance: {rouge.critical_chance}"
          f"\nDefense rating: {rouge.defense}"
          f"\nHealth: {rouge.health}\n")

    def character_creating():
        run = True
        while run:
            class_list = ["warrior", "rouge"]
            sex_list = ["man", "woman"]
            c_class = input("Which class do you choose?: ").lower()
            sex = input("Man or Woman?: ").lower()
            if c_class not in class_list:
                print("invalid class.")
                continue
            if sex not in sex_list:
                print("invalid sex. (it's risky i know)")
                continue

            name = input("What is your character's name?: ")

            player_stats_copy["name"] = name
            player_stats_copy["class"] = c_class
            player_stats_copy["sex"] = sex

            if c_class == "warrior":
                return Player(name, sex, 12, 10, 30, 200)
            if c_class == "rouge":
                return Rouge(name, sex, 10, 30, 20, 160)

    new_character = character_creating()

    player_stats_copy["damage"] = new_character.attack
    player_stats_copy["crit"] = new_character.critical_chance
    player_stats_copy["defense"] = new_character.defense
    player_stats_copy["health"] = new_character.health

    json_name = new_character.name + ".json"
    final_player_stat = {"Player info": player_stats_copy, "Player inventory": [],
                         "Player equipment": []}
    with open(json_name, "w") as file:
        json.dump(final_player_stat, file, indent=4)
        file.close()

    return final_player_stat


def hero_stats_from_json():
    hero_file = new_game_or_load()
    hero_stats = hero_file["Player info"]
    if hero_stats["class"] == "rouge":
        return Rouge(hero_stats["name"], hero_stats["sex"], hero_stats["damage"], hero_stats["crit"],
                     hero_stats["defense"], hero_stats["health"]), hero_stats, hero_stats["class"]
    if hero_stats["class"] == "warrior":
        return Player(hero_stats["name"], hero_stats["sex"], hero_stats["damage"], hero_stats["crit"],
                      hero_stats["defense"], hero_stats["health"]), hero_stats, hero_stats["class"]


hero, hero_attributes, hero_class = hero_stats_from_json()
player_json_file = hero.name + ".json"


def combat(attacker, target):
    skip_turn = {
        'name': 'Skip turn',
        'hotkey': 'skip',
        'description': 'Skip your turn',
        'skill_type': None,
        'skill_requirement': None,
        'skill_cooldown': None,
        'skill_debuff': None,
        'skill_debuff_duration': None,
        'skill_buff': None,
        'skill_buff_duration': None,
        'critical_modifier': attacker.critical_chance,
        'damage_modifier': attacker.attack
    }

    class_abilities = hero_class + " abilities"

    skill_list = []

    with open("item_and_ability_collection.json", "r") as f:
        item_and_ability_collection = json.load(f)
        class_ability_list = item_and_ability_collection[class_abilities]

    for ability in class_ability_list:
        skill_list.append(ability)

    skill_set = tuple(skill_list)

    def load_skills():
        if attacker.skill_cooldown == {} and attacker.status_cooldown == {}:
            for skill in skill_set:
                attacker.skill_cooldown[skill['name']] = 0
                attacker.status_cooldown[skill['name']] = 0

    def buff_gain():
        attacker.buffs_and_debuffs.append(ability['skill_buff'])
        attacker.status_cooldown[ability['name']] = ability["skill_buff_duration"]
        print(f"{attacker.name} gained {Color.gold}{ability['skill_buff']}{Color.end_of_modification} "
              f"for {ability['skill_buff_duration']} turn\n")

    def apply_debuff():
        target.buffs_and_debuffs.append(ability['skill_debuff'])
        target.status_cooldown[ability['name']] = ability["skill_debuff_duration"]
        print(
            f"{attacker.name} applied {Color.red}{ability['skill_debuff']}{Color.end_of_modification} on {target.name} for "
            f"{ability['skill_debuff_duration']} turn")

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

    def choose_ability():
        choose = True
        if attacker == hero:
            while choose:
                for skill in skill_set:
                    if attacker.skill_cooldown[skill['name']] > 0:
                        print(f"{Color.red}{skill['name']} '{skill['hotkey']}', CD",
                              f"{attacker.skill_cooldown[skill['name']]}{Color.end_of_modification}",
                              sep=' : ', end=' | ', flush=True)
                    else:
                        print(f"{skill['name']} '{skill['hotkey']}', CD", attacker.skill_cooldown[skill['name']],
                              sep=' : ', end=' | ', flush=True)
                print("\nIf you want to skip your turn, type 'skip' ")
                print("-----------------------------------------------------")
                skill_choice = input('\nChoose which ability to use: ')

                if skill_choice == skip_turn['hotkey']:
                    return skip_turn

                for skill in skill_set:
                    if skill_choice == skill['hotkey'] and attacker.skill_cooldown[skill['name']] == 0:
                        return skill
                else:
                    for key in attacker.skill_cooldown:
                        if attacker.skill_cooldown[key] > 0:
                            print(f"Ability is on cooldown for {attacker.skill_cooldown[key]} turn\n")

        else:
            enemy_set = (class_ability_list[0], class_ability_list[1], class_ability_list[2], class_ability_list[3])
            choice = random.choice(enemy_set)
            pick = True
            while pick:

                if 'stealth' in target.buffs_and_debuffs and choice['skill_type'] == 'physical':
                    for skill in enemy_set:
                        if skill['skill_type'] != 'physical' and attacker.skill_cooldown[skill['name']] == 0:
                            return skill
                    else:
                        return skip_turn

                for skill in enemy_set:
                    if choice == skill and choice['skill_requirement'] is not None:
                        if choice['skill_requirement'] in attacker.buffs_and_debuffs:
                            attacker.buffs_and_debuffs.remove(choice['skill_requirement'])
                            return skill
                        else:
                            choice = random.choice(enemy_set)

                    if choice == skill and attacker.skill_cooldown[skill['name']] == 0:
                        return skill

                    else:
                        choice = random.choice(enemy_set)

    run = True
    load_skills()
    she_or_he = attacker.he_she()
    her_or_him = target.him_her()
    decrease_cooldown()

    if attacker == hero:
        print("-----------------------------------------------------")
        print(f"{attacker.name} [{attacker.health}/{attacker.max_health}]                                      "
              f"{target.name} [{target.health}/{target.max_health}]\n"
              f"Combo points: {Color.gold}{attacker.combo_points['count'] * '* '}{Color.end_of_modification}\n"
              f"Buffs and debuffs: {attacker.buffs_and_debuffs}\n")

    ability = choose_ability()

    # TODO: CHANGE ABILITY DAMAGE FROM STATIC INTO PERCENTAGE

    while run:

        if ability == skip_turn:
            print(f'{attacker.name} skipped a turn\n')
            break

        if 'stun' in attacker.buffs_and_debuffs:
            print(f"{attacker.name} is stunned. {she_or_he} cannot attack this turn\n")
            break

        if 'stealth' in target.buffs_and_debuffs and ability['skill_type'] == 'physical':
            if attacker == hero:
                print(f'{target.name} is stealthed! Physical attacks wont work on {her_or_him}!\n')
            ability = choose_ability()

        else:

            if ability['skill_type'] == 'buff':
                buff_gain()
                attacker.skill_cooldown[ability['name']] = ability['skill_cooldown']
                return ability

            if ability['skill_type'] == 'combo':
                combo_lib = {
                    1: '1_point_damage',
                    2: '2_point_damage',
                    3: '3_point_damage',
                    4: '4_point_damage',
                    5: '5_point_damage'
                }

                if attacker.combo_points['count'] > 0:
                    variant = combo_lib[attacker.combo_points['count']]
                    critical_chance = ability['critical_modifier']
                    attack_power = int((ability[variant] + attacker.attack) * ((100 - target.defense) / 100))
                    crit = random.randint(0, 100)

                    if crit <= critical_chance:
                        print(f"\n{Color.red}CRITICAL STRIKE!{Color.end_of_modification}\n{Color.bold}{attacker.name} "
                              f"used {ability['name']} and dealt {attack_power * 2} damage!{Color.end_of_modification}")
                        target.health -= (attack_power * 2)

                    if crit > critical_chance:
                        print(f"\n{Color.bold}{attacker.name} used {ability['name']} "
                              f"and dealt {attack_power} damage!{Color.end_of_modification}")
                        target.health -= attack_power

                    attacker.combo_points['count'] = 0
                    return target.health

                else:
                    print("Requires combo points to use\n")
                    ability = choose_ability()

            if ability['skill_type'] == 'physical':

                if ability['skill_requirement'] is not None:
                    if ability['skill_requirement'] in attacker.buffs_and_debuffs:
                        attacker.buffs_and_debuffs.remove(ability['skill_requirement'])
                    else:
                        if attacker == hero:
                            print(f"{ability['name']} requires {ability['skill_requirement']} to use")
                        ability = choose_ability()

                if "stealth" in attacker.buffs_and_debuffs:
                    attacker.buffs_and_debuffs.remove('stealth')

                critical_chance = ability['critical_modifier']
                attack_power = int((ability['damage_modifier'] + attacker.attack) * ((100 - target.defense) / 100))
                crit = random.randint(0, 100)

                if crit <= critical_chance:
                    print(f"\n{Color.red}CRITICAL STRIKE!{Color.end_of_modification}\n{Color.bold}{attacker.name} used "
                          f"{ability['name']} and dealt {attack_power * 2} damage!{Color.end_of_modification}")
                    target.health -= (attack_power * 2)

                if crit > critical_chance:
                    print(f"\n{Color.bold}{attacker.name} used {ability['name']} "
                          f"and dealt {attack_power} damage!{Color.end_of_modification}")
                    target.health -= attack_power

                attacker.skill_cooldown[ability['name']] = ability['skill_cooldown']
                if ability['skill_debuff'] is not None:
                    apply_debuff()
                if attacker == hero and ability['resource_generation'] is True:
                    attacker.add_combo_points(ability['resource_gain'])
                return attacker.health, target.health

            else:
                ability = choose_ability()


# class specific weapon types, dual wield, shield, staff ctr...

enemies = {  # ENEMIES INTO JSON AS WELL?? IT WOULD BE HARD TO CODE WITH DAMAGE, HEALTH CTR...
    'grafted_scion': Enemy("Grafted Scion", "Man", 10, 10, 10, 500),
    'glass_orc': Enemy("Glass Orc", "Man", 12, 12, 12, 620),
    'burnt_wisp': Enemy("Burnt Wisp", "Woman", 15, 15, 15, 750),
    'ivory_fairy': Enemy("Ivory Fairy", "Woman", 20, 20, 20, 900),
    'shadow_pixie': Enemy("Shadow Pixie", "Woman", 25, 25, 25, 1300),
    'lava_wraith': Enemy("Lava Wraith", "Man", 30, 30, 30, 1800)
}


def combat_loop(player, enemy):
    print("Let's start\n")

    while True:
        want_to_manage = input("Do you want to manage your inventory? Y/N: ").lower()
        if want_to_manage != "y":
            break
        else:
            inventory_management()

    def player_attributes_update():
        player.attack = player_i["damage"]
        player.crit = player_i["crit"]
        player.defense = player_i["defense"]
        player.health = player_i["health"]

    player_i = Player.info_inventory_or_equipment(player, "info")
    player_attributes_update()
    print(player.attack, player.crit, player.defense, player.health)

    while player.health > 0 or enemy.health > 0:

        combat(hero, enemy)

        if enemy.health > 0:
            combat(enemy, hero)

        if enemy.health <= 0:
            print("Enemy felled!\n")
            print(f"{Color.cyan}You are victorious {player.name}!{Color.end_of_modification}")
            print(f"Health: [{player.health}/{player.max_health}]")
            loot_mechanism()
            return True

        elif player.health <= 0:
            print(f"{Color.red}You died{Color.end_of_modification}")
            return False


def loot_mechanism():
    with open("item_and_ability_collection.json", 'r') as f:
        item_and_ability_collection = json.load(f)
        loot_table = item_and_ability_collection["weapon_and_armor"]
        loot_name = []
        weight = []
        for item in loot_table:
            weight.append(item['drop_rate'])
            loot_name.append(item['name'])
        probability = list(zip(loot_name, weight))
        choices = []
        for item, weight in probability:
            choices.extend([item] * weight)
        loot_roll = random.choice(choices)
        for item in loot_table:
            if item['name'] == loot_roll:
                print(f"{item['name']} acquired!")
                acquired_loot = item

    add_to_inventory(acquired_loot)


def add_to_inventory(item_to_add):
    item_count = 0
    with open(player_json_file, 'r') as f2:
        player_json = json.load(f2)
        player_info = player_json["Player info"]
        player_inventory = player_json["Player inventory"]
        player_equipment = player_json["Player equipment"]

    for item in player_inventory:
        if item == item_to_add:
            item_count += 1

    if item_to_add["type"] == "armor" and item_count == 0 or item_to_add["type"] == "weapon" and item_count < 2:
        player_inventory.append(item_to_add)
        print(f"{item_to_add['name']} placed in inventory")

    else:
        player_info["gold_balance"] += item_to_add['value']
        print(f"Duplicate item! {hero.name} gained {item_to_add['value']} Gold instead")

    updated_player_json = {"Player info": player_info, "Player inventory": player_inventory,
                           "Player equipment": player_equipment}
    with open(player_json_file, 'w') as f3:
        json.dump(updated_player_json, f3, indent=4)


def inventory_management():
    with open(player_json_file, 'r') as f:
        player_json = json.load(f)
        player_info = player_json["Player info"]
        player_inventory = player_json['Player inventory']
        player_equipment = player_json['Player equipment']

    def inventory_item_info(item_in_question):
        print(f"\nRarity: {item_in_question['rarity']}\n"
              f"Slot: {item_in_question['slot']}\n"
              f"Type: {item_in_question['type']}\n"
              f"Value: {item_in_question['value']}\n"
              f"Drop rate: {item_in_question['drop_rate']}\n"
              f"Damage: {item_in_question['damage']}\n"
              f"Crit: {item_in_question['crit']}\n"
              f"Defense: {item_in_question['defense']}\n"
              f"Health: {item_in_question['health']}\n")

    def list_of_inventory_items():
        print(f"\n{Color.underline}INVENTORY{Color.end_of_modification}: ")
        name_list = []
        for stuff in player_inventory:
            name_list.append(stuff['name'])
        d = defaultdict(int)
        name_list.sort()
        for key in name_list:
            d[key] += 1
        for i in d:
            print(f"{i}: ({d[i]})")

        print()

    def list_of_player_stats():
        print(f"\n{Color.underline}PLAYER INFO{Color.end_of_modification}: ")
        print(f"Player name: {player_info['name']}\n"
              f"Class: {player_info['class']}\n"
              f"Experience: {player_info['experience']}\n"
              f"Gold balance: {player_info['gold_balance']}\n"
              f"Crystal balance: {player_info['crystal_balance']}\n"
              f"Upgrade materials: {player_info['upgrade_materials']}\n"
              f"Damage: {player_info['damage']}\n"
              f"Crit: {player_info['crit']}\n"
              f"Defense: {player_info['defense']}\n"
              f"Health: {player_info['health']}\n")

    def list_of_equipment_items():
        print(f"\n{Color.underline}EQUIPMENT{Color.end_of_modification}: ")
        for item in player_equipment:
            print(f"{item['slot']}: {item['name']}")
        print()

    def sell_or_equip():
        chosen_item = input("Choose an item or type 'q' in order to quit the equipment manager ").lower()
        is_it_in_the_inventory = []
        for finding_item in player_inventory:
            if finding_item['name'].lower() == chosen_item:
                is_it_in_the_inventory.append(finding_item)

        if not is_it_in_the_inventory:
            print(f"'{chosen_item}' not found in your inventory")
        else:
            valid_chosen_item = is_it_in_the_inventory[0]
            inventory_item_info(valid_chosen_item)
            run = True
            while run:
                sell_or_equip_the_item = input("Would you like to sell or equip this item?: ")

                if sell_or_equip_the_item == 'sell':
                    player_inventory.remove(valid_chosen_item)
                    player_info["gold_balance"] += valid_chosen_item['value']
                    print(f"{valid_chosen_item['name']} is removed from your inventory!\n"
                          f"{hero.name} gained {valid_chosen_item['value']} Gold!")

                    list_of_player_stats()
                    return

                if sell_or_equip_the_item == 'equip':

                    chosen_item_slot = valid_chosen_item['slot']
                    slot_list = []
                    for i in player_equipment:
                        slot_list.append(i['slot'])

                    if chosen_item_slot not in slot_list:
                        if chosen_item_slot == "Two-hand":
                            for a in player_equipment:
                                if a['slot'] == "Main-hand":
                                    player_equipment.remove(a)
                                    player_inventory.append(a)

                                    player_inventory.remove(valid_chosen_item)
                                    player_equipment.append(valid_chosen_item)

                                    player_stat_update(valid_chosen_item, a)
                                    print(f"{a['name']} unequipped")

                            for b in player_equipment:
                                if b['slot'] == "Off-hand":
                                    player_equipment.remove(b)
                                    player_inventory.append(b)

                                    player_inventory.remove(valid_chosen_item)
                                    player_equipment.append(valid_chosen_item)

                                    player_stat_update(valid_chosen_item, b)
                                    print(f"{b['name']} unequipped")

                            print(f"{valid_chosen_item['name']} equipped!")
                            return

                        if chosen_item_slot == "Two hand" and chosen_item_slot in slot_list:
                            for equipment_item in player_equipment:
                                if equipment_item['slot'].lower() == chosen_item_slot.lower():
                                    player_equipment.remove(equipment_item)
                                    player_inventory.append(equipment_item)
                                    player_inventory.remove(valid_chosen_item)
                                    player_equipment.append(valid_chosen_item)
                                    print(f"{equipment_item['name']} unequipped!"
                                          f"\n{valid_chosen_item['name']} equipped!")

                                    player_stat_update(valid_chosen_item, equipment_item)

                                    break
                        if chosen_item_slot != "Two-hand" and "Two-hand" in slot_list:
                            for i in player_equipment:
                                if i['slot'] == "Two-hand":
                                    player_equipment.remove(i)
                                    player_inventory.append(i)
                                    player_inventory.remove(valid_chosen_item)
                                    player_equipment.append(valid_chosen_item)
                                    print(f"{i['name']} unequipped\n{valid_chosen_item['name']} equipped!")

                                    player_stat_update(valid_chosen_item, i)

                                    break
                            return
                        else:
                            player_inventory.remove(valid_chosen_item)
                            player_equipment.append(valid_chosen_item)
                            print(f"{valid_chosen_item['name']} equipped!")

                            player_stat_update(valid_chosen_item)

                            break
                    else:
                        for equipment_item in player_equipment:
                            if equipment_item['slot'].lower() == chosen_item_slot.lower():
                                player_equipment.remove(equipment_item)
                                player_inventory.append(equipment_item)
                                player_inventory.remove(valid_chosen_item)
                                player_equipment.append(valid_chosen_item)
                                print(f"{equipment_item['name']} unequipped!"
                                      f"\n{valid_chosen_item['name']} equipped!")

                                player_stat_update(valid_chosen_item, equipment_item)

                                break

                        break

                if sell_or_equip_the_item != 'sell' or sell_or_equip_the_item != 'equip':
                    print('Invalid input')
                    continue

    def substract_stats(unequipped_item):

        player_damage = 0
        player_crit = 0
        player_defense = 0
        player_health = 0

        player_damage -= unequipped_item["damage"]
        player_crit -= unequipped_item["crit"]
        player_defense -= unequipped_item["defense"]
        player_health -= unequipped_item["health"]

        return player_damage, player_crit, player_defense, player_health

    def player_stat_update(item_plus, item_minus=0):

        player_damage = 0
        player_crit = 0
        player_defense = 0
        player_health = 0

        if item_minus != 0:
            player_damage -= item_minus["damage"]
            player_crit -= item_minus["crit"]
            player_defense -= item_minus["defense"]
            player_health -= item_minus["health"]

        player_damage += item_plus["damage"]
        player_crit += item_plus["crit"]
        player_defense += item_plus["defense"]
        player_health += item_plus["health"]

        player_info["damage"] += player_damage
        player_info["crit"] += player_crit
        player_info["defense"] += player_defense
        player_info["health"] += player_health

        updated_player_json_file = {"Player info": player_info, "Player inventory": player_inventory,
                                    "Player equipment": player_equipment}

        print(player_info)
        with open(player_json_file, "w") as f2:
            json.dump(updated_player_json_file, f2, indent=4)
            f2.close()

    managing = True
    while managing:
        list_of_player_stats()
        list_of_inventory_items()
        list_of_equipment_items()
        sell_or_equip()
        finished = input("\nAre you finished? Yes or No: ").lower()
        if finished != 'no':
            print("Quitting...")
            break


def loot_tower(attacker):
    values = enemies.values()
    enemy_list = list(values)

    print(enemy_list)

    enemy_count = 0
    run = True
    while run:

        print(enemy_count)

        enemy = enemy_list[enemy_count]

        is_it_a_win = combat_loop(attacker, enemy)
        if is_it_a_win is False:
            break
        else:
            enemy_count += 1
            print(enemy_count)


loot_tower(hero)
