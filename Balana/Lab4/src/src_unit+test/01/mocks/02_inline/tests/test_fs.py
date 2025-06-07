from unittest import mock, TestCase
from project import fs


class TestExamples(TestCase):
    def setUp(self):
        self.patcher = mock.patch('project.fs.print_contents_of_cwd',return_value=b'tests\nfoo\nbar\ntest\n')
        self.patcher.start()    
    
    def test_print_contents_of_cwd_success(self):
        actual_result = fs.print_contents_of_cwd()
        expected_directory = b'tests'
        self.assertIn(expected_directory,actual_result)
    def tearDown(self):
        self.patcher.stop()

