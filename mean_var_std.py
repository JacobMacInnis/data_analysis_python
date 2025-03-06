import numpy as np

# def calculate(list):
#     if not len(list) == 9:
#         raise ValueError("List must contain nine numbers.")
#     n = np.array(list)
#     reshaped = n.reshape((3,3))
#     # print(np.mean(reshaped, axis=0))


#     calculations = {
#         'mean': [np.mean(reshaped, axis=0).tolist(), np.mean(reshaped, axis=1).tolist(), n.mean()],
#         'variance': [np.var(reshaped, axis=0).tolist(), np.var(reshaped, axis=1).tolist(), n.var()],
#         'standard deviation': [np.std(reshaped, axis=0).tolist(), np.std(reshaped, axis=1).tolist(), n.std()],
#         'max': [np.max(reshaped, axis=0).tolist(), np.max(reshaped, axis=1).tolist(), n.max()],
#         'min': [np.min(reshaped, axis=0).tolist(), np.min(reshaped, axis=1).tolist(), n.min()],
#         'sum': [np.sum(reshaped, axis=0).tolist(), np.sum(reshaped, axis=1).tolist(), n.sum()],
#     }
#     # print(calculations['min'])
#     return calculations

#  Improved version

import numpy as np

def calculate(lst):
    if len(lst) != 9:
        raise ValueError("List must contain nine numbers.")

    n = np.array(lst).reshape(3, 3)
    operations = {
        'mean': np.mean,
        'variance': np.var,
        'standard deviation': np.std,
        'max': np.max,
        'min': np.min,
        'sum': np.sum,
    }

    return {key: [func(n, axis=0).tolist(), func(n, axis=1).tolist(), func(n).tolist()] for key, func in operations.items()}
