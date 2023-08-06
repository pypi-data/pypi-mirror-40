import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from Step.Step import Step  # noqa: E402

from FilesFinder.FilesFinder import FilesFinder  # noqa: E402


class StepCompile(Step):
    def __init__(self, step_config, compiler):
        self.configuration = step_config
        self._check_config()

        self.compiler = compiler

        self.files_finder = FilesFinder(list_of_paths_to_search=self. __source_directories)
        self.files_finder.set_files_extentions(self.__types)

    def perform(self):
        self._create_outpu_directory()
        self._find_files()
        self.compiler.compile(self.__files_to_compile, self.__output_directory)

    def _check_config(self):
        try:
            self.__source_directories = self.configuration["source_directories"]
        except KeyError:
            raise Exception("No source directories given")

        try:
            self.__output_directory = self.configuration["output_direcotry"]
        except KeyError:
            raise Exception("No output directory given")

        try:
            self.__types = self.configuration["types"]
        except KeyError:
            raise Exception("No type given")

    def _find_files(self):
        self.__files_to_compile = self.files_finder.search()

    def _create_outpu_directory(self):
        os.makedirs(self.__output_directory, exist_ok=True)
