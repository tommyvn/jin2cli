import unittest
from mock import patch, MagicMock, mock_open
import jin2cli
from jin2cli.exceptions import TemplateAssertionError, FileWontChange


class TestJin2cli(unittest.TestCase):

    def test_update_non_existant_file(self):
        ofh = mock_open()

        def non_existing_file_mock_side_effect(fn=None, *args):
            if len(args) > 0 and args[0] == "w":
                return ofh()
            else:
                raise(IOError(2, 'No such file or directory'))
        m = MagicMock(side_effect=non_existing_file_mock_side_effect)
        with patch('jin2cli.open', m, create=True):
            self.assertTrue(
                jin2cli.update_file("somefile", "testing1234"))
            ofh.return_value.write.assert_called_with("testing1234")

    def test_update_file(self):
        existing_file_mock = mock_open(read_data="testing123")
        with patch('jin2cli.open', existing_file_mock, create=True) as fm:
            self.assertRaises(
                FileWontChange,
                jin2cli.update_file, "somefile", "testing123")
            self.assertTrue(
                jin2cli.update_file("somefile", "testing1234"))
            fm().write.assert_called_with("testing1234")

    def test_render_data_plus_template(self):
        data = {"name": "testing"}
        good_template = "hello {{ data.name }}!"
        bad_template = "hello {{ data.name|notexistingfilter() }}!"

        self.assertEqual(
            jin2cli.render_data_plus_template(data, good_template),
            "hello testing!")

        self.assertRaises(
            TemplateAssertionError,
            jin2cli.render_data_plus_template, data, bad_template)
