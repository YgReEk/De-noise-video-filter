import cv2
import lib_functions
import sys
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter.filedialog as tkFileDialog
import cv2
import shutil
import tempfile
import AboutForm
import AuthorForm
import HowToForm
import LicenseForm

from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

data = {}
ResolutionDict = dict(SameAsSource=(0, 0), VGA=(640, 480), qHD=(960, 540), SVGA=(800, 600), HD=(1280, 720),
                  XGAplus=(1152, 864), HDplus=(1600, 900), UXGA=(1600, 1200), FullHD=(1920, 1080))

data['video'] = False
data['colored'] = True
data['outres'] = ResolutionDict['qHD']
data['fs'] = 3
data['hs'] = 4
data['iaddr'] = r'resourses\test.png'
data['exaddr'] = r'resourses\test-denoised.png'

# initialized = lib_functions.init_denoising(data)
# data.clear()
#
# edt = initialized['edt']
# emt = initialized['emt']
#
# lib_functions.denoising(initialized)
# initialized.clear()

# TODO: Write controller for connecting Model (lib_functions) and View (*Form)


def Quit(ev):
    global root
    root.destroy()


def LoadFile(ev):
    fileaddr = str(tkFileDialog.Open(root, filetypes=[('Images', '.png'), ('Videos', '.avi')]).show())
    if fileaddr == '':
        return
    else:
        FileAddr.set(fileaddr)
        data['iaddr'] = fileaddr
        initialized = lib_functions.init_denoising(data)
        emt = str(initialized['emt'])
        EMT_show_text.set(emt + 'Mbs')
        edt = str(initialized['edt'])
        EDT_show_text.set(edt[:edt.rfind('.')+2] + ' mins')
        oaddr = initialized['oaddr']
        tdaddr = tempfile.NamedTemporaryFile().name + iaddr[iaddr.rfind('.'):]
        shutil.copyfile(oaddr, tdaddr)
        Img = cv2.imread(tdaddr)
        cv2.imwrite(tdaddr, cv2.resize(Img, (380, 214), 0, 0, interpolation=cv2.INTER_AREA))
        DemoisedPreview = PhotoImage(file=tdaddr)
        Den = Label(MainFrame)
        Den['image'] = DemoisedPreview


def CheckFile():
    inaddr = str(FileAddr)
    if inaddr[inaddr.rfind('.'):] == '.avi':
        return True
    elif inaddr[inaddr.rfind('.'):] == '.png':
        return False
    else:
        return


def setresolution(res):
    if res == 'Same as source':
        return ResolutionDict['SameAsSource']
    elif res == 'VGA (640*480)':
        return ResolutionDict['VGA']
    elif res == 'SVGA (800*600)':
        return ResolutionDict['SVGA']
    elif res == 'qHD (960*540)':
        return ResolutionDict['qHD']
    elif res == 'HD (1280*720)':
        return ResolutionDict['HD']
    elif res == 'XGA+ (1152*864)':
        return ResolutionDict['XGAplus']
    elif res == 'HD+ (1600*900)':
        return ResolutionDict['HDplus']
    elif res == 'UXGA (1600*1200)':
        return ResolutionDict['UXGA']
    elif res == 'FullHD (1920*1080)':
        return ResolutionDict['FullHD']
    else:
        return


def setfilterstrenght():
    return int(LFS.get())


def setfiltercolorstrenght():
    return int(CFS.get())


def setcolored():
    if check.instate(['alternate']):
        data['colored'] = True
    elif color:
        data['colored'] = True
    else:
        data['colored'] = False


def menurestorecolor():
    if messagebox.askyesno(message='Restore color flag to defaults?', icon='question', title='Restore'):
        data['colored'] = True


def menurestorefilterstrenght():
    if messagebox.askyesno(message='Restore filter strenght to defaults?', icon='question', title='Restore'):
        data['fs'] = 3


def menurestorefiltercolorstrenght():
    if messagebox.askyesno(message='Restore filter color strenght to defaults?', icon='question', title='Restore'):
        data['hs'] = 4


