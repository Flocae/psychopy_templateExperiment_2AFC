"""
PSYCHOPY EXAMPLE EXPERIMENT version 0.1

Purpose: Simple template for Simple Forced-Choice Task
Task: Participant have to say whether the face that was presented to him was
    sad or happy
Design (example): EMOTION (Sad,Happy)*SPATIAL_FREQUENCY (High-Pass,Low-Pass
        Filter,No Filter)
DATA: Correct response (0/1), Reaction Time (ms)

# I tried to follow Python's PEP8 style guidelines : https://www.python.org/dev/peps/pep-0008/

@author: florent caetta 2016-12

"""
import os
import sys
import random
import csv
from psychopy import visual,core,event,gui,data

"""

VARIABLES (constants)

"""

# -- Trial
STIMULUS_FLASHED = True # Whether stimulus is flashed; if TRUE, set STIMULUS_DU
STIMULUS_DU = 100 # stimulus duration (ms); Only if STIMULUS_FLASHED = TRUE; Then converted into n frames for better temporal precision (see : http://www.psychopy.org/general/timing/millisecondPrecision.html)
N_REPETITION= 4 # N repetitions for each condition
TRIAL_MAX_DU = 5 #  Maximum duration for one trial (WARNING : if STIMULUS_DU>TRIAL_MAX_DU, then  STIMULUS_DU = TRIAL_MAX_DU)
INTERTRIAL_DU= 1 # DU between 2 trials (sec)
RESPONSE_SCREEN=True # takin into account if STIMULUS_FLASHED = true

# -- Text
INSTRUCTIONS = "Hi, I'm the instructor. Press Space to continue"
THANKS = "Thank you very very very much. Press Space to continue"

# -- Monitor (later implemented)
#SC_DISTANCE = 57  # Distance subject and monitor
#SC_WIDTH = 40  # Width of the monitor (cm)
#SC_SIZE = [1024, 768]  # resolution

"""

SETTINGS

"""
# -- Directories (images)
directory = os.getcwd()#Returns current working directory (e.g. where the script is located)
stimulus_directory = directory+ "/stim"
os.chdir(directory+ "/data" )# move to the data path

# -- Dialog Box, informations
myDlg = gui.Dlg(title="informations", pos=(400,200),size = [800,400])# Bug with size?
myDlg.addText('Subject', color='Blue')
myDlg.addField('Group', tip='control or patient')
myDlg.addField('Initials', tip='Name/Surname')
myDlg.addField('Session',tip='session number')
myDlg.show()
if myDlg.OK:
    this_info = myDlg.data #this will be a list of data returned from each field added in order
    groupe, initial, num= this_info
    INFO = groupe + "_" + initial + "_" + num
else:
   raise Exception

# -- Data File
if not STIMULUS_FLASHED:
    RESPONSE_SCREEN=False
    STIMULUS_DU = "NA" # If image is not flashed: Not Applicable
else:
    StimDU=STIMULUS_DU
exp= data.ExperimentHandler(name='Autism_Emotion',
                version='0.1',
                extraInfo={
                    'groupe': groupe,
                    'participant':initial,
                    'session':num,
                    'Stim DU (ms)':STIMULUS_DU,
                    'Max Trial DU':TRIAL_MAX_DU,
                    'Response screen':RESPONSE_SCREEN},
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=True,
                dataFileName=INFO)
data_path = INFO + '.csv'
data_path_exists = os.path.exists (data_path)
if data_path_exists and INFO!="__":
    sys.exit("File " + data_path + " already exists")

# -- Trial Handler

# Create a list of variable combinations (dictionaries)
trialList = []
for emotion in ["Happy","Sad"]: #first variable is emotion, 2 possible values
    for sf in ["BSF", "NSF", "HSF"]: #second variable is spatial frequency,3 possible values
        trialList.append(
            {'sf':sf, 'emotion':emotion} #this is a python 'dictionary'
            )
# Add trialList to the trial handler
trials = data.TrialHandler(trialList,N_REPETITION, method='random',
    extraInfo={'groupe': groupe,'participant':initial,'session':num})
exp.addLoop(trials)

# -- Window, stimuli (image) & clock

# Window object.
window = visual.Window(fullscr=False,size = [800,400],monitor='dellExt',units='cm')# set up a monitor (e.g. icon with 2 monitors)
# implemented later
#current_monitor = monitors.Monitor('currentMonitor', width=SC_WIDTH, distance=SC_DISTANCE)
#current_monitor.setSizePix(SC_SIZE)

# List of stim (image) name
images = []
for file in os.listdir(stimulus_directory):
    if file.lower().endswith(".bmp") : #converting the filenames to lower case and checking whether they have a .bmp extension
        images.append(file) #If .bmp, add image to our list of images
