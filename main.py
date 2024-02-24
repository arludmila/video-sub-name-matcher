import PySimpleGUI as sg
import os
import shutil


# Function to check if a file has a valid video format
def is_valid_video(filename):
    valid_formats = ['.mp4', '.avi', '.mkv']
    ext = os.path.splitext(filename)[1]
    return ext.lower() in valid_formats


# Function to check if a file has a valid subtitles format
def is_valid_subtitles(filename):
    valid_formats = ['.srt']
    ext = os.path.splitext(filename)[1]
    return ext.lower() in valid_formats


# Window layout
layout = [[sg.Text('Select video file and subtitles file to match')],
          [sg.Text('Video file', size=(10, 1)), sg.Input(key='-VIDEO-'),
           sg.FileBrowse(file_types=(("Video Files", "*.mp4;*.avi;*.mkv"),))],
          [sg.Text('Subtitles file', size=(10, 1)), sg.Input(key='-SUBTITLES-'),
           sg.FileBrowse(file_types=(("Subtitle Files", "*.srt"),))],
          [sg.Submit(button_color=('white', 'green')), sg.Cancel(button_color=('white', 'red'))],
          [sg.Text('Output:', size=(10, 1))],
          [sg.Multiline(size=(60, 10), key='-OUTPUT-', autoscroll=True)]]

# Create the Window
window = sg.Window('Match sub with video', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == 'Submit':
        video_file = values['-VIDEO-']
        sub_file = values['-SUBTITLES-']
        if video_file.strip() == '' or sub_file.strip() == '':
            window['-OUTPUT-'].print('Please choose both a video file and a subtitles file.')
            continue
        elif not is_valid_video(video_file):
            window['-OUTPUT-'].print('Please choose a valid video file (MP4, AVI, MKV).')
            continue
        elif not is_valid_subtitles(sub_file):
            window['-OUTPUT-'].print('Please choose a valid subtitles file (SRT).')
            continue

        # If both video and subtitles files are valid, proceed with copying
        video_path = os.path.dirname(video_file)
        video_name = os.path.basename(video_file)
        sub_name = os.path.basename(sub_file)
        sub_copy_name = os.path.splitext(video_name)[0] + '.srt'
        sub_copy_path = os.path.join(video_path, sub_copy_name)

        # Check if the .srt file already exists
        if os.path.exists(sub_copy_path):
            # If it exists, show a popup with options to overwrite or leave original
            overwrite_choice = sg.popup_yes_no(
                'An .srt file with the same name already exists.\nDo you want to overwrite it?',
                icon='warning'
            )

            if overwrite_choice == 'Yes':
                # If the user chooses to overwrite, remove the existing .srt file
                os.remove(sub_copy_path)
            else:
                # If the user chooses not to overwrite, skip copying the subtitles file
                window['-OUTPUT-'].print('Subtitles file was not copied. Original file remains.')
                continue

        shutil.copy(sub_file, sub_copy_path)
        window['-OUTPUT-'].print(f'Subtitles copied successfully to {sub_copy_path}')

        # Reset the input fields
        window['-VIDEO-'].update('')
        window['-SUBTITLES-'].update('')

window.close()
