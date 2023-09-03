import os
import unittest
import tempfile
from PyPDF2 import PdfReader
from pdf_operations import add_metadata, split_score_by_bookmarks

class TestPdfMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.mkdtemp()
        cls.metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.score_path = 'tests/test_score.pdf'
        cls.complete_set_path = 'Who lives in a pineapple under the sea? - Complete Set.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
    
    def test_empty_path(self):
        add_metadata('', self.temp, self.metadata)
        self.assertRaises(FileNotFoundError)
    
    def test_incorrect_file_format(self):
        add_metadata('./parts_alternate.txt', self.temp, self.metadata)
        self.assertRaises(TypeError)
    
    def test_output_location(self):
        add_metadata(self.score_path, self.temp, self.metadata)
        self.assertTrue(os.path.exists(f'{self.temp}/{self.complete_set_path}'))
        
    def test_metadata_output(self):
        add_metadata(self.score_path, self.temp, self.metadata)
        
        actualPdf = PdfReader(f'{self.temp}/{self.complete_set_path}')
    
        # Check the outputted file has the specified metadata
        self.assertEqual(actualPdf.metadata.author, self.metadata['/Author'])
        self.assertEqual(actualPdf.metadata.title, self.metadata['/Title'])
        self.assertEqual(actualPdf.metadata.subject, self.metadata['/Subject'])
        
    def test_pdf_content_unchanged(self):
        add_metadata(self.score_path, self.temp, self.metadata)
        expectedPdf = PdfReader(self.score_path)
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
        cls.metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.score_path = 'tests/test_score.pdf'
        cls.part_names = ['Score', 'Vibraphone 1', 'Vibraphone 2', 'Male Vocal']
        cls.complete_set_path = 'Who lives in a pineapple under the sea? - Complete Set.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        
    def setUp(self) -> None:
        new_test_folder = tempfile.mkdtemp(dir=self.temp)
        self.temp = new_test_folder
        
    def test_empty_path(self):
        split_score_by_bookmarks('', self.part_names, self.metadata, self.temp)
        self.assertRaises(FileNotFoundError)
    
    def test_incorrect_file_format(self):
        split_score_by_bookmarks('parts_alternate.txt', self.part_names, self.metadata, self.temp)
        self.assertRaises(TypeError)
        
    def test_part_bookmark_mismatch(self):
        split_score_by_bookmarks(self.score_path, ['Score', 'Vibraphone 1'], self.metadata, self.temp)
        self.assertRaises(ValueError)
    
    def test_output_location(self):
        split_score_by_bookmarks(self.score_path, self.test_parts_metadata, self.metadata, self.temp)
        parts = os.listdir(self.temp)
        
        for part in parts:
            self.assertTrue(os.path.exists(f'{self.temp}/{part}'))
         
    def test_file_output_count(self):
        add_metadata(self.score_path, self.temp, self.metadata)
        split_score_by_bookmarks(self.score_path, self.part_names, self.metadata, self.temp)
        parts = os.listdir(self.temp)
        
        bookmark_count = len(PdfReader(self.score_path).outline)
        file_count = len(parts) - 1 # One less as dont count the complete set
        complete_set_page_count = len(PdfReader(f'{self.temp}/{self.complete_set_path}').pages)
        parts_page_count = - complete_set_page_count # dont count complete set
        for part in parts:
            parts_page_count += len(PdfReader(f'{self.temp}/{part}').pages)
        
        self.assertEqual(bookmark_count, file_count)
        self.assertEqual(complete_set_page_count, parts_page_count)
         
    def test_parts_metadata(self):
        split_score_by_bookmarks(self.score_path, self.metadata, self.metadata, self.temp)
        parts = os.listdir(self.temp)
        
        for i, part in enumerate(parts):
            self.assertEqual(part.metadata.author, self.metadata['/Author'])
            self.assertEqual(part.metadata.title, f'{self.part_names["/Title"]} - {self.part_names[i]}.pdf')
            self.assertEqual(part.metadata.subject, self.metadata['/Subject'])
        
