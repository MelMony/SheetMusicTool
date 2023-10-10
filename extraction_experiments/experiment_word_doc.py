from pypdf import PdfReader
from text_extraction_operations import get_entire_document_as_dictionary, get_entire_document_as_text

pdf = f'./tests/test_score.pdf'

pdf_dict = get_entire_document_as_dictionary(pdf)
print(pdf_dict)

pdf_text = get_entire_document_as_text(pdf)
print(pdf_text)
