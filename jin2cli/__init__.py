#!/usr/bin/env python

from __future__ import print_function
from jinja2 import Template
from jin2cli.exceptions import FileWontChange


def render_data_plus_template(data, template):
    template_object = Template(template)
    render = template_object.render(data=data)
    return render


def update_file(file_name, data):
    try:
        with open(file_name) as f:
            if data == f.read():
                raise FileWontChange(file_name)
    except IOError:
        pass
    with open(file_name, "w") as f:
        f.write(data)
    return True
