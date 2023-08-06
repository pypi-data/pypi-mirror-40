import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from Step.StepFactory import StepFactory  # noqa: E402

from ConfigReader.ConfigReader import ConfigReader  # noqa: E402


class Project(ConfigReader):
    def __init__(self, project_config_file, toolchain):
        ConfigReader.__init__(self, project_config_file)

        self.__project_name = ((project_config_file.replace("\\", "/")).split("/")[-1]).split(".")[0]  # take the file name as a projecct name

        self.__toolchain = toolchain

        self.__toolchain.get_compiler().set_defines(self.__defines)
        self.__toolchain.get_compiler().set_includes(self.__includes)

        self._parse_steps_list()

        self.run()

    def _check_config(self):
        try:
            self.__defines = self.configuration["defines"]
        except KeyError:
            self.__defines = []

        try:
            self.__includes = self.configuration["includes"]
        except KeyError:
            self.__includes = []

        try:
            self.__steps_list = self.configuration["steps"]
        except KeyError:
            self.__steps_list = []

        self.__steps = []

    def get_project_name(self):
        return self.__project_name

    def get_defines(self):
        return self.__defines

    def get_includes(self):
        return self.__includes

    def _parse_steps_list(self):
        for step in self.__steps_list:
            self.__steps.append(StepFactory.create(step, object_to_inject=self.__toolchain))

    def run(self):
        for step in self.__steps:
            step.perform()
