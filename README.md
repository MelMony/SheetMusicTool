# Score Splitter

A simple python GUI that helps you digitise your ensemble sheet music collection.

## Description

Score Splitter 0.1.0 will take your pdf score (that has bookmarks on the first page of each new part/score) and split it by bookmarks into the part names outlined in the GUI. Each part will include your supplied metadata and be output into a single folder of your choice or into seperate part named folders.

** Please note that different pdf programs implement the PDF standard in different ways. Unfortunately Preview on MacOS does not create bookmarks in the appropriate outline format for this program so its best to use Adobe Acrobat or PDFExpert, PDFSam etc **

## Getting started

### Requirements

- Python 3.8^
- PIP 23.2^
- PySimpleGUI 4.60.5^
- PyPDF2 3.14^

### Installation

1. Download the zip file or clone the project
2. Install dependencies above
3. In your terminal or shell run the program using `python main.py`

### Use

1. Input your score to be split using the file browser
2. Input your output location using the folder browser
3. Input your desired metadata, for multiple values seperate each value with a comma
4. Check the part names list aligns with your score bookmarks
5. Click submit to start the process

## Example output
### GUI Screenshot
<img width="803" alt="GUI Screenshot" src="https://github.com/MelMony/ScoreSplitter/assets/31891015/37ab0a95-b186-4717-9104-7a1cf5309eff">

### Example parts in part folder
<img width="431" alt="Example part folder with parts" src="https://github.com/MelMony/ScoreSplitter/assets/31891015/991b2501-f1cf-4756-991c-eff30f824a0e">

### Example parts folder output
<img width="459" alt="Output directory with part folders" src="https://github.com/MelMony/ScoreSplitter/assets/31891015/6383ad79-5e0e-466b-b128-4276b60e28f1">


## Future dev work

- Unit tests
- GUI error popups
- Split by page numbers
- Windows, MacOS & Linux Standalone Executables
- Built in pdf preview and bookmarker
- OCR part detection
