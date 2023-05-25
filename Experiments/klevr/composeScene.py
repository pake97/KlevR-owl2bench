import random 
from time import time 
import numpy as np

class Node():
    def __init__(self,data):
        self.data=data
        self.prev = None
        self.next = None

    def get_data(self):
        return self.data
    
    def get_prev(self):
        return self.prev
    
    def get_next(self):
        return self.next
    
    def set_data(self,data):
        self.data=data
    
    def set_prev(self,prev):
        self.prev = prev
    
    def set_next(self,next):
        self.next=next


class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size=0
        
    def add_first(self,node):
        self.set_head(node)
        self.set_tail(node)
        self.size=1

    def add_to_head(self,node):
        node.set_next(self.head)
        self.head.set_prev(node)
        self.set_head(node)
        self.size+=1

    def add_to_tail(self,node):
        node.set_prev(self.tail)
        self.tail.set_next(node)
        self.set_tail(node)
        self.size+=1

    def set_head(self,node):
        self.head=node

    def set_tail(self,node):
        self.tail = node

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail
        
    def get_size(self):
        return self.size
    
    def to_lsit(self):
        ret = []
        current_node=self.head
        if(current_node==None):
            return ret
        while(True):
            ret.append(current_node.get_data())
            if(current_node.get_next()==None):
                break
            else:
                current_node=current_node.get_next()
        return ret


    def print_array(self):
        lista = []
        lista.append(self.head)
        while(True):
            if(lista[-1].get_next()!=None):
                lista.append(lista[-1].get_next())
            else:
                break

        print([l.get_data() for l in lista])


class Node3D():
    def __init__(self,data):
        self.data=data
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.row=None
        self.col=None

    def get_data(self):
        return self.data
    
    def get_top(self):
        return self.top
    
    def get_bottom(self):
        return self.bottom
    
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def set_data(self,data):
        self.data=data
    
    def set_prev(self,prev):
        self.prev = prev
    
    def set_bottom(self,bottom):
        self.bottom=bottom

    def set_left(self,left):
        self.left = left
    
    def set_right(self,right):
        self.right=right

    def set_row(self,row):
        self.row=row

    def set_col(self,col):
        self.col=col


def get_front_most(scene,split):
    return 'o'+str(scene['relationships']['front'].index([]))+'Scene'+str(scene['image_index'])+split
def get_back_most(scene,split):
    return 'o'+str(scene['relationships']['behind'].index([]))+'Scene'+str(scene['image_index'])+split
def get_left_most(scene,split):
    return 'o'+str(scene['relationships']['left'].index([]))+'Scene'+str(scene['image_index'])+split
def get_right_most(scene,split):
    return 'o'+str(scene['relationships']['right'].index([]))+'Scene'+str(scene['image_index'])+split


def rel_to_triples(scenes,relationships):
    triples=[]
    for rel in relationships:
        if(rel['p']=='b'):
            s =  get_back_most(list(filter(lambda d: d['image_index'] == int(rel['s'].split("-")[1]), scenes))[0],rel['s'].split("-")[0][0])
            o =  get_front_most(list(filter(lambda d: d['image_index'] == int(rel['o'].split("-")[1]), scenes))[0],rel['o'].split("-")[0][0])
            p = '-hasDirectlyBehind-'
            triples.append(s+p+o)
        if(rel['p']=='f'):
            s = get_front_most(list(filter(lambda d: d['image_index'] == int(rel['s'].split("-")[1]), scenes))[0],rel['s'].split("-")[0][0])
            o = get_back_most(list(filter(lambda d: d['image_index'] == int(rel['o'].split("-")[1]), scenes))[0],rel['o'].split("-")[0][0])
            p = '-hasDirectlyOnFront-'
            triples.append(s+p+o)
        if(rel['p']=='r'):
            s = get_right_most(list(filter(lambda d: d['image_index'] == int(rel['s'].split("-")[1]), scenes))[0],rel['s'].split("-")[0][0])
            o = get_left_most(list(filter(lambda d: d['image_index'] == int(rel['o'].split("-")[1]), scenes))[0],rel['o'].split("-")[0][0])
            p = '-hasDirectlyOnRight-'
            triples.append(s+p+o)
        if(rel['p']=='l'):
            s = get_left_most(list(filter(lambda d: d['image_index'] == int(rel['s'].split("-")[1]), scenes))[0],rel['s'].split("-")[0][0])
            o = get_right_most(list(filter(lambda d: d['image_index'] == int(rel['o'].split("-")[1]), scenes))[0],rel['o'].split("-")[0][0])
            p = '-hasDirectlyOnLeft-'
            triples.append(s+p+o)
        if(rel['p']=='a' or rel['p']=='u'):
            s = get_right_most(list(filter(lambda d: d['image_index'] == int(rel['s'].split("-")[1]), scenes))[0],rel['s'].split("-")[0][0])
            o = get_right_most(list(filter(lambda d: d['image_index'] == int(rel['o'].split("-")[1]), scenes))[0],rel['o'].split("-")[0][0])
            p = '-SameIndividual-'
            triples.append(s+p+o)
    return triples


