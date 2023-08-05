===============================
rmux
===============================

``rmux`` allows you to run your local project on multiple remote machines in
parallel.

The command names comes from remote-tmux as it allows to multiplex commands
on multiple remote machienes, syncronized.

The original purpose was to allow testing local changes to a project on other
platforms, like running tox on another distribution.

To use it you need to define the list of remote hosts like:
```
export HOSTS="node1 node2"
```
If you fail to define the ``HOSTS`` variable the tool will default to localhost
but it will still use its logic of doing a rsync and running commands using
tmux and ssh.

* Free software: Apache license
* Source: https://github.com/pycontribs/rmux
* Bugs: https://github.com/pycontribs/rmux
