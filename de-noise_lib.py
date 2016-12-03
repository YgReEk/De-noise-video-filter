# Copyright © 2016 Nemikhin Igor. All rights reserved. Licensed under GNU GPLv3.
# Author Nemikhin Igor.
# License: http://www.gnu.org/licenses/gpl.html
# Source code can be found there: https://github.com/YgReEk/De-noise-video-filter
# Project is using OpenCV 3, which license can be found there: http://opencv.org/license.html

# Warning! Algorithm used in program very hard computationally and needs lots of time and free memory, so be patient.
# Dependency on the resolution is exponentially: ~8.31088e^(1.73277×MP)

# import OpenCV 3, math and numpy modules
import cv2
import math
import numpy as np
import shutil
import tempfile

# import sentry system
from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

# video/image
video = False
# colored video/image and color rate
colored = True
if colored is True:
    colorrate = 3
else:
    colorrate = 1

# define input address and output one, in the same directory
iaddr = r'C:\Users\Игорь\test.png'
oaddr = iaddr[:iaddr.rfind('\\')] + '\\' + 'output' + iaddr[iaddr.rfind('.'):]

# imported image/videofile
if video is True:
    cap = cv2.VideoCapture(iaddr)
    vwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps rate we need
    fps = cap.get(cv2.CAP_PROP_FPS)
    # define the codec, more fourcc codes there: http://www.fourcc.org/codecs.php
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # sequence of filtered frames
    sq = []
    # sequence of unfiltered frames (input video)
    vid = []
    # how many frames we take for denoising (this temporalWindowSize should be odd)
    tws = int(5)
    # target image to denoise index in range(tws)
    itdi = int(tws // 2)
    # sequence of tws frames that will be used for denoising
    l_tws = []
else:  # WARNING: imread works ugly with unicode
    taddr = tempfile.NamedTemporaryFile().name
    shutil.copyfile(iaddr, taddr)
    if colored is True:
        img = cv2.imread(taddr)
    else:
        img = cv2.imread(taddr, 0)
    vheight = img.shape[0]
    vwidth = img.shape[1]
    num_frames = 1

# resolution we need
SameAsSource = (vwidth, vheight)
VGA = (640, 480)
qHD = (960, 540)
SVGA = (800, 600)
HD = (1280, 720)
XGAplus = (1152, 864)
HDplus = (1600, 900)
UXGA = (1600, 1200)
FullHD = (1920, 1080)
outres = SameAsSource

# search window size for filtering, more ws means more computation (recommended by author - 21)
if int((outres[0] // 60) % 2) == 0:
    ws = int(outres[0] // 60 + 1)
else:
    ws = int(outres[0] // 60)
# strength of filter (first fs for luminance noise, second for color noise; stronger filter -> less details)
fs = int(4)
hs = int(5)

# estimated denoising time in minutes ~ 1.09e^(0.003*x.res); better fits 8.31088e^(1.73277×MP), but less useful:
edt = 1.09 * math.exp(0.003 * outres[0])
# estimated memory use in Mb
# (based on empirical evidence equals 2 uncompressed 8-bit depth avi/png + ~30% for each hour of denoising)
emt = int((2 * outres[0] * outres[1] * colorrate * num_frames + 0.3 * (edt / 60)) / 1024 / 1024)

if video is True:
    # output video as VideoWriter object
    out = cv2.VideoWriter(oaddr, fourcc, fps, outres, True)
    # read the source video into vid[]
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            if colored is True:
                vid.append(cv2.resize(frame, outres, 0, 0, interpolation=cv2.INTER_AREA))
            else:
                # TODO: Make grayscale images working not like ~hit.
                # g_frame = np.asarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dtype=np.uint8)
                # k_frame = np.ndarray(shape=(len(g_frame), len(g_frame[0]), 1), dtype=np.uint8)
                # for k in range(len(g_frame)):
                #     for l in range(len(g_frame[k])):
                #         k_frame[k][l][0] = g_frame[k][l]
                vid.append(cv2.resize(frame, outres, 0, 0, interpolation=cv2.INTER_AREA))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # free videofile
    cap.release()

if video is True:
    if colored:
        # add unfiltered first itdi - 1 frames
        for i in range(itdi):
            sq.append(cv2.resize(
                cv2.fastNlMeansDenoisingColored(vid[i], None, fs, hs, 7, ws),
                outres, 0, 0, interpolation=cv2.INTER_LINEAR))

        for k in range(len(vid) - itdi * 2):
            # create a list of temporalWindowSize frames
            l_tws = [vid[k + 1] for i in range(tws)]

        # denoise itdi frame considering all the tws frames
        # 7 there is recommended size in pixels of the template patch that is used to compute weights (should be odd)

        # more method syntax details could be found there:
        # https://shimat.github.io/opencvsharp/html/d12fad98-53b0-c14a-6496-5c52ee633019.htm
            dst = cv2.fastNlMeansDenoisingColoredMulti(l_tws, itdi, tws, None, fs, hs, 7, ws)

        # there is a probability to use CUDA, but it'll be less accurate: there is no cuda method applicable to video
        # More here: http://docs.opencv.org/trunk/d1/d79/group__photo__denoise.html#ga21abc1c8b0e15f78cd3eff672cb6c476

        # merge all filtered images into sequence changing resolution to needed
        # more about resizing: http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
            sq.append(cv2.resize(dst, outres, 0, 0, interpolation=cv2.INTER_LINEAR))

        # add unfiltered last itdi - 1 frames
        for i in range(itdi):
            sq.append(cv2.resize(
                cv2.fastNlMeansDenoisingColored(vid[len(vid) - itdi + i], None, fs, hs, 7, ws),
                outres, 0, 0, interpolation=cv2.INTER_LINEAR))

    else:   # comments are the same, so I'd not repeat them
        for i in range(itdi):
            sq.append(cv2.resize(
                cv2.fastNlMeansDenoising(vid[i], None, fs, 7, ws),
                outres, 0, 0, interpolation=cv2.INTER_LINEAR))

        for k in range(len(vid) - itdi * 2):
            l_tws = [vid[k + 1] for i in range(tws)]
            dst = cv2.fastNlMeansDenoisingMulti(l_tws, itdi, tws, None, fs, 7, ws)
            sq.append(cv2.resize(dst, outres, 0, 0, interpolation=cv2.INTER_LINEAR))

        for i in range(itdi):
            sq.append(cv2.resize(
                cv2.fastNlMeansDenoising(vid[len(vid) - itdi + i], None, fs, 7, ws),
                outres, 0, 0, interpolation=cv2.INTER_LINEAR))

    # write the frame TODO write source audio into the videofile
    for i in vid:
        out.write(i)

    # free videofile
    out.release()
else:
    if colored is True:
        cv2.imwrite(oaddr, cv2.resize(
            cv2.fastNlMeansDenoisingColored(img, None, fs, hs, 7, ws),
            outres, 0, 0, interpolation=cv2.INTER_LINEAR))
    else:
        cv2.imwrite(oaddr, cv2.resize(
            cv2.fastNlMeansDenoising(img, None, fs, 7, ws),
            outres, 0, 0, interpolation=cv2.INTER_LINEAR))
    tempfile.NamedTemporaryFile().close()
cv2.destroyAllWindows()
