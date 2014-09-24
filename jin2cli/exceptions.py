from jinja2.exceptions import TemplateAssertionError  # noqa


class FileWontChange(Exception):
    def __init__(self, file_name):
        self.message = "data + template already == {}".format(file_name)
