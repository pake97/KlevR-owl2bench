import random
import json
from time import time


def getCombinationsUtil(a, sum, currIndex, result, curr):
    if sum == 0:
        result.append(list(curr))
        return
    elif sum < 0 or currIndex == len(a):
        return
    else:
        curr.append(a[currIndex])
        getCombinationsUtil(a, sum - a[currIndex], currIndex, result, curr)
        curr.pop()
        getCombinationsUtil(a, sum, currIndex + 1, result, curr)

def getCombinations(numbers, sum):
    result = []
    curr = []
    index = 0
    getCombinationsUtil(numbers, sum, index, result, curr)
    return result


def clevr_scene_loader(path):
    data={}
    with open(path) as f:
        data = json.load(f)
    return data['scenes']



def select_scene(clevr_train_scene_path,clevr_val_scene_path,SEED, num_objects):
    random.seed(SEED)

    if(num_objects<3):
        return "impossible to create an ABox with less than 3 objects"
    

    data_train= clevr_scene_loader(clevr_train_scene_path)
    data_valid= clevr_scene_loader(clevr_val_scene_path)
    data = data_train+data_valid


    reg_scenes = {'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[]}

    for sc_t in data_train:
        reg_scenes[str(len(sc_t['objects']))].append(sc_t['split']+'-'+str(sc_t['image_index']))
    for sc_v in data_valid:
        reg_scenes[str(len(sc_t['objects']))].append(sc_v['split']+'-'+str(sc_v['image_index']))

    total_objs = 0
    selected_scenes=[]
    scenes = []

    t0 = time()
    while(total_objs+10<num_objects):
        selection = random.randint(0,len(data)-1)
        if(data[selection]['split']+'-'+str(data[selection]['image_index']) not in selected_scenes):
            selected_scenes.append(data[selection]['split']+'-'+str(data[selection]['image_index']))
            scenes.append(data[selection])
            total_objs+=len((data[selection]['objects']))



    options = getCombinations([3,4,5,6,7,8,9,10], num_objects-total_objs)
    
    opt_sel = random.randint(0,len(options)-1)
    
    selected_options=options[opt_sel]

    for so in selected_options:
        valid = False
        
        while(not valid):
            scene_sel = random.randint(0,len(reg_scenes[str(so)])-1)
            if(reg_scenes[str(so)][scene_sel] not in selected_scenes):
                toAppend = reg_scenes[str(so)][scene_sel]
                selected_scenes.append(toAppend)
                
                split = toAppend.split('-')[0]
                sc_index = toAppend.split('-')[1]

                if(split=='train'):
                    scenes.append(data_train[int(sc_index)])
                if(split=='val'):
                    scenes.append(data_valid[int(sc_index)])
                valid=True


    
        
    

    t1 = time()
    print("SELECTED SCENES:" + str(len(selected_scenes)))
    print(selected_scenes)
    print("TIME TO SELECT SCENES")
    print(t1-t0)

    return selected_scenes, scenes