def Denoise(*args):
    data['video'] = CheckFile()
    data['colored'] = setcolored()
    data['outres'] = setresolution(Resolution.get())
    data['fs'] = setfilterstrenght()
    data['hs'] = setfiltercolorstrenght()
    data['iaddr'] = str(FileAddr.get())
    ProgressDenoising.start()
    initialized = lib_functions.init_denoising(data)
    lib_functions.denoising(initialized)
    data.clear()
    initialized.clear()
    ProgressDenoising.stop()


root = Tk()
icon = PhotoImage(file=r'C:\Users\Игорь\PycharmProjects\De-noise-video-filter\resourses\icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)
root.title('De-noise video filter')
root.option_add('*tearOff', FALSE)

MainFrame = Frame(root, height=460, width=800)
MainFrame.grid(column=0, row=0, padx=10, pady=10)

Default_fs_luminocity_label = Label(MainFrame, text='Default: 4')
Default_fs_luminocity_label.grid(column=0, row=9, sticky=(S, W), padx=6, pady=4)

FS_luminocity_label = Label(MainFrame, text='Filter luminosity strenght (from 1 to 30)')
FS_luminocity_label.grid(column=2, row=9, sticky=(S, E), padx=6, pady=4)

Default_fs_color_label = Label(MainFrame, text='Default: 5')
Default_fs_color_label.grid(column=3, row=9, sticky=(S, W), padx=6, pady=4)

FS_color_label = Label(MainFrame, text='Filter color strenght (from 1 to 30)')
FS_color_label.grid(column=5, row=9, sticky=(S, E), padx=6, pady=4)

Open_file_label = Label(MainFrame, text='Open file: ')
Open_file_label.grid(column=1, row=10, sticky=(S, E), padx=2, pady=6)

EMT_label = Label(MainFrame, text='Estimated memory use: ')
EMT_label.grid(column=0, row=6, sticky=(S, W), padx=6, pady=4)

EDT_label = Label(MainFrame, text='Estimated denoising time: ')
EDT_label.grid(column=3, row=6, sticky=(S, W), padx=6, pady=4)

EMT_show_text = StringVar()
EMT_show = Label(MainFrame)
EMT_show['textvariable'] = EMT_show_text
EMT_show.grid(column=2, row=6, sticky=(S, E), padx=6, pady=4)

EDT_show_text = StringVar()
EDT_show = Label(MainFrame)
EDT_show['textvariable'] = EDT_show_text
EDT_show.grid(column=5, row=6, sticky=(S, E), padx=6, pady=4)

color = bool()
check = Checkbutton(MainFrame, text='GrayScale', variable=color, onvalue=False, offvalue=True)
check.grid(column=0, row=7, sticky=(S, W), padx=6, pady=6)

iaddr = data['iaddr']
toaddr = tempfile.NamedTemporaryFile().name + iaddr[iaddr.rfind('.'):]
shutil.copyfile(iaddr, toaddr)
Img = cv2.imread(toaddr)
cv2.imwrite(toaddr, cv2.resize(Img, (380, 214), 0, 0, interpolation=cv2.INTER_AREA))
OriginalPreview = PhotoImage(file=toaddr)
Orig = Label(MainFrame)
Orig['image'] = OriginalPreview
Orig.grid(column=0, row=0, columnspan=3, rowspan=6, sticky=(N, S, E, W), padx=6, pady=6)

oaddr = data['exaddr']
tdaddr = tempfile.NamedTemporaryFile().name + iaddr[iaddr.rfind('.'):]
shutil.copyfile(oaddr, tdaddr)
Img = cv2.imread(tdaddr)
cv2.imwrite(tdaddr, cv2.resize(Img, (380, 214), 0, 0, interpolation=cv2.INTER_AREA))
DemoisedPreview = PhotoImage(file=tdaddr)
Den = Label(MainFrame)
Den['image'] = DemoisedPreview
Den.grid(column=3, row=0, columnspan=3, rowspan=6, sticky=(N, S, E, W), padx=6, pady=6)

LFS = Scale(MainFrame, orient=HORIZONTAL, from_=1, to=30)
LFS.set(4)
LFS.grid(column=0, row=8, columnspan=3, sticky=(N, S, E, W), padx=6, pady=2)

CFS = Scale(MainFrame, orient=HORIZONTAL, from_=1, to=30)
CFS.set(5)
CFS.grid(column=3, row=8, columnspan=3, sticky=(N, S, E, W), padx=6, pady=2)

FileAddr = StringVar()
InputAdress = Entry(MainFrame, textvariable=FileAddr)
InputAdress.grid(column=2, row=10, columnspan=3, sticky=(N, S, E, W), padx=6, pady=6)

FileButton = Button(MainFrame, text='Browse')
FileButton.grid(column=0, row=10, sticky=(S, W), padx=6, pady=6)
FileButton.bind("<Button-1>", LoadFile)

DenoiseButton = Button(MainFrame, text='Denoise it!')
DenoiseButton.grid(column=5, row=10, sticky=(S, E), padx=6, pady=6)
DenoiseButton.bind("<Button-1>", Denoise)

ProgressDenoising = Progressbar(MainFrame, orient=HORIZONTAL, mode='indeterminate')
ProgressDenoising.grid(column=1, row=7, columnspan=4, sticky=(N, S, E, W), padx=6, pady=6)

Resolution = Combobox(MainFrame,
                      values=['Same as source', 'VGA (640*480)', 'SVGA (800*600)', 'qHD (960*540)', 'HD (1280*720)',
                              'XGA+ (1152*864)', 'HD+ (1600*900)', 'UXGA (1600*1200)', 'FullHD (1920*1080)'])
Resolution.set('Same as source')
Resolution.grid(column=5, row=7, sticky=(S, E), padx=6, pady=6)

menubar = Menu(root)

menu_file = Menu(menubar, tearoff=0)
menu_file.add_command(label='Open...', command=LoadFile)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=root.quit)
menubar.add_cascade(menu=menu_file, label='File')

