import numpy as np

def is_cycle(a, b):
    # sum is not a power of 2 multiplied by an addend
    s = a+b
    mn = min(a,b)
    s_div = 1.0*s/mn
    if s_div == int(s_div):
        s = int(s_div)
    # power of two and the previous number has all different bits, thus:
    return ((s&(s-1)) != 0)

def solution(banana_list):
    '''
    Instead of trying all the possible sequences
    let's have a simple heuristic.
    We try to pair up the guards in a way
    that allows to maximize the numbers of pairings of the rest.
    '''
    l = len(banana_list)
    
    # check who can pair up with whom. -1 means no pair
    pairings_tf = np.array([[is_cycle(a,b) for a in banana_list] for b in banana_list])
    pairings = [set(line) for line in pairings_tf*range(1, l+1)-1]
    n_pairs = pairings_tf.sum(axis = 0)
    
    # keep track of who is already paired up
    unused_idx = [i for i in range(l) if n_pairs[i]]
    
    # let's start with the option with the lowest number of pairs
    sorted_idx = np.argsort(n_pairs)
    n_unpaired = sum(n_pairs == 0)
    
    for current_idx in sorted_idx:
        if current_idx not in unused_idx:
            continue
        else:            
            unused_idx.remove(current_idx)
        
        current_pair = -1
        
        mat_reduced = pairings_tf[unused_idx][:,unused_idx]
        # number of guards in all possible pairings, if we exclude the current guard and each other one
        n_paris_without_these_two = [np.delete(np.delete(mat_reduced,j,0),j,1).sum() for j in range(len(unused_idx))]

        for j in np.argsort(n_paris_without_these_two)[::-1]:
            candidate = unused_idx[j]
            if candidate in pairings[current_idx] and candidate != -1:
                current_pair = candidate
                unused_idx.remove(current_pair)
                break
            
        if current_pair == -1: # the pair wasn't found...
            n_unpaired+=1
            continue
        
    return n_unpaired


banana_list, ans = [],[]

banana_list.append([1,1])
ans.append(2)
banana_list.append([1, 7, 3, 21, 13, 19])
ans.append(0)

for i in range(len(ans)):
    print(ans[i] == solution(banana_list[i]))