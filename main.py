import PySimpleGUI as sg
import re
from pytube import YouTube
import os
import my_psg
from itertools import groupby


def get_max_resolution(video):
    return video.streams.get_highest_resolution().resolution


def youtube_check(values):
    return re.search(r'\byoutube.com\b', values[0]) or re.search(r'\byoutu.be\b', values[0])


sg.theme('DarkGrey8')
all_resolutions = []
all_fps = []
layout = [
            [sg.Text('Choose save path'), sg.FolderBrowse(key="-IN-"), sg.Button('Open save path')],
            [sg.Text('Enter Youtube video link'), sg.InputText()],
            [sg.Button('Get Description')],
            [sg.Button('Download'), sg.Button('Cancel')],
            ]
# Create the Window
window = sg.Window('Youtube Downloader', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    path = values["-IN-"]
    path = os.path.realpath(path)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == ('Download') and youtube_check(values):
        video = YouTube(values[0])
        all_resolutions = []
        all_fps = []
        for i in video.streams.filter(only_video=True):
            if i.type == "video":
                all_resolutions.append(str(i.resolution))
                all_fps.append(str(i.fps))
        sorted_all_fps = [el for el, _ in groupby(all_fps)]
        sorted_all_resolutions = [el for el, _ in groupby(all_resolutions)]
        fps_count = my_psg.popup_select(sorted_all_fps)
        res_count = my_psg.popup_select(sorted_all_resolutions)
        video.streams.filter(fps=int(fps_count), res=str(res_count), only_video=True).first().download(output_path=values["-IN-"])
        sg.popup('You downloaded: ', video.title)
    elif event == 'Open save path':
        os.startfile(path)
    elif event == 'Get Description':
        sg.popup_scrolled(YouTube(values[0]).description, title="Description", size=(60, 30)) if youtube_check(values) else sg.popup('Please enter the link first')
    else:
        sg.popup('This is not a Youtube link, please try again  ')
window.close()
