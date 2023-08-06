import os

from robot_cli.core import CommandError
from robot_cli.core.base import BaseCommand


class Command(BaseCommand):
    help = "Create a project."
    subcommand = "create"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the project.")
        parser.add_argument("-l", "--library", dest="library",
                            help="Library folder of the project.")

    def handle(self, *args, **options):
        project_name = options.get("name")
        if options.get("library") is not None:
            library_folder = options.get("library")
        else:
            library_folder = "%s_library" % project_name
        if os.path.exists(project_name):
            raise CommandError("FileExistsError: %s" % project_name)

        os.makedirs(project_name)
        os.chdir(project_name)

        with open("README.rst", "w") as f:
            text = [
                "=" * len(project_name),
                project_name,
                "=" * len(project_name),
                "",
                "`Robot Framework`_ is a generic open source test automation framework.",
                "",
                ".. _Robot Framework: http://robotframework.org/",
                "",
            ]
            f.write("\n".join(text))

        with open("requirements.txt", "w") as f:
            text = [
                "robotframework",
                ""
            ]
            f.write("\n".join(text))

        os.mkdir("tests")
        with open("tests/resource.robot", "w") as f:
            text = [
                "=========",
                "Resources",
                "=========",
                "",
                "*** Variables ***",
                "No Operation",
                "",
                "",
                "*** Settings ***",
                "No Operation",
                "",
                "",
                "*** Keywords ***",
                "No Operation",
                "",
            ]
            f.write("\n".join(text))
        with open("tests/%s.robot" % project_name, "w") as f:
            text = [
                "%s Tests" % project_name,
                "-" * (len(project_name) + 6),
                "",
                "*** Settings ***",
                "No Operation",
                "",
                "",
                "*** Test Cases ***",
                "No Operation",
                "",
                "",
                "*** Keywords ***",
                "No Operation",
                "",
            ]
            f.write("\n".join(text))

        os.mkdir(library_folder)
        with open("%s/__init__.py" % library_folder, "w"):
            pass
        with open("%s/DemoLibrary.py" % library_folder, "w") as f:
            text = [
                "class IndicesLibrary(object):",
                "    def __init__(self, *args, **kwargs):",
                "        pass",
                "",
            ]
            f.write("\n".join(text))
