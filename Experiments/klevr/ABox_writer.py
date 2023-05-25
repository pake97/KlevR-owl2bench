
import random
from rdflib import Graph


class Individual():
    def __init__(self,name):
        self.name=name
        self.properties=[]
        self.same_individual=[]

    def add_type(self,type):
        self.type = type

    def add_property(self,property,object):
        self.properties.append({"name":property, "object":object})

    def add_same_as(self,object):
        self.same_individual.append(object)


    def get_name(self):
        return self.name

    def serialize(self):
        o="<owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"+self.name+"\">\n"
        o+="<rdf:type rdf:resource=\"http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"+self.type+"\"/>\n"
        if(len(self.properties)>0):
            for p in self.properties:
                 o+="<"+p["name"]+" rdf:resource=\"http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"+p["object"]+"\"/>\n"
        if(len(self.same_individual)>0):
            for si in self.same_individual:
                 o+="<owl:sameAs rdf:resource=\"http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"+si+"\"/>\n"

        o+="</owl:NamedIndividual>\n"
        
        return o

    def __str__(self) -> str:
        return "Name: "+self.name+", Type: "+self.type+", Properties: "+ str(self.properties) +", Same As:"+ str(self.same_individual)

class FullScenes():
    def __init__(self):
        self.individuals=[]

    def add_individual(self,individual):
        self.individuals.append(individual)

    def get_individual(self,name):
        ret=None
        for i in self.individuals:
            if(i.get_name()==name):
                ret=i
        return ret

    def serialize(self):
        o = """<?xml version="1.0"?>
                <rdf:RDF xmlns="http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"
                    xml:base="http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"
                    xmlns:owl="http://www.w3.org/2002/07/owl#"
                    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                    xmlns:xml="http://www.w3.org/XML/1998/namespace"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
                    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
                    <owl:Ontology rdf:about="http://www.semanticweb.org/amedeo/ontologies/2022/7/KlevR_EL/"/>\n"""
        
        for ind in self.individuals:
            o+=(ind.serialize())

        o+="</rdf:RDF>"
        
        with open('ABox.owl','w') as f:
            f.write(o)

    def __str__(self) -> str:
        ret=""
        for i in self.individuals:
            ret+=str(i)+"\n"
        return ret
    


def write_ABox(output_scenes, relationships,inconsistency, profile, output_file_name):
    scene = FullScenes()

    for sc in output_scenes :
        for obj in sc['objects']:
            ind = Individual(obj['id'])

            perms = ['{material}{color}{shape}{size}','{color}{material}{shape}{size}','{shape}{material}{color}{size}','{material}{shape}{color}{size}','{color}{shape}{material}{size}','{shape}{color}{material}{size}','{shape}{color}{size}{material}','{color}{shape}{size}{material}','{size}{shape}{color}{material}','{shape}{size}{color}{material}','{color}{size}{shape}{material}','{size}{color}{shape}{material}','{size}{material}{shape}{color}','{material}{size}{shape}{color}','{shape}{size}{material}{color}','{size}{shape}{material}{color}','{material}{shape}{size}{color}','{shape}{material}{size}{color}','{color}{material}{size}{shape}','{material}{color}{size}{shape}','{size}{color}{material}{shape}','{color}{size}{material}{shape}','{material}{size}{color}{shape}','{size}{material}{color}{shape}']
            perm = perms[random.randrange(0,len(perms))]
            color = obj['color']
            material = obj['material']
            shape = obj['shape']
            size = obj['size']
            ind.add_type(perm.format(color=color,material=material,shape=shape,size=size)+"Object")
            if(len(obj['hasDirectlyBehind'])>0):
                ind.add_property('hasDirectlyBehind',obj['hasDirectlyBehind'][0])
            if(len(obj['hasDirectlyOnFront'])>0):
                ind.add_property('hasDirectlyOnFront',obj['hasDirectlyOnFront'][0])
            if(len(obj['hasDirectlyOnRight'])>0):
                ind.add_property('hasDirectlyOnRight',obj['hasDirectlyOnRight'][0])
            if(len(obj['hasDirectlyOnLeft'])>0):
                ind.add_property('hasDirectlyOnLeft',obj['hasDirectlyOnLeft'][0])
            scene.add_individual(ind)
    

   
    for rel in relationships:
        triple = rel.split('-')
        t_subject = scene.get_individual(triple[0])
        if(triple[1]=='SameIndividual'):
            t_subject.add_same_as(triple[2])
        else:
            t_subject.add_property(triple[1],triple[2]) 
            
    for inc in inconsistency:
        triple = inc.split('-')
        t_subject = scene.get_individual(triple[0])
        if(triple[1]=='SameIndividual'):
            t_subject.add_same_as(triple[2])
        else:
            t_subject.add_property(triple[1],triple[2])
        
        

    scene.serialize()
    g1 = Graph()
    g1.parse('ABox.owl', format="xml")
    g2 = Graph()
    if(profile=='EL'):
        g2.parse('elrdf.owl', format="xml")
    if(profile=='QL'):
        g2.parse('qlrdf.owl', format="xml")
    if(profile=='RL'):
        g2.parse('rlrdf.owl', format="xml")
    g3 = g1+g2
    g3.serialize(output_file_name, format="xml")




