#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv



def run(tid_list, ans, total):
    plot_origin(tid_list, ans, total)
    plot_with_name(tid_list, ans, total)
    plot_sub(tid_list, ans, total)
    #outputCSV(tid_list, ans, total)

def outputCSV(tid_list, ans, total):

    VMThread = getVMThread()
    # CSV data
    csvfile = open('../output/data.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['id','name','height','sum'])

    pre = 1
    for i in range(len(tid_list)):

        if ans[i] == 0:
            continue
        if VMThread.get(tid_list[i]) == None:
            label = "Thread " + str(tid_list[i]);
        else:
            label = VMThread[tid_list[i]] + " " + str(tid_list[i])

        data = [i+1, label, round(ans[i]*1.0/total,4), pre]
        pre = round(pre - ans[i]*1.0/total, 4)
        writer.writerow(data)

    csvfile.close()


def plot_origin(tid_list, ans, total):
    plt.figure(1)
    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    sub_tid = []
    sub_total = 0
    for i in range(len(tid_list)):
        if ans[i] == 0:
            continue

        print("ans %d ::: total %d ::: ans/total %.2f" % (ans[i], total, ans[i]/total))
        label = "thread " + str(tid_list[i]) + ": " + str(round(ans[i], 0)) + "/" + str(round(total,0)) + "=" + str(round(ans[i]/total,4))
        width = 0.35

        now = []
        now.append(pre[0] + ans[i]/total)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now

    plt.ylim(0,1)
    plt.legend()
    path = "../output/critical-origin.png"
    plt.savefig(path)

def plot_with_name(tid_list, ans, total):
    plt.figure(2)
    VMThread = getVMThread()
    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    sub_tid = []
    sub_total = 0
    for i in range(len(tid_list)):
        if ans[i] == 0:
            continue
        print("ans %d ::: total %d ::: ans/total %.2f" % (ans[i], total, ans[i]/total))
        label = ""
        if VMThread.get(tid_list[i]) == None:
            label = "thread " + str(tid_list[i]);
        else:
            label = VMThread[tid_list[i]] + " " + str(tid_list[i])
        label = label + ": " + str(round(ans[i]/total,4))
        width = 0.35

        now = []
        now.append(pre[0] + ans[i]/total)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now

    plt.ylim(0,1)
    plt.legend()
    path = "../output/critical-name.png"
    plt.savefig(path)

def plot_sub(tid_list, ans, total):
    plt.figure(3)
    VMThread = getVMThread()
    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    sub_tid = []
    sub_total = 0
    for i in range(len(tid_list)):
        if ans[i] == 0:
                continue
        if VMThread.get(tid_list[i]) == None:
            sub_tid.append(i)
            sub_total += ans[i]

    for i in sub_tid:
        print("ans %d ::: total %d ::: ans/total %.2f" % (ans[i], total, ans[i]/sub_total))
        label = "thread " + str(tid_list[i]) + ": " + str(round(ans[i]/sub_total,4))
        width = 0.35

        now = []
        now.append(pre[0] + ans[i]/sub_total)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now

    plt.ylim(0,1)
    plt.legend()
    path = "../output/critical-sub.png"
    plt.savefig(path)


def getVMThread():
    VMThread = {}
    with open('../output/out_stack.log', 'r') as f:
        jstack = f.readlines()
    for i in range(0, len(jstack)):
        if jstack[i][0] == "\"":
            x = jstack[i].split("\"")
            idx = jstack[i].find("nid")
            nid = ""
            for j in range(idx+6, len(jstack[i])):
                if jstack[i][j] == ' ':
                    break
                nid += jstack[i][j]
            nid_int = int(nid.upper(), 16)
            VMThread[nid_int] = x[1]
            #print(x[1], nid_int)
    return VMThread


# tid_list = [12324, 14545, 26135, 26134]
# ans = [10, 20, 30, 40]
# total = 100
# outputCSV(tid_list, ans, total)