INF = 2**32
def relabel_to_front(C, source, sink):
    '''
    Source: https://en.wikipedia.org/wiki/Push%E2%80%93relabel_maximum_flow_algorithm
    '''
    n = len(C)  # C is the capacity matrix
    F = [[0] * n for _ in range(n)]
    # residual capacity from u to v is C[u][v] - F[u][v]

    height = [0] * n  # height of node
    excess = [0] * n  # flow into node minus flow from node
    seen   = [0] * n  # neighbours seen since last relabel
    # node "queue"
    nodelist = [i for i in range(n) if i != source and i != sink]

    def push(u, v):
        send = min(excess[u], C[u][v] - F[u][v])
        F[u][v] += send
        F[v][u] -= send
        excess[u] -= send
        excess[v] += send

    def relabel(u):
        # Find smallest new height making a push possible,
        # if such a push is possible at all.
        min_height = INF
        for v in range(n):
            if C[u][v] - F[u][v] > 0:
                min_height = min(min_height, height[v])
                height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            if seen[u] < n:  # check next neighbour
                v = seen[u]
                if C[u][v] - F[u][v] > 0 and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:  # we have checked all neighbours. must relabel
                relabel(u)
                seen[u] = 0

    height[source] = n  # longest path from source to sink is less than n long
    excess[source] = INF  # send as much flow as possible to neighbours of source
    for v in range(n):
        push(source, v)

    p = 0
    while p < len(nodelist):
        u = nodelist[p]
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            nodelist.insert(0, nodelist.pop(p))  # move to front of list
            p = 0  # start from front of list
        else:
            p += 1
    return sum(F[source])

def solution(s, t, net):
    '''
    Implements push-relabel max flow from Wikipedia article:
    here the rooms are vertices, corridors are edges.
    For the multiple sources/tanks case, we create a super-source/tank node.
    '''

    ls = len(s)
    lt = len(t)
    l  = len(net)
    if ls==1 and lt==1:
        return relabel_to_front(net,s[0],t[0])
    else:
        new_net = []
        for i, line in enumerate(net):
            if i in t:
                 line += [INF, 0]
            else:
                line += [0, 0]
            new_net.append(line)
        new_net.append([0] * (l+2))
        new_net.append([0 if not i in s else INF/ls for i in range(l+2)])
        return relabel_to_front(new_net, l+1, l)

s,t,net = {},{},{}
ans = {}

s[0] = [0, 1]
t[0] = [4, 5]
net[0] = [[0, 0, 4, 6, 0, 0],
       [0, 0, 5, 2, 0, 0],
       [0, 0, 0, 0, 4, 4],
       [0, 0, 0, 0, 6, 6],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0]]
ans[0] = 16

s[1],t[1],net[1] = [0], [3], [[0, 7, 0, 0],
                     [0, 0, 6, 0],
                     [0, 0, 0, 8],
                     [9, 0, 0, 0]]
ans[1] = 6

for i in range(2):
    print(ans[i] == solution(s[i], t[i], net[i]))