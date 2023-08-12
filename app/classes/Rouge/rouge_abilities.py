"""
from combat.abilities import Skill, Buff, Debuff




stealth = Buff()
stealth.name = "Stealth"
stealth.description = "Gain stealth until the end of your next turn"



asd = {
            "name": "Stealth",
            "hotkey": "s",
            "description": "Gain stealth until the end of your next turn",
            "skill_type": "buff",
            "resource_generation": false,
            "skill_requirement": null,
            "skill_cooldown": 4,
            "skill_debuff": null,
            "skill_debuff_duration": null,
            "skill_buff": "stealth",
            "skill_buff_duration": 2,
            "critical_modifier": 30,
            "damage_modifier": 0
        }







rouge abilities = [

        {
            "name": "Cheap Shot",
            "hotkey": "c",
            "description": "Increases your critical chance by 20 for your next attack and stuns for 1 turn.\nYou need to be stealthed to use this ability.\nAwards two combo points.",
            "skill_type": "physical",
            "resource_generation": true,
            "resource_gain": 2,
            "skill_requirement": "stealth",
            "skill_cooldown": 0,
            "skill_debuff": "stun",
            "skill_debuff_duration": 1,
            "skill_buff": null,
            "skill_buff_duration": null,
            "critical_modifier": 50,
            "damage_modifier": 50
        },
        {
            "name": "Mutilate",
            "hotkey": "m",
            "description": "Attack with both weapons for an additional 24 with each weapon. Awards two combo points",
            "skill_type": "physical",
            "resource_generation": true,
            "resource_gain": 2,
            "skill_requirement": null,
            "skill_cooldown": 3,
            "skill_debuff": null,
            "skill_debuff_duration": null,
            "skill_buff": null,
            "skill_buff_duration": null,
            "critical_modifier": 30,
            "damage_modifier": 48
        },
        {
            "name": "Eviscerate",
            "hotkey": "e",
            "description": "Spend all of your combo points, and deal more damage for each one. 1 point: attack + 20, 2 point: attack + 40 ,3 point: attack + 60, 4 point: attack + 80, 5 point: attack + 100",
            "skill_type": "combo",
            "resource_generation": false,
            "skill_requirement": "combo_points",
            "skill_cooldown": 0,
            "skill_debuff": null,
            "skill_debuff_duration": null,
            "skill_buff": null,
            "skill_buff_duration": null,
            "critical_modifier": 30,
            "1_point_damage": 20,
            "2_point_damage": 40,
            "3_point_damage": 60,
            "4_point_damage": 80,
            "5_point_damage": 100
        }
    ]"""