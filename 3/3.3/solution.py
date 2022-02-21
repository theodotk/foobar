def solution(M, F):
    '''
    We go top-down, it's just about looking for a remainder and quotient at each stage
    '''
    count = 0
    M=int(M)
    F=int(F)
    mx = max(M, F)
    mn = min(M, F)
    while (mx>=1 and mn>=1):
        rest = mx%mn
        if not rest and mn>1:
            return 'impossible'
        count += mx//mn - int(mn==1)
        mx = max(rest,mn)
        mn = min(rest,mn)

    return str(count)

MF = []
ans = []

M = '7'
F = '4'


MF.append((M, F))
ans.append('4')

MF.append((2, 1))
ans.append('1')

for i in range(len(ans)):
    print(ans[i] == solution(*MF[i]))