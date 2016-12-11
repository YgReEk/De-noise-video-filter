import cv2
import lib_functions
import sys
import PyQt5
from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

data = {}
Resolution = dict(SameAsSource=(0, 0), VGA=(640, 480), qHD=(960, 540), SVGA=(800, 600), HD=(1280, 720),
                  XGAplus=(1152, 864), HDplus=(1600, 900), UXGA=(1600, 1200), FullHD=(1920, 1080))

data['video'] = True
data['colored'] = True
data['outres'] = Resolution['qHD']
data['fs'] = 3
data['hs'] = 4
data['iaddr'] = r'C:\Users\Игорь\test2.avi'

initialized = lib_functions.init_denoising(data)
data.clear()

edt = initialized['edt']
emt = initialized['emt']

lib_functions.denoising(initialized)
initialized.clear()

# TODO: Write controller for connecting Model (lib_functions) and View (*Form)
