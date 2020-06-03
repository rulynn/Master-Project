#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt



'''
 mtx 139911986011176
	 tid 9255 ::: start time 5073596298434.87us ::: wait time 85046.37us ::: hold time 35994.17us
	 tid 9258 ::: start time 5073596280492.59us ::: wait time 62791.55us ::: hold time 26878.19us
	 tid 9257 ::: start time 5073596258901.99us ::: wait time 65762.03us ::: hold time 28087.69us
	 tid 9256 ::: start time 5073596258763.20us ::: wait time 348452.35us ::: hold time 11421936.58us
	 tid 9260 ::: start time 5073596258691.26us ::: wait time 67576.99us ::: hold time 28922.44us
	 tid 9259 ::: start time 5073596345722.25us ::: wait time 66095.58us ::: hold time 28269.82us
 mtx 139911983519528
	 tid 9246 ::: start time 5073609629312.95us ::: wait time 14.65us ::: hold time 20.19us
	 tid 9259 ::: start time 5073597263174.33us ::: wait time 132.47us ::: hold time 110.96us
	 tid 9260 ::: start time 5073596391382.42us ::: wait time 96.93us ::: hold time 75.43us
	 tid 9255 ::: start time 5073597604515.55us ::: wait time 145.73us ::: hold time 121.50us
 ...
'''

class item_t:
    def __init__(self):
        self.tid = 0
        self.start_time_ns = 0
        self.wait_time_ns = 0
        self.lock_time_ns = 0

output_data = {}
#count = 0
start_time_min = 999999999999999
def collect_data(locks):
    for k, v in locks.items():
        # TODO: How to identify the thread
        tmp = item_t()
        tmp.tid = k.tid
        tmp.start_time_ns = v.start_time_ns/1000.0
        tmp.wait_time_ns = v.wait_time_ns/1000.0
        tmp.lock_time_ns = v.lock_time_ns/1000.0

        if output_data.get(k.mtx) == None:
            output_data[k.mtx] = []
        output_data[k.mtx].append(tmp)

        global start_time_min
        start_time_min = min(start_time_min, v.start_time_ns/1000.0)
    # plot
    plot_data(output_data)

def statistical_data(locks):
    for k, v in locks.items():
        print("\t tid %d ::: mtx %d" % (k.tid, k.mtx))
        print("\t start time %.2fus ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
            (v.start_time_ns, v.wait_time_ns, v.lock_time_ns, v.enter_count))

tid_dict = {}
tid_id = 0
def plot_data(output_data):
    for k, v in output_data.items():
        print("\t mtx %d" % (k))
        for item in v:
            global tid_id
            global tid_dict
            if tid_dict.get(item.tid) == None:
                tid_dict[item.tid] = tid_id
                tid_id = tid_id + 1

            x = [tid_dict[item.tid],tid_dict[item.tid]]
            start_time = item.start_time_ns - start_time_min
            print("\t tid %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
                                    (item.tid, start_time, item.wait_time_ns, item.lock_time_ns))

            plt.plot(x, [start_time, start_time + item.wait_time_ns], color='dimgray', label='wait')
            plt.plot(x, [start_time + item.wait_time_ns, start_time + item.wait_time_ns + item.lock_time_ns] ,
                        color='firebrick', label='hold')

        # output
        path = "out/" + str(k) + ".png"
        plt.savefig(path)

    output_data.clear()

