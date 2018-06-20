#!/usr/bin/env python
import freenect

tilt = 0

ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)

if not dev:
    freenect.error_open_device()

print "Setting TILT: ", tilt
freenect.set_tilt_degs(dev, tilt)