import matplotlib.pyplot as plt
import pandas as pd
plt.figure()
alpha = pd.read_csv('data/alpha.csv')
alf = alpha['tag']
alf.plot.hist(bins=6)
plt.show()

