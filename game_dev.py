#!/usr/bin/env python
# coding: utf-8

#IMPORTS
import random
import math
import time


def list_selection(dialogue, list_to_view):
    while True:
        try:
            print(dialogue+'\n')
            for k,v in enumerate(list_to_view):
                print(str(k)+': '+str(v))
            resp = int(input('\n> '))
        except ValueError:
            print('Invalid Selection\n')
            continue
        else:
            try:
                selection = list_to_view[resp]
            except IndexError:
                print('Invalid Selection\n')
                continue
            else:
                print('Selection: '+str(selection))
                break
    return selection


#CONSTANT VALUES
confirmation_prompt = ['Yes', 'No']
race_list = ['Human', 'Elf', 'Half-Elf', 'Dwarf', 'Half-Orc', 'Halfling']
attributes_list = ['Strength', 'Dexterity', 'Constitution', 'Luck']
racial_bonuses = {'Human': {'Strength': 1, 'Luck': 1},
                 'Elf': {'Strength': -1, 'Dexterity': 3, 'Constitution': -1},
                 'Half-Elf': {'Dexterity': 1, 'Luck': 1},
                 'Dwarf': {'Strength': 2, 'Dexterity': -1, 'Constitution': 2},
                 'Half-Orc': {'Strength': 3, 'Dexterity': -2, 'Constitution': 1},
                 'Halfling': {'Strength': -2, 'Dexterity': 2, 'Constitution': -1, 'Luck': 4}}
lvl_tree_1 = [2000]
for x in range(8):
    lvl_tree_1.append(lvl_tree_1[-1]*2)

lvl_tree_2 = [lvl_tree_1[-1]+250000]
for x in range(29):
    lvl_tree_2.append(lvl_tree_2[-1]+250000)

lvl_tree = [0]+lvl_tree_1+lvl_tree_2

lvl_dict = {}
for level,exp in enumerate(lvl_tree):
    lvl_dict[level+1] = exp


#Initial Character Build
base_character = {}
base_character['Name'] = str(input('Input Character Name\n> '))
print('\nRacial Bonuses\n')
for k,v in racial_bonuses.items():
    print(k)
    for att,bonus in v.items():
        print(att+': '+str(bonus))
    print('\n')

race = list_selection('Choose a Race', race_list)
base_character['Race'] = race
base_character['AC'] = 6
base_character['Lvl'] = 1
base_character['EXP'] = 0


#Attribute Point Roll
while True:
    total_attribute_rolls = []
    for num in range(len(attributes_list)):
        initial_attribute_roll = []
        for x in range(0,4):
            initial_attribute_roll.append(random.randint(1, 6))
        initial_attribute_roll.remove(min(initial_attribute_roll))
        total_attribute_rolls.append(sum(initial_attribute_roll))
    total_attribute_points = sum(total_attribute_rolls)
    print('You Have Rolled the Following Score\n'+str(total_attribute_points))
    roll_confirmation = list_selection('\nContinue with Roll?', confirmation_prompt)
    if roll_confirmation == 'Yes':
        break
    else:
        print('Rerolling\n')
        continue


#Attribute Distribution
for x in attributes_list:
    base_character[x] = 0
print('Racial Bonuses Applied\nRace: '+race)
for k,v in racial_bonuses[race].items():
    print(str(k)+': '+str(v))
while total_attribute_points != 0:
    print('\nYou Have '+str(total_attribute_points)+' Attribute Points to Assign')
    attribute_selection = list_selection('Choose Attribute to Assign Points', attributes_list)
    try:
        add_points = int(input('Number of Points to Assign\n> '))
    except ValueError:
        print('Selection Must be Int\n')
        continue
    else:
        total_attribute_points -= add_points
        if total_attribute_points < 0:
            print('Not Enough Points to Assign\n')
            total_attribute_points += add_points
            continue
        elif base_character[attribute_selection] + add_points > 18:
            print('Attribute Value Can Not Exceed 18')
            total_attribute_points += add_points
            continue
        else:
            base_character[attribute_selection] += add_points
            print('\nCurrent Character Stats')
            for k,v in base_character.items():
                print(k+': '+str(v))
for k,v in base_character.items():
    if k in racial_bonuses[race].keys():
        base_character[k] += racial_bonuses[race][k]

hit_point_roll = math.floor((random.randint(math.floor(base_character['Constitution']/2), 20)+base_character['Constitution'])*0.7)

base_character['Health'] = hit_point_roll

base_character['AC'] += math.floor(base_character['Dexterity']/5)
reordered_character_keys = ['Name', 'Race', 'Health', 'AC', 'Lvl', 'EXP']+attributes_list
base_character = {k: base_character[k] for k in reordered_character_keys}

print('\nFinal Character Stats')
for k,v in base_character.items():
    print(k+': '+str(v))


