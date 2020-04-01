### <span style="color: black">&#x1F535; Making Async HTTP Requests


We frequently have to check whether one of our servers has access to other servers on our internal network.

To make this a little easier for ourselves, we've decided to use Python to write a CLI that can take either a JSON file with servers and ports to check or a list of host/port combinations to make requests to.

In this hands-on lab, we will take a list of server/port combinations and make HTTP requests concurrently so that we can get the status of our servers as quickly as possible.

```
mkdir servercheck
cd servercheck
```

Create a virtualenv.

```
pipenv install --python python3.7
```
Activate the virtualenv.

```
pipenv shell
```

Create a module called http.py within the servercheck directory that contains __init__.py.
```
touch servercheck/http.py
```

Install the requests package as a dependency.
```
pipenv install requests
```

Open setup.py, and add requests to the REQUIRED list.

```
# What packages are required for this module to be executed?
REQUIRED = ["click", "requests"]
Make Concurrent Requests and Return the Results
```

From within the http module, create a function called ping_servers.
```
def ping_servers(servers):
   results = {'success': [], 'failure': []}
   asyncio.run(make_requests(servers, results))
   return results
```   
* Create the make_requests, ping, and get functions.

```
import asyncio
import requests
import os

def get(server):
   debug = os.getenv("DEBUG")
   try:
       if debug:
           print(f"Making request to {server}")
       response = requests.get(f"http://{server}")
       if debug:
           print(f"Received response from {server}")
       return {"status_code": response.status_code, "server": server}
   except:
       if debug:
           print(f"Failed to connect to {server}")
       return {"status_code": -1, "server": server}

async def ping(server, results):
   loop = asyncio.get_event_loop()
   future_result = loop.run_in_executor(None, get, server)
   result = await future_result
   if result["status_code"] in range(200, 299):
       results["success"].append(server)
   else:
       results["failure"].append(server)

async def make_requests(servers, results):
   tasks = []

   for server in servers:
       task = asyncio.create_task(ping(server, results))
       tasks.append(task)

   await asyncio.gather(*tasks)

def ping_servers(servers):
   results = {"success": [], "failure": []}
   asyncio.run(make_requests(servers, results))
   return results
```

Test Against Additional Servers Using REPL
From within the virtualenv, run the following:
```
DEBUG=true PYTHONPATH=. python

>>> from servercheck.http import ping_servers
>>> servers = ('web-node1:80', 'web-node2:80', 'web-node1:3000', 'web-node2:3000', 'web-node1:8080')
>>> ping_servers(servers)

```
Utilize servercheck.http.ping_servers in the CLI Function


Open cli.py, and edit the file to pass the server information collected by the cli function to the ping_servers function.

```
import click
import json
import sys
from .http import ping_servers

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

   # Make requests and collect results
   results = ping_servers(servers)
Add the following lines to the end of the file, under the line results = ping_servers(servers):

 print("Successful Connections")
 print("---------------------")
 for server in results['success']:
     print(server)

 print("\n Failed Connections")
 print("------------------")
 for server in results['failure']:
     print(server)
```

Install the package into the virtualenv in editable mode.
pip install -e .

Create a test JSON file named example.json within the project directory.
touch example.json


Add the following to the test file:
```
[
   "web-node1:80",
   "web-node1:8000",
   "web-node1:3000",
   "web-node2:80",
   "web-node2:3000"
]
```
Run the following command to test the tool:
servercheck -f example.json -s 'web-node1:80' -s 'web-node1:9000'
