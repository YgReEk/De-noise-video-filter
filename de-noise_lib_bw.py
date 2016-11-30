import cv2
import math
import numpy as np
import subprocess as sp

# import sentry system
from raven import Client

client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

# imported videofile
iaddr = r'C:\Users\Игорь\test2.avi'
cap = cv2.VideoCapture(iaddr)
ffmpeg_bin = "ffmpeg"  # on Linux ans Mac OS
ffmpeg_bin = "ffmpeg.exe"  # on Windows
# resolution we need
vwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
SameAsSource = (vwidth, vheight)
VGA = (640, 480)
qHD = (960, 540)
SVGA = (800, 600)
HD = (1280, 720)
XGAplus = (1152, 864)
HDplus = (1600, 900)
UXGA = (1600, 1200)
FullHD = (1920, 1080)
outres = VGA
# fps rate we need
fps = cap.get(cv2.CAP_PROP_FPS)
# define the codec, more fourcc codes there: http://www.fourcc.org/codecs.php
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# colored video and color rate
colorrate = 1

# search window size for filtering, more ws means more computation (recommended by author - 21)
if int((outres[0] // 60) % 2) == 0:
    ws = int(outres[0] // 60 + 1)
else:
    ws = int(outres[0] // 60)
# strength of filter (first fs for luminance noise, second for color noise; stronger filter -> less details)
fs = int(4)
hs = int(5)
# how many frames we take for denoising (this temporalWindowSize should be odd)
tws = int(5)
# target image to denoise index in range(tws)
itdi = int(tws // 2)

# sequence of filtered frames
sq = []
# sequence of 5 frames that will be used for denoising
img = []
# estimated denoising time in minutes ~ 1.09e^(0.003*x.res); better fits 8.31088e^(1.73277×MP), but less useful:
edt = 1.09 * math.exp(0.003 * outres[0])
# estimated memory use in Mb
# (based on empirical evidence equals 2 uncompressed 8-bit depth avi + ~30% for each hour of denoising)
emt = int((2 * outres[0] * outres[1] * colorrate * cap.get(cv2.CAP_PROP_FRAME_COUNT) + 0.3 * (edt / 60)) / 1024 / 1024)
# output video as VideoWriter object
oaddr = r'C:\Users\Игорь\output.avi'
out = cv2.VideoWriter(oaddr, fourcc, fps, outres, True)

command = [ffmpeg_bin,
            '-i', iaddr,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=2**23)

# read the source video into vid[]
vid = [cap.read()[1] for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))]

# free videofile
cap.release()

# convert all to grayscale
gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in vid]

# convert all to float64
gray = [np.float64(i) for i in gray]

# create a noise of variance 25
noise = np.random.randn(*gray[1].shape) * 10

# Add this noise to images
noisy = [i + noise for i in gray]

# Convert back to uint8
noisy = [np.uint8(np.clip(i, 0, 255)) for i in noisy]

for i in range(itdi):
    sq.append(cv2.resize(
        cv2.fastNlMeansDenoising(vid[i], None, fs, 7, ws),
        outres, 0, 0, interpolation=cv2.INTER_LINEAR))

for k in range(len(vid) - itdi * 2):
    img = [vid[k + 1] for i in range(tws)]
    dst = cv2.fastNlMeansDenoisingMulti(img, itdi, tws, None, fs, 7, ws)
    sq.append(cv2.resize(dst, outres, 0, 0, interpolation=cv2.INTER_LINEAR))

for i in range(itdi):
    sq.append(cv2.resize(
        cv2.fastNlMeansDenoising(noisy[len(vid) - itdi + i], None, fs, 7, ws),
        outres, 0, 0, interpolation=cv2.INTER_LINEAR))

# write the frame TODO write source audio into the videofile
for i in vid:
    out.write(i)

# free videofile
out.release()
cv2.destroyAllWindows()
