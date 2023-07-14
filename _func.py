# Public libraries:
import math
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


def file_reader(path):
    char_map = {'[': '', ' ': '', ']': '', '\n': ''}
    with open(Path(path), "r") as file:
        out = []
        for line in file:
            l = list(filter(None, line.translate(str.maketrans(char_map)).split(';')))
            out.append([list(map(int, list(filter(None, e.split(','))))) for e in l])
    return out


def file_writer(results, path):
    with open(Path(path), "w") as file:
        for result in results:
            line = ""
            for task in result:
                e_str = ""
                for e in task: e_str += str(e) + ","
                line += f"[{e_str}];"
            file.write(line + "\n")


def save_figs(examples, results, title, path, time_limit=40):
    n = len(examples)
    for i in range(n):
        plt.rcParams["figure.figsize"] = (20, 3 * n)
        fig = plt.figure('example ' + str(i + 1))
        m = len(results[i])
        T, C = examples[i][0], examples[i][1]
        if title == 'RM' or title == 'AP':
            D = T
        else:
            D = examples[i][2]
        t = [i for i in range(time_limit)]
        fig.suptitle(title + ' Scheduling for example ' + str(i + 1))
        for j in range(m - 1):
            errors = [x * y for x, y in zip(results[i][j], results[i][-1])]
            plt.subplot(100 * (m) + 10 + j + 1)
            if j == m - 2 and title == 'AP':
                plt.ylabel('Aperiodic Task')
                arival = [0 for k in t]
                deadLines = [0 for k in t]
            else:
                arival = [k % T[j] == 0 for k in t]
                deadLines = [-1 * (k % T[j] == D[j] % T[j]) for k in t]
                plt.ylabel('Task ' + str(j + 1) + ' , C=' + str(C[j]))
            plt.bar(t, results[i][j], align='edge', width=1, bottom=-0.5)
            plt.bar(t, errors, align='edge', width=1, bottom=-0.5, color='yellow')
            plt.bar(t, arival, width=0.2, color='green', label='Arrivals')
            plt.bar(t, deadLines, width=0.2, color='red', label='Deadlines')
            plt.grid(True, which='major')
            plt.xticks(t)
            plt.yticks([])
        plt.xlabel('Real-Time Clock')
        fig.legend()
        plt.savefig(path + title + '_example_' + str(i + 1))
        plt.show()


def rm_scheduler(examples, time_limit=40):
    results = []
    for exp in examples:
        T, C = exp[0], exp[1]
        n = len(T)
        current_time = 0
        queue = []
        result = [[0 for i in range(time_limit)] for i in range(n)]
        missed = [0 for i in range(time_limit)]
        while current_time < time_limit:
            for i in range(len(T)):
                if current_time % T[i] == 0:
                    queue.append([current_time, T[i], C[i], T[i], i])
            queue.sort(key=lambda x: x[1])
            if len(queue) != 0:
                hp_task = queue[0]
                if current_time >= hp_task[3] + hp_task[0]:
                    missed[current_time] = 1
                hp_task[2] -= 1
                if hp_task[2] == 0:
                    queue.remove(hp_task)
                result[hp_task[4]][current_time] = 1
            current_time += 1
        result.append(missed)
        results.append(result)
    return results


def dm_scheduler(examples, time_limit=40):
    results = []
    for exp in examples:
        T, C, D = exp[0], exp[1], exp[2]
        n = len(T)
        current_time = 0
        queue = []
        result = [[0 for i in range(time_limit)] for i in range(n)]
        missed = [0 for i in range(time_limit)]
        while current_time < time_limit:
            for i in range(len(T)):
                if current_time % T[i] == 0:
                    queue.append([current_time, T[i], C[i], D[i], i])
            queue.sort(key=lambda x: x[3])
            if len(queue) != 0:
                hp_task = queue[0]
                if current_time >= hp_task[3] + hp_task[0]:
                    missed[current_time] = 1
                hp_task[2] -= 1
                if hp_task[2] == 0:
                    queue.remove(hp_task)
                result[hp_task[4]][current_time] = 1
            current_time += 1
        result.append(missed)
        results.append(result)
    return results


