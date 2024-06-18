import duckdb

from ploomber_test.parse import iterate_code_chunks
from ploomber_test.commands import run_in_container


class CodeRunner:
    def __init__(self, text, python_version="3.12.2", conn=None):
        self.text = text
        self.python_version = python_version

        if conn:
            self.conn = conn
        else:
            self.conn = duckdb.connect()

    def run(self):
        run_in_container(self.python_version, self.get_code())

    def get_code(self):
        python_code = []
        for code in iterate_code_chunks(self.text):
            language = code["language"]
            if language == "python":
                python_code.append(code["code"])
            elif language == "sql":
                return self.conn.execute(code["code"]).fetchall()
        return ";".join(item.replace("\n", ";").replace('"', "'") for item in python_code)
