from random import random


def odd(probability=1 / 2):
    if random() < probability:
        return 1
    else:
        return 0


class Node:
    # valoare
    # nivelul nodului
    # liste de predecesori si succesori de forma [p/d de pe nivelul i, 0<=i<=nivel]
    def __init__(self, value, level, predecessors = None, successors = None):
        self.value = value
        self.level = level
        if isinstance(predecessors, Node):
            self.predecessors = []
            self.predecessors.append(predecessors)
        else:
            self.predecessors = predecessors
        if isinstance(successors, Node):
            self.successors = []
            self.successors.append(successors)
        else:
            self.successors = successors


class SkipList:
    # primul nod este -1 iar ultimul +inf
    # primul si ultimul nod se afla pe mereu nivelul maxim
    def __init__(self):
        self.startnode = Node(-1, 0, None, [])
        self.endnode = Node(float("inf"), 0, self.startnode, None)
        self.startnode.successors.append(self.endnode)
        self.level = 0

    def afisare(self):
        print("\n\nafisare")
        for i in range(self.startnode.level,-1,-1):
            print("Level {}: ".format(i), end="")
            currentnode = self.startnode
            while currentnode:
                print(currentnode.value, end=" ")
                if currentnode.successors == None:
                    currentnode = 0
                else:
                    currentnode = currentnode.successors[i]

            print()
        print("stop afisare")
        print()
    def search(self, value):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
                #print("Nivel curent {}, nod curent{}".format(level,currentnode.value))
            elif currentnode.successors[level].value == value:
                return 1
            else:
                level -= 1
        #print("cautare",value,level,currentnode.value)
        return 0


    def insert(self, value, probability=1/2):
        level = self.startnode.level
        currentnode = self.startnode
        while level>=0:
            #print("nivel",level,"nod",currentnode.value,"valoare",value)
            if currentnode.successors[level].value < value:
                #print("caz 1")
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                #print("caz 2")
                level-=1
            else:
                #print("caz 3")
                currentnode=currentnode.successors[level]
                break

        #print("inserare",value,"gasit predecesor",currentnode.value)
        level = 0
        aux=currentnode.successors[level]
        currentnode.successors[level] = Node(value, 0, currentnode, aux)
        aux.predecessors[level] = currentnode.successors[level]
        currentnode=currentnode.successors[level]
        while odd(probability):
            level+=1
            currentnode.level+=1
            if level > self.startnode.level:
                #print("nivel inexistent")
                self.startnode.level+=1
                self.startnode.successors.append(currentnode)
                self.endnode.level+=1
                self.endnode.predecessors.append(currentnode)
                currentnode.predecessors.append(self.startnode)
                currentnode.successors.append(self.endnode)
            else:
                #print("nivel existent")
                predecessor = currentnode.predecessors[level-1]
                #print("nod curent",currentnode.value,"predecesor",predecessor.value,"nivel",level)
                while predecessor.level<level:
                    #print("nod curent", currentnode.value, "predecesor", predecessor.value, "nivel", level)
                    #print(predecessor.predecessors,predecessor.successors)
                    predecessor = predecessor.predecessors[level-1]
                #("gasit primul predecesor cu nivel indeajuns de mare",predecessor.value)
                successor=predecessor.successors[level]
                predecessor.successors[level]=currentnode
                currentnode.predecessors.append(predecessor)
                currentnode.successors.append(successor)
                successor.predecessors[level]=currentnode




l = SkipList()
l.insert(7)
#l.afisare()
l.insert(3)
#l.afisare()
l.insert(8)
#l.afisare()
l.insert(9)
#l.afisare()
l.insert(5)
#l.afisare()
l.afisare()
print(l.search(7))
