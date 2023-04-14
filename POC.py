import random
import re
import numpy as np
import pandas as pd
import items
import time

# dupla cross
build1 = '109060606060606060606060601050606010010010010010010010010010010010010010010010010010050551051010050051010043040010010010010043300040552010550552010572430010010010050301041550552010550552010562420010010010240242010550552010550552010562410010010010240242010550552010550552010562360010010010240242010550552010550552010562210010010010240242010570552010550552010562260010010010240242010550552010550552010552160010010010053052010280552010550552010552160010010010010010010280042551041572010552510010010010010030010053153153651572010552480010010010010053363163163453343052010642470010010010010010010010010010010010010010020010010'

# aoe ys farmer
build2 = '105050506050705060501050605050506010010010010010010010010010010010010010010010043243243413363213243243243153040010010010242043563563563563563563563040620010010010242562043553553553553553040560240010010010242562552043543553553040550560440010010010242562552042541451051550550560620010010010242562552010010010162550550560160010010010572562552010010010162550550560160010010010572562552010030010362550550560160010010010572562552010053433052550550560160010010010572562042551551551551041550560510010010010562042561561551551551551041560470010010010042561561571571561561561561041480010010010010010010010010010010010010010020010010'

# mostly empty:
build3 = '105050506050705060501050605050506010010010010010010010010010010010010010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000010010010000000000000000010010010000000000010010010000000000000000010010010000000000010030010000000000000000010010010000000000010053000000000000203040010010010000000000000000000000000000000000010010010000000000000000000000000000000200010010010000000000000000000000000000000060010010010010010010010010010010010010010020010010'

# legenradies:
build4 = '105050506050705060501050605050506010010010010010010010010010010010010010010010043583573563553543533523000513040010010010592000000000000000000000000000500010010010602000000000000000000000000000490010010010612000000000000000000000000000400010010010622000000000000000000000000000470010010010632000000010010010000000000000420010010010000000000010010010000000000000450010010010000000000010030010000000000000440010010010000000000010000000000000000000430010010010042000000000041000000000000000460010010010000000000000000000000000000000410010010010000000000000000000000000000000480010010010010010010010010010010010010010020010010'

#portal:
build5 = '105050506050705060501050605050506010010010010010010010010010010010010010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000010010010000000000000000010010010000000000010010010000000000000000010010010000000000010030010000000000000000010010010000000000010000000000000000000000010010010000000000000652000000000000000000010010010000000000000000000000000000000640010010010000000000000000000000000000000000010010010010010010010010010010010010010020010010'

# to the wall
build6 = '105050506050705060501050605050506010010010010010010010010010010010010010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000000000000000000000000000010010010000000000010010010000000000000000010010010000000000010010010000000000000000010010010000000000010030010000000000000000010010010000000000010000000000000000000000010010010000000000000652000000000000000000010010010000000000000000000000000000000010010010010000000000000000000000000000000000010010010010010010010010010010010010010020010010'

# every item
build7 = '105050505050705050501050505050506010010010010010010010010010010010010010010010143000000000000283343253263363000040010010000043000333323383243193183230640000010010000000043000513503493000040000000390010010000352000043000000633040000000110210010010000162522042000000051620400000120200010010000272532010010010000610470000070310010010000372542010010010000600420000100130010010000292552010030010000590450000080000010010000302000010053000052580440000090652010010000000042000561571000041000000150010010010000042000481411461431000041000060010010010172000000000000000000000000221000010010010010010010010010010010010010010020010010'

# build with a single 3 way split
build8 = '100000000000000010000010600000006010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010030010010010010010010010010010010010010010000000010010010010010010010010010010010000000010010010010010010010010010010030010000000010010010010010010010010010010053000000170010010010010010010010010010010010010000000010010010010010010010010010010010010000000010010010010010010010010010010010010000000010010010010010010010010010010010010010020010010'

base_damage = 5

def parse_build(build):
    custom = build[0:1] # custom ship Y/N
    custom_blocks = build[1:33] # custom blocks
    custom_block_list = re.findall('..?',custom_blocks)
    custom_block_name_2d_array = np.reshape(custom_block_mapper(custom_block_list), (4,4))
    custom_block_id_2d_array = np.reshape(custom_block_list, (4,4))
    items = build[33:] #items
    items_and_orientation = re.findall('...?',items)
    items_and_orientation_2d_array = np.reshape(items_and_orientation, (14,14))
    return custom_block_list, custom_block_name_2d_array, custom_block_id_2d_array, items_and_orientation_2d_array
    
