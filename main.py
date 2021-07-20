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
button_names= ['Download video','Download Audio','Choose save path','Open save path','Enter Youtube video link','Get Description','Cancel']
layout = [
            [sg.Text(button_names[2]), sg.FolderBrowse(key="-IN-"), sg.Button(button_names[3])],
            [sg.Text(button_names[4]), sg.InputText()],
            [sg.Button(button_names[5])],
            [sg.Button(button_names[0]),sg.Button(button_names[1]),sg.Button(button_names[6])],
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
    elif event == (button_names[0]) and youtube_check(values):
        video = YouTube(values[0])
        all_resolutions = []
        all_fps = []
        for i in video.streams.filter(only_video=True):
            all_resolutions.append(str(i.resolution))
            all_fps.append(str(i.fps))
        sorted_all_fps = [el for el, _ in groupby(all_fps)]
        sorted_all_resolutions = [el for el, _ in groupby(all_resolutions)]
        fps_count = my_psg.popup_select(sorted_all_fps)
        res_count = my_psg.popup_select(sorted_all_resolutions)
        video.streams.filter(fps=int(fps_count), res=str(res_count), only_video=True).first().download(output_path=values["-IN-"])
        sg.popup('You downloaded: ', video.title)
    elif event == button_names[1] and youtube_check(values):
        video = YouTube(values[0])
        all_audio_rates = []
        for i in video.streams.filter(only_audio=True):
            all_audio_rates.append(str(i.abr))
        sorted_all_rates = [el for el, _ in groupby(all_audio_rates)]
        audio_rate_count = my_psg.popup_select(sorted_all_rates)
        print(audio_rate_count)
        video.streams.filter(only_audio=True, abr=str(audio_rate_count)).first().download(output_path=values["-IN-"])
    elif event == button_names[3]:
        os.startfile(path)
    elif event == button_names[5]:
        sg.popup_scrolled(YouTube(values[0]).description, title="Description", size=(60, 30)) if youtube_check(values) else sg.popup('Please enter the link first')
    else:
        sg.popup('This is not a Youtube link, please try again  ')
window.close()
