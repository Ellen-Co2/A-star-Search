import numpy as np
import math as mth
import time
import random as rd
import resource
class Grid():  # pass a list/tuple of index [r,c]
    def __init__(self, node):
        self.r = node[0]
        self.c = node[1]
        self.parent = []  # to store the grid object of its parent
        self.gval = {}
        self.fval = {}
        self.hval = {}

    def get_neighbor(self):  # 8 neighbor id list, remove those blocked
        nlist = [(self.r - 1, self.c - 1), (self.r - 1, self.c), (self.r - 1, self.c + 1), (self.r, self.c - 1),
                 (self.r, self.c + 1), (self.r + 1, self.c - 1), (self.r + 1, self.c), (self.r + 1, self.c + 1)]
        if (self.parent.r, self.parent.c) in nlist: nlist.remove((self.parent.r, self.parent.c))
        nlist_len = len(nlist)
        for n_ind in range(nlist_len - 1, -1, -1):
            (i, j) = nlist[n_ind]
            if ((i >= 0) and (j >= 0) and (i <= 119) and (j <= 159)):
                # print ("in if loop:"+str(i)+" "+str(j))
                s_id = mapdata[i][j]  # use the global mapdata variable
                if s_id == "0":
                    nlist.remove((i, j))
            else:
                # print ("need to remove "+str(i)+" "+str(j))
                nlist.remove((i, j))
        return nlist


