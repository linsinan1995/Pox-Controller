# It is a script to calculate the averate video quality from the latest log file
# put it in client VM: ~/tapas-master
import numpy as np
import os

for dir, _, files in  os.walk("logs/BBA0"):
  pass

ts = {}
for file in files:
  ts[dir+"/"+file] = os.path.getctime(dir+"/"+file)

ts = sorted(ts)[::-1]
data = np.genfromtxt(ts[0])
video_rate = data[:, 4]
print os.getcwd()+"/"+ts[0], "\n", np.mean(video_rate)

