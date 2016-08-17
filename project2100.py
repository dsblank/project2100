from __future__ import division, print_function, with_statement

## 2100 Project
## Art Installation, Fall 2016

## Rhine Singleton & Doug Blank
## http://www.ecologyandevolution.org/2100home.html

#import gtk
import freenect
import chuck
import os
import numpy as np
from PIL import Image
import time
import sys

ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
freenect.set_depth_format(dev, 

average = 14.0 # add to each, in celsius; not needed

def initialize_data():
    global tdata
    tdata = {} # temperature data
    tdata[1898] = -0.29
    tdata[1899] = -0.16
    tdata[1900] = -0.09
    tdata[1901] = -0.15
    tdata[1902] = -0.28
    tdata[1903] = -0.36
    tdata[1904] = -0.45
    tdata[1905] = -0.28
    tdata[1906] = -0.23
    tdata[1907] = -0.4
    tdata[1908] = -0.44
    tdata[1909] = -0.47
    tdata[1910] = -0.43
    tdata[1911] = -0.44
    tdata[1912] = -0.35
    tdata[1913] = -0.35
    tdata[1914] = -0.16
    tdata[1915] = -0.11
    tdata[1916] = -0.33
    tdata[1917] = -0.4
    tdata[1918] = -0.26
    tdata[1919] = -0.23
    tdata[1920] = -0.26
    tdata[1921] = -0.21
    tdata[1922] = -0.27
    tdata[1923] = -0.24
    tdata[1924] = -0.28
    tdata[1925] = -0.2
    tdata[1926] = -0.09
    tdata[1927] = -0.2
    tdata[1928] = -0.21
    tdata[1929] = -0.36
    tdata[1930] = -0.13
    tdata[1931] = -0.09
    tdata[1932] = -0.17
    tdata[1933] = -0.28
    tdata[1934] = -0.13
    tdata[1935] = -0.19
    tdata[1936] = -0.15
    tdata[1937] = -0.02
    tdata[1938] = -0.02
    tdata[1939] = -0.03
    tdata[1940] = 0.08
    tdata[1941] = 0.13
    tdata[1942] = 0.1
    tdata[1943] = 0.14
    tdata[1944] = 0.26
    tdata[1945] = 0.12
    tdata[1946] = -0.03
    tdata[1947] = -0.04
    tdata[1948] = -0.09
    tdata[1949] = -0.09
    tdata[1950] = -0.17
    tdata[1951] = -0.06
    tdata[1952] = 0.01
    tdata[1953] = 0.08
    tdata[1954] = -0.12
    tdata[1955] = -0.14
    tdata[1956] = -0.2
    tdata[1957] = 0.03
    tdata[1958] = 0.06
    tdata[1959] = 0.03
    tdata[1960] = -0.03
    tdata[1961] = 0.05
    tdata[1962] = 0.02
    tdata[1963] = 0.06
    tdata[1964] = -0.2
    tdata[1965] = -0.1
    tdata[1966] = -0.05
    tdata[1967] = -0.02
    tdata[1968] = -0.07
    tdata[1969] = 0.07
    tdata[1970] = 0.03
    tdata[1971] = -0.09
    tdata[1972] = 0.01
    tdata[1973] = 0.15
    tdata[1974] = -0.08
    tdata[1975] = -0.01
    tdata[1976] = -0.11
    tdata[1977] = 0.18
    tdata[1978] = 0.07
    tdata[1979] = 0.16
    tdata[1980] = 0.27
    tdata[1981] = 0.32
    tdata[1982] = 0.13
    tdata[1983] = 0.31
    tdata[1984] = 0.16
    tdata[1985] = 0.12
    tdata[1986] = 0.19
    tdata[1987] = 0.33
    tdata[1988] = 0.4
    tdata[1989] = 0.29
    tdata[1990] = 0.44
    tdata[1991] = 0.42
    tdata[1992] = 0.23
    tdata[1993] = 0.24
    tdata[1994] = 0.32
    tdata[1995] = 0.46
    tdata[1996] = 0.34
    tdata[1997] = 0.48
    tdata[1998] = 0.63
    tdata[1999] = 0.42
    tdata[2000] = 0.42
    tdata[2001] = 0.55
    tdata[2002] = 0.63
    tdata[2003] = 0.62
    tdata[2004] = 0.55
    tdata[2005] = 0.69
    tdata[2006] = 0.63
    tdata[2007] = 0.66
    tdata[2008] = 0.54
    tdata[2009] = 0.64
    tdata[2010] = 0.72
    tdata[2011] = 0.6
    tdata[2012] = 0.63
    tdata[2013] = 0.66
    tdata[2014] = 0.75
    tdata[2015] = 0.87

class HiHatOpen(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/hihat-open.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

class HiHat(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/hihat.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

class SnareChili(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/snare-chili.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

class Kick(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/kick.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

class SnareHop(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/snare-hop.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

class Snare(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile("data/snare.wav")

    def noteOn(self):
        self.setLooping(1)
        time.sleep(.1)
        self.setLooping(0)

def get_scan():
     try:
        scan = freenect.sync_get_depth(format=freenect.DEPTH_MM)[0]
     except:
        scan = None
     return scan

def get_depth(scan):
     """
     The depth range is 40cm to 800cm, represented as 0 to 255.
     """
     depth = scan/30.0
     depth = depth.astype(np.uint8)
     depth[0:479, 630:639] = depth[0:479, 620:629]
     return depth

def start_server(name="chuck", user="turtle"):
    # Start chuck server:
    os.system(("%s --verbose:9 --port:9000 " % name) +
              ("/home/%s/chuck/chuck/osc/oscrecv.ck &" % user))

# chuck --verbose:9 --port:9000 /home/turtle/chuck/chuck/osc/oscrecv.ck &

chuck.init()
initialize_data()

instr1 = chuck.MoogSynthesizer()
#instr1.setFilterQ(0)
#instr1.setFilterSweepRate(0.2)
#instr1.setVibrato(0, 0)
#instr1.setAfterTouch(0)
instr1.connect()

instr2 = chuck.Mandolin()
instr2.connect()

percussion = chuck.Shakers()
percussion.connect()

HIGHEST_DEVIATION = 4.87

def key_to_freq(n):
    # given  key on piano, what is freq?
    # From: https://en.wikipedia.org/wiki/Piano_key_frequencies
    return 2 ** ((n - 49) / 12) * 440

def tdata_to_freq(celsius):
    # convert celsius to freq
    # historic data is 50% of 88 key range
    # the -1.2 at the end of the minc value makes higher lowest note.-RS
    minc = min(tdata.values())-1.2
    maxc = HIGHEST_DEVIATION # max(tdata.values())
    scale = (celsius - minc) / (maxc - minc)
    key = int(scale * 88)
    freq = key_to_freq(key)
    return freq

def play_percussion(instrument, volume):
    instrument.noteOn(volume)

def play_note(instrument, percussion, frequency, volume, quarter_note, 
              note_percent, count, year):
    seconds1 = quarter_note / 2.0
    seconds2 = max((quarter_note * note_percent) - seconds1, 0)
    instrument.setFrequency(frequency)
    if count == 1:
        v1 = 1.0
        v2 = 0.7
    else:
        v1 = 0.7
        v2 = 0.7
    if percussion:
        play_percussion(percussion, v1)
    instrument.setGain(volume)
    #for synth, use noteOn; for mandolin, use pluck
    #instrument.noteOn(1.0)
    instrument.pluck(0.3)
    time.sleep(seconds1)
    # present!
    if percussion: # 2050
        play_percussion(percussion, v2)
    time.sleep(seconds2)
    #instrument.noteOff(0.5)
    # mandolin: use pluck, no noteoff
    time.sleep(quarter_note * (1.0 - note_percent))

def play_note2(instrument, percussion, frequency, volume, quarter_note, 
              note_percent, count, year):
    seconds1 = quarter_note / 2.0
    seconds2 = max((quarter_note * note_percent) - seconds1, 0)
    instrument.setFrequency(frequency)
    if count == 1:
        v1 = 1.0
        v2 = 0.7
    else:
        v1 = 0.7
        v2 = 0.7
    if percussion:
        play_percussion(percussion, v1)
    instrument.setGain(volume)
    #for synth, use noteOn; for mandolin, use pluck
    #instrument.noteOn(1.0)
    instrument.pluck(0.3)
    time.sleep(seconds1)
    # present!
    #if percussion: # 2050
        #play_percussion(percussion, v2)
    #time.sleep(seconds2)
    #instrument.noteOff(0.5)
    # mandolin: use pluck, no noteoff
    time.sleep(quarter_note * (1.0 - note_percent))

def get_or_make_estimate(year, angle):
    ## angle is 0 to 1, 0 is left side of sensor (worst)
    global tdata
    tdata1 = tdata.get(year, None)
    if tdata1:
        return tdata1
    ## estimate it based on past years:
    previous_year = get_or_make_estimate(year - 1, angle)
    tdata[year] = min(previous_year + (1.0 - angle) * 3./84 + 1./84, 
                      HIGHEST_DEVIATION)
    return tdata[year]

def play_measure(instrument, percussion, year, angle, tempo):
    ## higher tempo?
    # year 1900 to 2100
    # angle 0 to 1
    # temp 0 to 1
    note_percent = 0.75 # percent of beat that note plays

    tdata1 = get_or_make_estimate(year - 2, angle)
    tdata2 = get_or_make_estimate(year - 1, angle)
    tdata3 = get_or_make_estimate(year, angle)

    tfreq1 = tdata_to_freq(tdata1)
    tfreq2 = tdata_to_freq(tdata2)
    tfreq3 = tdata_to_freq(tdata3)

    quarter_note = 1.0 - tempo/1.0 
    eighth_note = quarter_note/2.0

    if False and year > 2016: # present!
        instr2.setFrequency(tfreq3)
        instr2.pluck(0.7)

    play_note(instrument, percussion, tfreq3, 1.0, 
              quarter_note, note_percent, 1, year)

    play_note(instrument, percussion, tfreq2, 0.7, 
              quarter_note, note_percent, 2, year)

    play_note(instrument, percussion, tfreq2, 0.6, 
              quarter_note, note_percent, 3, year)


def play_measure2(instrument, percussion, year, angle, tempo):
    ## higher tempo?
    # year 1900 to 2100
    # angle 0 to 1
    # temp 0 to 1
    note_percent = 0.75 # percent of beat that note plays

    #tdata1 = get_or_make_estimate(year - 2, angle)
    #tdata2 = get_or_make_estimate(year - 1, angle)
    tdata3 = get_or_make_estimate(year, angle)

    #tfreq1 = tdata_to_freq(tdata1)
    #tfreq2 = tdata_to_freq(tdata2)
    tfreq3 = tdata_to_freq(tdata3)

    quarter_note = 1.0 - tempo/1.0 
    #triplet = quarter_note * 1.333333
    whole_note = quarter_note * 3

    if False and year > 2016: # present!
        instr2.setFrequency(tfreq3)
        instr2.pluck(0.7)

    play_note2(instrument, percussion, tfreq3, 1.0, whole_note,
              note_percent, 1, year)

    play_note2(instrument, percussion, tfreq3, 0, quarter_note,
              note_percent, 2, year)

    play_note2(instrument, percussion, tfreq3, 0, quarter_note,
              note_percent, 3, year)


def main():
    #window = gtk.Window()
    #window.fullscreen()
    #window.show()
    chuck.init()

    # Start infinite loop:
    #year = int(sys.argv[1])
    #angle = float(sys.argv[2])
    while True:
        # get scan:
        print("scan!")
        scan = get_scan()
        if not scan:
            continue
        else:
            data = get_depth(scan) # 0 is close, 255 is nothing
            rows, cols = data.shape
            minimum = 255
            minimum_col = 0
            pic = np.zeros(shape=(5, cols), dtype="uint8")
            r = 0
            for row in range(240, 240 + 5): # middle 10
                c = 0
                for col in range(100, cols - 200, 1): # 640
                    if data[row][col] < minimum:
                        minimum = data[row][col]
                        minimum_col = c
                    pic[r][col] = data[row][col]
                    c += 1
                r += 1
            angle = minimum_col/c
            print("min angle:", angle, "distance:", minimum)
        year = int(minimum/255.0 * 200.0 + 1900)
        tempo = (year - 1900)/220.0
        print("year:", year, "tempo:", tempo)
        play_measure(instr2, percussion, year, angle, tempo)
        print("temp:", tdata.get(year, None))
        #image = Image.fromarray(data, mode="L")
        #image.save("test1.png")
        #print(image)
        #time.sleep(5)
        #if year >= 2100:
        #    initialize_data()
        #year += 1

if __name__ == "__main__":
    main()