def getInconsitency1D(list, SEED):
    random.seed(SEED)
    first = random.randint(0, len(list) - 1)
    second = first
    while True:
        second = random.randint(0, len(list) - 1)
        if second != first and abs(first - second) > 1:
            break

    if first < second:
        return {"s": list[first], "p": "l", "o": list[second]}
    else:
        return {"s": list[first], "p": "r", "o": list[second]}


def getInconsitency2D(matrix, SEED):
    random.seed(SEED)
    cells = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            cells.append((i, j))
    while True:
        first = random.randint(0, len(cells) - 1)
        second = random.randint(0, len(cells) - 1)
        if (
            matrix[cells[first][0]][cells[first][1]] != 0.0
            and matrix[cells[second][0]][cells[second][1]] != 0.0
        ):
            if second != first and (
                abs(cells[first][0] - cells[second][0]) > 1
                or abs(cells[first][1] - cells[second][1]) > 1
            ):
                break
    possible_rel = []
    if cells[first][0] - cells[second][0] > 1:
        possible_rel.append("l")
    if cells[first][0] - cells[second][0] < -1:
        possible_rel.append("r")
    if cells[first][1] - cells[second][1] > 1:
        possible_rel.append("b")
    if cells[first][1] - cells[second][1] < -1:
        possible_rel.append("f")

    selected_relationship = random.choice(possible_rel)

    if selected_relationship == "l":
        return {
            "s": matrix[cells[first][0]][cells[first][1]],
            "p": "r",
            "o": matrix[cells[second][0]][cells[second][1]],
        }
    if selected_relationship == "r":
        return {
            "s": matrix[cells[first][0]][cells[first][1]],
            "p": "l",
            "o": matrix[cells[second][0]][cells[second][1]],
        }
    if selected_relationship == "f":
        return {
            "s": matrix[cells[first][0]][cells[first][1]],
            "p": "b",
            "o": matrix[cells[second][0]][cells[second][1]],
        }
    if selected_relationship == "b":
        return {
            "s": matrix[cells[first][0]][cells[first][1]],
            "p": "f",
            "o": matrix[cells[second][0]][cells[second][1]],
        }


