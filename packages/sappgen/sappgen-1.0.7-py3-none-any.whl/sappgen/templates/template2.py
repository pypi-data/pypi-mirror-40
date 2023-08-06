""" Template - 2
project
│
├── testapp
│   ├── routes
│   │   ├── __init__.py
│   │   └── test_routes.py
│   │
│   └── util
│   │   ├── __init__.py
│   │   └── log_util.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── config.ini
├── Makefile
├── README.md
├── requirements.txt
│
└── tests
    └── test_main.py
"""
import os
import logging
from ..util import process_template, cleanup


my_path = os.path.abspath(os.path.dirname(__file__))


class Template2:
    TEMPLATE_PROJ_PATH = f"{my_path[:-10]}/template_files/template2/project"

    def __init__(self, project_name, app_name):
        self.project_name = project_name
        self.app_name = app_name

    def __create_skeleton(self):
        cleanup(self.project_name)

        logging.info(
            f"setting up project structure for {self.project_name}/{self.app_name}"
        )

        os.system(f"mkdir -p {self.project_name}/{self.app_name}/util")
        os.system(f"mkdir -p {self.project_name}/{self.app_name}/routes")
        os.system(f"mkdir -p {self.project_name}/tests")

        os.system(f"touch {self.project_name}/config.ini")
        os.system(f"touch {self.project_name}/Makefile")
        os.system(f"touch {self.project_name}/README.md")
        os.system(f"touch {self.project_name}/requirements.txt")

        os.system(f"touch {self.project_name}/{self.app_name}/__init__.py")
        os.system(f"touch {self.project_name}/{self.app_name}/main.py")

        os.system(f"touch {self.project_name}/{self.app_name}/util/__init__.py")
        os.system(f"touch {self.project_name}/{self.app_name}/util/log_util.py")

        os.system(f"touch {self.project_name}/{self.app_name}/routes/__init__.py")
        os.system(f"touch {self.project_name}/{self.app_name}/routes/test_routes.py")

        os.system(f"touch {self.project_name}/tests/test_main.py")

    def __create_files(self):
        logging.info(f"generating files for {self.project_name}/{self.app_name}")

        dest_proj_path = f"{self.project_name}"

        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/config.ini.template",
            f"{dest_proj_path}/config.ini",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/Makefile.template",
            f"{dest_proj_path}/Makefile",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/README.md.template",
            f"{dest_proj_path}/README.md",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/requirements.txt.template",
            f"{dest_proj_path}/requirements.txt",
        )

        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/__init__.py.template",
            f"{dest_proj_path}/{self.app_name}/__init__.py",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/main.py.template",
            f"{dest_proj_path}/{self.app_name}/main.py",
        )

        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/util/__init__.py.template",
            f"{dest_proj_path}/{self.app_name}/util/__init__.py",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/util/log_util.py.template",
            f"{dest_proj_path}/{self.app_name}/util/log_util.py",
        )

        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/routes/__init__.py.template",
            f"{dest_proj_path}/{self.app_name}/routes/__init__.py",
        )
        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/testapp/routes/test_routes.py.template",
            f"{dest_proj_path}/{self.app_name}/routes/test_routes.py",
        )

        process_template(
            self.project_name,
            self.app_name,
            f"{Template2.TEMPLATE_PROJ_PATH}/tests/test_main.py.template",
            f"{dest_proj_path}/tests/test_main.py",
        )

    def process(self):
        self.__create_skeleton()
        self.__create_files()
        logging.info("=== DONE ===")
        os.system(f"tree -a {self.project_name}")
