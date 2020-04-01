### <span style="color: black">&#x1F535; Making Async HTTP Requests

```
mkdir -p servercheck/servercheck
```

Change to the servercheck subdirectory.

```
cd servercheck
```

In the servercheck subdirectory, create a new file named __init__.py.
```
touch servercheck/__init__.py
```
Install Pipenv.
```
pip3.7 install --user -U pipenv
```
Create a virtualenv, and install click:
```
pipenv --python python3.7 install click
```

Activate the virtualenv.
```
pipenv shell
```
Define the CLI Function
Create the command line function in a module named cli within the servercheck package.

```
import click

@click.command()
def cli():
   pass

if __name__ == "__main__":
   cli()
Run the CLI.
python servercheck/cli.py --help
Add the required decorators from the Click library.

import click

@click.command()
@click.option("--filename", "-f", default=None)
@click.option("--server", "-s", default=None, multiple=True)
def cli(filename, server):
   if not filename and not server:
       raise click.UsageError("must provide a JSON file or servers")

if __name__ == "__main__":
   cli()
```

You should receive an error, which is expected since we haven't passed any arguments yet.

Create a set to hold on to all of the server/IP combinations, and add anything from the JSON file if given and also the values passed using the --server or -s flags.

```
import click
import json
import sys

@click.command()
@click.option("--filename", "-f", default=None)
@click.option("--server", "-s", default=None, multiple=True)
def cli(filename, server):
   if not filename and not server:
       raise click.UsageError("must provide a JSON file or servers")

   # Create a set to prevent duplicate server/port combinations
   servers = set()

   # If --filename or -f option is used then attempt to read
   # the file and add all values to the `servers` set.
   if filename:
       try:
           with open(filename) as f:
               json_servers = json.load(f)
               for s in json_servers:
                   servers.add(s)
       except:
           print("Error: Unable to open or read JSON file")
           sys.exit(1)

   # If --server or -s option are used then add those values
   # to the set.
   if server:
       for s in server:
           servers.add(s)

   print(servers)

if __name__ == "__main__":
   cli()
```

Create an example JSON file to parse.
touch example.json

Open the file with your preferred editor (e.g., vim).
vim example.json
Add the following content to the file:
```
[
   "JSONIP:PORT",
   "JSONIP:PORT",
   "JSONIP2:PORT2"
]
```

Test the function by passing it the example JSON file in combination with the --server option.
```
python servercheck/cli.py -f example.json --server "IP1:PORT1" -s "IP2:Port1"
```

Create setup.py with console_scripts for servercheck
Pull down the starter setup.py.
```
curl -O https://raw.githubusercontent.com/kennethreitz/setup.py/master/setup.py
```

Edit the file to add click as a dependency in the REQUIRED list, create the console_script, and remove the UploadCommand.
```

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "servercheck"
DESCRIPTION = (
   "CLI to ensure that HTTP requests can be made to various server/port combinations"
)
URL = "https://github.com/me/myproject"
EMAIL = "me@example.com"
AUTHOR = "Awesome Soul"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.1.0"

# What packages are required for this module to be executed?
REQUIRED = ["click"]

# What packages are optional?
EXTRAS = {
   # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
   with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
       long_description = "\n" + f.read()
except FileNotFoundError:
   long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
   project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
   with open(os.path.join(here, project_slug, "__version__.py")) as f:
       exec(f.read(), about)
else:
   about["__version__"] = VERSION

# Where the magic happens:
setup(
   name=NAME,
   version=about["__version__"],
   description=DESCRIPTION,
   long_description=long_description,
   long_description_content_type="text/markdown",
   author=AUTHOR,
   author_email=EMAIL,
   python_requires=REQUIRES_PYTHON,
   url=URL,
   packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
   # If your package is a single module, use this instead of 'packages':
   # py_modules=['mypackage'],
   entry_points={"console_scripts": ["servercheck=servercheck.cli:cli"]},
   install_requires=REQUIRED,
   extras_require=EXTRAS,
   include_package_data=True,
   license="MIT",
   classifiers=[
       # Trove classifiers
       # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python",
       "Programming Language :: Python :: 3",
       "Programming Language :: Python :: 3.7",
       "Programming Language :: Python :: Implementation :: CPython",
       "Programming Language :: Python :: Implementation :: PyPy",
   ],
)
```

Install the tool and make it editable.
```
pip install -e .
```
Run the tool.
```
servercheck -s "SERVER:1000" -s "SERVER2:2000" -f example.json

```

Conclusion

Congratulations, you've successfully completed this hands-on lab!
