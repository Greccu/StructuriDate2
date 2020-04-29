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

    def search(self, value):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value == value:
                return 1
            else:
                level -= 1
        return 0


    def insert(self, value, probability=1/2):
        level = self.startnode.level
        currentnode = self.startnode
        while level>=0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                level-=1
            else:
                currentnode=currentnode.successors[level]
                break

        level = 0
        aux=currentnode.successors[level]
        currentnode.successors[level] = Node(value, 0, currentnode, aux)
        aux.predecessors[level] = currentnode.successors[level]
        currentnode=currentnode.successors[level]
        while odd(probability):
            level+=1
            currentnode.level+=1
            if level > self.startnode.level:
                self.startnode.level+=1
                self.startnode.successors.append(currentnode)
                self.endnode.level+=1
                self.endnode.predecessors.append(currentnode)
                currentnode.predecessors.append(self.startnode)
                currentnode.successors.append(self.endnode)
            else:
                predecessor = currentnode.predecessors[level-1]
                while predecessor.level<level:
                    predecessor = predecessor.predecessors[level-1]
                successor=predecessor.successors[level]
                predecessor.successors[level]=currentnode
                currentnode.predecessors.append(predecessor)
                currentnode.successors.append(successor)
                successor.predecessors[level]=currentnode


    def delete(self,value):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                level -= 1
            else:
                currentnode = currentnode.successors[level]
                break
        nr=0
        while currentnode.value==value:
            while currentnode.level>=0:
                currentnode.predecessors[currentnode.level].successors[currentnode.level]=currentnode.successors[currentnode.level]
                currentnode.successors[currentnode.level].predecessors[currentnode.level]=currentnode.predecessors[currentnode.level]
                currentnode.level-=1
            if currentnode.predecessors[0].value==value:
                currentnode=currentnode.predecessors[0]
            else:
                currentnode=currentnode.successors[0]
            nr+=1
        return nr

    def predecessor(self,value):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                level -= 1
            else:
                currentnode = currentnode.successors[level]
                break
        return currentnode.value

    def successor(self,value):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                level -= 1
            else:
                currentnode = currentnode.successors[level]
                break
        if currentnode.value<value:
            currentnode=currentnode.successors[0]
        if currentnode.value==float("inf"):
            return -1
        return currentnode.value

    def interval(self,value,value2):
        level = self.startnode.level
        currentnode = self.startnode
        while level >= 0:
            if currentnode.successors[level].value < value:
                currentnode = currentnode.successors[level]
            elif currentnode.successors[level].value > value:
                level -= 1
            else:
                currentnode = currentnode.successors[level]
                break
        while currentnode.value <= value:
            currentnode = currentnode.successors[0]
        inter=""
        while currentnode.value < value2:
            inter = inter + str(currentnode.value) + " "
            currentnode=currentnode.successors[0]
        return inter[:-1]


switcher = {
    "1":SkipList.insert,
    "2":SkipList.delete,
    "3":SkipList.search,
    "4":SkipList.predecessor,
    "5":SkipList.successor,
    "6":SkipList.interval
}

with open("abce.in",'r') as f:
    with open("abce.out",'w') as g:
        l = SkipList()
        n=int(f.readline())
        for _ in range(n):
            x=f.readline().split()
            if x[0] in ("1","2"):
                switcher[x[0]](l,int(x[1]))
            elif x[0] == "6":
                g.write(switcher[x[0]](l,int(x[1]),int(x[2]))+"\n")

            else:
                g.write(str(switcher[x[0]](l,int(x[1])))+"\n")