import PySimpleGUI as sg
from file_operations import convert_string_to_part_pages, convert_txt_file_to_string, convert_string_to_array, move_files_to_directories
from pdf_operations import add_metadata, split_score_by_bookmarks, split_score_by_pages

# Misc
sg.theme("TealMono")
default_parts = convert_txt_file_to_string('parts_default.txt')
help_text = convert_txt_file_to_string('help.txt')

# Fonts
h1 = ("Helvetica", 36)
h2 = ("Helvetica", 18)
h3 = ("Helvetica", 14)
body = ("Helvetica", 12)
button_font = ("Helvetica", 18)

# Elements
submit = sg.Button("Submit", font=button_font)
reset = sg.Button("Reset", font=button_font)
help = sg.Button("?",font=button_font)
form_buttons = [sg.HorizontalSeparator(pad=20, color=(173, 204, 218)), reset, sg.HorizontalSeparator(color=(173, 204, 218)), submit, sg.HorizontalSeparator(pad=(160,0), color=(173, 204, 218)), help,  sg.HorizontalSeparator(pad=(1,0), color=(173, 204, 218))]
header = [sg.Push(), sg.Text("Score Splitter", font=h1), sg.Push()]
input_output_file = [sg.Text("Input/Output", font=h2)]
score_title = [sg.Text("Score:", font=h3)]
score_browse = [sg.Input(key="score", font=body), sg.FileBrowse()]
output_title = [sg.Text("Output Directory:", font=h3)]
output_browse = [sg.Input(key="output", font=body), sg.FolderBrowse()]
meta_title = [sg.Text("Metadata", font=h2)]
title_title = [(sg.Text("Title:", font=h3))]
title_input = [sg.Input(key="title", font=body)]
composer_title = [sg.Text("Composer/Arranger:", font=h3)]
composer_input = [sg.Input(key="composer", font=body)]
style_title = [sg.Text("Style:", font=h3)]
style_input = [sg.Input(key="style", font=body)]
parts_input_title = [sg.Text("Parts", font=h2)]
parts_input = [sg.Multiline(default_parts, size=(40, 20), font=body, key="part_names")]
output_checkbox = [sg.Checkbox('Output to individual part folders',font=h3, key='checkbox', default=True)]
split_setting = [sg.Text('Split by'), sg.Radio('Bookmarks', default=True, key='split_bookmarks', group_id=1), sg.Radio('Pages', key='split_pages', default=False, group_id=1)]

col1 = [
    input_output_file,
    score_title,
    score_browse,
    output_title,
    output_browse,
    output_checkbox,
    meta_title,
    title_title,
    title_input,
    composer_title,
    composer_input,
    style_title,
    style_input,
]

col2 = [parts_input_title, parts_input, split_setting]

# Create Layout
layout = [header, [sg.Push(), sg.Column(col1), sg.Column(col2), sg.Push()], [sg.VerticalSeparator(pad=(0,10))], form_buttons]

# Create the Window
window = sg.Window("Score Splitter", layout, size=(800, 500))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "?":
        sg.popup_scrolled(help_text, title='Score Splitter Instructions',font=h3, size=(50,10))
    if event == "Reset":
        window["score"].update("")
        window["title"].update("")
        window["composer"].update("")
        window["style"].update("")
        window['part_names'].update(default_parts)
    if event == "Submit":
        # Get data from form
        score_path = values["score"]
        output_path = values["output"]
        title = values["title"].strip()
        author = values["composer"].strip()
        subject = values["style"].strip()
        score_metadata = {"/Title": title, "/Author": author, "/Subject": subject}
        parts = convert_string_to_array(values['part_names']) if values['split_bookmarks'] == True else convert_string_to_part_pages(values['part_names']).keys()

        # Get part names & final directory paths
        part_folder_directories = [f"{output_path}/{part}" for part in parts]
        part_file_paths = [f"{output_path}/{title} - {part}.pdf" for part in parts]

        # Add metadata to the score & output to directory
        add_metadata(score_path, f'{output_path}/Complete Sets' if values['checkbox'] == True else output_path, score_metadata)
        

        # Split score into parts
        if values['split_bookmarks'] == True:
            split_score_by_bookmarks(score_path, parts, score_metadata, output_path)
        else:
            split_score_by_pages(score_path, convert_string_to_part_pages(values['part_names']), score_metadata, output_path)

        # Move files to directories
        if values['checkbox'] == True:
            move_files_to_directories(part_file_paths, part_folder_directories)

    if event == sg.WIN_CLOSED: 
        break


window.close()
