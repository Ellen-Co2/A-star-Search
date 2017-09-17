import numpy as np
import random as rd

# input size of whole map and probability in float
# return the (i,j) list of hard to travel index and center of hard to travel index
def hard_to_travel(col,row,p):
    #rd.seed(seed_num)
    hard_x = rd.sample(range(col),8)
    hard_y = rd.sample(range(row),8)
    hard = set()
    for (i, j) in zip(hard_x,hard_y):
        if (i < 15):
            min_x = 0
            max_x = i + 16
        elif(i > col-16):
            min_x = i - 15
            max_x = col
        else:
            min_x = i - 15
            max_x = i + 16
        if (j < 15):
            min_y = 0
            max_y = j + 16
        elif(j > row-16):
            min_y = j - 15
            max_y = row
        else:
            min_y = j - 15
            max_y = j + 16
        for x in range(min_x,max_x):
            for y in range(min_y,max_y):
                if rd.randrange(10) < 10*p:
                    hard.add((y,x))
    return (dict(center = zip(hard_y,hard_x),hard = list(hard)))
    
    # update current direction randomely
def update_direction(direction): # update current direction with 20% turn left(right),60% keep current direction
    dir_list = ["left", "down", "right", "up"]
    # if -1 then turn right, 1 turn left, 4 keep original direction
    mov_seed = rd.sample([-1,1,4,4,4],1) 
    prev = dir_list.index(direction)
    new = prev + mov_seed[0]
    if new in range(len(dir_list)):
        return dir_list[new]
    else:
        return dir_list[(new + 4)%4]

    # extend the highway from point (nr, nc) in current direction
    # return a dictionary with path and whether hit boundary 
#extend the highway from (nr,nc) at direction "direction"( )
def extend_highway(direction, nr, nc):
    path = []
    hit = 0
    if direction == "left":
        if (nc-20 > 0):
            h_min = nc - 20
        else: 
            h_min = 0
            hit = 1 
        for j in range(h_min,nc): path.append(( nr, j)) # nr,nc already in the prev_path
        end = (nr,h_min)
    if direction == "right":
        if (nc + 20 < col):
            h_max = nc + 21
        else: 
            h_max = col
            hit = 1
        for j in range(nc+1,h_max): path.append(( nr, j))
        end = (nr,h_max-1)
    if direction == "up":
        if (nr - 20 > 0):
            v_min = nr - 20
        else: 
            v_min = 0
            hit = 1
        for i in range(v_min,nr): path.append(( i, nc))
        end = (v_min,nc)
    if direction == "down":
        if (nr + 20 < row):
            v_max = nr + 21
        else: 
            v_max = row
            hit = 1
        for i in range(nr + 1, v_max): path.append((i, nc))
        end = (v_max - 1,nc)
    return dict(path = path, hit = hit, end = end)
#generate certain number of highway at least certain length
def highway(num, length):
    p_num = 0
    # initialize the population for starting point
    samp = set()
    for j in range(col):
        for i in [0,row-1]: 
            samp.add((i,j))
    for i in range(row):
        for j in [0,col-1]: 
            samp.add((i,j))
    samp.remove((0,0))
    samp.remove((row-1,0))
    samp.remove((0,col-1))
    samp.remove((row-1,col-1))    
    #len(samp) = 552
    all_path = []
    while (p_num < num):
        start = rd.sample(samp,1) # start is a single tuple list
        l = 0
        cur_r = start[0][0]
        cur_c = start[0][1]
        p = [start[0]] # list to store the single path
        all_list = [start[0]] # list to store current path nodes
        if len(all_path)>0:
            for p_n in range(len(all_path)):
                all_list.extend(all_path[p_n]) 
        while len(p) < length:
            #choose start direction
            if cur_c == 0: 
                cur_dir = "right"
            elif cur_c == col-1:
                cur_dir = "left"
            elif cur_r == 0:
                cur_dir = "down"
            elif cur_r == row-1:
                cur_dir = "up"
            hh = extend_highway(cur_dir, cur_r, cur_c)
            #whether hit the previous highways or itself
            if (len(set(hh["path"]).intersection(set(all_list))) > 0) | (len(set(hh["path"]).intersection(set(p))) > 0):
                break
            elif hh["hit"] == 1:
                # whether its length enough
                if (len(hh["path"]) + len(p) >= length) :
                        p.extend(hh["path"])
                        #p.append(hh["end"])
                        all_path.append(p)
                        p_num = p_num + 1
                break
            else:# put the new grids in extended path to current highway
                p.extend(hh["path"])
                l = len(p)
                #update the direction and the starting point
                cur_dir = update_direction(cur_dir)
                cur_r = hh["end"][0]
                cur_c = hh["end"][1]
                continue
    return all_path
def start_goal(row,col,mapvar): # pass the generated map variable to the function
    s = (9,10)
    g = (10,0)
    while (((abs(s[0]-g[0])+abs(s[1]-g[1]))<=100)|(mapvar[s[0]][s[1]] == "0") |(mapvar[g[0]][g[1]] == "0" )):
        if rd.randrange(2)>0:
            r = rd.sample((range(20)+range(row-20,row)),1)
            c = rd.randrange(col)
            g = (r[0],c)
        else:
            r = rd.randrange(row)
            c = rd.sample((range(20)+range(col-20,col)),1)
            s = (r,c[0])
    return [s,g]

# add a variable for the file name as :ask (such as map1 map2)then put in a for loop..
def map_parser(nnr=120, nnc=160): # call this function would generate a txt file with input name
    global row
    global col
    row = nnr
    col = nnc
    semi_blk = hard_to_travel(col,row,0.5)
    print len(semi_blk["hard"])
    hlist = highway(4,100)
    MapInit = np.ones((row,col)).astype(np.int32).astype(np.string_)
    for (i , j) in semi_blk["hard"]:
        #print i,j
        MapInit[i][j] = "2"
#mark ai as highway with unblocked cell
#mark bi as highway with semi_blocked cell
    for i in range(1,5):
        for (r , c) in hlist[i-1]:
            if MapInit[r][c] == "1": 
                MapInit[r][c] = "a"+str(i)
            if MapInit[r][c] == "2": 
                MapInit[r][c] = "b"+str(i)
#mark blocked cell as 0
    hway_cell = []
    for p_n in range(len(hlist)):
            hway_cell.extend(hlist[p_n])
    for r in range(row):
        for c in range(col):
            if (rd.randrange(10) < 2)&((r,c) not in hway_cell):
                MapInit[r][c] = "0"
#choose start and goal block
    pdict = start_goal(row,col,MapInit)
    S = pdict[0]
    T = pdict[1]
    ask = raw_input("please input the file name to save as map:  ")
    mw = str(ask)+".txt"
    with open(mw,"w") as f:
        # following commented is to write one start/ end id to file
        '''a = str(S[0])+" "+str(S[1])
        b = str(T[0])+" "+str(T[1])
        f.write(a)
        f.write("\n")
        f.write(b)
        f.write("\n")'''
        # print the center of hard to travel region
        for i ,j in semi_blk["center"]:
            ind = str(i)+" "+str(j)
            f.write(ind)
            f.write("\n")    
        '''size_str = str(row)+","+str(col)
        f.write(size_str)
        f.write("\n")'''
        np.savetxt(f,MapInit,fmt= '%s',delimiter=',')
    f.close()
    return dict(h_center = semi_blk["center"],map_all = MapInit)
map_parser()
            


        	

