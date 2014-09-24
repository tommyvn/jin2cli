import unittest
from mock import patch, MagicMock, mock_open
from jin2cli import cli
from jin2cli.exceptions import TemplateAssertionError, FileWontChange
from StringIO import StringIO
import contextlib


class TestJin2cliCli(unittest.TestCase):

    def setUp(self):
        self.parser = cli.create_argument_parser()

        def non_existing_file_mock_side_effect(fn=None, *args):
            if len(args) > 0 and args[0] == "w":
                mocked_opened = mock_open()
            elif fn == "my_template":
                mocked_opened = mock_open(
                    read_data="""Hello {{ data.name }}""")
            elif fn == "my_bad_template":
                mocked_opened = mock_open(
                    read_data="""Hello {{ data.name|bum_filter() }}""")
            elif fn == "my_json":
                mocked_opened = mock_open(read_data="""{"name": "Tom"}""")
            elif fn == "my_bad_json":
                mocked_opened = mock_open(read_data="""bad_json""")
            elif fn == "my_output":
                print "heereee!!!"
                mocked_opened = mock_open(read_data="""Hello Tom""")
            elif fn == "my_old_output":
                mocked_opened = mock_open(read_data="""Hello Jim""")
            elif fn == "not_there":
                raise(IOError(2, 'No such file or directory'))
            return mocked_opened()
        self.mocked_open = MagicMock(
            side_effect=non_existing_file_mock_side_effect)

    def test_bad_template(self):
        args = self.parser.parse_args(["my_bad_template", "my_json", "-v"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(TemplateAssertionError):
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)

        args = self.parser.parse_args(["my_bad_template", "my_json"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(SystemExit) as cm:
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)
            self.assertEquals(cm.exception.message, 4)

    def test_missing_template(self):
        args = self.parser.parse_args(["not_there", "my_json", "-v"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(IOError):
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)

        args = self.parser.parse_args(["not_there", "my_json"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(SystemExit) as cm:
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)
            self.assertEquals(cm.exception.message, 2)

    def test_missing_json(self):
        args = self.parser.parse_args(["my_template", "not_there", "-v"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(IOError):
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)

        args = self.parser.parse_args(["my_template", "not_there"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(SystemExit) as cm:
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)
            self.assertEquals(cm.exception.message, 2)

    def test_bad_json(self):
        args = self.parser.parse_args(["my_template", "my_bad_json", "-v"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(ValueError):
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)

        args = self.parser.parse_args(["my_template", "my_bad_json"])
        with contextlib.nested(
                patch('jin2cli.cli.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(SystemExit) as cm:
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)
            self.assertEquals(cm.exception.message, 3)

    def test_no_file_changes(self):
        args = self.parser.parse_args(
            ["my_template", "my_json", "-o", "my_output", "-v"])
        with contextlib.nested(
                # This requires some deep patching
                patch('__builtin__.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(FileWontChange):
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)

        args = self.parser.parse_args(
            ["my_template", "my_json", "-o", "my_output"])
        with contextlib.nested(
                # This requires some deep patching
                patch('__builtin__.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            with self.assertRaises(SystemExit) as cm:
                cli.render(args.json, args.template,
                           args.output_file, args.verbose)
        self.assertEquals(cm.exception.message, 1)

    def test_file_changes(self):
        args = self.parser.parse_args(
            ["my_template", "my_json", "-o", "my_old_output", "-v"])
        with contextlib.nested(
                # This requires some deep patching
                patch('__builtin__.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            self.assertIsNone(cli.render(
                args.json, args.template, args.output_file, args.verbose))

        args = self.parser.parse_args(
            ["my_template", "my_json", "-o", "my_old_output"])
        with contextlib.nested(
                # This requires some deep patching
                patch('__builtin__.open', self.mocked_open, create=True),
                patch('sys.stdout', new=StringIO()),
                patch('sys.stderr', new=StringIO())
                ) as (_, fake_out, fake_err):
            self.assertIsNone(cli.render(
                args.json, args.template, args.output_file, args.verbose))