def getInconsitency3D(matrix, SEED):
    random.seed(SEED)
    cells = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                cells.append((i, j, k))
    while True:
        first = random.randint(0, len(cells) - 1)
        second = random.randint(0, len(cells) - 1)
        if (
            matrix[cells[first][0]][cells[first][1]][cells[first][2]] != 0.0
            and matrix[cells[second][0]][cells[second][1]][cells[second][2]] != 0.0
        ):
            if second != first and (
                abs(cells[first][0] - cells[second][0]) > 1
                or abs(cells[first][1] - cells[second][1]) > 1
                or abs(cells[first][2] - cells[second][2]) > 1
            ):
                break
    possible_rel = []
    if cells[first][0] - cells[second][0] > 1:
        possible_rel.append("l")
    if cells[first][0] - cells[second][0] < -1:
        possible_rel.append("r")
    if cells[first][1] - cells[second][1] > 1:
        possible_rel.append("b")
    if cells[first][1] - cells[second][1] < -1:
        possible_rel.append("f")
    if cells[first][2] - cells[second][2] > 1:
        possible_rel.append("a")
    if cells[first][2] - cells[second][2] < -1:
        possible_rel.append("u")

    selected_relationship = random.choice(possible_rel)

    if selected_relationship == "l":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "r",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }
    if selected_relationship == "r":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "l",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }
    if selected_relationship == "f":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "b",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }
    if selected_relationship == "b":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "f",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }
    if selected_relationship == "a":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "u",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }
    if selected_relationship == "u":
        return {
            "s": matrix[cells[first][0]][cells[first][1]][cells[first][2]],
            "p": "a",
            "o": matrix[cells[second][0]][cells[second][1]][cells[second][2]],
        }

def scene1D(scenes,SEED, scenes_array, inconsistency):
    random.seed(SEED)
    t0=time()
    scenes_list=LinkedList()
    scenes_pool = scenes.copy()
    relationships=[]
    while(len(scenes_pool)>0):
        selected_scene = random.choice(scenes_pool)
        scenes_pool.remove(selected_scene)
        scene_node = Node(selected_scene)
        if(scenes_list.get_size()==0):
            scenes_list.add_first(scene_node)            
        else:
            direction = random.choice([0,1])
            if(direction==0):
                relationships.append({'s':scenes_list.get_head().get_data(),'p':'l', 'o':selected_scene})
                scenes_list.add_to_head(scene_node)
            else:
                relationships.append({'s':scenes_list.get_tail().get_data(),'p':'r', 'o':selected_scene})
                scenes_list.add_to_tail(scene_node)
    
    t1=time()
    print("1D ARRAY OF SCENES")
    print()
    print()
    print(scenes_list.to_lsit())
    print()
    print()
    print("RELATIONSHIPS TO ADD")
    print(relationships)
    print()
    print()
    print("TIME TO GENERATE 1D ARRAY OF SCENES")
    print(t1-t0)
    print()
    print()
    print("TO TRIPLES")
    print()
    print()
    triples1d=rel_to_triples(scenes_array,relationships)
    print(triples1d)
    print()
    print()

    inconsistency_triples=[]
    if inconsistency:
        inc = getInconsitency1D(scenes_list.to_lsit(), SEED)
        print("INCONSITENCY")
        print()
        print()
        print(inc)
        print()
        print()
        print("TO TRIPLES")
        print()
        print()
        inconsistency_triples = rel_to_triples(scenes_array, [inc])
        print(inconsistency_triples)
        print()
        print()

    return triples1d, inconsistency_triples


