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

### NOTE: the chuck server should already be running
###       Run start_chuck

def initialize_data():
    """
    This is the average temperature data. It is the deviation from
    the average (14.0) in celsius.
    """
    global tdata
    # these data have been smoothed (1950-80, +.014667/yr; 1981-2015, +.01716/yr)
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
    tdata[1951] = -0.16
    tdata[1952] = -0.14
    tdata[1953] = -0.13
    tdata[1954] = -0.11
    tdata[1955] = -0.10
    tdata[1956] = -0.08
    tdata[1957] = -0.07
    tdata[1958] = -0.05
    tdata[1959] = -0.04
    tdata[1960] = -0.02
    tdata[1961] = -0.01
    tdata[1962] = 0.01
    tdata[1963] = 0.02
    tdata[1964] = 0.04
    tdata[1965] = 0.05
    tdata[1966] = 0.06
    tdata[1967] = 0.08
    tdata[1968] = 0.09
    tdata[1969] = 0.11
    tdata[1970] = 0.12
    tdata[1971] = 0.14
    tdata[1972] = 0.15
    tdata[1973] = 0.17
    tdata[1974] = 0.18
    tdata[1975] = 0.20
    tdata[1976] = 0.21
    tdata[1977] = 0.23
    tdata[1978] = 0.24
    tdata[1979] = 0.26
    tdata[1980] = 0.27
    tdata[1981] = 0.29
    tdata[1982] = 0.30
    tdata[1983] = 0.32
    tdata[1984] = 0.34
    tdata[1985] = 0.36
    tdata[1986] = 0.37
    tdata[1987] = 0.39
    tdata[1988] = 0.41
    tdata[1989] = 0.42
    tdata[1990] = 0.44
    tdata[1991] = 0.46
    tdata[1992] = 0.48
    tdata[1993] = 0.49
    tdata[1994] = 0.51
    tdata[1995] = 0.53
    tdata[1996] = 0.54
    tdata[1997] = 0.56
    tdata[1998] = 0.58
    tdata[1999] = 0.60
    tdata[2000] = 0.61
    tdata[2001] = 0.63
    tdata[2002] = 0.65
    tdata[2003] = 0.66
    tdata[2004] = 0.68
    tdata[2005] = 0.70
    tdata[2006] = 0.72
    tdata[2007] = 0.73
    tdata[2008] = 0.75
    tdata[2009] = 0.77
    tdata[2010] = 0.78
    tdata[2011] = 0.80
    tdata[2012] = 0.82
    tdata[2013] = 0.84
    tdata[2014] = 0.85
    tdata[2015] = 0.87

### Some useful wav files. Reads/plays if connected on construction.

class Wav(chuck.FileRead):
    def __init__(self):
        chuck.FileRead.__init__(self)
        self.setFile(self.filename)

    def noteOn(self, volume=1.0, wait=0.1):
        self.setGain(volume)
        self.setLooping(1)
        time.sleep(wait)
        self.setLooping(0)

class HiHatOpen(Wav):
    filename = "data/hihat-open.wav"

class HiHat(Wav):
    filename = "data/hihat.wav"

class SnareChili(Wav):
    filename = "data/snare-chili.wav"

class Kick(Wav):
    filename = "data/kick.wav"

class SnareHop(Wav):
    filename = "data/snare-hop.wav"

class Snare(Wav):
    filename = "data/snare.wav"

class Crash(Wav):
    filename = "data/crash.wav"

def combine_counts(counts, diff):
    """
    Given dictionary of {depth: [column, column, ...], ...}
    this function will combine counts of nearby depths.
    """
    depths = sorted(counts.keys())
    sets = [[depths[0]]]
    for d in range(len(depths) - 1):
        if abs(int(depths[d]) - int(depths[d+1])) <= diff:
            sets[-1].append(depths[d+1])
        else:
            sets.append([depths[d+1]])
    retval = {}
    for set in sets:
        columns = []
        for depth in set:
            columns.extend(counts[depth])
        retval[set[0]] = columns
    return retval

def get_scan():
    """
    Get a scan from the Kinect, if possible.
    """
    try:
        scan = freenect.sync_get_depth(format=freenect.DEPTH_MM)[0]
    except:
        scan = None
    return scan

