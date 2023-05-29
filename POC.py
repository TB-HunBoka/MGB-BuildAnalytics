import re
import random
import numpy as np
import pandas as pd
# import items
import time
import math
from yaml import safe_load

# example build with a single 3 way split
build8 = '100000000000000010000010600000006010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010030010010010010010010010010010010010010010000000010010010010010010010010010010010000000010010010010010010010010010010030010000000010010010010010010010010010010053000000170010010010010010010010010010010010010000000010010010010010010010010010010010010000000010010010010010010010010010010010010000000010010010010010010010010010010010010010020010010'

base_damage = 5

with open('skills.yaml', 'r') as skills_file:
    skill_yaml = safe_load(skills_file)
    skills = skill_yaml['skills']

with open('base_stats.yaml', 'r') as base_stats_file:
    base_stats_yaml = safe_load(base_stats_file)
    base_stats = base_stats_yaml['base_stats']

def chance(percentage):
    rand_num = random.uniform(0, 1)
    return rand_num < (percentage / 100)

def increase_value_by_random_percentage(value, factor):
    # Generate a random value between 0 and factor
    rand_factor = random.uniform(0, factor/100)
    # Multiply the value by the random factor
    new_value = value + value * rand_factor
    return new_value

# def effective_damage_updater(item_id, projectile_att, previous_item_att, skills, base_damage, count_add_1_damage):
#     difference = projectile_att['current_damage'] - projectile_att['previous_damage']
#     match str(item_id):
#         case '25':
#             projectile_att['effective_damage'] = projectile_att['effective_damage'] + projectile_att['current_damage']

#         case other:
#             projectile_att['effective_damage'] = projectile_att['effective_damage'] + difference

#     return projectile_att

def projectile_damage_updater(item_id, projectile_att, previous_projectile_att, skills, base_damage, count_add_1_damage):
    match str(item_id):
        case '02':
            #generator
            projectile_att['previous_damage'] = 0
            projectile_att['effective_damage'] = 0
            if skills['generator_skilled']:
                projectile_att['current_damage'] = base_damage+5
                projectile_att['effective_damage'] = projectile_att['current_damage']
            else:
                projectile_att['current_damage'] = base_damage
            
        case '00':
            #empty
            if skills['empty_slot_skilled']:
                projectile_att['current_damage'] = projectile_att['previous_damage']+70
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        
        case '04':
            #turn_right
            if skills['turn_right_skilled']:
                projectile_att['current_damage'] = projectile_att['previous_damage']+5
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']

        case '05':
             #turn_left
            if skills['turn_left_skilled']:
                projectile_att['current_damage'] = projectile_att['previous_damage']+5
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '06':
            projectile_att['current_damage'] = projectile_att['previous_damage']+1
            if skills['add_1_damage_5_skilled']:
                projectile_att['current_damage'] = projectile_att['current_damage']+5
            if skills['add_1_damage_20_skilled']:
                projectile_att['current_damage'] = projectile_att['current_damage']+20*count_add_1_damage

        case '07':
            if skills['small_spread_skilled']:
                projectile_att['current_damage'] = projectile_att['previous_damage']+increase_value_by_random_percentage(previous_projectile_att['previous_damage'],0.5)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '08':
            if skills['large_spread_skilled']:
                projectile_att['current_damage'] = increase_value_by_random_percentage(projectile_att['previous_damage'],50)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']

        case '09':
            if skills['spread_left_skilled']:
                projectile_att['current_damage'] = increase_value_by_random_percentage(projectile_att['previous_damage'],40)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']

        case '10':
            if skills['spread_right_skilled']:
                projectile_att['current_damage'] = increase_value_by_random_percentage(projectile_att['previous_damage'],40)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '11':
            if skills['random_curve_skilled']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '12':
            if skills['curve_left']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*1.3
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '13':
            if skills['curve_right']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*1.3
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
        
        case '20':
            if skills['x2_damage_chance']:
                x2_chance = 40
            else:
                x2_chance = 33
                
            if skills['x2_damage_multi']:
                x2_multi = 2.5
            else:
                x2_multi = 2
            projectile_att['current_damage'] = projectile_att['previous_damage']+projectile_att['previous_damage']*chance(x2_chance)*(x2_multi-1)
        
        case '21':
            if skills['x10_damage_x30']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1+29*chance(4))
            elif skills['x10_damage_x20']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1+19*chance(4))
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1+9*chance(4))
                
        case '22': # for later use
            if skills['2_way_random_split']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*3
                # and start projectile in 2 direction
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']*2
                # and start projectile in 2 direction
        
        case '23': # for later use
            if skills['3_way_random_split']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*4
                # and start projectile in 3 direction
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']*3
                # and start projectile in 3 direction
                
        case '24':
            #to do: calculate the damage increase for aoe
            projectile_att['cycle_aoe'] += 1
            if skills['circle_aoe_penalty']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1-0.03)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1-0.06)

        case '38':
            #to do: calculate the damage increase for aoe
            projectile_att['square_aoe'] += 1
            if skills['square_aoe_penalty']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1-0.03)
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']*(1-0.06)

        case '25':
            # to do: a bounce által okozott damagenövekedés számolása. Bounceonként 17% -al nő. plusz a bounce duplázza a damaget.
            # ezt szeretném figyelembe venni a kimutatásoknál, ezért valahogy le kell implementáljam
            # ha simán úgy viszem tovább, hogy item_att['current_damage'] = item_att['previous_damage']*bounce, akkor félek
            # hogy a többi bounce típus hibásan fogja tovább szorozni. Ezért szétszedem a projectile_damaget és az effective_damaget
            if skills['random_bounce_damage']:
                projectile_att['current_damage'] = projectile_att['previous_damage']*1.17
            if skills['random_bounce_bounce'] and skills['random_bounce_damage']:
                projectile_att['random_bounce'] = projectile_att['random_bounce']+1*chance(25)
                projectile_att['current_damage'] = projectile_att['current_damage']*1.17
            elif skills['random_bounce_bounce']:
                projectile_att['random_bounce'] = projectile_att['random_bounce']+1*chance(25)
                projectile_att['current_damage'] = projectile_att['previous_damage']
            projectile_att['random_bounce'] = projectile_att['random_bounce']+1
                
        case '26':
            if skills['return_bounce_bounce']:
                projectile_att['return_bounce'] = projectile_att['return_bounce']+1*chance(25)
            projectile_att['return_bounce'] = projectile_att['return_bounce']+1
                
        case '27':
            if skills['shoot_upward']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '28':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']

        case '29':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '30':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '31':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '32':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '33':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '34':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '35':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '36':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '37':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '39':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
                
        case '':
            if skills['']:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            else:
                projectile_att['current_damage'] = projectile_att['previous_damage']
            
            
        case other:
            print('Undeveloped item: '+ item_id)
            projectile_att['current_damage'] = projectile_att['previous_damage']

    return projectile_att


