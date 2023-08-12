"""
1: Color code items, make combat screen more transparent

2: Experience gain, lvl gain, abiliy unlock

3: Add some kind of base ability set for enemies, +specials for bigger ones and bosses

4: Add more abilities and some sort of healing

    ---INGAME CURRENCY REMAINS.---

"""

import json
import random
from collections import defaultdict

from interface.style import Color


def combat(attacker, target): # TODO: COMBAT CLASS


    class_abilities = hero_class + " abilities"

    skill_list = []

    with open("item_and_ability_collection.json", "r") as f:
        item_and_ability_collection = json.load(f)
        class_ability_list = item_and_ability_collection[class_abilities]

    for ability in class_ability_list:
        skill_list.append(ability)

    skill_set = tuple(skill_list)

    def choose_ability():
        choose = True
        if attacker == hero:
            while choose:
                for skill in skill_set:
                    if attacker.skill_cooldown[skill['name']] > 0:
                        print(f" * {Color.red}{skill['name']} '{skill['hotkey']}', CD",
                              f"{attacker.skill_cooldown[skill['name']]}{Color.end_of_modification}",
                              sep=': ', end=' \n', flush=True)
                    else:
                        print(f" * {skill['name']} '{skill['hotkey']}', CD", attacker.skill_cooldown[skill['name']],
                              sep=': ', end=' \n', flush=True)
                print("\nIf you want to skip your turn, type 'skip' ")
                skill_choice = input('Choose which ability to use: ')

                if skill_choice == skip_turn['hotkey']:
                    return skip_turn

                for skill in skill_set:
                    if skill_choice == skill['hotkey'] and attacker.skill_cooldown[skill['name']] == 0:
                        return skill

                else:
                    for key in attacker.skill_cooldown:
                        pairing_skill_and_CD = key.startswith(skill_choice.upper())
                        cooldown_of_skill = attacker.skill_cooldown[key]
                        if cooldown_of_skill > 0 and pairing_skill_and_CD is True:
                            print(f"\n{key} is on cooldown for {attacker.skill_cooldown[key]} turn\n")

        else:
            enemy_set = (class_ability_list[0], class_ability_list[1], class_ability_list[3])

            pick = True
            while pick:
                choice = random.choice(enemy_set)

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
                            break

                    if choice == skill and attacker.skill_cooldown[skill['name']] == 0:
                        return skill

                    else:
                        break

    run = True
    load_skills()
    she_or_he = attacker.he_she()
    her_or_him = target.him_her()
    decrease_cooldown()




    if attacker == hero:

        print("-----------------------------------------------------")
        bar_color = Color.green

        if attacker.health >= int(attacker.max_health * 0.7):
            bar_color = Color.green

        if int(attacker.max_health * 0.7) > attacker.health >= int(attacker.max_health * 0.2):
            bar_color = Color.gold

        if attacker.health < int(attacker.max_health * 0.2):
            bar_color = Color.red

        print(
            f"{Color.pink}{attacker.name}{Color.end_of_modification} [{bar_color}{attacker.health}"
            f"{Color.end_of_modification}/{attacker.max_health}]   "
            f"{Color.pink}{target.name}{Color.end_of_modification} [{target.health}/{target.max_health}]\n"
            f"Combo points: {Color.gold}{attacker.combo_points['count'] * '* '}{Color.end_of_modification}\n"
            f"Buffs and debuffs: {attacker.buffs_and_debuffs}\n")



    # TODO: CHANGE ABILITY DAMAGE FROM STATIC INTO PERCENTAGE


    while run:
        ability = choose_ability()

        if ability == skip_turn:
            print(f'{attacker.name} skipped a turn\n')
            break

        if 'stun' in attacker.buffs_and_debuffs:
            print(f"{attacker.name} is stunned. {she_or_he} cannot attack this turn\n")
            break

        if 'stealth' in target.buffs_and_debuffs and ability['skill_type'] == 'physical':
            if attacker == hero:
                print(f'{target.name} is stealthed! Physical attacks wont work on {her_or_him}!\n')
            return False

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
                    return False

            if ability['skill_type'] == 'physical':

                if ability['skill_requirement'] is not None:
                    if ability['skill_requirement'] in attacker.buffs_and_debuffs:
                        attacker.buffs_and_debuffs.remove(ability['skill_requirement'])
                    else:
                        if attacker == hero:
                            print(f"\n{ability['name']} requires {ability['skill_requirement']} to use\n")
                        return False

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
                return False


