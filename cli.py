# ijkl to move
# sequence writing interface

import wave, math, struct


# print shitloads of lines
def clear():
    for i in range(0, 40, 1):
        print("")

# note to frequency
def ntof(note):
    # chromatic scale in hz, starting at C4, finishing at B4.
    octave4 = [0.00,
               261.63, 277.18, 293.66, 311.13,
               329.63, 349.23, 369.99, 392.00,
               415.30, 440.00, 466.16, 493.88]
    # possible note values
    notes = "0cCdDefFgGaAb"
    # find inputted note in notes, use it's index to find relevant frequency.
    return(octave4[notes.find(note)])

    
def render(table, length_samples=10000, repetitions=4):
    
    # table is a 2d array of note names.
    stream = wave.open("./test.wav", 'w')
    sample_rate = 44100
    
    stream.setframerate(sample_rate)
    stream.setnchannels(1)
    stream.setsampwidth(1)
        
    sequence_step = int(0)
    volume = int(127/len(table))

    for i in range(0, repetitions, 1):
        sequence_step = 0
        for note in table[0]:
            for i in range(0, length_samples, 1):
                value = 0
                trackno = 0
                for track in table:
                    # 2^ trackno means each successive track is an octave higher than previous
                    freq = ntof(str(table[trackno][sequence_step]))
                    rads = 2*math.pi*float(i)/float(sample_rate)
                    value += int(volume*math.sin(freq*rads))
                    trackno += 1
                value += 127
                stream.writeframesraw(struct.pack('<B', int(value)))
            sequence_step += 1
        
        stream.writeframes('')
    stream.close()
    return 0
    
    
tempo = 90
tracks = 4 # rows
length = 16 # columns
beatevery = 4 # highlight every nth column
editstep = True # advance cursor after inserting note? 
cursor = [0, 0] # cursor coordinates
running = True # for main loop + quit

# generate empty table for notes
def zap(tracks=4, length=16):
    table = []
    for i in range(0, tracks, 1):
        table.append([])
        for j in range(0, length, 1):
            table[i].append("0")
    return table 


table = zap(tracks, length)

# main loop, waits for keypresses and does stuff
while running:
    clear()
    # instructions
    print("ijkl to move cursor, h to jump to start of line")
    print("cCdDefFgGaAb for notes, 0 to insert silence.")
    print("z will destroy all notes. q will quit. r to render.")
    print("press return after command(s)\n\n\n")
    # draw
    # generate "beat row"
    beatrow = str()        
    # generate cursor row above "note matrix"
    cursorrow = str()
    for i in range(0, length, 1):
        if i == int(cursor[0]):
            cursorrow = cursorrow + ". "
        else:
            cursorrow = cursorrow + "  "

        if i % beatevery == 0:
            beatrow = beatrow + "| "
        else:
            beatrow = beatrow + "  "

    print(beatrow)
    print(cursorrow)

    trackno = 0
    for track in table:
        currenttrack = str()
        for note in track:
            if note != "0":
                currenttrack = currenttrack + str(note) + " "
            else:
                currenttrack = currenttrack + "_ "
        if trackno == cursor[1]:
            currenttrack = currenttrack + "-"
        print(currenttrack)
        trackno += 1
    print("")


    # user input
    try:
        actions = raw_input(": ")
    except:
        actions = ""
    #type multiple commands at once!
    for action in actions:
        # catch notes and add to grid.
        # capital letter represent sharps in single char. zero represents silence.
        for note in "cCdDefFgGaAb0":
            if action == note:
                table[cursor[1]][cursor[0]] = note
                if editstep:
                    if cursor[0] < (length - 1):
                        cursor[0] += 1
        # quit
        if action == "q":
            running = False

        # zap song
        if action == "z":
            table = zap(tracks, length)
            cursor = [0, 0]

        if action == "r":
            render(table)

        # move the cursor. make sure within index ranges of table.
        # vertically
        if action == "i":
            if cursor[1] > 0:
                cursor[1] -= 1
        if action == "k":
            if cursor[1] < (tracks-1):
                cursor[1] += 1
        # horizontally
        if action == "j":
            if cursor[0] > 0:
                cursor[0] -= 1
        if action == "l":
            if cursor[0] < (length-1):
                cursor[0] += 1
        if action == "h":
            cursor[0] = 0
        
