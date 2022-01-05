import math
import subprocess

N_PROC = 6    # 子プロセスの展開数．
FID = "[1]"   # 目的関数のID．"[1]" or "[2]" or "[1,2]"
CITY = "naha" # 実行する都市名．"naha" or "hakodate"

# コーディングした遺伝子から，設計変数へと変換する
def gene2pay(gene):
    q = ''
    
    family_type_val = [1, 2, 3, 4, 50, 60, 70, 80]
    family_type = [family_type_val[j] for i,j in zip(range(0, 8), range(8)) if gene[i] == 1]
    family_type = ",".join(map(str, family_type))
    q = q + 'family_type_id == [0,' + family_type + ']'

    role_household_type_val = [10, 11, 20, 21, 30, 31]
    role_household_type = [role_household_type_val[j] for i,j in zip(range(8, 14), range(6)) if gene[i] == 1]
    role_household_type = ",".join(map(str, role_household_type))
    q = q + ' and role_household_type_id == [0,1,' + role_household_type + ']'

    industry_type_val = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    industry_type = [industry_type_val[j] for i,j in zip(range(14, 34), range(20)) if gene[i] == 1]
    industry_type = ",".join(map(str, industry_type))
    q = q + ' and industry_type_id == [-1,' + industry_type + ']'

    employment_type_val = [10, 30]
    employment_type = [employment_type_val[j] for i,j in zip(range(34, 36), range(2)) if gene[i] == 1]
    employment_type = ",".join(map(str, employment_type))
    q = q + ' and employment_type_id == [-1,20,' + employment_type + ']'        

    company_size_val = [10 ,100, 1000]
    company_size = [company_size_val[j] for i,j in zip(range(36, 39), range(3)) if gene[i] == 1]
    company_size = ",".join(map(str, company_size))
    q = q + ' and company_size_id == [-1,5,' + company_size + ']'

    return q

# 子プロセスが完了することを待って，最適な値mを返す
def get_optm(p):
    a, _ = p.communicate(timeout=1_000)
    if CITY == "naha":
        x = 5613300000 / (5613300000 - min(eval(a)[-1]))
    else:
        x = 4752780000 / (4752780000 - min(eval(a)[-1]))
    return math.floor(x * 100) / 100

# 子プロセスが完了することを待って，適応度を返す
def ret_fitness(p):
    a, _ = p.communicate(timeout=1_000)
    a_split = eval(a)
    if a_split[0] == None:
        return 1_000, 1_000
    else:
        return float(a_split[0]), float(a_split[2])

# 個体の評価を行う
def evaluation(pop):
    f1_list, f2_list, m_list = [], [], []
    n_ind = len(pop)
    batch_list, ind_list = [], []
    for i in range(n_ind):
        ind_list.append(i)
        if (i + 1) % N_PROC == 0 or i == n_ind - 1:
            batch_list.append(ind_list)
            ind_list = []
            
    for ind_list in batch_list:
        job_list, procs = [], []
        for i in ind_list:
            q = gene2pay(pop[i])
            cmd = ["python", "eval/syn_pop.py", str(q), "1", FID, CITY, "[42]"]
            job_list.append(cmd)
        procs = [subprocess.Popen(job, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for job in job_list]

        for i in range(len(ind_list)):
            optm = get_optm(procs[i])
            m_list = m_list + [optm]
            job_list[i][3] = str(optm)
        procs = [subprocess.Popen(job, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for job in job_list]

        for i in range(len(ind_list)):
            avg_1, avg_2 = ret_fitness(procs[i])
            f1_list = f1_list + [avg_1]
            f2_list = f2_list + [avg_2]

    return f1_list, f2_list, m_list
