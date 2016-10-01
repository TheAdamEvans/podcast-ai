import os
from subprocess import call, check_output

# phone must be in media transfer mode
# call(["adb", "usb"])
# adb shell ls '/sdcard/Android/data/'

SOUND_DIR = '/Users/adam/audio/freak/sound/'
PHONE_INTERNAL_DIR = '/sdcard/Android/data/com.bambuna.podcastaddict/files/podcast/Freakonomics Radio/'

def save_info_from(SOUND_DIR, PHONE_INTERNAL_DIR):    

    already_gotten = os.listdir(SOUND_DIR)

    output = check_output(['adb','shell','ls',PHONE_INTERNAL_DIR])
    filenames = output.split('\r\n')[:-1]
    
    for fn in filenames:
        if fn in already_gotten:
            print "Already got", fn
        else:
            call(['adb','pull',PHONE_INTERNAL_DIR+fn,SOUND_DIR+'.'])
            print "Copied", fn

save_info_from(SOUND_DIR, PHONE_INTERNAL_DIR)