# -*- coding: utf-8 -*-
import math
from Antmicro.Renode.Time import TimeInterval
import System.IO

pipe_path = "/home/tom/Renode_experiments/python_log_scripts/distance_status_pipe"

try:
    # Use .NET System.IO.File.Open for non-blocking access to FIFO
    # Specify FileMode.Open and FileAccess.Write (FileShare.ReadWrite allows writing while others read)
    pipe_stream = System.IO.File.Open(pipe_path, System.IO.FileMode.Open, System.IO.FileAccess.Write, System.IO.FileShare.ReadWrite)
    pipe = System.IO.StreamWriter(pipe_stream)
    pipe.AutoFlush = True
except Exception as e:
    print("Could not open distance pipe via .NET: {}. Is it created and has a reader?".format(e))
    pipe = None

sensor = self.Machine["sysbus.i2c1.dist_sensor"]

def log_distance(time):
    if pipe:
        try:
            seconds = float(time.TimeElapsed.TotalSeconds)
            current_dist = sensor.Distance
            pipe.WriteLine("[{:.2f}s] SENSOR DISTANCE: {}m".format(seconds, current_dist))
        except Exception as e:
            print("Logging error to distance pipe: {}".format(e))

# Fix: Added *args to handle the TimeInterval argument passed by Renode
def schedule_log(*args):
    log_distance(self.Machine.ElapsedVirtualTime)
    self.Machine.ScheduleAction(TimeInterval.FromMilliseconds(100), schedule_log)

schedule_log()
