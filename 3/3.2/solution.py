import numpy as np

def solution(l):
    '''
    We are looking for the number of paths of length 2 in a DAG, where:
        - the vertices are elemets of the list.
        - the edge exists if the next element divides the previous one, and we can't go backwards wrt the index of the list.
    We need to find a transition matrix A where a_ij is 1 if the transition is possible and 0 if it is not.
    
    Then, A.sum(axis = 0) is a vector that shows the number of ways each element can be reached after the first step (i.e. how many divisors it has between the previous elements of the list l).
    And A.sum(axis = 0).dot(A) is the same after the second step.
    If we would look for "lucky quadruples", there would be one more matrix multiplication and so on.
    (me from the future: "hehe what a pathetic excuse for a two-liner attmept")
    
    And the answer is the sum of the final matrix multiplication.
    '''
    # transition matrix:
    A = np.array([[(l[i]%l[k]==0)&(k<i) for i in range(len(l))] for k in range(len(l))])
    # A.sum(axis = 0) - number of the ways to get to each state 
    return (A.sum(axis = 0).dot(A)).sum()

j = []
ans = []

j.append([1,1,1])
ans.append(1)
j.append([1, 2, 3, 4, 5, 6])
ans.append(3)
j.append([1, 2, 3, 4, 8, 6])
ans.append(6)
j.append([1, 2, 4, 8])
ans.append(4)
j.append([1, 2, 4, 8, 1])
ans.append(4)

for i in range(len(ans)):
    print(ans[i] == solution(j[i]))