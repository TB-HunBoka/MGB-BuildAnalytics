def item_att_damage_updater(item_id, item_att, previous_item_att):
    
    #with the current setup, adding flat damage to the projectile, after a bounce or aoe item, will be ignored in the bounce and aoe calculation.
    #most of the time we need to update both current_damage and effective_damage
    ce_damage = ['current_damage','effective_damage']
    e_damage = ['effective_damage']
    
    match str(item_id):
        case '02':
            #generator
            item_att['previous_damage'] = 0
            for key in ce_damage:
                if skills['generator_skilled']:
                    item_att[key] = base_damage+5
                else:
                    item_att[key] = base_damage
            
        case '00':
            #empty
            for key in ce_damage:
                if skills['empty_slot_skilled']:
                    item_att[key] = previous_item_att[key]+70
                else:
                    item_att[key] = previous_item_att[key]
                
        
        case '04':
            #turn_right
            if skills['turn_right_skilled']:
                item_att[key] = previous_item_att[key]+5
            else:
                item_att[key] = previous_item_att[key]

        case '05':
             #turn_left
            if skills['turn_left_skilled']:
                item_att[key] = previous_item_att[key]+5
            else:
                item_att[key] = previous_item_att[key]
                
        case '06':
            item_att[key] = previous_item_att[key]+1
            if skills['add_1_damage_5_skilled']:
                item_att[key] = item_att[key]+5
            if skills['add_1_damage_20_skilled']:
                item_att[key] = item_att[key]+20*count_add_1_damage

        case '07':
            if skills['small_spread_skilled']:
                item_att[key] = previous_item_att[key]+increase_value_by_random_percentage(previous_previous_item_att[key],0.5)
            else:
                item_att[key] = previous_item_att[key]
                
        case '08':
            if skills['large_spread_skilled']:
                item_att[key] = increase_value_by_random_percentage(previous_item_att[key],50)
            else:
                item_att[key] = previous_item_att[key]

        case '09':
            if skills['spread_left_skilled']:
                item_att[key] = increase_value_by_random_percentage(previous_item_att[key],40)
            else:
                item_att[key] = previous_item_att[key]

        case '10':
            if skills['spread_right_skilled']:
                item_att[key] = increase_value_by_random_percentage(previous_item_att[key],40)
            else:
                item_att[key] = previous_item_att[key]
                
        case '11':
            if skills['random_curve_skilled']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '12':
            if skilled['curve_left']:
                item_att[key] = previous_item_att[key]*1.3
            else:
                item_att[key] = previous_item_att[key]
                
        case '13':
            if skilled['curve_right']:
                item_att[key] = previous_item_att[key]*1.3
            else:
                item_att[key] = previous_item_att[key]
        
        case '20':
            if skills['x2_damage_chance']:
                x2_chance = 40
            else:
                x2_chance = 33
                
            if skills['x2_damage_multi']:
                x2_multi = 2.5
            else:
                x2_multi = 2
            item_att[key] = previous_item_att[key]+previous_item_att[key]*chance(x2_chance)*(x2_multi-1)
        
        case '21':
            if skilled['x10_damage_x30']:
                item_att[key] = previous_item_att[key]*(1+29*chance(4))
            elif skilled['x10_damage_x20']:
                item_att[key] = previous_item_att[key]*(1+19*chance(4))
            else:
                item_att[key] = previous_item_att[key]*(1+9*chance(4))
                
        case '22': # for later use
            if skilled['2_way_random_split']:
                item_att[key] = previous_item_att[key]*3
                # and start projectile in 2 direction
            else:
                item_att[key] = previous_item_att[key]*2
                # and start projectile in 2 direction
        
        case '23': # for later use
            if skilled['3_way_random_split']:
                item_att[key] = previous_item_att[key]*4
                # and start projectile in 3 direction
            else:
                item_att[key] = previous_item_att[key]*3
                # and start projectile in 3 direction
                
        case '24':
            #to do: calculate the damage increase for aoe
            item_att['cycle_aoe'] += 1
            if skilled['circle_aoe_penalty']:
                item_att[key] = previous_item_att[key]*(1-0.03)
            else:
                item_att[key] = previous_item_att[key]*(1-0.06)

        case '38':
            #to do: calculate the damage increase for aoe
            item_att['square_aoe'] += 1
            if skilled['square_aoe_penalty']:
                item_att[key] = previous_item_att[key]*(1-0.03)
            else:
                item_att[key] = previous_item_att[key]*(1-0.06)

        case '25':
            # to do: a bounce által okozott damagenövekedés számolása. Bounceonként 17% -al nő. plusz a bounce duplázza a damaget.
            # ezt szeretném figyelembe venni a kimutatásoknál, ezért valahogy le kell implementáljam
            # ha simán úgy viszem tovább, hogy item_att[key] = previous_item_att[key]*bounce, akkor félek
            # hogy a többi bounce típus hibásan fogja tovább szorozni. Ezért lehet ki kell kérjem az item_att-ot. Végig kell gondolni.
            # A bounce úgy kéne működjön, hogy effective_damage = effective_damage+projectile_damage
            if skilled['random_bounce_damage']:
                item_att[key] = previous_item_att[key]*1.17
            if skilled['random_bounce_bounce']:
                item_att['random_bounce'] = item_att['random_bounce']+1*chance(25)
            item_att['random_bounce'] = item_att['random_bounce']+1
                
        case '26':
            if skilled['return_bounce_bounce']:
                item_att['return_bounce'] = item_att['return_bounce']+1*chance(25)
            item_att['return_bounce'] = item_att['return_bounce']+1
                
        case '27':
            if skilled['shoot_upward']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '28':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]

        case '29':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '30':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '31':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '32':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '33':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '34':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '35':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '36':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '37':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '39':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
                
        case '':
            if skilled['']:
                item_att[key] = previous_item_att[key]
            else:
                item_att[key] = previous_item_att[key]
            
            
        case other:
            item_att = {
                "coord": (current_x, current_y),
                "item_id": item[0:2],
                "orientation": orientation,
                "previous_damage" : previous_previous_item_att[key],
                "current_damage": previous_item_att[key]
            }
            
    return item_att