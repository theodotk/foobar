import numpy as np
import time

def solution(g):
    '''
    The idea is explore the current nebula cell by cell.
    Each of them has a set of corresponding 2x2 cell configuraions.
    They can be combined only in certain ways, so for each subsequent cell we check if it fits with previous ones.
    
    To avoid keeping in memory all the explored combinations, we keep track only of the border between the explored and unexplored parts.
    We also go first along the shorter side, to keep shorter border -> less indices -> less memory usage.
            
    Then the total number of combitations is the number associated with each type of final border
    '''
    
    def compare_and_compose_border(cell, old_border, x, y, h):
        '''
        Returns:
            new_border: str: border that will be formed if the current cell fits.
        -------------------------
        There are 3 possible comparison situations:

        1-3. In the following cases one cell (c) is deleted from border, as it won't partake in the comparisons.
        1. The first row: we compare cells by 2 (C,c), vertically, and add 2 new cells (A) to the border (B).
            ..cA.
            BBCA.
        1a. In the last column we need to add only 1 cell, as the upper right won't partake in the comparisons
            ..c.
            BBCA

        2. The first column is similar: we compare cells by 2 (C,c), horizontally, and add 2 new cells (A) to the border (B).
            cCBB
            AA..

        3. All the rest: we compare three cells (C,c), add one (A) and delete one (c)
            ..cCBB
            BBCA..
        3a. For the last colums we compare three (C,c), add one (A), but two are deleted (c) 
            ..cc
            BBCA
        '''
        new_border = ''
        if x == 0: # 1
            if [int(old_border[-2]),int(old_border[-1])] == cell[0]: 
                if y < h-1:
                    new_border = old_border[:-1] + ''.join([str(i) for i in cell[1]])
                else:
                    new_border = old_border[:-1] + str(cell[1][0])
        
        elif y == 0: # 2
            if [int(old_border[0]),int(old_border[1])] == cell[0]:
                new_border = old_border[1:] + ''.join([str(i) for i in cell[1]])
        
        else: # 3
            if [int(old_border[-1]),int(old_border[0]),int(old_border[1])] == cell[0]+[cell[1][1]]:
                if y < h-1:
                    new_border = old_border[1:] + str(cell[1][0])
                else:
                    new_border = old_border[2:] + str(cell[1][0])
                
        return new_border
    
    # all the possible 2x2 configuraions:
    zero_cells = [np.reshape([int(n) for n in bin(i)[2:].zfill(4)],[2,2]).tolist() for i in range(16)]
    # 2x2 configurations that lead to 1:
    one_cells = [cell for cell in zero_cells if np.sum(cell)==1]
    # 2x2 configurations that lead to 0:
    zero_cells = [i for i in zero_cells if not i in one_cells]
    
    g = np.array(g).astype(int)
    h,w = g.shape

    border = {}
    for x in range(w):
        for y in range(h):

            new_borders = {}

            if g[y][x]:
                current_cells = one_cells
            else:
                current_cells = zero_cells
            
            for cell in current_cells:
                if x+y==0: # the first cell
                    new_border = ''.join(str(i) for i in [cell[0][0]]+cell[1])
                    if new_border in new_borders.keys():
                        new_borders[new_border] += 1
                    else:
                        new_borders[new_border] = 1

                # does a cell fit with any of the borders? If so, compose a new border and save num cases
                for old_border in border.keys():
                    new_border = compare_and_compose_border(cell, old_border, x, y, h)
                    if len(new_border):
                        if new_border in new_borders.keys():
                            new_borders[new_border] += border[old_border]
                        else:
                            new_borders[new_border] = border[old_border]

            border = new_borders

    return np.sum([v for v in border.values()])


example = {}
answer = {}
example[0] =[[True, True, False, True, False, True, False, True, True, False],
           [True, True, False, False, False, False, True, True, True, False],
           [True, True, False, False, False, False, False, False, False, True],
           [False, True, False, False, False, False, True, True, False, False]]
answer[0] =11567

example[1] = [[True, False, True, False, False, True, True, True],
           [True, False, True, False, False, False, True, False],
           [True, True, True, False, False, False, True, False],
           [True, False, True, False, False, False, True, False],
           [True, False, True, False, False, True, True, True]]
answer[1] = 254

example[2] = [[True, False, True],
           [False, True, False],
           [True, False, True]]
answer[2] = 4


repeats = 1
for i in range(3):
    start_time = time.time()
    for _ in range(repeats):
        s = solution(example[i])
    print(s == answer[i], (time.time() - start_time)/repeats)