def get_depth(scan):
     """
     The depth range is 40cm to 800cm, represented as 0 to 255.
     After https://github.com/eyantrainternship/eYSIP_2015_Depth_Mapping_Kinect
     """
     depth = scan/30.0
     depth = depth.astype(np.uint8)
     depth[0:479, 630:639] = depth[0:479, 620:629]
     return depth

def key_to_freq(n):
    """
    Given a key number, return the frequency. 88 keys.
    """
    # given  key on piano, what is freq?
    # From: https://en.wikipedia.org/wiki/Piano_key_frequencies
    return 2 ** ((n - 49) / 12) * 440

def tdata_to_freq(celsius):
    """
    Given a deviation from the average, return freq.
    """
    # convert celsius to freq
    # historic data is 50% of 88 key range
    # the -1.2 at the end of the minc value makes higher lowest note.-RS
    # i'm trying -0.9 for now when starting at 1950
    # it might also work to raise the HIGHEST_DEVIATION in order to make temps go up more by 2016
    minc = min(tdata.values())-0.9
    maxc = HIGHEST_DEVIATION # max(tdata.values())
    scale = (celsius - minc) / (maxc - minc)
    key = int(scale * 88)
    freq = key_to_freq(key)
    return freq

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
    instrument.setGain(volume)
    #for synth, use noteOn; for mandolin, use pluck
    #instrument.noteOn(1.0)
    instrument.pluck(0.2)
    time.sleep(seconds1)
    time.sleep(seconds2)
    # mandolin: use pluck, no noteoff
    time.sleep(quarter_note * (1.0 - note_percent))

def get_or_make_estimate(year, angle):
    ## angle is 0 to 1, 0 is left side of sensor (worst)
    global tdata
    tdata1 = tdata.get(year, None)
    if tdata1:
        for i in range(max(year + 1, 2016), 2100):
            if i in tdata:
                del tdata[i]
        return tdata1
    ## estimate it based on past years:
    previous_year = get_or_make_estimate(year - 1, angle)
        # i changed 3/84 to 5/84 and 1/84 to .3/84 for more contrast
    tdata[year] = min(previous_year + (1.0 - angle) * 5./84 + .3/84,
                      HIGHEST_DEVIATION)
    return tdata[year]

def play_measure(instrument, percussion, year, angle, tempo):
    ## higher tempo?
    # year 1950 to 2100
    # angle 0 to 1
    # temp 0 to 1
    note_percent = 1.00 # percent of beat that note plays

    tdata1 = get_or_make_estimate(year - 2, angle)
    tdata2 = get_or_make_estimate(year - 1, angle)
    tdata3 = get_or_make_estimate(year, angle)

    tfreq1 = tdata_to_freq(tdata1)
    tfreq2 = tdata_to_freq(tdata2)
    tfreq3 = tdata_to_freq(tdata3)

    quarter_note = 1.0 - tempo/1.0
    eighth_note = quarter_note/2.0

    instr1.noteOff(0.7)

    play_note(instrument, percussion, tfreq3, 1.0,
              quarter_note, note_percent, 1, year)

    if year >= 2016: # present!
        instr1.setGain(0.2)
        instr1.setFrequency(tfreq3)
        instr1.noteOn(0.7)

    #play_note(instrument, percussion, tfreq2, 0.7,
    #          quarter_note, note_percent, 2, year)

    #play_note(instrument, percussion, tfreq1, 0.6,
    #          quarter_note, note_percent, 3, year)

def play_ending(year, angle):
    for i in range(10):
        tempo_end = 0.7 + (0.03 * i)
        play_measure(instr2, percussion, 2100, angle, tempo_end)
    instr1.noteOff(0.7)
    # time.sleep(1)
    # for now, trying a percussion sound end
    percussion.noteOn(1)
    time.sleep(6)
    percussion.noteOff(1)
    # can't get the crash or any wav to work
    # crash.noteOn(volume=0.6, wait=4.0)
    # this next line prevents ending from playing 2100 end notes stored from previous iterations
    initialize_data()

