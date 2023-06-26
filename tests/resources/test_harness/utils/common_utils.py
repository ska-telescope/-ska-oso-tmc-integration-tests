"""This module implement common utils
"""
from os.path import dirname, join


def get_subarray_input_json(slug):
    assign_json_file_path = join(
        dirname(__file__),
        "..",
        "..",
        "..",
        "data",
        "subarray",
        f"{slug}.json",
    )
    with open(assign_json_file_path, "r", encoding="UTF-8") as f:
        assign_json = f.read()
    return assign_json


class JsonFactory(object):
    """Implement methods required for getting json"""

    def create_subarray_configuration(self, json_type):
        """Return configuration json"""
        return get_subarray_input_json(json_type)

    def create_assign_resource(self, json_type):
        """Return Assign Resource Json"""
        return get_subarray_input_json(json_type)