# future use: The effective damage calculation will be done on item level. There are some items that are counted at or after the ejection happened.
# These should be calculated at the end of the path. I will have an estimated damage by the damage updater it self, but it will be incorrect. 
# example: Flat damage increase after a bounce item will be ignored. The bounce calculation should be calculated on items after the bounce itself.
# to_do:
#   move it to the damage_updater.py
#   complete the code
'''
def ejection_level_damage_updater(item_att, previous_item_att, item_list, skills):
    if skills['circle_aoe_penalty']:
        item_att['current_damage'] = item_att['current_damage']*((1-0.03)**item_att['cycle_aoe'])
    else:
        item_att['current_damage'] = item_att['current_damage']*((1-0.06)**item_att['cycle_aoe'])
    # majd a végén olyat kellene, hogy az item hatékonyság mutatókat vissza számoljam ezek alapján.
    # tehát, ha 1 aoe lecsökkenti 6%-al a damaget, akkor annak az aoe-nak a hatékonysága 0.96 legyen
    # ha két aoe lecsökkenti 11.64%-al, akkor mind a két aoe-nak legyen ott vagy a 0.96, vagy 94,18
    # final_current_damage/original_current_damage
    # current_damage/item_list[-1]['current_damage']   /  item_att['cycle_aoe']
        
    if skills['square_aoe_penalty']:
        item_att['current_damage'] = item_att['current_damage']*((1-0.03)**item_att['square_aoe'])
    else:
        item_att['current_damage'] = item_att['current_damage']*((1-0.06)**item_att['square_aoe'])
        

    if skills['random_bounce_damage'] and item_att['repeatedly_turn_upward'] > 0:
        item_att[''] = item_att['previous_damage']
    elif skills['repeatedly_turn_upward'] > 0:
        item_att['current_damage'] = item_att['previous_damage']*2*skills['random_bounce_damage']
    '''

