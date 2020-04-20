import yaml


class YamlConfigReader:

    def __init__(self):
        file = open("../Resources/config.yaml", mode='r')
        self._yaml_file = yaml.safe_load(file)

    def get_config(self):
        return self._yaml_file