def chance(percentage):
    rand_num = random.uniform(0, 1)
    return rand_num < (percentage / 100)

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
                     '18':'death_pierce', '19':'pirce', '24':'circle_aoe', '38':'rectangle_aoe',
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
def convert_array_to_list_v2(items_and_orientation_2d_array, current_x=None, current_y=None, previous_item_att=None, previous_direction=None, item_list=None):
#     global item_list
    if current_x is None or current_y is None:
        current_x, current_y = get_starting_position(items_and_orientation_2d_array)
        print('starting position', current_x, current_y)
        item_list = []
    item = items_and_orientation_2d_array[current_x,current_y]
    
    item_id = item[0:2]
    orientation = int(item[2])
    
# Option A:    
#     match item_name_mapper(item_id):
#         case 'generator':

# Option B:
    #basic dictionary
    if previous_item_att is None:
        item_att = {
            "coord": (current_x, current_y),
            "item_id": item[0:2],
            "orientation": orientation,
        } 
    else:
        item_att = {
            "coord": (current_x, current_y),
            "item_id": item[0:2],
            "orientation": orientation,
            "previous_damage": previous_item_att['current_damage'],
#             "current_damage": previous_item_att['current_damage']
        } 
    
    match str(item_id):
        case '02':
            #generator
            item_att['previous_damage'] = 0
            item_att['current_damage'] = base_damage
            if generator_skilled:
                item_att['current_damage'] = item_att['current_damage']+5
            
        case '00':
            #empty
            item_att['current_damage'] = item_att['previous_damage']
            if empty_slot_skilled:
                item_att['current_damage'] = item_att['current_damage']+70*empty_slot_skilled
        
        case '04':
            #turn_right
            item_att['current_damage'] = item_att['previous_damage']
            if turn_right_skilled:
                item_att['current_damage'] = item_att['current_damage']+5*

        case '05':
             #turn_left
            item_att['current_damage'] = item_att['previous_damage']+5*turn_left_skilled
                
        case '06':
            item_att['current_damage'] = item_att['previous_damage']+1
            if add_1_damage_5_skilled:
                item_att['current_damage'] = item_att['current_damage']+5
            if add_1_damage_20_skilled:
                item_att['current_damage'] = item_att['current_damage']+20*count_add_1_damage

        case '07':
            if small_spread_skilled:
                item_att['current_damage'] = item_att['previous_damage']+small_spread_skilled*increase_value_by_random_percentage(previous_item_att['previous_damage'],0.5)
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '08':
            if large_spread_skilled:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],50)
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '09':
            if spread_left_skilled:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],40)
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '10':
            if spread_right_skilled:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],40)
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '11':
            if random_curve_skilled:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '12':
            if _skilled:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '':
            if _skilled:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '':
            if _skilled:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
            
            
        case other:
            item_att = {
                "coord": (current_x, current_y),
                "item_id": item[0:2],
                "orientation": orientation,
                "previous_damage" : previous_item_att['previous_damage'],
                "current_damage": previous_item_att['current_damage']
            }
            
#     if item_att is None:
#         # create the basic damage structure

#     else:
#         try:
#             item_att = {
#                 "coord": (current_x, current_y),
#                 "item_id": item[0:2],
#                 "orientation": orientation,
#                 "previous_damage" : item_list[-1]['current_damage']
#             }
#         except Exception as ex:
#             print(f'Error in creating the dictionary: {ex}')
        
#         try:
#             # call the function to update the dictionary
#             item_att = eval(f'{item_name_mapper(item_id)}({item_att},{item_list})')
#         except SyntaxError:
#             print(f'Error in the dictionary update code. Current list: {item_list},{chr(10)} current item: {item_att}.')
#         except Exception as ex:
#             print(ex)
        

    
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

    if len(item_list) > 150:
        print('Infinite loop terminated!')
    
    # ejection
    elif item_id == '03': 
        item_list.append(item_att)
        print('Ejection found at:', current_x, current_y)
        print(f'the final item list is: {item_list}')
    
    # cross money, cross damage
    elif item_id in ('30','29'):
        print('Item is not implemented:', item_name_mapper(item_id))
        item_list.append(item_att)
        convert_array_to_list_v2(items_and_orientation_2d_array, next_x, next_y, item_att, current_direction, item_list)
    
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
        item_list.append(item_att)
        convert_array_to_list_v2(items_and_orientation_2d_array, next_x, next_y, item_att, current_direction, item_list)
    
    if item_list[-1]['item_id']=='03':
        print('item list is returned.')
        return item_list
    else:
        print('No item list will be returned by this path.')

def wrapper():
    print(chance(100))

if __name__ == "__main__":
    wrapper()
