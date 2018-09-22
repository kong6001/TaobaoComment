class SpearmanStruct:
    origin_index = 0
    factor_a = 0
    d_a = 0
    factor_b = 0
    d_b = 0
    delta_d = 0

    def __init__(self, a, b):
        self.factor_a = a
        self.factor_b = b

    def getFactor_a(self):
        return self.factor_a

    def getFactor_b(self):
        return self.factor_b


def SpearmanRankCorrelation(spearman_struct_list):
    # spearman_struct_list is a list
    n = len(spearman_struct_list)
    for i in range(0, n):
        spearman_struct_list[i].origin_index = i

    templist = list(spearman_struct_list)

    templist.sort(key=SpearmanStruct.getFactor_a, reverse=True)
    for i in range(0, n):
        index = templist[i].origin_index
        spearman_struct_list[index].d_a = i+1

    templist.sort(key=SpearmanStruct.getFactor_b, reverse=True)
    for i in range(0, n):
        index = templist[i].origin_index
        spearman_struct_list[index].d_b = i+1

    for item in spearman_struct_list:
        item.delta_d = item.d_a - item.d_b

    sum_delta_d_power = 0
    for item in spearman_struct_list:
        sum_delta_d_power += pow(item.delta_d, 2)

    p_rho = 1 - (6 * sum_delta_d_power) / n / (pow(n, 2) - 1)

    return p_rho


def testcase():
    spearman1 = SpearmanStruct(11, 2)
    spearman2 = SpearmanStruct(490, 75)
    spearman3 = SpearmanStruct(14, 3)
    spearman4 = SpearmanStruct(43, 44)
    spearman5 = SpearmanStruct(30, 7)
    spearman6 = SpearmanStruct(3, 42)
    spearman_struct_list = []
    spearman_struct_list.append(spearman1)
    spearman_struct_list.append(spearman2)
    spearman_struct_list.append(spearman3)
    spearman_struct_list.append(spearman4)
    spearman_struct_list.append(spearman5)
    spearman_struct_list.append(spearman6)

    print(SpearmanRankCorrelation(spearman_struct_list))


testcase()
