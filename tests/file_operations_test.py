import os
import shutil
import unittest
import tempfile as tf
from file_operations import convert_string_to_part_pages, move_files_to_directories


class TestMoveFilesToDirectories(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tf.TemporaryDirectory()
        dirname = os.path.dirname(__file__)
        cls.dirname = dirname
        cls.parts = os.listdir(os.path.join(f"{dirname}/test_data"))
        cls.part_folder_names = [
            "Score",
            "Vibraphone 1",
            "Vibraphone 2",
            "Complete Sets",
            "Male Vocal",
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def setUp(self) -> None:
        self.source = tf.mkdtemp(dir=self.temp.name)
        self.destination = tf.mkdtemp(dir=self.temp.name)
        for part in self.parts:
            shutil.copy(os.path.join(f"{self.dirname}/test_data", part), self.source)
        self.files_to_move = []
        for file in self.parts:
            self.files_to_move.append(f"{self.source}/{file}")
        self.destination_folder_paths = []
        for part in self.part_folder_names:
            self.destination_folder_paths.append(f"{self.destination}/{part}")

    def teardown(self) -> None:
        self.temp.cleanup()

    def test_no_existing_directories_at_destination(self):
        move_files_to_directories(self.files_to_move, self.destination_folder_paths)

        expectedFolders = self.part_folder_names
        actualFolders = os.listdir(self.destination)
        actualFolders.sort()
        expectedFolders.sort()

        self.assertListEqual(actualFolders, expectedFolders)

    def test_existing_directories_at_destination(self):
        for part in self.part_folder_names:
            os.mkdir(f"{self.source}/{part}")

        move_files_to_directories(self.files_to_move, self.destination_folder_paths)

        expectedFolders = self.part_folder_names
        actualFolders = os.listdir(self.destination)
        actualFolders.sort()
        expectedFolders.sort()

        self.assertListEqual(actualFolders, expectedFolders)

    def test_empty_destination(self):
        move_files_to_directories(self.source, "")

        self.assertRaises(FileNotFoundError)

    def test_empty_file_list(self):
        move_files_to_directories("", self.destination)

        self.assertRaises(FileNotFoundError)


class TestConvertStringToPartPages(unittest.TestCase):
    def test_good_input(self):
        expected = {"Alto Sax 1": (0, 1), "Alto Sax 2": (2, 4), "Tenor Sax 1": (5, 9)}
        actual = convert_string_to_part_pages(
            "Alto Sax 1, 1-2\nAlto Sax 2, 3-5\nTenor Sax 1, 6-10"
        )

        self.assertDictEqual(actual, expected)

    def test_no_newline(self):
        with self.assertRaisesRegex(
            ValueError, "Text must contain a newline between each part."
        ):
            convert_string_to_part_pages(
                "Alto Sax 1, 1-2 Alto Sax 2, 3-5 Tenor Sax 1, 6-10"
            )

    def test_no_comma(self):
        with self.assertRaisesRegex(
            ValueError, "Text must contain a comma between the part name and page range"
        ):
            convert_string_to_part_pages(
                "Alto Sax 1 1-2\nAlto Sax 2 3-5\nTenor Sax 1 6-10"
            )

    def test_no_hyphen(self):
        with self.assertRaisesRegex(
            ValueError, "Text must contain a hyphen between the page range numbers."
        ):
            convert_string_to_part_pages(
                "Alto Sax 1, 1 2\nAlto Sax 2, 3 5\nTenor Sax 1, 6 10"
            )
