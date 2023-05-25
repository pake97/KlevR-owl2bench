def adjust_scene(scene):
    if(('objects' in scene.keys()) or len(scene['objects'])>0):
        idx=0
        dictt={}
        for obj in scene['objects']:
            if(obj["material"] == 'metal'):
                obj["material"] = 'metallic'
            dictt['o'+str(idx)]='o'+str(idx)+"Scene"+str(scene['image_index'])+scene["split"][0]
            idx+=1
        idx=0
        for obj in scene['objects']:
            obj["id"]= dictt['o'+str(idx)]
            obj["hasOnLeft"]=["o"+str(j)  for j in scene["relationships"]["left"][idx]]
            obj["hasOnRight"] = [dictt["o" + str(j)]  for j in scene["relationships"]["right"][idx]]
            obj["hasOnFront"] = [dictt["o" + str(j)]  for j in scene["relationships"]["front"][idx]]
            obj["hasBehind"] = [dictt["o" + str(j)]  for j in scene["relationships"]["behind"][idx]]
            obj["hasDirectlyOnLeft"] = [dictt["o" + str(scene["relationships"]["left"][idx][0])] ] if len(scene["relationships"]["left"][idx])>0 else []
            obj["hasDirectlyOnRight"] = [dictt["o" + str(scene["relationships"]["right"][idx][0])] ] if len(scene["relationships"]["right"][idx])>0 else []
            obj["hasDirectlyOnFront"] = [dictt["o" + str(scene["relationships"]["front"][idx][0]) ]] if len(scene["relationships"]["front"][idx])>0 else []
            obj["hasDirectlyBehind"] = [dictt["o" + str(scene["relationships"]["behind"][idx][0]) ]] if len(scene["relationships"]["behind"][idx])>0 else []
            obj["color"] = obj["color"].capitalize()
            obj["size"] = obj["size"].capitalize()
            obj["shape"] = obj["shape"].capitalize()
            obj["material"] = obj["material"].capitalize()
            idx = idx+1
        return scene
    else:
        raise Exception("Empty scene")