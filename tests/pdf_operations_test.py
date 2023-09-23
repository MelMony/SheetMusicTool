import os
import unittest
import tempfile
from pypdf import PdfReader
from pdf_operations import add_metadata, split_score_by_bookmarks, split_score_by_pages

class TestPdfMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.TemporaryDirectory()
        cls.metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.score_path = 'tests/test_score.pdf'
        cls.complete_set_path = 'Who lives in a pineapple under the sea? - Complete Set.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
    
    def test_empty_path(self):
        add_metadata('', self.temp.name, self.metadata)
        self.assertRaises(FileNotFoundError)
    
    def test_incorrect_file_format(self):
        add_metadata('./parts_alternate.txt', self.temp.name, self.metadata)
        self.assertRaises(TypeError)
    
    def test_output_location(self):
        add_metadata(self.score_path, self.temp.name, self.metadata)
        self.assertTrue(os.path.exists(f'{self.temp.name}/{self.complete_set_path}'))
        
    def test_metadata_output(self):
        add_metadata(self.score_path, self.temp.name, self.metadata)
        
        actualPdf = PdfReader(f'{self.temp.name}/{self.complete_set_path}')
    
        # Check the outputted file has the specified metadata
        self.assertEqual(actualPdf.metadata.author, self.metadata['/Author'])
        self.assertEqual(actualPdf.metadata.title, self.metadata['/Title'])
        self.assertEqual(actualPdf.metadata.subject, self.metadata['/Subject'])
        
    def test_pdf_content_unchanged(self):
        add_metadata(self.score_path, self.temp.name, self.metadata)
        expectedPdf = PdfReader(self.score_path)
        actualPdf = PdfReader(f'{self.temp.name}/Who lives in a pineapple under the sea? - Complete Set.pdf')
        
        # Check outputted pdf has the same number of pages/content
        self.assertEqual(len(actualPdf.pages), len(expectedPdf.pages))
        for i in range(len(actualPdf.pages)):
            self.assertEqual(actualPdf.pages[i].extract_text(), expectedPdf.pages[i].extract_text())

class TestSplitPdfBookmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.TemporaryDirectory()
        cls.metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.score_path = 'tests/test_score.pdf'
        cls.part_names = ['Score', 'Vibraphone 1', 'Vibraphone 2', 'Male Vocal']
        cls.complete_set_path = 'Who lives in a pineapple under the sea? - Complete Set.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        
    def setUp(self) -> None:
        new_test_folder = tempfile.mkdtemp(dir=self.temp.name)
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
        actual_parts = sorted(os.listdir(self.temp))
        
        expected_parts = sorted(self.part_names)
        
        for i, part in enumerate(actual_parts):
            self.assertTrue(os.path.exists(f'{self.temp}/{part}'))
            self.assertEquals(f'{self.temp}/{part}', f'{self.temp}/{self.metadata["/Title"]} - {expected_parts[i]}.pdf')
         
         
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
        
        for part in parts:
            pdf_reader = PdfReader(f'{self.temp}/{part}')
            self.assertEqual(pdf_reader.metadata.author, self.metadata['/Author'])
            self.assertEqual(pdf_reader.metadata.title, f'{self.metadata["/Title"]}')
            self.assertEqual(pdf_reader.metadata.subject, self.metadata['/Subject'])
        

class TestSplitPdfPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Make temporary directory to house output
        cls.temp = tempfile.TemporaryDirectory()
        cls.metadata = {'/Author': 'SpongeBob Squarepants, Patrick Star', '/Title': 'Who lives in a pineapple under the sea?', '/Subject': 'Calypso, Vocal'}
        cls.score_path = 'tests/test_score.pdf'
        cls.part_page_nums = {'Score': (0,2), 'Vibraphone 1': (3,3), 'Vibraphone 2': (4,5), 'Male Vocal': (6,6)}
        cls.complete_set_path = 'Who lives in a pineapple under the sea? - Complete Set.pdf'
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        
    def setUp(self) -> None:
        new_test_folder = tempfile.mkdtemp(dir=self.temp.name)
        self.temp = new_test_folder
        
    def test_empty_path(self):
        split_score_by_pages('', self.part_page_nums, self.metadata, self.temp)
        self.assertRaises(FileNotFoundError)
    
    def test_incorrect_file_format(self):
        split_score_by_pages('parts_alternate.txt', self.part_page_nums, self.metadata, self.temp)
        self.assertRaises(TypeError)
        
    def test_output_location(self):
        split_score_by_pages(self.score_path, self.part_page_nums, self.metadata, self.temp)
        actual_parts = sorted(os.listdir(self.temp))
        
        expected_parts = sorted(self.part_page_nums.keys())
    
        for i, part in enumerate(actual_parts):
            self.assertTrue(os.path.exists(f'{self.temp}/{part}'))
            self.assertEquals(f'{self.temp}/{part}', f'{self.temp}/{self.metadata["/Title"]} - {expected_parts[i]}.pdf')
         
    def test_file_output_count(self):
        add_metadata(self.score_path, self.temp, self.metadata)
        split_score_by_pages(self.score_path, self.part_page_nums, self.metadata, self.temp)
        actual_parts = os.listdir(self.temp)
        
        expected_part_count = len(self.part_page_nums.keys())
        actual_part_count = len(actual_parts) - 1 # One less as dont count the complete set
        
        complete_set_page_count = len(PdfReader(f'{self.temp}/{self.complete_set_path}').pages)
        parts_page_count = -complete_set_page_count # dont count complete set
        for part in actual_parts:
            parts_page_count += len(PdfReader(f'{self.temp}/{part}').pages)
        
        self.assertEqual(actual_part_count, expected_part_count)
        self.assertEqual(complete_set_page_count, parts_page_count)
         
    def test_parts_metadata(self):
        split_score_by_pages(self.score_path, self.part_page_nums, self.metadata, self.temp)
        parts = os.listdir(self.temp)
        
        for part in parts:
            pdf_reader = PdfReader(f'{self.temp}/{part}')
            self.assertEqual(pdf_reader.metadata.author, self.metadata['/Author'])
            self.assertEqual(pdf_reader.metadata.title, f'{self.metadata["/Title"]}')
            self.assertEqual(pdf_reader.metadata.subject, self.metadata['/Subject'])
        