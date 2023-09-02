import os
import shutil
import unittest
import tempfile
from pdf_operations import add_metadata
from PyPDF2 import PdfReader



class TestPdfMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.mkdtemp()
        cls.test_metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.test_score_path = './test_score.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
    
    def test_empty_path(self):
        add_metadata('', self.temp, self.test_metadata)
        self.assertRaises(FileNotFoundError)
    
    def test_incorrect_file_format(self):
        add_metadata('./parts_alternate.txt', self.temp, self.test_metadata)
        self.assertRaises(TypeError)
    
    def test_output_location(self):
        add_metadata(self.test_score_path, self.temp, self.test_metadata)
        self.assertTrue(os.path.exists(f'{self.temp}/Who lives in a pineapple under the sea? - Complete Set.pdf'))
        
    def test_metadata_output(self):
        add_metadata(self.test_score_path, self.temp, self.test_metadata)
        
        actualPdf = PdfReader(f'{self.temp}/Who lives in a pineapple under the sea? - Complete Set.pdf')
    
        # Check the outputted file has the specified metadata
        self.assertEqual(actualPdf.metadata.author, self.test_metadata['/Author'])
        self.assertEqual(actualPdf.metadata.title, self.test_metadata['/Title'])
        self.assertEqual(actualPdf.metadata.subject, self.test_metadata['/Subject'])
        
    def test_pdf_content_unchanged(self):
        add_metadata(self.test_score_path, self.temp, self.test_metadata)
        expectedPdf = PdfReader(self.test_score_path)
        actualPdf = PdfReader(f'{self.temp}/Who lives in a pineapple under the sea? - Complete Set.pdf')
        
        # Check outputted pdf has the same number of pages/content
        self.assertEqual(len(actualPdf.pages), len(expectedPdf.pages))
        for i in range(len(actualPdf.pages)):
            self.assertEqual(actualPdf.pages[i].extract_text(), expectedPdf.pages[i].extract_text())

class TestSplitPdfBookmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.mkdtemp()
        cls.test_metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.test_score_path = './test_score.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        
        
    # def test_split_bookmarks():
    #     # throw file not found error
    #     # Number of files is same as number of parts
    #     # Parts exist at output location
    #     # Parts all include the metadata
    #     # Number of pages for complete set should be reflected in total pages of parts
        