import array

import pandas as pd

seq = [0, 0, 0, 0, 0, 0, 0, 10, 0, 0]
seq = pd.DataFrame(seq)
std = seq.std()
print(std)