import math
import numpy as np

from _func import *

root = str(Path(__file__).parent) + "\\"

time_limit = 40
T, C = [6, 6, 8, 9], [1, 1, 2, 3]

# apt: Aperiodic Task
apt_time, apt_jobs, apt_dls = [3, 22], [2, 3], [8, 5]
apt_number = 2  # The 3rd task

# Start Coding!
data = poll_server_rm(T, C, apt_time, apt_jobs, apt_dls, apt_number, time_limit=40)
print(data)

# visualizing
plt.rcParams["figure.figsize"] = (20, 10)
fig = plt.figure()
m = len(data)
t = [i for i in range(time_limit)]
fig.suptitle('Polling Server Scheduling ')
for j in range(m - 1):
    errors = [x * y for x, y in zip(data[j], data[-1])]
    plt.subplot(100 * (m) + 10 + j + 1)
    if j == m-3:
        arival = [0 for k in t]
        deadLines = [0 for k in t]
        for i in range(len(apt_dls)):
            arival[apt_time[i]] = 1
            deadLines[apt_time[i]+apt_dls[i]] = -1
    else:
        arival = [k % T[j] == 0 for k in t]
        deadLines = [-1 * (k % T[j] == T[j] % T[j]) for k in t]
    plt.ylabel('Task ' + str(j + 1) + ' , C=' + str(C[j]))
    plt.bar(t, data[j], align='edge', width=1, bottom=-0.5)
    plt.bar(t, errors, align='edge', width=1, bottom=-0.5, color='yellow')
    plt.bar(t, arival, width=0.2, color='green', label='Arrivals')
    plt.bar(t, deadLines, width=0.2, color='red', label='Deadlines')
    plt.grid(True, which='major')
    plt.xticks(t)
    plt.yticks([])
plt.xlabel('Real-Time Clock')
fig.legend()
plt.savefig(root + 'imgs\\poll_server')
plt.show()