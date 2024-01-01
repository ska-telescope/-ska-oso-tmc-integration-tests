"""This module implement common utils
"""
from os.path import dirname, join


def get_subarray_input_json(slug):
    """
    Args:
        slug (str): base name of file
    Return:
        Read and return content of file
    """
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


def get_centralnode_input_json(slug):
    """
    Args:
        slug (str): base name of file
    Return:
        Read and return content of file
    """
    assign_json_file_path = join(
        dirname(__file__),
        "..",
        "..",
        "..",
        "data",
        "centralnode",
        f"{slug}.json",
    )
    with open(assign_json_file_path, "r", encoding="UTF-8") as f:
        assign_json = f.read()
    return assign_json


def get_schema(slug: str) -> str:
    """
    Args:
        slug (str): base name of file
    Return:
        Read and return content of file
    """
    file_path = join(
        dirname(__file__),
        "..",
        "..",
        "..",
        "data",
        "schemas",
        f"{slug}.json",
    )
    with open(file_path, "r", encoding="UTF-8") as f:
        required_schema = f.read()
    return required_schema


class JsonFactory(object):
    """Implement methods required for getting json"""

    def create_subarray_configuration(self, json_type):
        """Read and return configuration json file from
            tests/data/subarray folder
        Args:
            json_type (str): Base name of file which is stored in data folder
        Return:
            config_json (str): Return configure json based json type provided
        """
        return get_subarray_input_json(json_type)

    def create_assign_resources_configuration(self, json_type):
        """Read and return configuration json file from
            tests/data/subarray folder
        Args:
            json_type (str): Base name of file which is stored in data folder
        Return:
            config_json (str): Return configure json based json type provided
        """
        return get_subarray_input_json(json_type)

    def create_centralnode_configuration(self, json_type):
        """Read and return configuration json file from
            tests/data/centralnode folder
        Args:
            json_type (str): Base name of file which is stored in data folder
        Return:
            config_json (str): Return configure json based json type provided
        """
        return get_centralnode_input_json(json_type)

    def create_command_or_attribute_schema(self, json_type: str) -> dict:
        """Read and return json schema for requested attribute or commands
            from tests/data/schema folder.
        Args:
            json_type (str): Base name of file which is stored in data folder
        Return:
            schema (dict): Returns requested schema for attribute or command
            json
        """
        return get_schema(json_type)
