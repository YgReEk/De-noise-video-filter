# De-noise videos filter is a python module / program that can be used for reducing noise level in videos or images
#
# Copyright © 2016 Nemikhin Igor. All rights reserved. Licensed under GNU GPLv3.
# Author Nemikhin Igor.
# This program is free software: you can redistribute it and / or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses/
# Source code can be found there: https://github.com/YgReEk/De-noise-video-filter
# Project is using OpenCV 3, which license can be found there: http://opencv.org/license.html

# Warning! Algorithm used in program very hard computationally and needs lots of time and free memory, so be patient.
# Dependency on the resolution is exponentially: ~8.31088e^(1.73277×MP)

# import OpenCV 3, math, numpy modules and some for temporary files
import cv2
import math
import shutil
import tempfile
# yes, we don't use it directly, but OpenCV is based on it and it is recommended to import it also
import numpy as np

# import sentry system
from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')


def init_denoising(data):
    # defaults:
    # data['video'] = True
    # data['colored'] = True
    # data['outres'] = Resolution['HD']
    # data['fs'] = 4
    # data['hs'] = 5
    # data['iaddr'] = r'C:\Users\Игорь\test.png'

    initialized = data.copy()

    if initialized['colored']:
        # one bite for one rgb chanel
        colorrate = 3
    else:
        # and one for grayscale
        colorrate = 1

    # define input address and output one, in the same directory
    iaddr = initialized['iaddr']
    initialized['oaddr'] = iaddr[:iaddr.rfind('.')] + '-denoised' + iaddr[iaddr.rfind('.'):]

    # imported image/videofile
    if initialized['video']:
        # define mostly all variables that'll be used in video denoising
        cap = cv2.VideoCapture(iaddr)
        # resolution of video
        vwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        vheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # fps rate we need
        fps = cap.get(cv2.CAP_PROP_FPS)
        # define the codec, more fourcc codes there: http://www.fourcc.org/codecs.php
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # how many frames video have; needed to time and memory use estimation
        num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # sequence of filtered frames
        initialized['sq'] = []
        # sequence of unfiltered frames (input video)
        initialized['vid'] = []
        # how many frames we take for denoising (this temporalWindowSize should be odd)
        initialized['tws'] = int(5)
        # target image to denoise index in range(tws)
        initialized['itdi'] = int(initialized['tws'] // 2)
        # sequence of tws frames that will be used for denoising
        initialized['l_tws'] = []
    else:  # same to images denoising; tempfile needed due to ugly imread's support of unicode
        # make local temporary copy of image
        initialized['taddr'] = tempfile.NamedTemporaryFile().name + iaddr[iaddr.rfind('.'):]
        shutil.copyfile(iaddr, initialized['taddr'])
        if initialized['colored']:
            initialized['img'] = cv2.imread(initialized['taddr'])
        else:   # argument 0 after address allows us to use grayscale image instead of coloured
            initialized['img'] = cv2.imread(initialized['taddr'], 0)
        # resolution of image
        vheight = initialized['img'].shape[0]
        vwidth = initialized['img'].shape[1]
        # yes, we know, that single image consists of single frame, but we need that variable...
        num_frames = 1

    # resolution we need
    if initialized['outres'] == (0, 0):
        same_as_source = (vwidth, vheight)
        initialized['outres'] = same_as_source

    # search window size for filtering, more ws means more computation (recommended by author - 21)
    if int((initialized['outres'][0] // 60) % 2) == 0:
        initialized['ws'] = int(initialized['outres'][0] // 60 + 1)
    else:
        initialized['ws'] = int(initialized['outres'][0] // 60)

    # template patch size (# 7 is recommended size in pixels that is used to compute weights (should be odd))
    if int(initialized['outres'][0]) < 1000:
        initialized['tps'] = int(5)
    elif int(initialized['outres'][0]) > 1600:
        initialized['tps'] = int(9)
    else:
        initialized['tps'] = int(7)

    # estimated denoising time in minutes ~ 1.09e^(0.003*x.res); better fits 8.31088e^(1.73277×MP), but less useful:
    initialized['edt'] = 1.09 * math.exp(0.003 * initialized['outres'][0])
    # estimated memory use in Mb
    # (based on empirical evidence equals 2 uncompressed 8-bit depth avi/png + ~30% for each hour of denoising)
    initialized['emt'] = int((2 * initialized['outres'][0] * initialized['outres'][1] * colorrate * num_frames +
                              0.3 * (initialized['edt'] / 60)) / 1024 / 1024)

    if initialized['video']:
        # output video as VideoWriter object
        initialized['out'] = cv2.VideoWriter(initialized['oaddr'], fourcc, fps, initialized['outres'], True)
        # read the source video into vid[]
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if initialized['colored']:
                    initialized['vid'].append(cv2.resize(
                        frame, initialized['outres'], 0, 0, interpolation=cv2.INTER_AREA))
                else:
                    # TODO: Make grayscale images working not like ~hit.
                    # all the code below is for grayscale images and it's commented due to unworking yet
                    # g_frame = np.asarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dtype=np.uint8)
                    # k_frame = np.ndarray(shape=(len(g_frame), len(g_frame[0]), 1), dtype=np.uint8)
                    # for k in range(len(g_frame)):
                    #     for l in range(len(g_frame[k])):
                    #         k_frame[k][l][0] = g_frame[k][l]
                    initialized['vid'].append(cv2.resize(
                        frame, initialized['outres'], 0, 0, interpolation=cv2.INTER_AREA))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # free videofile
        cap.release()
    else:
        initialized['img'] = cv2.resize(initialized['img'], initialized['outres'], 0, 0, interpolation=cv2.INTER_AREA)

    return initialized


def denoising_video_colored(itdi, sq, vid, fs, hs, tps, ws, tws):
    # add unfiltered first itdi - 1 frames and resize it, just for be sure all is ok
    for i in range(itdi):
        sq.append(cv2.fastNlMeansDenoisingColored(vid[i], None, fs, hs, tps, ws))

    # denoise all possible frames in itdi range considering all the tws frames
    for k in range(len(vid) - itdi * 2):
        # create a list of temporalWindowSize frames
        l_tws = [vid[k + 1] for i in range(tws)]

        # 7 there is recommended size in pixels of the template patch that is used to compute weights (should be odd)
        # more method syntax details could be found there:
        # https://shimat.github.io/opencvsharp/html/d12fad98-53b0-c14a-6496-5c52ee633019.htm
        sq.append(cv2.fastNlMeansDenoisingColoredMulti(l_tws, itdi, tws, None, fs, hs, tps, ws))

        # there is a probability to use CUDA, but it'll be less accurate: there is no cuda method applicable to video
        # More here: http://docs.opencv.org/trunk/d1/d79/group__photo__denoise.html#ga21abc1c8b0e15f78cd3eff672cb6c476

        # merge all filtered images into sequence changing resolution to needed
        # more about resizing: http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize

    # add unfiltered last itdi - 1 frames
    for i in range(itdi):
        sq.append(cv2.fastNlMeansDenoisingColored(vid[len(vid) - itdi + i], None, fs, hs, tps, ws))


def denoising_video_grayscale(itdi, sq, vid, fs, tps, ws, tws):
    for i in range(itdi):
        sq.append(cv2.fastNlMeansDenoising(vid[i], None, fs, tps, ws))

    for k in range(len(vid) - itdi * 2):
        l_tws = [vid[k + 1] for i in range(tws)]
        sq.append(cv2.fastNlMeansDenoisingMulti(l_tws, itdi, tws, None, fs, tps, ws))

    for i in range(itdi):
        sq.append(cv2.fastNlMeansDenoising(vid[len(vid) - itdi + i], None, fs, tps, ws))


def denoising_image_colored(taddr, img, fs, hs, tps, ws):
    cv2.imwrite(taddr, cv2.fastNlMeansDenoisingColored(img, None, fs, hs, tps, ws))


def denoising_image_grayscale(taddr, img, fs, tps, ws):
    cv2.imwrite(taddr, cv2.fastNlMeansDenoising(img, None, fs, tps, ws))


def denoising(initialized):
    # parse initialized variables
    ws = initialized['ws']
    fs = initialized['fs']
    hs = initialized['hs']
    tps = initialized['tps']
    if initialized['video']:
        itdi = initialized['itdi']
        sq = initialized['sq']
        tws = initialized['tws']
        vid = initialized['vid']
        out = initialized['out']
        if initialized['colored']:
            denoising_video_colored(itdi, sq, vid, fs, hs, tps, ws, tws)
        else:   # comments for grayscale denoising mostly are the same, so I'd not repeat them
            denoising_video_grayscale(itdi, sq, vid, fs, tps, ws, tws)
        # write the frame TODO write source audio into the videofile
        # (OpenCV can't write audio and FFMpeg doesn't work properly :(
        for i in vid:
            out.write(i)
        # free videofile
        out.release()

    else:   # it's image denoising time! Comment are just like in the video denosing, so look above if you need them
        oaddr = initialized['oaddr']
        taddr = initialized['taddr']
        img = initialized['img']
        if initialized['colored']:
            denoising_image_colored(taddr, img, fs, hs, tps, ws)
        else:
            denoising_image_grayscale(taddr, img, fs, tps, ws)
        # copy denoised image from temporary file to original destination and then free temporary file
        shutil.copyfile(taddr, oaddr)
        tempfile.NamedTemporaryFile().close()

    # free all the memory used by OpenCV processes
    cv2.destroyAllWindows()
