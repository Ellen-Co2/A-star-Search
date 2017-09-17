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


class BinaryHeap_S():  # to implement fringe with priority fval, 
    def __init__(self):
        self.heapList = [0]
        self.size = 0
        self.idlist = {}  # dictionary to store the (r,c): address for grids put in
    
    def __getitem__(self, key):
        return self.heapList[key]

    def heapUp(self, i):  # bubble up the ith element
        while i // 2 > 0:
            if self.heapList[i].fval <= self.heapList[i // 2].fval:  # smaller than its parent then change
                if ((self.heapList[i].fval == self.heapList[i // 2].fval) and (self.heapList[i].gval <= self.heapList[i // 2].gval)):
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
            if (self.heapList[i * 2].fval == self.heapList[i * 2 + 1].fval) and (self.heapList[i * 2].gval <= self.heapList[i * 2 + 1].gval): return i * 2 + 1
            return i * 2
        else:
            return i * 2 + 1

    def heapDown(self, i):  # put down from the ith element
        while (i * 2) <= self.size:
            m = self.minChild(i)
            if self.heapList[i].fval >= self.heapList[m].fval:  # swap when larger fval
                if ((self.heapList[i].fval == self.heapList[m].fval) and (self.heapList[i].gval > self.heapList[m].gval)):
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
        self.idlist[(grid.r, grid.c)] = grid   # point the address to the new object

    def update(self, new):  # update the old grid' gval, fval & parent to new grid
        old = self.idlist.get((new.r, new.c))
        old.gval = new.gval
        old.fval = new.fval
        old.parent = new.parent
        self.heapUp(self.heapList.index(old))

def Astar_seq(start, target, Map, W1, W2):
    global S
    global T
    S = []
    T = [] 
    Open_i = []
    closed_i = []
    clos_set = []
    for h_id in range(5): # initial open_i from 0 to 4
        s = Grid(start)
        t = Grid(target)
        t.hval = 0
        T.append(t)
        s.parent = s
        s.gval = 0
        s.hval = get_hval(s, h_id, Map)
        s.fval = s.gval + W1 * s.hval
        fringe_i = BinaryHeap_S()  # frindge stores Grids
        fringe_i.insert(s)
        Open_i.append(fringe_i)
        closed_i.append([s])   # closed [[s0][s1][s2]...]
        c_set = set()
        c_set.add((s.r,s.c))
        clos_set.append(c_set) # clos_set[set0,set1,...]
        S.append(s)
    #f_set = set()  # f_list stores id in fringe
    #c_set = set()  # c_list stores id in closed
    while Open_i[0].size > 0: # the anchor search fringe not empty
        for h_id in range(1,5): 
            if Open_i[h_id].size > 0:
                u = Open_i[h_id][1]
                A_min = Open_i[0][1] # get the Min node in anchor search
                #print "before compare: ",A_min.fval
                if u.fval <= W2 * A_min.fval:
                    print "in search: ", h_id
                    print u.fval, A_min.fval
                    if (u.r, u.c) == (T[h_id].r, T[h_id].c):
                        closed_i[h_id].append(u)
                        print "path found! Return the %s path" % h_id
                        return dict(expanded = closed_i, h = h_id, gval = u.gval)
                        break
                    else: #expand Open_i h_id
                        u = Open_i[h_id].popMin()
                        if u.gval > 0: # not the start node
                            closed_i[h_id].append(u)
                            clos_set[h_id].add((u.r,u.c))
                        if len(u.get_neighbor()) > 0:
                            for (r,c) in u.get_neighbor():
                                #print "enconter %s , %s" %(r , c)
                                if (r,c) not in clos_set[h_id]: # not in closed set i
                                    if Open_i[h_id].idlist.get((r,c), 0) == 0: # not in open list i
                                        #print "initialize %s %s" %(r,c)
                                        v = Grid([r, c])
                                        v.parent = u
                                        v.hval = get_hval(v, h_id, Map)
                                        v.gval = float("inf")
                                        v.fval = W1 * v.hval + v.gval
                                    else:
                                        v = Open_i[h_id].idlist.get((r, c))  # fetch the node from frindge and update it
                                    UpdateFringe(u, v, Map, Open_i[h_id], W1)
                else:
                    #print "expand 0:", count
                    #print "before: ",Open_i[0][1].fval
                    u = Open_i[0].popMin()
                    print u.fval
                    closed_i[0].append(u)
                    clos_set[0].add((u.r,u.c))
                    if (u.r, u.c) == (T[0].r, T[0].c):
                        print "path found! Return the anchor path"
                        return dict(expanded = closed_i, h = 0, gval = u.gval)
                        break
                    elif len(u.get_neighbor()) > 0:  # if has neighbor can be expanded
                        for (r, c) in u.get_neighbor():
                            if (r, c) not in clos_set[0]:
                                if Open_i[0].idlist.get((r, c), 0) == 0: # not in the anchor open list
                                    v = Grid([r, c])
                                    v.parent = u
                                    v.hval = get_hval(v, 0, Map)
                                    v.gval = float("inf")
                                    v.fval = W1 * v.hval + v.gval
                                else:
                                    v = Open_i[0].idlist.get((r, c))  # fetch the node from frindge and update it
                                UpdateFringe(u, v, Map, Open_i[0], W1)
                        #print "after: ", Open_i[0][1].fval
            else: # nothing inside this fringe, the minKey = Inf, also expand the anchor
                #count = count + 1
                #print "expand 0 in: ",count
                #print Open_i[0][1].fval
                u = Open_i[0].popMin()
                #print "after expand: ",Open_i[0][1].fval
                closed_i[0].append(u)
                clos_set[0].add((u.r,u.c))
                if (u.r, u.c) == (T[h_id].r, T[h_id].c):
                    print "path found! Return the anchor path" 
                    return dict(expanded = closed_i, h = 0, gval = u.gval)
                    break
                elif len(u.get_neighbor()) > 0:  # if has neighbor can be expanded
                    for (r, c) in u.get_neighbor():
                        if (r, c) not in clos_set[0]:
                            if Open_i[0].idlist.get((r, c), 0) == 0: # not in the anchor open list
                                v = Grid([r, c])
                                v.parent = u
                                v.hval = get_hval(v, 0, Map)
                                v.gval = float("inf")
                                v.fval = W1 * v.hval + v.gval
                            else:
                                v = Open_i[0].idlist.get((r, c))  # fetch the node from frindge and update it
                            UpdateFringe(u, v, Map, Open_i[0], W1)
    print "---------no paths found------- stop at search %s, %s with cost: %s" % (h_id,(u.r, u.c), u.gval)
    return dict(expanded=closed_i, h = h_id,gval=u.gval)    

def get_hval(grids, H_id, Map):
    if H_id == 0:
        h_num = 0
        ll = 0
        for (i, j) in grids.get_neighbor():
            if Map[i][j] not in ["1", "0", "2"]: 
                h_num = h_num + 1
                ll = ll + 1
        hard_ratio = min(0.25, (1.-h_num/(1.+ ll)) ) # removed the parent so add 1
        #print hard_ratio
        M_distance = abs(grids.r - T[H_id].r) + abs(grids.c - T[H_id].c)
        return hard_ratio * M_distance
    if H_id == 1:  # use actual travel distance to Goal node as hval
        travel = mth.sqrt(2) * min(abs(grids.r - T[H_id].r), abs(grids.c - T[H_id].c)) + abs(abs(grids.r - T[H_id].r)-abs(grids.c -T[H_id].c)) 
        return travel
    if H_id == 2:  # use Manhattan Distance to Goal node as hval
        return abs(grids.r - T[H_id].r) + abs(grids.c - T[H_id].c)
    if H_id == 3:  # use weighted Manhattan
        mov_cost = get_cost(grids.parent,grids,Map)
        return mov_cost * (abs(grids.r - T[H_id].r) + abs(grids.c - T[H_id].c))
    if H_id == 4:  # consider the number of blocked cell in neighbor of v
        # count the highway cell in the region
        block_ratio = 1 - len(grids.get_neighbor()) / 8
        travel_distance = mth.sqrt(2) * min(abs(grids.r - T[H_id].r), abs(grids.c -T[H_id].c)) + abs(abs(grids.r - T[H_id].r)-abs(grids.c - T[H_id].c))
        return block_ratio * travel_distance
    '''if H_id == 5:  # consider the highway block cell and blocked cell ratio as weight to minimum distance
        h_num = 0
        for (i, j) in grids.get_neighbor():
            if Map[i][j] not in ["1", "0", "2"]: 
                h_num = h_num + 1
        hard_ratio = min(0.25, (1-h_num/(1.+len(grids.get_neighbor()))) ) # removed the parent so add 1
        #print hard_ratio
        M_distance = abs(grids.r - T[H_id].r) + abs(grids.c - T[H_id].c)
        return hard_ratio * M_distance'''

def UpdateFringe(u, v, Map, fringe, W1):  # u, v are grids
    edge = get_cost(u, v, Map)  # additional g added to move to v
    if u.gval + edge < v.gval:
        v.fval = u.gval + edge + W1 * v.hval
        v.gval = u.gval + edge
        v.parent = u
        if fringe.idlist.get((v.r, v.c), 0) != 0:
            #print "update",v.r,v.c
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


def trace_path(close,s_node):  # pass the list of expanded, start node in tuple (r,c)
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
#pairs = int(raw_input("please input number for pairs of start/goal nodes: "))
#print "start generating pairs...."
pair_l = []  # list to put [start,goal] tuple list
'''
for i in range(pairs):
    p_obj = start_goal(120, 160, mapdata)
    pair_l.append(p_obj)
'''
#pair_l =[[(114,5 ),(115,155)]]

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
        #h_id = int(raw_input("Enter the heuristics ID(0-5): "))
        ww = float(raw_input("Enter the W1 for heuristics: "))
        ww2 = float(raw_input("Enter the W2 for bound: "))
    except:
        print "unacceptable input! Restart..."
        continue
    ff = mapid + str(ww)+str(ww2)+"seq" + ".csv"
    with open(ff, "w") as sw:
        for [start, goal] in pair_l:
            print "start at: %s, goal is : %s" % (str((start[0] + 1, start[1] + 1)), str((goal[0] + 1, goal[1] + 1)))

            memo = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
            print "memory peak before search: %s Kb " % memo
            t1 = time.time()
            Astar_closedi = Astar_seq(start=start, target=goal, Map=mapdata, W1=ww,W2 = ww2)
            num = Astar_closedi["h"]
            Astar_closed = Astar_closedi["expanded"][num] # the h returned final path
            t2 = time.time()
            memo2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024

            print "memory peak after search: %s Kb " % memo2
            mem = memo2 - memo

            print "used time: ", t2 - t1
            tcount = round(t2 - t1, 4)
            sw.write(str(tcount))
            sw.write(",")

            print "total path cost: ", Astar_closedi["gval"]
            cos = str(round(Astar_closedi["gval"], 3))
            sw.write(cos)
            sw.write(",")

            Anip = trace_path(Astar_closed, start)
            total_l = 0
            for i in range(5):
                print "other path length: " ,len(Astar_closedi["expanded"][i])
                total_l = total_l + len(Astar_closedi["expanded"][i])
            print "expanded %s nodes" % total_l
            

            expand_len = str(total_l)
            sw.write(expand_len)
            sw.write(",")

            print "cost of memory: ", mem
            sw.write(str(mem))
            sw.write(",")

            print " the path length is : ", len(Anip) + 1
            sw.write(str(int(len(Anip) + 1)))
            sw.write(",")
            
            print "returned path is: ", Astar_closedi["h"]
            sw.write(str(Astar_closedi["h"]))
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
                        sn_w = str(start[0]) + " " + str(start[1]) + " " +str(0)+ " " +str(Astar_closed[0].hval)
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

