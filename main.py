import PySimpleGUI as sg
import os.path
from object_wrapper import ObjectWrapper


# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("s3://healthqx-chc-cert-analytics-cloud/hqxmt/client/ibc/202109_all_01_006", size=(15, 1), key="bucket_name"),
        sg.In(size=(32, 1), enable_events=True, key="-FOLDER-"),
        sg.Button("Browse", size=(5, 1), key="-BROWSE-"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(32, 20), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
multi_line_column = [
    [sg.Multiline("Choose config file:", size=(40, 35), key="-MULTILINE-")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(multi_line_column),
    ]
]
# layout = [ [sg.Text('Enter your name')],       # Text input
#            [sg.InputText()],                   # Input box
#            [sg.Button('Ok'), sg.Button('Cancel')] ] # Buttons


sg.theme('Dark Blue 3')  # Add a touch of color
window = sg.Window('Demo', layout)  # Create the Window

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".json", ".config"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-LOA-":
        bucket_name = values["FOLDER"]
        ObjectWrapper.set_bucket_name(bucket_name)
        objectwrapper = ObjectWrapper()

        try:
            # Get list of files in folder
            file_list = objectwrapper.get_file_list()
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".json", ".config"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            sg.Window["-TOUT-"].update(filename)
            sg.Window["-IMAGE-"].update(filename=filename)

        except:
            pass

window.close()
# sg.Window(title="Hello World", layout=[[]], margins=(600, 350)).read()
# Create an event loop
# while True:
#     event, values = sg.Window.read('sself' )
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break

# sg.Window.close()
