# Use this test file during development (e.g to skip using the CLI all the time).

import os.path
from pathlib import Path

from commands import run_in_container
from ploomber_test.runner import CodeRunner

file = "../../examples/print-python-version.md"
python_version = "3.12.2"

# The CodeRunner, allows you to just return the python code blocks (cells) or to actually run the code.
# Example: Get only the prepared code to be run as part of a Dockerfile:

python_code = CodeRunner(Path(file).read_text(), python_version).get_code()

print(f"The parsed python code to execute is {python_code}")

# Now, you can actually run that code in a Docker container:

run_in_container(python_version, python_code)

# You should see the output of the execution of the python code in the console.