# class specific weapon types, dual wield, shield, staff ctr...

enemies = {  # ENEMIES INTO JSON AS WELL?? IT WOULD BE HARD TO CODE WITH DAMAGE, HEALTH CTR...
    'grafted_scion': Enemy("Grafted Scion", "Man", 10, 10, 10, 100),
    'glass_orc': Enemy("Glass Orc", "Man", 12, 12, 12, 200),
    'burnt_wisp': Enemy("Burnt Wisp", "Woman", 15, 15, 15, 300),
    'ivory_fairy': Enemy("Ivory Fairy", "Woman", 20, 20, 20, 400),
    'shadow_pixie': Enemy("Shadow Pixie", "Woman", 25, 25, 25, 500),
    'lava_wraith': Enemy("Lava Wraith", "Man", 30, 30, 30, 600)
}


def combat_loop(player, enemy):
    print("Let's start\n")

    while True:
        want_to_manage = input("Do you want to manage your inventory? Y/N: ").lower()
        if want_to_manage == "y":
            inventory_management()
        else:
            break

    def player_attributes_update():
        player.attack = player_i["damage"]
        player.crit = player_i["crit"]
        player.defense = player_i["defense"]
        player.health = player_i["health"]
        player.max_health = player_i["health"]

    player_i = load_from_json()[0]
    player_attributes_update()

    while player.health > 0 or enemy.health > 0:

        while True:
            is_it_valid = combat(hero, enemy)

            if is_it_valid is False:
                continue
            else:
                break

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

    player_info = load_from_json()[0]
    chance_of_material = random.randint(0, 100)

    if 20 < chance_of_material <= 50:
        number_of_upgrade_materials = random.randint(1, 3)
        print(f"Upgrade material({number_of_upgrade_materials}) acquired")
        player_info["upgrade_materials"] += number_of_upgrade_materials

    if chance_of_material <= 20:
        number_of_crystals = 1
        print(f"{Color.gold}Crystal{Color.end_of_modification} acquired")
        player_info["crystal_balance"] += number_of_crystals

    with open("item_and_ability_collection.json", 'r') as f:
        item_and_ability_collection = json.load(f)
        loot_table = item_and_ability_collection["weapon_and_armor"]

        loot_name = []
        weight = []

        for item in loot_table:
            loot_name.append(item['name'])
            weight.append(item['drop_rate'])

        probability = list(zip(loot_name, weight))

        choices = []
        for item, weight in probability:
            choices.extend([item] * weight)
        loot_roll = random.choice(choices)



        for item in loot_table:
            if item['name'] == loot_roll:
                print(f"{Color.bold}{item['name']}{Color.end_of_modification} acquired!")
                acquired_loot = item

    add_to_inventory(acquired_loot, player_info)


def add_to_inventory(item_to_add, player_info_update):
    item_count = 0

    player_info = player_info_update

    try:
        player_inventory = load_from_json()[1]
    except ValueError:
        player_inventory = []

    try:
        player_equipment = load_from_json()[2]
    except ValueError:
        player_equipment = []

    for item in player_inventory:
        if item == item_to_add:
            item_count += 1

    if item_to_add["type"] == "armor" and item_count == 0 or item_to_add["type"] == "weapon" and item_count < 2:
        player_inventory.append(item_to_add)
        print(f"{item_to_add['name']} placed in inventory\n")

    else:
        player_info["gold_balance"] += item_to_add['value']
        print(f"Duplicate item! {hero.name} gained {item_to_add['value']} Gold instead")

    updated_player_json = {"Player info": player_info, "Player inventory": player_inventory,
                           "Player equipment": player_equipment}
    with open(player_json_file, 'w') as f3:
        json.dump(updated_player_json, f3, indent=4)


