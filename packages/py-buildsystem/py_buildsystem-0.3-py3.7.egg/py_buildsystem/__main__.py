import argparse

from .Project.Project import Project
from .Toolchain.Toolchain import Toolchain

# sys.tracebacklimit = 0


parser = argparse.ArgumentParser(description='Python based build system.')

parser.add_argument('compiler_config', metavar='CC', type=str, nargs=1,
                    help='Compiler configuration file')

parser.add_argument('project_config', metavar='PC', type=str, nargs=1,
                    help='Project configuration file')

parser.add_argument('compiler_path', metavar='path', type=str, nargs='?', default='',
                    help='Path to compiler')

args = parser.parse_args()

toolchain = Toolchain(args.compiler_config[0], args.compiler_path)
project = Project(args.project_config[0], toolchain)
