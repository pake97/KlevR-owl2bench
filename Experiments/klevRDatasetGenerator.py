import sys
from klevr.select_scenes import select_scene
from klevr.composeScene import scene2D, scene3D, scene1D
from klevr.adjust_scene import adjust_scene
from klevr.ABox_writer import write_ABox
import os 
def main(clevr_train_scene_path,clevr_val_scene_path,SEED,num_objects,mode,inc, profile):

    inconsistency =  inc=='True'

    selected_scene, scenes = select_scene(clevr_train_scene_path,clevr_val_scene_path,SEED,num_objects)
    if(mode=='1D'):
        relationships, inconsistency_triples = scene1D(selected_scene,SEED,scenes,inconsistency)
    if(mode=='2D'):
        relationships, inconsistency_triples = scene2D(selected_scene,SEED,scenes,inconsistency)
    if(mode=='3D'):
        relationships, inconsistency_triples = scene3D(selected_scene,SEED,scenes,inconsistency)


    output_scenes = []
    for scene in scenes:
        output_scenes.append(adjust_scene(scene))

    print(inconsistency)
    output_file=""
    if inconsistency:
        output_file = "{object}{mode}{profile}-inconsistent-KlevR.owl".format(object=num_objects,mode=mode,profile=profile)
    else:
        output_file = "{object}{mode}{profile}-KlevR.owl".format(object=num_objects,mode=mode,profile=profile)
    #output = {"selected_scene": output_scenes, "connection_triples": relationships, "inconsistency": inconsistency}
    write_ABox(output_scenes, relationships,inconsistency_triples, profile, output_file)

if __name__ == '__main__':
    argv = sys.argv[1:]
    main(clevr_train_scene_path = os.getcwd()+argv[0],clevr_val_scene_path = os.getcwd()+argv[1],SEED=int(argv[2]),num_objects=int(argv[3]),mode=argv[4]+'D',inc=argv[5],profile=argv[6]) 