# Fixation
fixation = visual.ShapeStim(window,
    vertices=((0, -0.2), (0, 0.2), (0,0), (-0.2,0), (0.2, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor='black'
)

# Clock object
clock = core.Clock()
# Determine the screen Refresh Rate and then convert DU-s ms to frames number (better precision for stimulus presentation);
window.recordFrameIntervals=True;
for frame in range(2):
    window.flip()
if STIMULUS_FLASHED:
    stimulus_DU_nFR=int((STIMULUS_DU)/(window.frameIntervals[0]*1000))
    print stimulus_DU_nFR,window.frameIntervals[0]
window.recordFrameIntervals=False;

"""

FUNCTIONS

"""

def draw_text_function (myText):
    """displays text on screen && wait for key_press (space)
    """
    text = visual.TextStim(window, text= myText, color=[-1.000,-1.000,-1.000], height=0.5 )
    text.draw()
    window.flip()
    # Wait for special Key (space)
    key = event.waitKeys(keyList = ['space','escape'])
    if key[0] == 'escape':
        raise Exception

def one_trial_function(image,TRIAL_MAX_DUration):
    """displays Trials, returns Key and reaction time :
    1 - Fixation (random)
    2 - Stimulus and wait for key_press
    Break if > TRIAL_MAX_DUration
    """
    # --1-- Fixation
    fixation.draw()
    window.flip()
    core.wait(1);

    # --2-- Stimulus
    stimulus_image = visual.ImageStim(window,stimulus_directory+"/"+image)
    event.clearEvents()# flush the key buffer
    window.callOnFlip(clock.reset)# Call a function immediately after the next .flip() command, synchronize with the frame; clock.reset, reset clock to 0

    if STIMULUS_FLASHED:
        frame=0
        key_press = False
        while not key_press:
            if frame < stimulus_DU_nFR:
                stimulus_image.draw(window)# draw  image to the window's back buffer
            elif frame > stimulus_DU_nFR+10 and RESPONSE_SCREEN:
                text = visual.TextStim(window, pos=(0.0, 2.0),text= "Response",
                    color=[-1.000,-1.000,-1.000], height=0.5 )
                text.draw()
                text2 = visual.TextStim(window,text= "<- Sad                                Happy ->",
                    color=[-1.000,-1.000,-1.000], height=0.5 )
                text.draw()
                text2.draw()
            window.flip()
            #if (frame==stimulus_DU_nFR):
                #print clock.getTime() # Uncomment these lines to check if durations are close to STIMULUS_DU
            keys=event.getKeys(keyList = ['left','right','escape'],timeStamped=clock)
            if keys !=[]:
                if keys[0][0] == 'escape':
                    raise Exception
                else:
                    key_press = True
                    return keys
            frame+=1
    else:
        # Wait for specials keys ('left','right','escape'), get the RT (timeStamped), and set max wait DU (maxWait)
        stimulus_image.draw(window)# draw  image to the window's back buffer
        window.flip()
        keys = event.waitKeys(keyList = ['left','right','escape'],timeStamped=clock,maxWait=TRIAL_MAX_DU)
        if keys is not None and keys[0][0] == 'escape':
            raise Exception
        return keys # return results, eg : response (left/right) & RT

"""

EXPERIMENT

"""

# --1-- Instructions
draw_text_function(INSTRUCTIONS)
window.flip()
core.wait(1);

# --2-- Trials (main loop)
for thisTrial in trials:
    imageIndex=images.index(thisTrial["emotion"]+"_"+thisTrial["sf"]+".bmp")# get index by image name (from trialList)
    oneTrial=one_trial_function(images[imageIndex],TRIAL_MAX_DU)# start one trial, wait return
    # Is correct?
    print oneTrial[0][0]
    if thisTrial["emotion"] == "Sad" and oneTrial[0][0]=="left":
        correct_resp = 1
    elif thisTrial["emotion"] == "Happy" and oneTrial[0][0]=="right":
        correct_resp = 1
    else:
        correct_resp = 0
    # Add Data
    if oneTrial is not None:
        # Handle Accuracy/RT Here
        # TrialHandler
        trials.data.add('Response', oneTrial[0][0])
        trials.data.add('CR', correct_resp)
        trials.data.add('RT', oneTrial[0][1]*1000)
        # ExperimentHandler
        exp.addData('Response', oneTrial[0][0])
        exp.addData('CR', correct_resp)
        exp.addData('RT', oneTrial[0][1]*1000)
    else:
        # Handle "No Response Trials" Here
        trials.data.add('Response', "No resp")
        trials.data.add('CR', "NaN")
        trials.data.add('RT', "Nan")
        exp.addData('Response', "NoResp")
        exp.addData('CR', "NaN")
        exp.addData('RT', "NoRT")
    exp.nextEntry()
    # Intertrial
    window.flip()
    core.wait(INTERTRIAL_DU);

# --3-- Final
# saving Data
trials.saveAsExcel(fileName=data_path,
                  sheetName = 'Results',
                  stimOut=[],
                  dataOut=['all_raw'])
draw_text_function(THANKS)
# Goodbye
window.close()# Close the window
core.quit()# Close PsychoPy



"""
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#          Notes
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
# ---- Data Attributes (.css) :
# .thisN - total trials completed so far
# .thisRepN - which repeat you are currently on
# .thisTrialN - which trial number within that repeat

# ---- Difference between exp.addData() and trials.addData()
# Jon P. says "ExperimentHandler came later and any data
#   received by a loop (TrialHandler) is passed on to the experiment, so
#   it's stored in both. But the ExperimentHandler can technically store
#   additional data, including things that occurred before or between loops.
#   For the standard csv output these things will be almost
#   indistinugishable. But if you save out to an xlsx file, for example,
#   that stores data according to loops, with one worksheet for each loop in
#   the experiment. Data saved using exp.addData() won't be included in that
#   output because the experiment doesn't know which loop it belongs to"
