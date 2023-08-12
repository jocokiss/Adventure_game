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