#Testing Weapons and Armor
weapons = {'Melee':{'Fist': '1d4',
                   'Dagger': '2d2',
                   'Shortsword': '1d6',
                   'Longsword': '1d8',
                   'Bastard Sword': '2d4'},
          'Ranged':{'Dart': '1d4',
                   'Throwing Knife': '2d2',
                   'Sling': '1d6',
                   'Shortbow': '2d3',
                   'Longbow': '2d4'}}
armor = {'Light':{'Leather Armor': {'AC Bonus': 1, 'DMG Reduction': 2, 'STR Req': 10},
                  'Padded Leather Armor': {'AC Bonus': 2, 'DMG Reduction': 2, 'STR Req': 11},
                  'Elven Mail': {'AC Bonus': 4, 'DMG Reduction': 3, 'STR Req': 12}},
         'Medium':{'Chainlink Mail Armor': {'AC Bonus': 2, 'DMG Reduction': 1, 'STR Req': 12},
                  'Scale Plate Armor': {'AC Bonus': 3, 'DMG Reduction': 2, 'STR Req': 13}},
         'Heavy':{'Platemail Armor': {'AC Bonus': 2, 'DMG Reduction': 4, 'STR Req': 14},
                 'Ebony Plate Armor': {'AC Bonus': 3, 'DMG Reduction': 6, 'STR Req': 16}}}


#Sample Character for Testing
current_character = base_character
current_character['Weapon'] = 'Throwing Knife'
current_character['Armor'] = 'Padded Leather Armor'
armor_class = [k for k,v in armor.items() if current_character['Armor'] in v][0]
current_character['AC'] += armor[armor_class][current_character['Armor']]['AC Bonus']
current_character


#Sample Enemy for Testing
enemy = {'Name': 'Goblin',
         'Strength': 10,
         'Dexterity': 12,
         'Constitution': 10,
         'Luck': 6,
         'AC': 6}
hit_point_roll = math.floor((random.randint(math.floor(enemy['Constitution']/2), 20)+enemy['Constitution'])*0.7)
enemy['Health'] = hit_point_roll
enemy['AC'] += math.floor(enemy['Dexterity']/5)
reordered_enemy_keys = ['Name', 'Health', 'AC']+attributes_list
enemy = {k: enemy[k] for k in reordered_enemy_keys}
enemy['Weapon'] = 'Shortsword'
enemy['Armor'] = 'Leather Armor'
armor_class = [k for k,v in armor.items() if enemy['Armor'] in v][0]
enemy['AC'] += armor[armor_class][enemy['Armor']]['AC Bonus']
enemy


def battle_sequence(attacker, defender):
    total_dmg = 0
    equipped_weapon = attacker['Weapon']
    weapon_class = [k for k,v in weapons.items() if equipped_weapon in v][0]
    equipped_armor = defender['Armor']
    armor_class = [k for k,v in armor.items() if equipped_armor in v][0]
    hit_roll = random.randint(math.floor(attacker['Dexterity']/3), 20)+math.floor(attacker['Dexterity']/3)
    defense_roll = math.floor(random.randint(1, 5)+defender['AC']+(defender['Luck']/5))
    if hit_roll > defense_roll:
        for x in range(int(weapons[weapon_class][equipped_weapon][0])):
            dmg_roll = random.randint(1, int(weapons[weapon_class][equipped_weapon].split('d')[1]))
            total_dmg += dmg_roll
            if weapon_class == 'Melee':
                total_dmg += math.floor(attacker['Strength']/4)
                if armor_class != 'Light':
                    total_dmg -= armor[armor_class][equipped_armor]['DMG Reduction']
            else:
                total_dmg += math.floor(attacker['Dexterity']/4)
                if armor_class != 'Heavy':
                    total_dmg -= armor[armor_class][equipped_armor]['DMG Reduction']
        crit_roll = random.randint(1, 100)
        if crit_roll < attacker['Luck']:
            total_dmg = math.floor(total_dmg*1.5)
        print(attacker['Name']+' Deals '+str(total_dmg)+' Damage')
        defender['Health'] -= total_dmg
    else:
        print(defender['Name']+' Dodges Attack')
    if defender['Health'] > 0:
        print(defender['Name']+' Has '+str(defender['Health'])+' Health Remaining\n')


#Basic Combat Sequence
while current_character['Health'] > 0 and enemy['Health'] > 0:
    battle_sequence(current_character, enemy)
    time.sleep(1)
    if enemy['Health'] <= 0:
        print(enemy['Name']+' Defeated')
        break
    else:
        battle_sequence(enemy, current_character)
        time.sleep(1)
        if current_character['Health'] <= 0:
            print(current_character['Name']+' Defeated\nGAME OVER')

