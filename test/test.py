import numpy as np

E_L = np.array([
    [[0., 0.],         [0., 0.],                  [0., 0.]],
    [[0., 0.12150325], [0.40357533, 38.97276172], [0.4483013, 6.34968223]],
    [[0.0, 0.0],     [2.74539679, 4.38547227],  [0.0, 0.0]]
])

for e_l in E_L:
    pass
#    print("First element of row = {}".format(e_l[0]))
#    print("Second element of row = {}".format(e_l[1]))
#    print("Third element of row = {}".format(e_l[2]))

r_11 = [[0.0, 0.1, 0.3]]
r_12 = [[0.5, 0.3, 0.1]]

T = np.array([
    [0.123, 0.231, 0.321],
    [0.231, 0.123, 0.321],
    [0.321, 0.231, 0.123]
])

N = 3
A = np.eye(N)

# Add a column.
B = np.c_[A, np.ones(N)]
#print(B)

# Adding a row.
C = np.r_[B, [np.ones(4)]]
#print(C)

# Adding a column.
D = np.c_[C, np.ones(4)]
#print(D)

# Lets do one more.
E = np.r_[D, [np.ones(5)]]
#print(E)

#print(np.ones(2))

F = [[]]
for j in range(2):
    F = np.c_[F, [[1., 2.]]]
#print(F)


f_i_E_k = np.zeros(shape=(2, 2))
print(f_i_E_k)
for i in range(2):
    for j in range(2):
        index = str(i) + '_' + str(j)
        print("Index = {}".format(index))
        line_index = 0
        lines = [line.rstrip('\n') for line in open('test/EL_%s.csv' % index, 'r')]
        for l in lines:
            index = str(i) + '_' + str(line_index)
            f = open('test/fE%s.csv' % index, 'a')
            f.write(str(float(l)) + '\n')
            f_i_E_k[i][line_index] = [float(l)]
            #print("Line Index = {}".format(line_index))
            #line_index += 1
print(f_i_E_k)