def scene2D(scenes,SEED,scenes_array, inconsistency):
    random.seed(SEED)
    t0=time()
    scenes_pool = scenes.copy()
    scene_matrix = np.zeros((len(scenes),len(scenes))).tolist()
    possible_additions=[]
    relationships=[]
    while(len(scenes_pool)>0):
        selected_scene = random.choice(scenes_pool)
        scenes_pool.remove(selected_scene)    
        scene_node = Node3D(selected_scene)


        if(len(scenes_pool)==(len(scenes)-1)):
            row = random.randint(0,len(scenes)-1)
            col = random.randint(0,len(scenes)-1)            
            """ scene_node.set_col(col)
            scene_node.set_row(row)
            scene_matrix[row][col]=scene_node """
            scene_matrix[row][col]=selected_scene
            if(col>0):
                possible_additions.append([row,col-1])#left
            if(col<(len(scenes)-1)):
                possible_additions.append([row,col+1])#right
            if(row>0):
                possible_additions.append([row-1,col])#top
            if(row<(len(scenes)-1)):
                possible_additions.append([row+1,col])#bottom
        else:
            new_coordinates = random.choice(possible_additions)
            possible_additions.remove(new_coordinates)
            row = new_coordinates[0]
            col=new_coordinates[1]
            scene_matrix[row][col]=selected_scene
            possible_relationships=[]
            try:
                if(scene_matrix[row+1][col]!=0.0):
                    possible_relationships.append('b')
            except:
                pass
            try:
                if(scene_matrix[row-1][col]!=0.0):
                    possible_relationships.append('f')
            except:
                pass
            try:
                if(scene_matrix[row][col+1]!=0.0):
                    possible_relationships.append('l')
            except:
                pass
            try:
                if(scene_matrix[row][col-1]!=0.0):
                    possible_relationships.append('r')
            except:
                pass
            selected_relationship=random.choice(possible_relationships)
            new_relationship={'s':'','p':selected_relationship,'o':selected_scene}
            if(selected_relationship=='f'):
                new_relationship['s']=scene_matrix[row-1][col]
            if(selected_relationship=='b'):
                new_relationship['s']=scene_matrix[row+1][col]
            if(selected_relationship=='l'):
                new_relationship['s']=scene_matrix[row][col+1]
            if(selected_relationship=='r'):
                new_relationship['s']=scene_matrix[row][col-1]
            
            relationships.append(new_relationship)
            if(col>0 and scene_matrix[row][col-1]==0.0):
                if([row,col-1] not in possible_additions):
                    possible_additions.append([row,col-1])#left
            if(col<(len(scenes)-1) and scene_matrix[row][col+1]==0.0):
                if([row,col+1] not in possible_additions):
                    possible_additions.append([row,col+1])#right
            if(row>0 and scene_matrix[row-1][col]==0.0):
                if([row-1,col] not in possible_additions):
                    possible_additions.append([row-1,col])#top
            if(row<(len(scenes)-1) and scene_matrix[row+1][col]==0.0):
                if([row+1,col] not in possible_additions):
                    possible_additions.append([row+1,col])#bottom
    t1=time()
    print("2D ARRAY OF SCENES")
    print()
    print()
    for row in scene_matrix:
        print(row)
    print()
    print()
    print("RELATIONSHIPS TO ADD")
    print(relationships)
    print()
    print()
    print("TIME TO GENERATE 2D ARRAY OF SCENES")
    print(t1-t0)
    print()
    print()
    print("TO TRIPLES")
    print()
    print()
    triples2d=rel_to_triples(scenes_array,relationships)
    print(triples2d)
    print()
    print()

    inconsistency_triples=[]
    if inconsistency:
        inc = getInconsitency2D(scene_matrix, SEED)
        print("INCONSITENCY")
        print()
        print()
        print(inc)
        print()
        print()
        print("TO TRIPLES")
        print()
        print()
        inconsistency_triples = rel_to_triples(scenes_array, [inc])
        print(inconsistency_triples)
        print()
        print()

    return triples2d, inconsistency_triples