def parse_build(build):
    custom = build[0:1] # custom ship Y/N
    custom_blocks = build[1:33] # custom blocks
    custom_block_list = re.findall('..?',custom_blocks)
    custom_block_name_2d_array = np.reshape(custom_block_mapper(custom_block_list), (4,4))
    custom_block_id_2d_array = np.reshape(custom_block_list, (4,4))
    items = build[33:] #items
    items_and_orientation = re.findall('...?',items)
    items_and_orientation_2d_array = np.reshape(items_and_orientation, (14,14))
#     item_list = pd.Series(items_and_orientation).str[0:2].values
#     item_list_named_2d_array = ...
#     item_list_2d_array = np.reshape(item_list, (14,14))
    return custom_block_list, custom_block_name_2d_array, custom_block_id_2d_array, items_and_orientation_2d_array

def custom_block_mapper(custom_block_number):
    custom_block_mapping = {'00' : 'empty', '01':'ejection_up', '02':'auto_fly', '03':'second_try'
                        , '04':'manual_burst', '05':'3x3', '06':'blue'
                        , '07':'longer_countdown', '08':'light_green', '09':'skipp'
                        , '10':'10%_more', '11':'ejection_side', '12':'red_after_wave'}
    custom_block_element_name = [custom_block_mapping[x] for x in custom_block_number]
    return custom_block_element_name

def item_name_mapper(item):
    item_mappings = {'00': 'empty_slot', '01':'solid_block', '02': 'generator', '03':'ejector',
                     '04':'turn_right', '05':'turn_left', '06':'add_1_damage', '15':'speed_up',
                     '09':'spread_left', '08':'large_spread', '10':'spread_right', '07':'small_spread',
                     '12':'curve_left', '11':'random_curve', '13':'curve_right', '31':'slow_down',
                     '20':'x2_damage', '21':'x10_damage', '39':'random_damage', '36':'charge',
                     '26':'return_bounce', '25':'random_bounce', '34':'ricochet', '28':'double_lifetime',
                     '14':'2_way_split', '17':'3_way_split', '22':'2_way_random_split', '23':'3_way_random_split',
                     '18':'death_pierce', '19':'pierce', '24':'circle_aoe', '38':'rectangle_aoe',
                     '32':'magnet', '33':'align_direction', '35':'line_magnet', '16':'add_projectile',
                     '27':'shoot_upward', '37':'shoot_sideways', '29':'money_cross', '30':'damage_cross',
                     '48':'tier_damage', '41':'damage_comeback', '46':'evolved_damage', '43':'damage_stockpile',
                     '44':'slow_burn', '45':'combine_10', '42':'crisscross', '47':'guided_damage',
                     '40':'add_100_damage', '49':'ejector_damage', '50':'sparse_damage', '51':'clone',
                     '52': 'shield_piercing', '53': 'armor_piercing', '54': 'double_piercing', '55': 'charged_round',
                     '56': 'thermit_round', '57': 'plutonium_round', '58': 'protonic', '59': 'incendiary',
                     '60': 'energy_siphon', '61': 'energy_disrupt', '62': 'void_resistance', '63': 'void_inoculation',
                     '64': 'input_portal', '65': 'output_portal'
    }
    item_name = item_mappings[item]
    return item_name

def get_starting_position(items_and_orientation_2d_array):
    starting_position = np.where(items_and_orientation_2d_array=='020')
    x0 = np.asarray(starting_position).T[0][0]
    y0 = np.asarray(starting_position).T[0][1]
    return x0, y0

def find_portal_exit(items_and_orientation_2d_array):
    portal_exit_position = np.where((items_and_orientation_2d_array >= '650') & (items_and_orientation_2d_array <= '653'))
    xp = np.asarray(portal_exit_position).T[0][0]
    yp = np.asarray(portal_exit_position).T[0][1]
    return xp,yp

directions = (0,1,2,3)
def turn(id: int, turn: str):
    # 0 - up, 1 - right, 2 - down, 3 - left
    match turn:
        case 'turn_left':
            id -= 1
            if id < 0:
                id = 3
        case 'turn_right':
            id += 1
            if id > 3:
                id = 0
    return directions[id]

def next_coordination(x_coord, y_coord, item_with_orientation, previous_direction=None):
    item = item_with_orientation[0:2]
    orientation = int(item_with_orientation[2])
    match item:
        case '04':
            direction = turn(orientation,'turn_left')
        case '05':
            direction = turn(orientation,'turn_right')
        case '00':
            direction = previous_direction
        case '02':
            direction = 0
        case other:
            direction = previous_direction
    match int(direction):
        case 0:
            x_coord -= 1
        case 1:
            y_coord += 1
        case 2:
            x_coord += 1
        case 3:
            y_coord -= 1
    return x_coord, y_coord, direction

