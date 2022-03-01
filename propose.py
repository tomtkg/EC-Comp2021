import sys
from eval import evaluator

def create_pop(ind,v):
    pop = []
    for i in range(evaluator.D):
        if ind[i] == v:
            continue
        tmp = [x for x in ind]
        tmp[i] = v
        pop.append(tmp)
    return pop

# 目的関数値のみを考慮した解選択
def get_indexA(f1_list,m_list,best,pay):
    index = -1
    for i, f1 in enumerate(f1_list):
        if best > f1:
            index = i
            best = f1
    return index

# 目的関数値と支給金額を考慮した解選択
def get_indexB(f1_list,m_list,best,pay):
    index, value = -1, 0 
    for i, (f1, m) in enumerate(zip(f1_list, m_list)):
        if pay == m:
            v = (best - f1) / 0.001
        else:
            v = (best - f1) / abs(pay - m)
        if value < v:
            index = i
            value = v
    return index

def main():
    args = sys.argv
    evaluator.init(args[1], args[2])
    if args[3] == "A":
        get_index = get_indexA
    else:
        get_index = get_indexB
    b = int(args[4])

    change_count, fe = 0, 2
    ind = [b] * evaluator.D
    b = abs(b-1)
    f1_list, _, m_list = evaluator.evaluation([ind])
    best = f1_list[0]
    pay = m_list[0]
    print(-1, best, pay, *ind, sep=",")
    print(fe, best, pay, -1, -1, sep=",", file=sys.stderr)

    for num in range(40):
        if change_count == 2:
            break
        pop = create_pop(ind,b)
        f1_list, _, m_list = evaluator.evaluation(pop)
        for p, f1, m in zip(pop, f1_list, m_list):
            print(num, f1, m, *p, sep=",")
        fe += 2*len(pop)
        
        index = get_index(f1_list,m_list,best,pay)

        if index == -1:
            print(fe, best, -1, -1, -1, sep=",", file=sys.stderr)
            b = abs(b-1)
            change_count += 1
            continue
        
        for i in range(evaluator.D):
            if ind[i] != pop[index][i]:
                break
        print(fe, f1_list[index], m_list[index], i, index, sep=",", file=sys.stderr)
        change_count = 0
        ind = [x for x in pop[index]]
        best = f1_list[index]

if __name__ == "__main__":
    main()
