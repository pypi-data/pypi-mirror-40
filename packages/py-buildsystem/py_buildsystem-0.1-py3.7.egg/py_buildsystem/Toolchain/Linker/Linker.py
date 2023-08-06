import subprocess


class Linker:
    def __init__(self, linker_path, output_flag, command_line_file):
        self.__linker_path = linker_path
        self.__output_flag = output_flag
        self.__command_line_file = command_line_file

    def set_flags(self, list_of_flags):
        self.__flags = list_of_flags

    def link(self, list_of_files, output_file, list_of_additional_flags=[]):

        with open("it_will_be_called_diferently", "w") as comand_line_file:
            for file in list_of_files:
                comand_line_file.write(file + " ")

        return subprocess.call(" ".join([self.__linker_path] + self.__flags + list_of_additional_flags + [self.__output_flag + " " + output_file] + [self.__command_line_file + "it_will_be_called_diferently"]))
