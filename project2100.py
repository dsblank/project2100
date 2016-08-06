from __future__ import division, print_function, with_statement

## 2100 Project
## Art Installation, Fall 2016

## Rhine Singleton & Doug Blank
## http://www.ecologyandevolution.org/2100home.html

import gtk
import freenect
import chuck
import os
import numpy as np

def get_scan():
    try:
        image = freenect.sync_get_depth()[0]
    except:
        image = None
    return image

def convert_depth(depth):
    """
    depth: A numpy array with 2 bytes per pixel
    """
    depth = np.copy(depth)
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = (depth - 205)/50.0 * 255
    depth = depth.astype(np.uint8)
    # Scale it:
    return depth

if __name__ == "__main__":
    window = gtk.Window()
    window.fullscreen()
    window.show()

    # Start chuck server:
    os.system("chuck --verbose:9 --port:9000 " +
              "/home/turtlebot/chuck/chuck/osc/oscrecv.ck &")

    # Start infinite loop:
    while True:
        # get scan:
        scan = get_scan()
        if scan is None:
            break
        print(image)

# data = get_scan()
# pic = convert_depth(data)
# image = PIL.Image.fromarray(pic, mode="L")
# image.save("test1.png")
