#!/usr/bin/env python

from __future__ import print_function
from jinja2 import Template
import sys


def process_data_thru_template(data, template, output_file=None):
    template_object = Template(template)
    rendered_template = template_object.render(data=data)
    if output_file:
        try:
            with open(output_file) as f:
                current = f.read()
        except IOError:
            current = None
        if current == rendered_template:
            print("data + template already == {}".format(output_file),
                  file=sys.stderr)
            sys.exit(1)
        else:
            with open(output_file, "w") as f:
                f.write(rendered_template)
    else:
        print(rendered_template)


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("template", type=str,
                        help="The Jinja2 template file")
    parser.add_argument("json", type=str,
                        help="The json data file")
    parser.add_argument("-o", "--output-file", action="store", default=None,
                        help="update file")
    parser.add_argument("-v", "--verbose", action="store_true", default=None,
                        help="verbose output")
    args = parser.parse_args()

    try:
        data = json.load(open(args.json))
    except Exception as e:
        print("error processing {}, is it valid json?".format(args.json),
              file=sys.stderr)
        if args.verbose:
            print(e)
        sys.exit(2)

    try:
        process_data_thru_template(data, open(args.template).read(),
                                   output_file=args.output_file)
    except SystemExit as e:
        raise e
    except Exception as e:
        print("error processing {}, is it a valid jinja2 template?".format(args.template),
              file=sys.stderr)
        if args.verbose:
            print(e)
        sys.exit(2)
