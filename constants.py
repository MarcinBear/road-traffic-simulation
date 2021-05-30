from itertools import product


# --------------------------------- default table parameters
ids = list(range(1, 14))
taus = [5 for _ in range(13)]
sigmas = [3 for _ in range(13)]
P_ups = 2 * [0.33] + 8 * [0.25] + 3 * [0.33]
P_downs = 2 * [0.33] + 8 * [0.25] + 3 * [0.0]
P_lefts = 2 * [0.33] + 8 * [0.25] + 3 * [0.33]
P_rights = 2 * [0.0] + 8 * [0.25] + 3 * [0.33]

# ------------------------------------ map positions including road name

D_S2 = list(product(range(11), [18, 20]))
D_S2.remove((10, 20))

S2_S3 = list(product(range(12, 27), [18, 20]))
S2_S3.remove((12, 18))
S2_S3.remove((26, 20))

S3_S4 = list(product(range(28, 36), [18, 20]))
S3_S4.remove((28, 18))
S3_S4.remove((35, 20))

C_S4 = list(product(range(37, 43), [18, 20]))

A_S1 = list(product([10, 12], range(0, 7)))

S1_S2 = list(product([10, 12], range(7, 19)))
S1_S2.remove((10, 18))

S1_ = list(product(range(0, 10), [7]))

E_S2 = list(product([10, 12], range(20, 30)))
E_S2.remove((12, 20))

B_S3 = list(product([26, 28], range(0, 19)))
B_S3.remove((26, 18))

F_S3 = list(product([26, 28], range(20, 30)))
F_S3.remove((28, 20))

G_S4 = list(product([35, 37], range(20, 30)))
G_S4.remove((37, 20))

named_roads = {'D_S2': D_S2, 'S2_S3': S2_S3, 'S3_S4': S3_S4, 'C_S4': C_S4, 'A_S1': A_S1,
               'S1_S2': S1_S2, '_S1': S1_, 'E_S2': E_S2, 'B_S3': B_S3, 'F_S3': F_S3, 'G_S4': G_S4}