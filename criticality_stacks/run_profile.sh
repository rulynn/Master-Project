#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1
name="avrora"

java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar ~/dacapo.jar -n 3 $name &

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`
output=`~/bcc/tools/profile.py -adf -p $pid $time > out/out.profile`
output=`~/FlameGraph/flamegraph.pl < out/out.profile > out/out.svg`