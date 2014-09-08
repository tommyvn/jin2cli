jin2cli
=====

json + jinja2 template == file

## Install it

`pip install jin2cli`

## Use it

jin2cli takes json data and passes it into a jinja2 template under the `data` variable.

`jin2cli --help`

### Simple stuff

```ShellSession
$ echo '{"name": "Tom"}' > my_json
$ echo 'Hello {{ data.name }}' > my_template
$ jin2cli my_template my_json
Hello Tom
```
jin2cli will output to stdout if no output file is provided.

### Intermediate stuff

```ShellSession
$ echo 'server { server_name {{ data.name }}; location / { echo {{ data.message }}; } }' > my_template
$ echo '{"name": "frontend", "message": "Hello World"}' > my_json
$ jin2cli my_template my_json -o server.conf && service nginx reload
 * Reloading nginx configuration nginx
   ...done.
$ !!
data + template already == test
```
If an output file is provided jin2cli will output to that file.
jin2cli will exit with a status of 1 if the result will not change the current file, meaning commands like nginx reloads can be chained and executed only when changes occur.

### Intermediate stuff with an API request thrown in

```ShellSession
$ curl http://someapi/app_data.json
{"name": "frontend", "message": "Hello World"}
$ echo 'server { server_name {{ data.name }}; location / { echo {{ data.message }}; } }' > my_template
$ jin2cli my_template <(curl http://someapi/app_data.json) -o server.conf && service nginx reload
 * Reloading nginx configuration nginx
   ...done.
$ !!
data + template already == test
```
Anonymous pipes are awesome and people don't use them enough. Anywhere a file is used for input (or output) an anonymous pipe can build that file on the fly from any other command.

### (Maybe too) advanced stuff

```ShellSession
$ jin2cli \
    <(curl https://raw.githubusercontent.com/tommyvn/jin2cli/master/examples/docker_to_nginx/nginx.template) \
    <(echo '{"node": "app-1", "containers": '$(curl https://raw.githubusercontent.com/tommyvn/jin2cli/master/examples/docker_to_nginx/docker.json | python -c 'import json; import sys; print json.dumps([ dict(map(lambda (k, v): (k, v) if k != "Names" else ("Name", v[0].split("_")[0][1:]), c.iteritems())) for c in json.load(sys.stdin) ]);')'}') \
  -o servers.conf && service nginx reload
 * Reloading nginx configuration nginx
   ...done.
$ !!
data + template already == test
```
Anonymous pipes mean data for templates and json can come from anywhere, including json APIs like Docker.
This example command uses an nginx template on github and example output from the /v1.12/containers/json docker API endpoint parsed thru a Python one-liner to generate an nginx config file which will route traffic to containers based on their names.
It will reload nginx but only if the nginx config file changed.
