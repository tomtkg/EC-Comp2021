import sys
import random
from deap import base
from deap import creator
from deap import tools
from eval import evaluator

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

def create_valid_pop():
    valid_pop = []
    for _ in range(N_IND):
        tmp = [0] * evaluator.D
        for i in range(evaluator.D):
            if random.random() < 0.5:
                tmp[i] = 1
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
    evaluator.init(args[1], args[2])
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
    f1_list, _, m_list = evaluator.evaluation(pop)
    for ind, f1, m in zip(pop, f1_list, m_list):
        ind.fitness.values = f1, 
        print(0,f1,m,sum(ind),*ind,sep=',')
    
    count = 2*N_IND
    print(count, *min([ind.fitness.values for ind in pop]), sep=",", file=sys.stderr)
    # 進化のサイクルを回す
    for g in range(1, N_GEN):
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
        f1_list, _, m_list = evaluator.evaluation(invalid_ind)
        for ind, f1, m in zip(invalid_ind, f1_list, m_list):
            ind.fitness.values = f1, 
            print(g,f1,m,sum(ind),*ind,sep=',')
        # 子の世代を次の個体集合へ置き換える
        pop[:] = offspring

        count += 2*len(invalid_ind)
        print(count, *min([ind.fitness.values for ind in pop]), sep=",", file=sys.stderr)

if __name__ == "__main__":
    main()
