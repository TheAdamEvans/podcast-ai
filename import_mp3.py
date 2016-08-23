import os
from subprocess import call, check_output

# phone must be in media transfer mode
# call(["adb", "usb"])

DATA_DIR = '/Users/adam/audio/data/'
SOUND_DIR = '/Users/adam/audio/sound/'
PHONE_INTERNAL_DIR = '/sdcard/Android/data/org.prx.talbot/files/'

def save_info_from(DATA_DIR, SOUND_DIR, PHONE_INTERNAL_DIR):    

    already_gotten = os.listdir(SOUND_DIR)

    output = check_output(['adb','shell','ls',PHONE_INTERNAL_DIR])
    filenames = output.split('\r\n')[:-1]
    
    for fn in filenames:
        if fn in already_gotten:
            print "Already got", fn
        else:
            call(['adb','pull','/sdcard/Android/data/org.prx.talbot/files/'+fn,SOUND_DIR+'.'])
            print "Copied", fn

save_info_from(DATA_DIR, SOUND_DIR, PHONE_INTERNAL_DIR)