import snowboydecoder
import signal

interrupted = False

MODEL = 'snowboy.umdl'

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted
    
def loadModel(model):
    global MODEL
    MODEL = model
    
def waitForWakeUp():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(MODEL, sensitivity=0.5)
    detector.start(detected_callback=detector.terminate(),
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    return True