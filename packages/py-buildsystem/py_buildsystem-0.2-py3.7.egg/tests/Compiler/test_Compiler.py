import os
import shutil
import subprocess

import unittest

from py_buildsystem.Toolchain.Compiler.Compiler import Compiler

script_file_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

test_compiler_dir_name = "test_compier"
test_compiler_name = "test_compiler"

test_compiler_path = os.path.join(script_file_path, test_compiler_dir_name).replace("\\", "/")
test_compiler_exe_path = os.path.join(test_compiler_path, test_compiler_name).replace("\\", "/")

config = {
    "define_flag": "-D",
    "output_flag": "-o",
    "compile_flag": "-c",
    "include_flag": "-I"
}

flags = ["-std=c++14"]
defines = ["DEBUG", "X86"]
includes = ["../inc", "../../framework/include"]

files_to_compile = ["test1.c", "test2.c"]


class TestCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(test_compiler_path, exist_ok=True)

        with open(test_compiler_exe_path, "wb") as file:
            pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(test_compiler_path, ignore_errors=True)

    def test_read_config_file(self):
        pass

    def test_compile(self):
        subprocess.call = self.subprocess_call_mock

        self.expected_command = [test_compiler_exe_path, config["compile_flag"], config["define_flag"] + defines[0], config["define_flag"] + defines[1],
                                 flags[0], config["include_flag"] + includes[0], config["include_flag"] + includes[1], files_to_compile[0]]

        a = Compiler(test_compiler_exe_path, config["define_flag"], config["output_flag"], config["compile_flag"], config["include_flag"])
        a.set_defines(defines)
        a.set_includes(includes)
        a.set_flags(flags)

        a.compile([files_to_compile[0]], "")

    def subprocess_call_mock(self, command):
        command = command.split(" ")

        self.assertCountEqual(command, self.expected_command)