# v5 adding the function that calls the item functions. nem tudom, hogy az egész listát adjam-e át, vagy csak az item_att-ot
# új ötlet, simán match item, case kombó elég. Ha id-vel dolgozom, akkor 10 000 hívásonként fél másodpercel gyorsabb
# mintha meghívnám az item_name mappert, de kevésbé lesz átlátható.
# v5 adding the function that calls the item functions. nem tudom, hogy az egész listát adjam-e át, vagy csak az item_att-ot
# új ötlet, simán match item, case kombó elég. Ha id-vel dolgozom, akkor 10 000 hívásonként fél másodpercel gyorsabb
# mintha meghívnám az item_name mappert, de kevésbé lesz átlátható.
def convert_array_to_list_v2(items_and_orientation_2d_array, projectile_id, current_x=None, current_y=None, previous_projectile_att=None, previous_direction=None, item_list=None):
#     global item_list
    if current_x is None or current_y is None:
        current_x, current_y = get_starting_position(items_and_orientation_2d_array)
        print('starting position', current_x, current_y)
        item_list = []
    item = items_and_orientation_2d_array[current_x,current_y]
    
    item_id = item[0:2]
    orientation = int(item[2])
    
    #basic dictionary
    if previous_projectile_att is None:
        projectile_att = {
            "coord": (current_x, current_y),
            "item_id": item[0:2],
            "projectile_id": projectile_id,
            "orientation": orientation,
            "cycle_aoe" : 0,
            "square_aoe" : 0,
            "pierce" : 0,
            "death_pierce" : 0,
            "return_bounce" : 0,
            "random_bounce" : 0,
            "ricochet" : 0,
            "repeatedly_turn_upward" : 0
        } 
    else:
        projectile_att = {
            "coord": (current_x, current_y),
            "item_id": item[0:2],
            "projectile_id": projectile_id,
            "orientation": orientation,
            "previous_damage": previous_projectile_att['current_damage'],
            "current_damage": previous_projectile_att['current_damage'], # later I might re-enable this for safety
            # "effective_damage": previous_item_att['effective_damage'],
            "cycle_aoe" : previous_projectile_att["cycle_aoe"],
            "square_aoe" : previous_projectile_att["square_aoe"],
            "pierce" : previous_projectile_att["pierce"],
            "death_pierce" : previous_projectile_att["death_pierce"],
            "return_bounce" : previous_projectile_att["return_bounce"],
            "random_bounce" : previous_projectile_att["random_bounce"],
            "ricochet" : previous_projectile_att["ricochet"],
            "repeatedly_turn_upward" : previous_projectile_att["repeatedly_turn_upward"]
        } 
        
    # projectile_damage_updater will give back the current damage and effective damage after modifications
    projectile_att = projectile_damage_updater(item_id=item_id, projectile_att=projectile_att, previous_projectile_att=previous_projectile_att, skills=skills, base_damage=base_damage, count_add_1_damage=count_add_1_damage)

    # if the effective_damage was not updated, then use the projectile difference
    try:
        projectile_att['effective_damage']
    except KeyError:
        damage_increase = projectile_att['current_damage'] - previous_projectile_att['current_damage']
        projectile_att['effective_damage'] = previous_projectile_att['effective_damage'] + damage_increase
    
    if item_id == '64':
        next_x, next_y = find_portal_exit(items_and_orientation_2d_array)
        current_direction = turn(turn(int(items_and_orientation_2d_array[next_x,next_y][2]), 'turn_left'), 'turn_left')
        print(f'Portal found at {current_x}, {current_y}, orientation: {orientation}. Portal exit at: {next_x},{next_y}. Exit portal direction: {current_direction}')
    else:
        next_x, next_y, current_direction = next_coordination(current_x, current_y, item, previous_direction)

    
    #compare the orientation of the current item with the previous item, they need to be matched. (Rotating is done)
    print('item found:', item, 'current direction', current_direction)
    correct_direction = previous_direction == int(orientation)
    
    print('next coordinations are:', next_x, next_y)

    if len(item_list) > 250:
        print('Infinite loop terminated!')
    
    # ejection
    elif item_id == '03': 
        item_list.append(projectile_att)
        print('Ejection found at:', current_x, current_y)
        print(f'the final item list is: {item_list}')
    
    # cross money, cross damage
    elif item_id in ('30','29'):
        print('Item is not implemented:', item_name_mapper(item_id))
        item_list.append(projectile_att)
        convert_array_to_list_v2(items_and_orientation_2d_array=items_and_orientation_2d_array, projectile_id=projectile_id, current_x=next_x, current_y=next_y, previous_projectile_att=projectile_att, previous_direction=current_direction, item_list=item_list)
    
    # hitting a wall
    elif item_id == '01': 
        print('Path ended in the wall!')
    
    # incorrect orientation
    elif (correct_direction == False) and len(item_list)>0:
        print('Incorrect orientation at:', next_x, next_y, 'item:',item)
        print('Orientation:', orientation, 'previous_direction:', previous_direction, 'current_direction:', current_direction)
        print(previous_direction == orientation)
        print(type(previous_direction))
        print(type(orientation))
    
    # continue the path  
    else:
        item_list.append(projectile_att)
        convert_array_to_list_v2(items_and_orientation_2d_array=items_and_orientation_2d_array, projectile_id=projectile_id, current_x=next_x, current_y=next_y, previous_projectile_att=projectile_att, previous_direction=current_direction, item_list=item_list)
    
    if item_list[-1]['item_id']=='03':
        print('item list is returned.')
        return item_list
    else:
        print('No item list will be returned by this path.')
    
