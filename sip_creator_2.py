import FreeSimpleGUI as sg
from funcs import *

vsc_theme = {'BACKGROUND': '#252525',
            'TEXT': '#7edcf0',
            'INPUT': '#181818',
            'TEXT_INPUT': '#5dd495',
            'SCROLL': '#252525',
            'BUTTON': ('#dcdca1', '#181818'),
            'PROGRESS': ('#dcdca1', '#181818'),
            'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

alt_background = '#181818'
medium_font = 'Courier 12 bold'
big_font = 'Courier 14 bold'
sg.set_options(font='Courier 12')
sg.theme_add_new('VSC Theme', vsc_theme)
sg.theme('VSC Theme')

layout = [[sg.Text('Project CSV:'), sg.Input(size=39, background_color=alt_background, key='-CSV_PATH-'), sg.FileBrowse(key='-FILE_BROWSE_BUTTON-')],
    [sg.Text('Project Folder:'), sg.Input(size=36, background_color=alt_background, key='-OUTPUT-'), sg.FolderBrowse(key='-FOLDER_BROWSE_BUTTON-')],
    [sg.Button('Generate SIPs', tooltip="LET'S GOOOOOOOOOO", font=big_font, key='-LETS_GOOOO-'), sg.ProgressBar(max_value=1, size=(28, 30), bar_color=('#ffaf5f', alt_background), key='-PROGRESS_BAR-'), sg.Button('About', key='-ABOUT-'), sg.Button('Exit', key='-EXIT-')],
    [sg.Text(expand_x=True, text_color='#ffaf5f', background_color=alt_background, key='-STATUS_BAR-')]
]

window = sg.Window('PAX/OPEX Workbench', layout, finalize=True, resizable=False)
window.set_min_size(window.size)
project_csv_inp = window['-CSV_PATH-']
project_csv_but = window['-FILE_BROWSE_BUTTON-']
project_dir_inp = window['-OUTPUT-']
project_dir_but = window['-FOLDER_BROWSE_BUTTON-']
lets_gooo = window['-LETS_GOOOO-']
progress_bar = window['-PROGRESS_BAR-']
status_bar = window['-STATUS_BAR-']

about_text = '''Created by: John Dewees
Version: 0.2
Last Updated: 2025-03-13
Email: john.dewees@rochester.edu'''

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '-EXIT-', 'Exit', 'Quit'):
        break    
    project_csv_value = values['-CSV_PATH-']
    project_dir_value = values['-OUTPUT-']
    window.refresh()
    if event == '-ABOUT-':
        sg.popup_ok(about_text, title='About PAX/OPEX Workbench')
    if event == '-LETS_GOOOO-':
        disable_all(window)
        progress_bar.update(bar_color=('#ffaf5f', alt_background))
        max_hand = open(project_csv_value, 'r')
        progress_bar.update(current_count = 0, max=len(max_hand.readlines())-1)
        max_hand.close()
        window.refresh()
        main_process(window, status_bar, project_csv_value, project_dir_value, progress_bar)
        progress_bar.update(bar_color=('#5dd495', alt_background))
        status_bar.update(value='All PAX objects generated and OPEX metadata created')
        enable_all(window)
window.close()