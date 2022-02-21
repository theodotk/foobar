import numpy as np

def bfs(start, finish, maze_map):
    '''
    bredth-first search, iterative
    '''
    w, h = np.shape(maze_map)
    possible_steps = [start]
    seen = [start]
    counter = 0
    while len(possible_steps):
        new_possible_steps = []
        counter+=1
        for this_step in possible_steps:
            x, y = this_step
            if this_step == finish:
                return counter
            for x2, y2 in ([x+1,y], [x-1,y], [x,y+1], [x,y-1]):
                if 0<=x2<w and 0<=y2<h and maze_map[x2][y2] != 1 and [x2, y2] not in seen:
                    new_possible_steps.append([x2, y2])
                    seen.append([x2, y2])
        possible_steps = new_possible_steps

def solution(maze_map):
    '''
    The shortest path with a wall removed is a shortest path to the wall plus the shortest path from the wall.
    Shortest path = bfs algorithm.
    We check every wall segment and the start position (it has no walls)
    '''
    w, h = np.shape(maze_map)
    min_dist = w + h - 1
    current_dist = h*w
    # map with wall at (i,j) removed
    ij_map = np.empty_like(maze_map)
    for i in range(w):
        for j in range(h):
            # check only start (no walls to rm) and walls
            if not i+j or maze_map[i][j]:
                ij_map[:] = list(maze_map)
                ij_map[i][j]=0
                # to the rm-ed wall
                i2f = bfs([0,0],[i,j], ij_map)
                # from the rm-ed wall
                f2i = bfs([i,j],[w-1,h-1], ij_map)
                try:
                    this_dist = i2f+f2i-1
                    if this_dist == min_dist:
                        return min_dist
                    current_dist = min(current_dist, this_dist)
                except TypeError:
                    continue
    return current_dist


j= [[[0, 1, 1, 0],
 [0, 0, 0, 1],
 [1, 1, 0, 0],
 [1, 1, 1, 0]]]


j.append([[0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 1, 1, 1, 1, 1],
     [0, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0]])

j.append([ [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 1, 1, 0],
      [1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 0, 0, 0, 1, 1, 0],
      [0, 1, 1, 1, 1, 1, 1, 1, 0],
      [0, 1, 1, 1, 1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0] ])

j.append([ [0],
      [1],
      [0] ])

j.append([ [0, 0, 0, 0],
      [1, 1, 1, 0],
      [1, 0, 1, 0],
      [1, 1, 1, 0],
      [1, 0, 0, 0],
      [1, 0, 1, 1],
      [1, 0, 0, 0] ])

ans = [7, 11, 72, 3, 10]

for i in range(len(ans)):
    print(ans[i] == solution(j[i]))