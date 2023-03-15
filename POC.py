import random
import re
import numpy as np
import pandas as pd

base_damage = 5
build_example = '109060606060606060606060601050606010010010010010010010010010010010010010010010010010050551051010050051010043040010010010010043300040552010550552010572430010010010050301041550552010550552010562420010010010240242010550552010550552010562410010010010240242010550552010550552010562360010010010240242010550552010550552010562210010010010240242010570552010550552010562260010010010240242010550552010550552010552160010010010053052010280552010550552010552160010010010010010010280042551041572010552510010010010010030010053153153651572010552480010010010010053363163163453343052010642470010010010010010010010010010010010010010020010010'

custom_block_mapping = {'01':'ejection_up', '02':'auto_fly', '03':'second_try'
                        , '04':'manual_burst', '05':'3x3', '06':'blue'
                        , '07':'longer_countdown', '08':'light_green', '09':'skipp'
                        , '10':'10%_more', '11':'ejection_side', '12':'red_after_wave'}

def parse_build(build):
    custom = build[0:1] # custom ship Y/N
    custom_blocks = build[1:33] # custom blocks
    custom_block_list = re.findall('..?',custom_blocks)
    custom_block_name_2d_array = np.reshape(custom_block_mapper(custom_block_list), (4,4))
    custom_block_id_2d_array = np.reshape(custom_block_list, (4,4))
    items = build[33:] #items
    item_list = re.findall('...?',items)
    return custom_block_list, custom_block_name_2d_array, custom_block_id_2d_array, item_list
    
def chance(percentage):
    chance = random.randint(0,percentage)
    return chance

def custom_block_mapper(custom_block_number):
    custom_block_mapping = {'01':'ejection_up', '02':'auto_fly', '03':'second_try'
                        , '04':'manual_burst', '05':'3x3', '06':'blue'
                        , '07':'longer_countdown', '08':'light_green', '09':'skipp'
                        , '10':'10%_more', '11':'ejection_side', '12':'red_after_wave'}
    custom_block_element_name = [custom_block_mapping[x] for x in custom_block_number]
    return custom_block_element_name

def wrapper():
    print(chance(100))

if __name__ == "__main__":
    wrapper()
