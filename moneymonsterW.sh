#!/bin/bash

#move to correct working directory for proper relative file locations
cd ~/git/moneymonster

#create backup of data
mv data/masterData.csv mmBKP/masterData$(date -I)

#collect data (This takes a awhile)
python3 librarian/weekLibrarian.py > output/cron$(date -I).log

#parse data into training set
python3 librarian/dataClassifierW.py >> output/cron$(date -I).log

#collect slice data for predictions
#python3 librarian/getSliceW.py >> output/cron$(date -I).log

#feed the moneymonster
#python3 ai/auto-kerasW.py 2>> output/cron$(date -I).log

#print predictions
#note: this should be run at open ideally
#python3 ai/algo.py > output/predictions$(date -I).mm
