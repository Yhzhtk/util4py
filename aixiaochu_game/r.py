# coding=utf-8
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
sys.path.append(".")
print sys.path
import time, run

device = MonkeyRunner.waitForConnection()

#device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

while True:
    print "=" * 30
    start = time.clock()
    result = device.takeSnapshot()
    end = time.clock()
    print "SnapShot Time:", end - start
    
    if not result:
        continue
    
    step = run.get_step(result)
    if not step:
        continue
    
    start = time.clock()
    if step:
        for s in step:
            device.drag(s[0], s[1], 0.001, 1)
    end = time.clock()
    print "Drag Time:", end - start