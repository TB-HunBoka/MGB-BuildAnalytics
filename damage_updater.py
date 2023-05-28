import random

def chance(percentage):
    rand_num = random.uniform(0, 1)
    return rand_num < (percentage / 100)

def increase_value_by_random_percentage(value, factor):
    # Generate a random value between 0 and factor
    rand_factor = random.uniform(0, factor/100)
    # Multiply the value by the random factor
    new_value = value + value * rand_factor
    return new_value

def effective_damage_updater(item_id, item_att, previous_item_att, skills, base_damage, count_add_1_damage):
    difference = item_att['current_damage'] - item_att['previous_damage']
    match str(item_id):
        case '25':
            item_att['effective_damage'] = item_att['effective_damage'] + item_att['current_damage']

        case other:
            item_att['effective_damage'] = item_att['effective_damage'] + difference

    return item_att

def projectile_damage_updater(item_id, item_att, previous_item_att, skills, base_damage, count_add_1_damage):
    match str(item_id):
        case '02':
            #generator
            item_att['previous_damage'] = 0
            if skills['generator_skilled']:
                item_att['current_damage'] = base_damage+5
            else:
                item_att['current_damage'] = base_damage
            
        case '00':
            #empty
            if skills['empty_slot_skilled']:
                item_att['current_damage'] = item_att['previous_damage']+70
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        
        case '04':
            #turn_right
            if skills['turn_right_skilled']:
                item_att['current_damage'] = item_att['previous_damage']+5
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '05':
             #turn_left
            if skills['turn_left_skilled']:
                item_att['current_damage'] = item_att['previous_damage']+5
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '06':
            item_att['current_damage'] = item_att['previous_damage']+1
            if skills['add_1_damage_5_skilled']:
                item_att['current_damage'] = item_att['current_damage']+5
            if skills['add_1_damage_20_skilled']:
                item_att['current_damage'] = item_att['current_damage']+20*count_add_1_damage

        case '07':
            if skills['small_spread_skilled']:
                item_att['current_damage'] = item_att['previous_damage']+increase_value_by_random_percentage(previous_item_att['previous_damage'],0.5)
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '08':
            if skills['large_spread_skilled']:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],50)
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '09':
            if skills['spread_left_skilled']:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],40)
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '10':
            if skills['spread_right_skilled']:
                item_att['current_damage'] = increase_value_by_random_percentage(item_att['previous_damage'],40)
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '11':
            if skills['random_curve_skilled']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '12':
            if skills['curve_left']:
                item_att['current_damage'] = item_att['previous_damage']*1.3
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '13':
            if skills['curve_right']:
                item_att['current_damage'] = item_att['previous_damage']*1.3
            else:
                item_att['current_damage'] = item_att['previous_damage']
        
        case '20':
            if skills['x2_damage_chance']:
                x2_chance = 40
            else:
                x2_chance = 33
                
            if skills['x2_damage_multi']:
                x2_multi = 2.5
            else:
                x2_multi = 2
            item_att['current_damage'] = item_att['previous_damage']+item_att['previous_damage']*chance(x2_chance)*(x2_multi-1)
        
        case '21':
            if skills['x10_damage_x30']:
                item_att['current_damage'] = item_att['previous_damage']*(1+29*chance(4))
            elif skills['x10_damage_x20']:
                item_att['current_damage'] = item_att['previous_damage']*(1+19*chance(4))
            else:
                item_att['current_damage'] = item_att['previous_damage']*(1+9*chance(4))
                
        case '22': # for later use
            if skills['2_way_random_split']:
                item_att['current_damage'] = item_att['previous_damage']*3
                # and start projectile in 2 direction
            else:
                item_att['current_damage'] = item_att['previous_damage']*2
                # and start projectile in 2 direction
        
        case '23': # for later use
            if skills['3_way_random_split']:
                item_att['current_damage'] = item_att['previous_damage']*4
                # and start projectile in 3 direction
            else:
                item_att['current_damage'] = item_att['previous_damage']*3
                # and start projectile in 3 direction
                
        case '24':
            #to do: calculate the damage increase for aoe
            item_att['cycle_aoe'] += 1
            if skills['circle_aoe_penalty']:
                item_att['current_damage'] = item_att['previous_damage']*(1-0.03)
            else:
                item_att['current_damage'] = item_att['previous_damage']*(1-0.06)

        case '38':
            #to do: calculate the damage increase for aoe
            item_att['square_aoe'] += 1
            if skills['square_aoe_penalty']:
                item_att['current_damage'] = item_att['previous_damage']*(1-0.03)
            else:
                item_att['current_damage'] = item_att['previous_damage']*(1-0.06)

        case '25':
            # to do: a bounce által okozott damagenövekedés számolása. Bounceonként 17% -al nő. plusz a bounce duplázza a damaget.
            # ezt szeretném figyelembe venni a kimutatásoknál, ezért valahogy le kell implementáljam
            # ha simán úgy viszem tovább, hogy item_att['current_damage'] = item_att['previous_damage']*bounce, akkor félek
            # hogy a többi bounce típus hibásan fogja tovább szorozni. Ezért lehet ki kell kérjem az item_att-ot. Végig kell gondolni.
            if skills['random_bounce_damage']:
                item_att['current_damage'] = item_att['previous_damage']*1.17
            if skills['random_bounce_bounce']:
                item_att['random_bounce'] = item_att['random_bounce']+1*chance(25)
            item_att['random_bounce'] = item_att['random_bounce']+1
                
        case '26':
            if skills['return_bounce_bounce']:
                item_att['return_bounce'] = item_att['return_bounce']+1*chance(25)
            item_att['return_bounce'] = item_att['return_bounce']+1
                
        case '27':
            if skills['shoot_upward']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '28':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']

        case '29':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '30':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '31':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '32':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '33':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '34':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '35':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '36':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '37':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '39':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
                
        case '':
            if skills['']:
                item_att['current_damage'] = item_att['previous_damage']
            else:
                item_att['current_damage'] = item_att['previous_damage']
            
            
        case other:
            print('Undeveloped item: '+item_att[item_id])

    item_att = effective_damage_updater(item_id=item_id, item_att=item_att, previous_item_att=previous_item_att, skills=skills, base_damage=base_damage, count_add_1_damage=count_add_1_damage)

    return item_att


# future use: The effective damage calculation will be done on item level. There are some items that are counted at or after the ejection happened.
# These should be calculated at the end of the path. I will have an estimated damage by the damage updater it self, but it will be incorrect. 
# example: Flat damage increase after a bounce item will be ignored. The bounce calculation should be calculated on items after the bounce itself.
# to_do:
#   move it to the damage_updater.py
#   complete the code
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