class BinaryHeap_A():  # to implement frindge in Astar
    def __init__(self):
        self.heapList = [0]
        self.size = 0
        self.idlist = {}  # dictionary to store the (r,c): address for grids put in

    def heapUp(self, i):  # bubble up the ith element
        while i // 2 > 0:
            if self.heapList[i].fval <= self.heapList[i // 2].fval:  # smaller than its parent then change
                if ((self.heapList[i].fval == self.heapList[i // 2].fval) and (
                    self.heapList[i].gval <= self.heapList[i // 2].gval)):
                    i = i // 2
                    continue
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def minChild(self, i):  # return the index of min child of i
        if i * 2 + 1 > self.size:
            return i * 2
        elif self.heapList[i * 2].fval <= self.heapList[i * 2 + 1].fval:
            if (self.heapList[i * 2].fval == self.heapList[i * 2 + 1].fval) and (
                self.heapList[i * 2].gval <= self.heapList[i * 2 + 1].gval): return i * 2 + 1
            return i * 2
        else:
            return i * 2 + 1

    def heapDown(self, i):  # put down from the ith element
        while (i * 2) <= self.size:
            m = self.minChild(i)
            if self.heapList[i].fval >= self.heapList[m].fval:  # swap when larger fval
                if ((self.heapList[i].fval == self.heapList[m].fval) and (
                    self.heapList[i].gval > self.heapList[m].gval)):
                    i = m
                    continue
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[m]
                self.heapList[m] = tmp
            i = m

    def popMin(self):  # dummy node at 0
        poped = self.heapList[1]
        self.idlist.pop((poped.r, poped.c), None)  # remove the poped id from dictionary
        self.heapList[1] = self.heapList[self.size]
        self.size = self.size - 1
        self.heapList.pop()
        self.heapDown(1)
        return poped

    def insert(self, grid):
        self.heapList.append(grid)
        self.size = self.size + 1
        self.heapUp(self.size)
        self.idlist[(grid.r, grid.c)] = grid

    def update(self, new):  # update the old grid' gval, fval & parent to new grid
        old = self.idlist.get((new.r, new.c))
        old.gval = new.gval
        old.fval = new.fval
        old.parent = new.parent
        self.heapUp(self.heapList.index(old))


def Astar_weight(start, target, Map, H_id, W=1):
    global S
    global T
    S = Grid(start)
    T = Grid(target)
    S.parent = S
    S.gval = 0
    S.hval = get_hval(S, H_id, Map)
    S.fval = S.gval + W * S.hval
    T.hval = 0
    fringe = BinaryHeap_A()  # frindge stores Grids
    fringe.insert(S)
    f_set = set()  # f_list stores id in frindge
    c_set = set()  # c_list stores id in closed
    closed = []

    while fringe.size > 0:
        u = fringe.popMin()
        f_set.discard((u.r, u.c))
        c_set.add((u.r, u.c))
        closed.append(u)
        if (u.r, u.c) == (T.r, T.c):
            print "path found!"
            return dict(expanded=closed, gval=u.gval)
            break
            # return path then can trace paths
        if len(u.get_neighbor()) > 0:  # if has neighbor can be expanded
            for (r, c) in u.get_neighbor():
                if (r, c) not in c_set:
                    if (r, c) not in f_set:
                        v = Grid([r, c])
                        f_set.add((r, c))
                        v.parent = u
                        v.hval = get_hval(v, H_id, Map)
                        v.gval = float("inf")
                        v.fval = W * v.hval + v.gval
                    else:
                        v = fringe.idlist.get((r, c))  # fetch the node from frindge and update it
                    UpdateVertex_A(u, v, Map, fringe, W)  # pass the Grid to update fringe
        else:
            continue
    print "---------no paths found------- stop at %s with cost: %s" % ((u.r, u.c), u.gval)
    return dict(expanded=closed, gval=u.gval)


def get_hval(grids, H_id, Map):
    if H_id == 0:
        return 0
    if H_id == 1:  # use Manhattan Distance to Goal node as hval
        return abs(grids.r - T.r) + abs(grids.c - T.c)
    if H_id == 2:  # use actual travel distance to Goal node as hval
        travel = mth.sqrt(2) * min(abs(grids.r - T.r), abs(grids.c - T.c)) + abs(abs(grids.r - T.r)-abs(grids.c - T.c)) 
        return travel
    if H_id == 3:  # use weighted Manhattan
        mov_cost = get_cost(grids.parent,grids,Map)
        return mov_cost * (abs(grids.r - T.r) + abs(grids.c - T.c))
    if H_id == 4:  # consider the number of blocked cell in neighbor of v
        # count the highway cell in the region
        block_ratio = 1 - len(grids.get_neighbor()) / 8
        travel_distance = mth.sqrt(2) * min(abs(grids.r - T.r), abs(grids.c - T.c)) + max(abs(grids.r - T.r),abs(grids.c - T.c)) - min(abs(grids.r - T.r), abs(grids.c - T.c))
        return block_ratio * travel_distance
    if H_id == 5:  # consider the highway block cell and blocked cell ratio as weight to minimum distance
        h_num = 0
        total_l = 0
        for (i, j) in grids.get_neighbor():
            total_l = total_l + 1
            if Map[i][j] not in ["1", "0", "2"]: 
                h_num = h_num + 1
        hard_ratio = min(0.25, (1.-h_num/(1.+len(grids.get_neighbor()))) ) # removed the parent so add 1
        #print hard_ratio
        M_distance = abs(grids.r - T.r) + abs(grids.c - T.c)
        return hard_ratio * M_distance


def UpdateVertex_A(u, v, Map, fringe, W):  # u, v are grids
    edge = get_cost(u, v, Map)  # additional g added to move to v
    if u.gval + edge < v.gval:
        v.fval = u.gval + edge + W * v.hval
        v.gval = u.gval + edge
        v.parent = u
        if fringe.idlist.get((v.r, v.c), 0) != 0:
            # print "update",v.r,v.c
            fringe.update(v)
        else:
            fringe.insert(v)


def get_cost(old, new, Map):  # pass the Grid ,travel from old to new
    act = [Map[old.r][old.c], Map[new.r][new.c]]  # Map from function UniformSearch
    multi = 1  # to add the highway effet to cost
    for i in act:
        if i[0] == "a":
            act[act.index(i)] = "1"
            multi = multi * 0.5
        elif i[0] == "b":
            act[act.index(i)] = "2"
            multi = multi * 0.5
            # make the highway with number mark to type only
    move = set(act)
    if len(move) < 2:
        if "1" in move:
            action_cost = 1 * multi
        else:
            action_cost = 2 * multi
        if min(abs(new.r - old.r), abs(new.c - old.c)) > 0:  # move diagonally
            action_cost = action_cost * mth.sqrt(2.)
    else:
        action_cost = (1. + 2.) / 2 * multi
        if min(abs(new.r - old.r), abs(new.c - old.c)) > 0:  # move diagonally
            action_cost = action_cost * mth.sqrt(2.)
    return action_cost


def trace_path(close, s_node):  # pass the list of expanded, start node in tuple (r,c)
    max_p = len(close)
    t_node = close[-1]
    count = 0
    path_list = []
    while (t_node.r, t_node.c) != s_node:
        pathinfo = (t_node.r, t_node.c, t_node.gval, t_node.hval)
        path_list.append(pathinfo)
        t_node = t_node.parent
        # print type(pid),pid
        count = count + 1
        if count >= max_p:
            print "cycle!!"
            break
    return path_list


def start_goal(row, col, mapvar):  # pass the generated map variable to the function,return a list of 2 tuples
    s = (0, 10)
    g = (9, 3)
    while (((abs(s[0] - g[0]) + abs(s[1] - g[1])) <= 100) | (mapvar[s[0]][s[1]] == "0") | (mapvar[g[0]][g[1]] == "0")):
        if rd.randrange(2) > 0:
            r = rd.sample((range(20) + range(row - 20, row)), 1)
            c = rd.randrange(col)
            g = (r[0], c)
        else:
            r = rd.randrange(row)
            c = rd.sample((range(20) + range(col - 20, col)), 1)
            s = (r, c[0])
    return [s, g]


ask1 = raw_input("Run the Search? (1: yes, other: no) =>>> ")
try:
    if int(ask1) == 1:
        flag = 1
except:
    flag = 0
    print "other input, exit!"
    pass
flag = 1
mapid = raw_input("please input the input map file name,or hit enter exit: ")
if len(mapid) <= 0: flag = 0
mr = str(mapid) + ".txt"
mapdata = np.loadtxt(mr, skiprows=8, delimiter=",", dtype="S4")  # mapdata need to be globle
pairs = int(raw_input("please input number for pairs of start/goal nodes: "))
print "start generating pairs...."
pair_l = []  # list to put [start,goal] tuple list
'''
for i in range(pairs):
    p_obj = start_goal(120, 160, mapdata)
    pair_l.append(p_obj)
'''
#pair_l =[[(114,5 ),(115,155)]]#demo test

pair_l = [[(13, 140), (9, 3)]]#, [(1, 157), (9, 3)], [(0, 10), (109, 50)], [(0, 10), (108, 132)], [(34, 146), (9, 3)], [(118, 141), (9, 3)], [(48, 159), (9, 3)], [(93, 142), (9, 3)], [(0, 10), (8, 117)], [(102, 7), (10, 80)]]
print "start/end list: ", pair_l
'''    l = []  
    with open(mr,"r") as fr:
        for i in range(11):
            line = fr.next()
            l.append(line.rstrip().split())
print l
    fr.close()
start = [int(i) for i in l[0]]
goal = [int(i) for i in l[1]]'''
while flag == 1:
    print "please choose the algorithms coefficients: "
    try:
        h_id = int(raw_input("Enter the heuristics ID(0-5): "))
        ww = float(raw_input("Enter the weight for heuristics: "))
    except:
        print "unacceptable input! Restart..."
        continue
    ff = mapid + "H" + str(h_id) + str(ww) + "S.csv"
    with open(ff, "w") as sw:
        for [start, goal] in pair_l:
            print "start at: %s, goal is : %s" % (str((start[0] + 1, start[1] + 1)), str((goal[0] + 1, goal[1] + 1)))

            memo = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
            print "memory peak before search: %s Kb " % memo
            t1 = time.time()
            Astar_closed = Astar_weight(start=start, target=goal, Map=mapdata, W=ww, H_id=h_id)
            t2 = time.time()
            memo2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024

            print "memory peak after search: %s Mb " % memo2
            mem = memo2 - memo

            print "used time: ", t2 - t1
            tcount = round(t2 - t1, 4)
            sw.write(str(tcount))
            sw.write(",")

            print "total path cost: ", Astar_closed["gval"]
            cos = str(round(Astar_closed["gval"], 3))
            sw.write(cos)
            sw.write(",")

            Anip = trace_path(Astar_closed["expanded"], start)

            print "expanded %s nodes" % len(Astar_closed["expanded"])
            expand_len = str(len(Astar_closed["expanded"]))
            sw.write(expand_len)
            sw.write(",")

            print "cost of memory: ", mem
            sw.write(str(mem))
            sw.write(",")

            print " the path length is : ", len(Anip) + 1
            sw.write(str(int(len(Anip) + 1)))
            sw.write("\n")

            ask = raw_input("please input the path file name or hit enter to skip print: ")
            if len(ask) > 0:
                aa = raw_input("would you like to print the h,g value? 1 for yes,otherwise no: => ")
                pw = str(ask) + ".txt"
                with open(pw, "w") as f:
                    f.write(cos)
                    f.write("\n")
                    if (aa!="1"):
                        sn_w = str(start[0]) + " " + str(start[1])
                        f.write(sn_w)
                        f.write("\n")
                        for ind in range(len(Anip) - 1, -1, -1):
                            node = Anip[ind]
                            n_w = str(node[0]) + " " + str((node[1]))
                            f.write(n_w)
                            f.write("\n")
                    else:
                        sn_w = str(start[0]) + " " + str(start[1]) + " " +str(0)+ " " +str(Astar_closed["expanded"][0].hval)
                        f.write(sn_w)
                        f.write("\n")
                        for ind in range(len(Anip) - 1, -1, -1):
                            node = Anip[ind]
                            n_w = str(node[0]) + " " + str((node[1])) + " " + str((node[2])) + " " + str((node[3])) 
                            f.write(n_w)
                            f.write("\n")
                f.close()
                print "path file written, finished"
    sw.close()
    flag = int(len(raw_input("stop? hit other key! enter to continue..."))) + 1

'''
hard_center = []
for [i,j] in l:
    hard_center.append((int(i),int(j)))
#print hard_center
print "memory peak1: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024/1024

print "memory peak2: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024/1024

'''