def inventory_management():

    player_info, player_inventory, player_equipment = load_from_json()

    def inventory_item_info(item_in_question):
        print(f"\nRarity: {item_in_question['rarity']}\n"
              f"Slot: {item_in_question['slot']}\n"
              f"Type: {item_in_question['type']}\n"
              f"Upgrade level: {item_in_question['upgrade lvl']}\n"            
              f"Value: {item_in_question['value']}\n"
              f"Drop rate: {item_in_question['drop_rate']}\n"
              f"Damage: {item_in_question['damage']}\n"
              f"Crit: {item_in_question['crit']}\n"
              f"Defense: {item_in_question['defense']}\n"
              f"Health: {item_in_question['health']}\n")

    def list_of_items_sorted():
        print(f"\n{Color.underline}INVENTORY{Color.end_of_modification}: ")
        name_list = []
        for stuff in player_inventory:
            if stuff['upgrade lvl'] > 0:
                upgraded_item_name = stuff['name'] + " +" + str(stuff['upgrade lvl'])
                name_list.append(upgraded_item_name)
            else:

                name_list.append(stuff['name'])
        d = defaultdict(int)
        name_list.sort()
        for key in name_list:
            d[key] += 1
        for i in d:
            print(f"{i}: ({d[i]})")

        print(f"\n{Color.underline}EQUIPMENT{Color.end_of_modification}: ")
        for item in player_equipment:
            if item['upgrade lvl'] > 0:
                print(item['name'] + " +" + str(item['upgrade lvl']))
            else:
                print(f"{item['slot']}: {item['name']}")

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

    def sell_or_equip():

        """
        TODO: SEPARATE WEAPON AND ARMOR FOR A MORE ASTETIC LOOK

        """

        is_it_in_the_inventory = []
        for finding_item in player_inventory:
            if finding_item['name'].lower() == chosen_item:
                is_it_in_the_inventory.append(finding_item)

        for finding_item in player_equipment:
            if finding_item['name'].lower() == chosen_item:
                is_it_in_the_inventory.append(finding_item)

        if not is_it_in_the_inventory:
            print(f"'{chosen_item}' not found in your inventory")
        else:
            valid_chosen_item = is_it_in_the_inventory[0]
            inventory_item_info(valid_chosen_item)
            run = True
            while run:
                sell_equip_upgrade = input(f"Would you like to {Color.pink}sell{Color.end_of_modification},"
                                           f" {Color.pink}equip{Color.end_of_modification} or "
                                           f"{Color.pink}upgrade"
                                           f"{Color.end_of_modification} this item?: ")

                if sell_equip_upgrade == 'sell':
                    try:
                        player_inventory.remove(valid_chosen_item)
                    except ValueError:
                        player_equipment.remove(valid_chosen_item)
                    player_info["gold_balance"] += valid_chosen_item['value']
                    print(f"{valid_chosen_item['name']} is removed from your inventory!\n"
                          f"{hero.name} gained {valid_chosen_item['value']} Gold!")
                    json_update(player_info, player_inventory, player_equipment)

                    return

                if sell_equip_upgrade == 'upgrade':

                    print(f"This item is at level {valid_chosen_item['upgrade lvl']}.\n")

                    def gold_and_material_check():
                        if gold_requirement <= budget and upgrade_material_requirement <= upgrade_materials:
                            return True
                        else:
                            if gold_requirement > budget:
                                print("\nNot enough Gold\n")
                                return False
                            if upgrade_material_requirement > upgrade_materials:
                                print("\nNot enough upgrade materials\n")
                                return False

                    run = True
                    while run:

                        budget = player_info["gold_balance"]
                        upgrade_materials = player_info["upgrade_materials"]
                        lvl = valid_chosen_item["upgrade lvl"]
                        gold_requirement = 2 ** (lvl + 1)
                        upgrade_material_requirement = (lvl + 1)

                        if lvl == 5:
                            print("Max upgrade level reached. Quiting...")
                            return


                        if gold_requirement <= budget and upgrade_material_requirement <= upgrade_materials:
                            print(f"Gold required for update: {gold_requirement}/{budget}")
                            print(f"Upgrade material requirement: {upgrade_material_requirement}/{upgrade_materials}")
                        else:
                            if gold_requirement > budget:
                                print(f"Gold required for update: {gold_requirement}/"
                                      f"{Color.red}{budget}{Color.end_of_modification}")
                                print(
                                    f"Upgrade material requirement: {upgrade_material_requirement}/{upgrade_materials}")
                            if upgrade_material_requirement > upgrade_materials:
                                print(f"Gold required for update: {gold_requirement}/{budget}")
                                print(f"Upgrade material requirement: {upgrade_material_requirement}/"
                                      f"{Color.red}{upgrade_materials}{Color.end_of_modification}")

                        wanna_upgrade = input("Would you like to upgrade? Y/N: ").lower()

                        if wanna_upgrade == 'y':
                            if gold_and_material_check():

                                player_info["gold_balance"] -= gold_requirement
                                player_info["upgrade_materials"] -= upgrade_material_requirement


                                print("upgraded")
                                valid_chosen_item["upgrade lvl"] += 1
                                print(f"This item is at level {lvl + 1}.\n")
                                if valid_chosen_item['type'] == 'armor':
                                    valid_chosen_item['defense'] += 1
                                    valid_chosen_item['health'] += 1 * valid_chosen_item["upgrade lvl"]
                                if valid_chosen_item['type'] == 'weapon':
                                    valid_chosen_item['damage'] += 1 * valid_chosen_item["upgrade lvl"]
                                    valid_chosen_item['crit'] += 1
                                json_update(player_info, player_inventory, player_equipment)
                                continue

                        else:
                            return

                if sell_equip_upgrade == 'equip':

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

                                    player_stat_update(valid_chosen_item, a)
                                    json_update(player_info, player_inventory, player_equipment)
                                    print(f"{a['name']} unequipped")

                            for b in player_equipment:
                                if b['slot'] == "Off-hand":
                                    player_equipment.remove(b)
                                    player_inventory.append(b)

                                    player_stat_update(valid_chosen_item, b)
                                    json_update(player_info, player_inventory, player_equipment)
                                    print(f"{b['name']} unequipped")

                            player_inventory.remove(valid_chosen_item)
                            player_equipment.append(valid_chosen_item)

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
                                    json_update(player_info, player_inventory, player_equipment)

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
                                    json_update(player_info, player_inventory, player_equipment)

                                    break
                            return
                        else:
                            player_inventory.remove(valid_chosen_item)
                            player_equipment.append(valid_chosen_item)
                            print(f"{valid_chosen_item['name']} equipped!")

                            player_stat_update(valid_chosen_item)
                            json_update(player_info, player_inventory, player_equipment)

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
                                json_update(player_info, player_inventory, player_equipment)

                                break

                        break



                if sell_equip_upgrade != 'sell' or sell_equip_upgrade != 'equip' or sell_equip_upgrade != 'upgrade':
                    print('Invalid input')
                    continue

    def subtract_stats():

        for item in player_equipment:
            player_info["damage"] -= item["damage"]
            player_info["crit"] -= item["crit"]
            player_info["defense"] -= item["defense"]
            player_info["health"] -= item["health"]

        return player_info

    def player_stat_update(item_plus, item_minus=None):

        player_damage = 0
        player_crit = 0
        player_defense = 0
        player_health = 0

        if item_minus is not None:
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


    managing = True
    while managing:
        list_of_player_stats()
        list_of_items_sorted()

        chosen_item = input(f" * Type in the {Color.pink}name of the item{Color.end_of_modification}"
                            f" in order to take"
                            "\n    a closer look on it,"
                            f"\n * Type '{Color.pink}unequip all{Color.end_of_modification}' to strip your equipment"
                            "\n    and start fresh,"
                            f"\n * Type '{Color.pink}quit{Color.end_of_modification}' to leave the equipment manager: "
                            f"").lower()

        if chosen_item == 'quit':
            return

        if chosen_item == 'unequip all':
            player_info = subtract_stats()
            player_inventory += player_equipment
            player_equipment = []
            json_update(player_info, player_inventory, player_equipment)
            print("Equipment has been moved to the inventory")

        if chosen_item == "upgrade":
            pass


        else:
            sell_or_equip()



def loot_tower(attacker):

    # TODO: RESET HERO COOLDOWN ON NEW LEVELS, EVERY 5TH ENEMY SHOULD BE A BOSS, THEN REPEAT WITH SAME
    #  ENEMIES BUT WITH INCREASED STATS, BOSS SHOULD DROP INCREASED REWARD, INCREASED CHANCE FOR LEGENDARY TOO,
    #  EXPERIENCE AND CHECKPOINT SHOULD BE ADDED AS WELL, >>?AT THE END OF TURNS, REGAIN LIKE 20% HEALTH?<<,
    #

    print(f"\n{Color.gold}Welcome in the Loot Tower. Ascend to the top\nand earn powerful rewards"
          f"{Color.end_of_modification}")

    values = enemies.values()
    enemy_list = list(values)
    enemy_count = 0
    run = True

    while run:

        print(f"\nYou're on level {enemy_count + 1}")

        enemy = enemy_list[enemy_count]

        is_it_a_win = combat_loop(attacker, enemy)
        if is_it_a_win is False:
            break
        else:
            enemy_count += 1



loot_tower(hero)
