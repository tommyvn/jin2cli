jin2cli
=====

json + jinja2 template == file

## Install it

`pip jin2cli`

## Use it

### Simple stuff

```ShellSession
$ echo 'Hello {{ data.name }}' > my_template
$ echo '{"name": "Tom"}' > my_json
$ jin2cli my_template my_json
Hello Tom
```
If no output file is provided jin2cli will output to stdout.

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
If the result will not change the current file contents jin2cli will exit with a status of 1, meaning commands like reloads can be chained and executed only when changes occur.

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
