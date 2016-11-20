# Copyright © 2016 Nemikhin Igor. All rights reserved. Licensed under GNU GPLv3.
# Author Nemikhin Igor.
# License: http://www.gnu.org/licenses/gpl.html
# Source code can be found there: https://github.com/YgReEk/De-noise-video-filter
# Project is using OpenCV 3, which license can be found there: http://opencv.org/license.html

# Warning! Algorithm used in program very hard computationally and needs lots of time and free memory, so be patient.
# Denoising of 11-sec video takes ~5 hours 10 minutes on Windows 8.1 x64, Anaconda 4.2, OpenCV 3.1, PyCharm 2016.2.3,
# Intel Haswell 4771, 16 Gb DDR3. Average CPU load ~90-100%, max memory usage ~3.9 Gb, usual priority process.
# That gives ~0.01527 frames/second (284 frames)

# import OpenCV 3
import cv2

# imported videofile
iaddr = r'C:\Users\Игорь\test.avi'
cap = cv2.VideoCapture(iaddr)
# resolution we need
vwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
outres = (vwidth, vheight)
# fps rate we need
fps = cap.get(cv2.CAP_PROP_FPS)
# define the codec, more fourcc codes there: http://www.fourcc.org/codecs.php
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# search window size for filtering, more ws means more computation (recommended by author - 21)
if int(vwidth % 60) == 0:
    ws = vwidth // 60 + 1
else:
    ws = vwidth // 60
# strength of filter (first fs in filter parameters is for luminance noise, second for color noise)
fs = 3
# how many frames we take for denoising (this temporalWindowSize should be odd)
tws = 5
# target image to denoise index in range(tws)
itdi = tws // 2

# sequence of filtered frames
sq = []
# sequence of unfiltered frames (input video)
vid = []
# output video as VideoWriter object
oaddr = r'C:\Users\Игорь\output.avi'
out = cv2.VideoWriter(oaddr, fourcc, fps, outres, True)

# read the source video into vid[]
while cap.isOpened():
    ret, frame = cap.read()
    if ret==True:
        vid.append(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# free videofile
cap.release()

# add unfiltered first itdi - 1 frames
for i in range(itdi):
    sq.append(cv2.resize(vid[i], outres, 0, 0, interpolation=cv2.INTER_LINEAR))

for k in range(len(vid) - itdi  * 2):
    # create a list of temporalWindowSize frames
    img = [vid[k + 1] for i in range(tws)]

    # denoise itdi frame considering all the tws frames
    # 7 there is recommended size in pixels of the template patch that is used to compute weights (should be odd)

    # more method syntax details could be found there:
    # https://shimat.github.io/opencvsharp/html/d12fad98-53b0-c14a-6496-5c52ee633019.htm
    dst = cv2.fastNlMeansDenoisingColoredMulti(img, itdi, tws, None, fs, fs, 7, ws)

    # there is a probability to use CUDA, but it'll be less accurate: there is no cuda method applicable to video
    # More here: http://docs.opencv.org/trunk/d1/d79/group__photo__denoise.html#ga21abc1c8b0e15f78cd3eff672cb6c476

    # merge all filtered images into sequence changing resolution to needed
    # more about resizing: http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
    sq.append(cv2.resize(dst, outres, 0, 0, interpolation=cv2.INTER_LINEAR))

# add unfiltered last itdi frames
for i in range(itdi):
    sq.append(cv2.resize(vid[len(vid) - itdi + i], outres, 0, 0, interpolation=cv2.INTER_LINEAR))

# write the frame TODO write source audio into the videofile
for i in sq:
    out.write(i)

# free videofile
out.release()
cv2.destroyAllWindows()
