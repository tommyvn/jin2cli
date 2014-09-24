#!/usr/bin/env python

from __future__ import print_function
from jin2cli.exceptions import TemplateAssertionError, FileWontChange
import jin2cli
import sys
import json
import argparse


def render(json_file, template_file, output_file=None, verbose=False):
    try:
        data = json.load(open(json_file))
        with open(template_file) as f:
            template = f.read()
        render = jin2cli.render_data_plus_template(data, template)
        if output_file:
            jin2cli.update_file(output_file, render)
        else:
            print(render)
    except FileWontChange as e:
        print(e.message,
              file=sys.stderr)
        if verbose:
            raise(e)
        sys.exit(1)
    except IOError as e:
        print("{}: {}".format(e.filename, e.strerror),
              file=sys.stderr)
        if verbose:
            raise(e)
        sys.exit(2)
    except ValueError as e:
        print(e.message,
              file=sys.stderr)
        if verbose:
            raise(e)
        sys.exit(3)
    except TemplateAssertionError as e:
        print(e.message,
              file=sys.stderr)
        if verbose:
            raise(e)
        sys.exit(4)


def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("template", type=str, help="The Jinja2 template file")
    parser.add_argument("json", type=str, help="The json data file")
    parser.add_argument("-o", "--output-file", action="store",
                        default=None, help="update file")
    parser.add_argument("-v", "--verbose", action="store_true",
                        default=None, help="verbose output")
    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    render(args.json, args.template, args.output_file, args.verbose)

if __name__ == "__main__":
    main()