def ed_scheduler(examples, time_limit=40):
    results = []
    for exp in examples:
        T, C, D = exp[0], exp[1], exp[2]
        n = len(T)
        current_time = 0
        queue = []
        result = [[0 for i in range(time_limit)] for i in range(n)]
        missed = [0 for i in range(time_limit)]
        while current_time < time_limit:
            for i in range(len(T)):
                if current_time % T[i] == 0:
                    queue.append([current_time, T[i], C[i], current_time + D[i], i])
            queue.sort(key=lambda x: x[3])
            if len(queue) != 0:
                hp_task = queue[0]
                if current_time >= hp_task[3]:
                    missed[current_time] = 1
                hp_task[2] -= 1
                if hp_task[2] == 0:
                    queue.remove(hp_task)
                result[hp_task[4]][current_time] = 1
            current_time += 1
        result.append(missed)
        results.append(result)
    return results


def ap_rm_scheduler(examples, ap_task_time, ap_task_jobs, time_limit=40):
    # This is an Interrupt-Driven Aperiodic RM task scheduler
    # In this scheduler, Aperiodic task should be processed 
    # immediately after reception to the server.
    # Periodic Tasks may miss some deadlines.
    results = []
    for exp in examples:
        T, C = exp[0], exp[1]
        n = len(T)
        current_time = 0
        queue = []
        result = [[0 for i in range(time_limit)] for i in range(n)]
        missed = [0 for i in range(time_limit)]
        interrupt = []
        int_flag = 0
        while current_time < time_limit:
            if current_time == ap_task_time:
                queue.insert(0, [current_time, 0, ap_task_jobs, 40])
                int_flag = 1
            for i in range(len(T)):
                if current_time % T[i] == 0:
                    queue.append([current_time, T[i], C[i], T[i], i])
            if not int_flag:
                queue.sort(key=lambda x: x[1])
            if len(queue) != 0:
                hp_task = queue[0]
                if current_time >= hp_task[3] + hp_task[0] and not int_flag:
                    missed[current_time] = 1
                hp_task[2] -= 1
                interrupt.append(int_flag)
                if not int_flag:
                    result[hp_task[4]][current_time] = 1
                if hp_task[2] == 0:
                    queue.remove(hp_task)
                    if int_flag:
                        int_flag = 0
            current_time += 1
        result.append(interrupt)
        result.append(missed)
        results.append(result)
    return results


def poll_server_rm(T, C, apt_time, apt_jobs, apt_dls, apt_num, time_limit=40):
    n = len(T)
    current_time = 0
    queue = []
    server = []
    result = [[0 for i in range(time_limit)] for i in range(n)]
    missed = [0 for i in range(time_limit)]
    p_priority = T.copy()
    p_priority.remove(T[apt_num])
    p_priority.sort()
    indexes = [i for i in range(n)]
    indexes.remove(apt_num)
    while current_time < time_limit:
        for i in indexes:
            if current_time % T[i] == 0:
                p = p_priority.index(T[i])
                if p >= apt_num: p += 1
                queue.append([current_time, T[i], C[i], T[i], i, p])
        if current_time in apt_time:
            index = apt_time.index(current_time)
            server.append([current_time, T[2], apt_jobs[index], apt_dls[index], 2, apt_num])
        if current_time % T[2] == 0 and current_time != 0 and len(server) != 0 and len(queue) == 0:
            queue.append(server[0])
            server = []
        queue.sort(key=lambda x: x[5])
        if len(queue) != 0:
            hp_task = queue[0]
            if current_time >= hp_task[3] + hp_task[0]:
                missed[current_time] = 1
            hp_task[2] -= 1
            if hp_task[2] == 0:
                queue.remove(hp_task)
            result[hp_task[4]][current_time] = 1
        current_time += 1
    result.append(missed)
    return result