def scene3D(scenes,SEED,scenes_array, inconsistency):
    random.seed(SEED)
    t0=time()
    scenes_pool = scenes.copy()
    scene_matrix = np.zeros((len(scenes),len(scenes),len(scenes))).tolist()
    possible_additions=[]
    relationships=[]
    while(len(scenes_pool)>0):
        selected_scene = random.choice(scenes_pool)
        scenes_pool.remove(selected_scene)


        if(len(scenes_pool)==(len(scenes)-1)):
            row = random.randint(0,len(scenes)-1)
            col = random.randint(0,len(scenes)-1)
            z = random.randint(0,len(scenes)-1)            
            scene_matrix[row][col][z]=selected_scene
            if(col>0):
                possible_additions.append([row,col-1,z])#left
            if(col<(len(scenes)-1)):
                possible_additions.append([row,col+1,z])#right
            if(row>0):
                possible_additions.append([row-1,col,z])#top
            if(row<(len(scenes)-1)):
                possible_additions.append([row+1,col,z])#bottom
            if(z>0):
                possible_additions.append([row,col,z-1])
            if(z<(len(scenes)-1)):
                possible_additions.append([row,col,z+1])
        else:
            new_coordinates = random.choice(possible_additions)
            possible_additions.remove(new_coordinates)
            row = new_coordinates[0]
            col=new_coordinates[1]
            z=new_coordinates[2]
            scene_matrix[row][col][z]=selected_scene
            possible_relationships=[]
            try:
                if(scene_matrix[row+1][col][z]!=0.0):
                    possible_relationships.append('b')
            except:
                pass
            try:
                if(scene_matrix[row-1][col][z]!=0.0):
                    possible_relationships.append('f')
            except:
                pass
            try:
                if(scene_matrix[row][col+1][z]!=0.0):
                    possible_relationships.append('l')
            except:
                pass
            try:
                if(scene_matrix[row][col-1][z]!=0.0):
                    possible_relationships.append('r')
            except:
                pass
            try:
                if(scene_matrix[row][col][z+1]!=0.0):
                    possible_relationships.append('a')
            except:
                pass
            try:
                if(scene_matrix[row][col][z-1]!=0.0):
                    possible_relationships.append('u')
            except:
                pass
            selected_relationship=random.choice(possible_relationships)
            new_relationship={'s':'','p':selected_relationship,'o':selected_scene}
            if(selected_relationship=='f'):
                new_relationship['s']=scene_matrix[row-1][col][z]
            if(selected_relationship=='b'):
                new_relationship['s']=scene_matrix[row+1][col][z]
            if(selected_relationship=='l'):
                new_relationship['s']=scene_matrix[row][col+1][z]
            if(selected_relationship=='r'):
                new_relationship['s']=scene_matrix[row][col-1][z]
            if(selected_relationship=='a'):
                new_relationship['s']=scene_matrix[row][col][z+1]
            if(selected_relationship=='u'):
                new_relationship['s']=scene_matrix[row][col][z-1]
            
            relationships.append(new_relationship)

            if(col>0 and scene_matrix[row][col-1][z]==0.0):
                if([row,col-1,z] not in possible_additions):
                    possible_additions.append([row,col-1,z])#left
            if(col<(len(scenes)-1) and scene_matrix[row][col+1][z]==0.0):
                if([row,col+1,z] not in possible_additions):
                    possible_additions.append([row,col+1,z])#right
            if(row>0 and scene_matrix[row-1][col][z]==0.0):
                if([row-1,col,z] not in possible_additions):
                    possible_additions.append([row-1,col,z])#top
            if(row<(len(scenes)-1) and scene_matrix[row+1][col][z]==0.0):
                if([row+1,col,z] not in possible_additions):
                    possible_additions.append([row+1,col,z])#bottom
            if(z>0 and scene_matrix[row][col][z-1]==0.0):
                if([row,col,z-1] not in possible_additions):
                    possible_additions.append([row,col,z-1])#top
            if(z<(len(scenes)-1) and scene_matrix[row][col][z+1]==0.0):
                if([row,col,z+1] not in possible_additions):
                    possible_additions.append([row,col,z+1])#bottom
    
    t1=time()
    print("3D ARRAY OF SCENES")
    print()
    print()
    for row in scene_matrix:
        for col in row:
            print(col)
    print()
    print()
    print("RELATIONSHIPS TO ADD")
    print(relationships)
    print()
    print()
    print("TIME TO GENERATE 3D ARRAY OF SCENES")
    print(t1-t0)
    print()
    print()
    print("TO TRIPLES")
    print()
    print()
    triples3d=rel_to_triples(scenes_array,relationships)
    print(triples3d)
    print()
    print()

    inconsistency_triples=[]
    if inconsistency:
        inc = getInconsitency3D(scene_matrix, SEED)
        print("INCONSITENCY")
        print()
        print()
        print(inc)
        print()
        print()
        print("TO TRIPLES")
        print()
        print()
        inconsistency_triples = rel_to_triples(scenes_array, [inc])
        print(inconsistency_triples)
        print()
        print()

    return triples3d, inconsistency_triples








