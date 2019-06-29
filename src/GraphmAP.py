#计算mAP值并画图
import matplotlib.pyplot as plt
import config


def isPositive(data):
    if float(data) > 0.55:
        return True
    return False


map_num = [99,10,33,27,20,9,72,3,42,93]
no_index = 0
score_index = 12

data_list = list()
with open("totalresult_1.csv", "r", encoding="GBK") as f:
    a = f.readlines()
    for i in range(3, len(a)):
        data_list.append(a[i].strip().split(','))

f = open("mAP.txt", "w")

data_list.sort(key=lambda score: score[score_index], reverse=True)
total_num = len(data_list)
point_list = list()
for i in range(0, total_num):
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    for j in range(0, total_num):
        data = data_list[j]
        if j <= i:
            if int(data[no_index]) in map_num:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if int(data[no_index]) not in map_num:
                true_negative += 1
            else:
                false_negative += 1
    point_list.append((true_positive, false_positive,
                       true_negative, false_negative))

#true_positive, false_positive,true_negative, false_negative
xlabel_list = list()
ylabel_list = list()
for data in point_list:
    precision = 0
    if (data[0] + data[1]) > 0:
        precision = data[0] / (data[0] + data[1])
    recall = 0
    if (data[0] + data[3]) > 0:
        recall = data[0] / (data[0] + data[3])
    xlabel_list.append(recall)
    ylabel_list.append(precision)

ap_param = list()
for i in range(1, len(map_num)+1):
    ap_param.append(i / len(map_num))

max_precision_list = list()
for param in ap_param:
    max_precision = 0
    for i in range(0, len(xlabel_list)):
        if xlabel_list[i] >= param and max_precision < ylabel_list[i]:
            max_precision = ylabel_list[i]
    max_precision_list.append(max_precision)
    f.write(str(param) + ',' + str(max_precision)+'\n')

precision_sum = 0
for precision in max_precision_list:
    precision_sum += precision

print(max_precision_list)
print(precision_sum / len(max_precision_list))

f.write("mean average precision: " +
        str(precision_sum / len(max_precision_list)))
f.close()

plt.title("Precision-Recall")
plt.xlabel("recall")
plt.ylabel("precision")
plt.plot(xlabel_list, ylabel_list)
plt.show()

plt.title("Precision-Recall(mean)")
plt.xlabel("recall")
plt.ylabel("precision")
plt.plot(ap_param, max_precision_list)
plt.show()