menu_edit = Menu(menubar, tearoff=0)
menu_edit.add_command(label='Colored', command=menurestorecolor)
menu_edit.add_command(label='Set filter luminosity strenght', command=menurestorefilterstrenght)
menu_edit.add_command(label='Filter color strenght', command=menurestorefiltercolorstrenght)

menu_res = Menu(menu_edit, tearoff=0)
menu_res.add_command(label='Same as source', command=setresolution('Same as source'))
menu_res.add_command(label='VGA (640*480)', command=setresolution('VGA (640*480)'))
menu_res.add_command(label='SVGA (800*600)', command=setresolution('SVGA (800*600)'))
menu_res.add_command(label='qHD (960*540)', command=setresolution('qHD (960*540)'))
menu_res.add_command(label='HD (1280*720)', command=setresolution('HD (1280*720)'))
menu_res.add_command(label='XGA+ (1152*864)', command=setresolution('XGA+ (1152*864)'))
menu_res.add_command(label='HD+ (1600*900)', command=setresolution('HD+ (1600*900)'))
menu_res.add_command(label='UXGA (1600*1200)', command=setresolution('UXGA (1600*1200)'))
menu_res.add_command(label='FullHD (1920*1080)', command=setresolution('FullHD (1920*1080)'))

menubar.add_cascade(menu=menu_edit, label='Edit')
menu_edit.add_cascade(menu=menu_res, label='Resolution')

menu_about = Menu(menubar, tearoff=0)
menu_about.add_command(label='License', command=LicenseForm.init)
menu_about.add_command(label='Author', command=AuthorForm.init)
menu_about.add_command(label='About', command=AboutForm.init)
menu_about.add_command(label='HowTo:', command=HowToForm.init)
menubar.add_cascade(menu=menu_about, label='About')

root.config(menu=menubar)
root.mainloop()
