#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run.sh 5


# dir
rm -rf out
mkdir out
time=$1

echo "start running program..."


# 2 ** 22 = 4,194,304
# 2 ** 26 = 67,108,864
#cd /root/splash2/codes/kernels/fft
#./FFT -p8 -m26 &

# 1024*1024
cd /root/splash2/codes/kernels/lu/non_contiguous_blocks
./LU -p8 -n2048 &


echo "start get pid..."
pid=$(pgrep -f "LU")
echo "program pid: "  $pid

echo "start running eBPF..."
cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

#echo "start kill the program..."
#kill -9 $pid
#echo "finish"
