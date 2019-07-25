#!/bin/bash
export topFile="picks/top5_$(date -I).csv"
export bottomFile="picks/bottom5_$(date -I).csv"
cd /home/jb007/git/moneymonster
cp data/bottom5.csv $bottomFile
git add $bottomFile
cp data/top5.csv $topFile
git add $topFile
git commit -m "auto committing picks from $(date -I)"
git push

