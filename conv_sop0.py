import sys
import random
import subprocess

from deap import base
from deap import creator
from deap import tools

D = 63        # 支給対象を決める遺伝子長．設計変数の次元数．
N_PROC = 6    # 子プロセスの展開数．
FID = "[1]"   # 目的関数のID．"[1]" or "[2]" or "[1,2]"
CITY = "naha" # 実行する都市名．"naha" or "hakodate"
SEED = "[42]" # 実行時の乱数シード. "[42]" or "[256]"

def init(city, seed):
    global CITY
    CITY = city
    global SEED
    SEED = seed

### GAの設定
# - N_IND：個体数
# - N_GEN：世代数
# - S_TOUR: トーナメントサイズ
# - P_CROSS_1：交叉確率（交叉を行うかどうか決定する確率）
# - P_CROSS_2：交叉確率（一様交叉を行うときに，その遺伝子座が交叉する確率）
# - P_MUTATION：各遺伝子座が突然変異する確率
N_IND = 20
N_GEN = 100
S_TOUR = 3
P_CROSS_1 = 0.5
P_CROSS_2 = 0.5
P_MUTATION = 0.025

# コーディングした遺伝子から，設計変数へと変換する
def gene2pay(gene):
    q = ''
    
    family_type_val = [0, 1, 2, 3, 4, 50, 60, 70, 80]
    family_type = [family_type_val[j] for i,j in zip(range(0, 9), range(9)) if gene[i] == 1]
    family_type = ",".join(map(str, family_type))
    q = q + 'family_type_id == [' + family_type + ']'

    role_household_type_val = [0, 1, 10, 11, 20, 21, 30, 31]
    role_household_type = [role_household_type_val[j] for i,j in zip(range(9, 17), range(8)) if gene[i] == 1]
    role_household_type = ",".join(map(str, role_household_type))
    q = q + ' and role_household_type_id == [' + role_household_type + ']'

    industry_type_val = [-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    industry_type = [industry_type_val[j] for i,j in zip(range(17, 38), range(21)) if gene[i] == 1]
    industry_type = ",".join(map(str, industry_type))
    q = q + ' and industry_type_id == [' + industry_type + ']'

    employment_type_val = [-1, 10, 20 ,30]
    employment_type = [employment_type_val[j] for i,j in zip(range(38, 42), range(4)) if gene[i] == 1]
    employment_type = ",".join(map(str, employment_type))
    q = q + ' and employment_type_id == [' + employment_type + ']'        

    company_size_val = [-1, 5, 10 ,100, 1000]
    company_size = [company_size_val[j] for i,j in zip(range(42, 47), range(5)) if gene[i] == 1]
    company_size = ",".join(map(str, company_size))
    q = q + ' and company_size_id == [' + company_size + ']'

    pay = 0
    for i in range(47, D):
        pay += gene[i]

    return q, str(pay)

# 子プロセスが完了することを待って，適応度を返す
def ret_fitness(p):
    a, _ = p.communicate(timeout=1_000)
    a_split = eval(a)
    if a_split[0] == None:
        return 1_000, 1_000
    else:
        return float(a_split[0]), float(a_split[2])

# popをN_PROC個を単位として，バッチに分ける．
def get_batch_list(pop):
    n_ind = len(pop)
    batch_list, ind_list = [], []
    for i in range(n_ind):
        ind_list.append(i)
        if (i + 1) % N_PROC == 0 or i == n_ind - 1:
            batch_list.append(ind_list)
            ind_list = []
    return batch_list

# 個体の評価を行う
def evaluation(pop):
    f1_list, f2_list, m_list = [], [], []
    batch_list = get_batch_list(pop)
            
    for ind_list in batch_list:
        job_list = []

        for i in ind_list:
            q, pay = gene2pay(pop[i])
            m_list = m_list + [pay]
            job_list.append(["python", "eval/syn_pop.py", q, pay, FID, CITY, SEED])
        procs = [subprocess.Popen(job, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for job in job_list]

        for i in range(len(ind_list)):
            f1, f2 = ret_fitness(procs[i])
            f1_list = f1_list + [f1]
            f2_list = f2_list + [f2]

    return f1_list, f2_list, m_list

def create_valid_pop():
    true_list = [0,9,10,17,38,40,42,43] # これは必ず1を立てる
    valid_pop = []
    for i in range(N_IND):
        tmp = []
        for j in range(D):
            if j in true_list:
                tmp.append(1)
            elif random.random() < 0.5:
                tmp.append(1)
            else:
                tmp.append(0)
        valid_pop.append(tmp)
    return valid_pop

def main():
    ### メインルーチン
    # GAはDEAPを使って実装する
    # 詳細は https://deap.readthedocs.io/en/master/index.html
    # 遺伝子：0 or 1で生成（ランダムに生成．生成/割当のしかたは改善の余地あり）
    # 交叉：一様交叉
    # 突然変異：ビット反転
    # 選択：トーナメント選択
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()

    args = sys.argv
    init(args[1], args[2])
    random.seed(args[3])
    valid_pop = create_valid_pop()

    def initPopulation(pcls, ind_init, file):    
        return pcls(ind_init(c) for c in file)

    toolbox.register("population_byhand", initPopulation, list, creator.Individual, valid_pop)
    toolbox.register("mate", tools.cxUniform)
    toolbox.register("mutate", tools.mutFlipBit, indpb=P_MUTATION)
    toolbox.register("select", tools.selTournament, tournsize=S_TOUR)
    
    # 個体集合の作成
    pop = toolbox.population_byhand()
    # 個体の評価
    f1_list, _, m_list = evaluation(pop)
    for ind, f1, m in zip(pop, f1_list, m_list):
        ind.fitness.values = f1, 
        print(0,f1,m,sum(ind),*ind,sep=',')
    
    count = N_IND
    print(count, *min([ind.fitness.values for ind in pop]), sep=",", file=sys.stderr)
    # 進化のサイクルを回す
    for g in range(1, N_GEN + 1):
        if count > 1000:
            break
        # 子の世代の選択と複製
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        # 交叉
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSS_1:
                toolbox.mate(child1, child2, P_CROSS_2)
                del child1.fitness.values
                del child2.fitness.values
        # 突然変異
        for mutant in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # 子の世代で無効な適応度（delされたもの）をもつ個体を対象として評価を行う
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        f1_list, _, m_list = evaluation(invalid_ind)
        for ind, f1, m in zip(invalid_ind, f1_list, m_list):
            ind.fitness.values = f1, 
            print(g,f1,m,sum(ind),*ind,sep=',')
        # 子の世代を次の個体集合へ置き換える
        pop[:] = offspring

        count += len(invalid_ind)
        print(count, *min([ind.fitness.values for ind in pop]), sep=",", file=sys.stderr)

if __name__ == "__main__":
    main()