def wrapper():
    global count_add_1_damage
    build = build8 # to_do: make it as a user input?
    projectile_count = 2 # to_do: make this as a user input

    custom_block_list, custom_block_name_2d_array, custom_block_id_2d_array, items_and_orientation_2d_array = parse_build(build)
    print(custom_block_name_2d_array)
    print(custom_block_id_2d_array)
    print(items_and_orientation_2d_array)

    # performance improver global variables
    count_add_1_damage = np.count_nonzero(custom_block_id_2d_array == '06')
    
    every_projectile_df = pd.DataFrame()

    for projectile_id in range(1,projectile_count):
        item_list = convert_array_to_list_v2(items_and_orientation_2d_array=items_and_orientation_2d_array, projectile_id=projectile_id)
        # print(item_list)

        single_projectile_df = pd.DataFrame(item_list)
        single_projectile_df = single_projectile_df[['coord','item_id','projectile_id','previous_damage','current_damage','effective_damage']]
        single_projectile_df.set_index(['coord','item_id'],inplace=True)
        # I can calculate the efficiency per projectile or in the mean grouped by DF 5 rows below this
        single_projectile_df['efficiency'] = single_projectile_df['effective_damage']/single_projectile_df['previous_damage']
        
        every_projectile_df = pd.concat((single_projectile_df.replace(np.inf,np.NaN), every_projectile_df))
    
    # create single item statistics, but multiple aggregation
    inpected_item_coord = (12, 11) # the user can select the id on the UI
    one_item_stat = every_projectile_df.loc[inpected_item_coord].agg([np.mean,min,max]) # len => projectile_number
    one_item_stat['coord'] = inpected_item_coord
    # efficiency can be recaulculated based on these aggregations
    one_item_stat['new_eff'] = one_item_stat['effective_damage']/one_item_stat['previous_damage']
    '''
    pro:
        Multiple aggregation can be used.
        Easy to extend the aggregation list. 
        Easy to work with the result DF.
        Single item view
    cons:
        coordination based. What would it do for crossing items?
        it might need to rework to use the coordination and position in the path. (position alone also not good, because of multiple different path can have different items at position 3)
        it need to recalculate the aggregation every time I change the coordination
        Only one item at a time.
        Index information needs to be re entered as a column, or need to keep in the DF
    '''

    # create statistics for the whole path, but with a single aggregation. The result is a DF.
    mean_projectile_df = every_projectile_df.groupby(level=(0,1), sort=False).mean()
    # efficiency can be recaulculated based on the aggregation
    mean_projectile_df['new_eff'] = mean_projectile_df['effective_damage']/mean_projectile_df['previous_damage']
    '''
    pro:
        the aggregation done once
        the whole path will be visible on the final DF, just need to iterate on it. Quick user experience
        memory efficient (I can generate all the aggregation and drop the calculation table.)
        the indexes are kept in the results
    cons:
        a bit harder to work with the data (multi level index sliceing)
        limited aggregations (min,max,mean,median,quantile,std,var ...)
    '''

if __name__ == "__main__":
    wrapper()
