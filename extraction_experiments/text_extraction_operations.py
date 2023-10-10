# Experiment to ascertain the potential of text extraction vs OCR for determining part names and locations

from pypdf import PdfReader

def get_entire_document_as_text(pdf):
    result = ''
    for page in PdfReader(pdf).pages:
        page_text = page.extract_text()
        page_text = ' '.join(page_text.split())
        result += page_text + '\n'
    
    return '' #result
        
         
def get_entire_document_as_dictionary(pdf):
    result = {}
    parts = []
    def visitor_part_name(text, cm, tm, font_dict, font_size):
        # Get x and y coordinates from the transformation matrix
        y = tm[5] 
        x = tm[4]
        
        # Only add text from particular coordinates of the page
        if x < 80 and y < 400:
            parts.append(text)
    for page in PdfReader(pdf).pages:
        page_text = page.extract_text(0)
        page_text = ' '.join(page_text.split())
        result[page.page_number] = page_text + '\n'
        
    
        page.extract_text(visitor_text=visitor_part_name)
        text_body = "".join(parts)
    
    

        

    print(text_body)
    return {} #result

   
# Loop through each page in the complete set and make a dictionary where the key is the page number and value is the extracted text
# How many pages is the part?

# Try get part - top left 

# Try get title - top center

# Try get composers / arrangers - top right