def main():
    #window = gtk.Window()
    #window.fullscreen()
    #window.show()
    chuck.init()
    last_year = 0
    started = False
    # fail_count = 0
    while True:
        # empty print lines to make it easier to parse repetitive output
        print("")
        print("")
        # print("where that snare at!")
        # snare.noteOn(volume=0.6, wait=4.0)
        # wait=4
        print("scan!", started) # shows start status
        # get scan:
        scan = get_scan()
        if scan is not None:
            data = get_depth(scan) # 0 is close, 255 is nothing
            rows, cols = data.shape
            start_row = 0
            stop_row = 400 # 480 max, was 300
            start_col = 150
            stop_col = 490 # 640 max
            height, width = (stop_row - start_row), (stop_col - start_col)
            pic = np.zeros(shape=(height, width), dtype="uint8")
            r = 0
            counts = {}
            for row in range(start_row, stop_row, 5):
                c = 0
                #counts = {}
                for col in range(start_col, stop_col, 5):
                    if 0 < data[row][col] < 145:
                        list = counts.get(data[row][col], [])
                        list.append(c)
                        counts[data[row][col]] = list
                        pic[r][c] = data[row][col]
                    c += 1
                r += 1
            # Debug: ########################
            image = Image.fromarray(pic, mode="L")
            image.save("test1.jpg")
            #################################
            # counts = {32: [c, c, c, c], 67: [c, c, c]}
            if counts == {}:
                # this is if no pixels get detected, at least I think, - RS
                print("No one seen")
                continue
            if counts != {}:
                #print("before:", counts)
                #counts = combine_counts(counts, diff=1)
                #print("after:", counts)
                depths = sorted([(len(cnt), depth) for (depth, cnt) in
                                 counts.items()], reverse=True)
                minimum_count_depth = depths[0] # (len of count, depth)
                minimum = minimum_count_depth[1]
                print("matched pixels:", minimum_count_depth[0], "distance:", minimum)
        # this is a proximity "filter" to prevent artifcats at a distance of 3 from triggering anything
                if minimum < 10:
                    print("too close")
                    instr1.noteOff(0.7)
                    started = False
                    continue
        # this next "filter" has been changed to simply serve as a size of object/person filter
                if minimum_count_depth[0] < 25: # and minimum_count_depth[1] < 50:
                    print("Not big enough to count as being a person")
                    instr1.noteOff(0.7)
                    started = False
                    continue
                    # if started and fail_count < 4:
                    #     year = last_year
                    #     fail_count += 1
                    # else:
                    #     instr1.noteOff(0.7)
                    #     started = False
                    #     continue
        # it will only get to this section of code if something large enough is in the field
                column = sum(counts[minimum_count_depth[1]])/float(minimum_count_depth[0])
                angle = column/float(width)
                print("angle:", angle) #, "distance:", minimum)
        year = min(max(int((minimum - 15)/120.0 * 150.0 + 1950), 1950), 2100)
        tempo = (year - 1950)/170+0.08 #changed from 220 for smaller year range
        #new formula is attempt to get earlier years to play faster
        print("YOU GOT THROUGH THE SIZE FILTER")
        if started:
            # Message to confirm that started is True. Why is next if/else skipped when started is true?
            print("started:", started)
        # which of these is best? perhaps min>=137 so quick exist trigger ending
            if minimum >= 137:
                    print("YEAR = ", year, "END TRIGGER")
                    started = False
                    play_ending(2100, angle)
                    continue
        else:
            if year <= 1980:
                print("year <= 1980:, START TRIGGER")
                started = True
            else:
                print("Not yet! go to start!")
                started = False
                instr1.noteOff(0.7)
                continue
        # print("min count depth", minimum_count_depth[0])
        # if minimum_count_depth[0] > 999:
        print("YEAR:", year)
        play_measure(instr2, percussion, year, angle, tempo)
        print("sound should be playing")
        print("TEMP=PITCH OF NOTE:", tdata.get(year, None))
        last_year = year
    # else:
    #     print("NO SOUND!")

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
# been playing with different shakers for possible ending
# would rather have crash.wav ending and shakers available to play during experience in field if we want
percussion.preset(5)
# percussion.setEnergy(.8)
percussion.setDecay(1)
percussion.setObjects(128)
percussion.connect()

crash = Crash()
crash.connect()

#snare = SnareChili()
#snare.connect()

# i upped this to 5.87 to make the frequencies go up a bit faster
HIGHEST_DEVIATION = 5.87

if __name__ == "__main__":
    if sys.argv[1:]:
        start_year = int(sys.argv[1])
        stop_year = int(sys.argv[2])
        angle = float(sys.argv[3])
        for year in range(start_year, stop_year + 1):
            print("Year:", year)
            tempo = (year - 1950)/170+0.08 #changed from 220 for smaller year range
            play_measure(instr2, percussion, year, angle, tempo)
        if stop_year == 2100:
            play_ending(2100, angle)
    else:
        main()
