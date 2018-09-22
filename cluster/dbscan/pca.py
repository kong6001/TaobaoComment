from sklearn.decomposition import PCA
import numpy as np

f = open('output.vec', 'r', encoding='UTF-8')
raw_data = f.read()
f.close()
lines = raw_data.split(' \n')

high_dim_list = list()
dim = len(lines[0].split(' ')[1:])
for line in lines:
    line = line.split(' ')
    data = line[1:]

    if len(data) < dim:
        print('error data:' + str(data))
        continue

    high_dim_list.append(data)

X = np.array(high_dim_list)
pca = PCA(n_components=2)
Y = pca.fit_transform(X)
Y = list(Y)

f = open('pca_output.vec', 'w', encoding='UTF-8')
for i in range(0, len(Y)):
    f.write(lines[i].split(' ')[0])
    for data in Y[i]:
        f.write(' '+str(data))
    f.write("\n")
