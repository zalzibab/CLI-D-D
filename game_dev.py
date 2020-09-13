#!/usr/bin/env python
# coding: utf-8

#IMPORTS#
import random
import math

#CONSTANT VALUES#
confirmation_prompt = ['Yes', 'No']
race_list = ['Human', 'Elf', 'Half-Elf', 'Dwarf', 'Half-Orc', 'Halfling']
attributes_list = ['Strength', 'Dexterity', 'Constitution', 'Luck']
racial_bonuses = {'Human': {'Strength': 1, 'Luck': 1},
                 'Elf': {'Strength': -1, 'Dexterity': 3, 'Constitution': -1},
                 'Half-Elf': {'Dexterity': 1, 'Luck': 1},
                 'Dwarf': {'Strength': 2, 'Dexterity': -1, 'Constitution': 2},
                 'Half-Orc': {'Strength': 3, 'Dexterity': -2, 'Constitution': 1},
                 'Halfling': {'Strength': -2, 'Dexterity': 2, 'Constitution': -1, 'Luck': 4}}


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
print('\nFinal Character Stats')
for k,v in base_character.items():
    print(k+': '+str(v))

