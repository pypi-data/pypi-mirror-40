.. image:: https://codecov.io/bb/go8ose/pingboard/branch/master/graph/badge.svg
  :target: https://codecov.io/bb/go8ose/pingboard

This tool pings all the servers named on the command line, and shows you a
dashboard display of which hosts are up, which are down, and how long that
has been the case for. It uses raw sockets with protocol icmp, which
normally requires elevated permissions.  Hence you'll typically invoke it
with something like sudo ::

  sudo pingboard www1.example.com www2.example.com

pingboard attempts uses socket.getaddinfo() to resolve your servers to
IPv4 or IPv6 addresses. It only takes the first returned result. Hence you
can specify an IP address (as socket.getaddrinfo() will 'resolve' that to
the relevant IP address).  But also, if your name resolves into multiple IP
addresses then it may not be obvious to you which server is actually being
pinged.

Instead of listing servers on the command line, you can pass a --server-list
file that lists the servers.  If you do this, the file format is one server
per line.  Any text on a line after a white space is treated as a comment
for that server, and is also displayed by pingboard.

Use the --log-file option to have pingboard write a log file of events, so
you can have a historical record of when servers came up and down.

For other options, run pingboard with the -h option.

Installing:
===========

In order to install locally, clone it, then from within your checkout run:

::

  pip install .

Or, to install just for yourself (note that unless you take extra steps,
this won't work, as the script requires running as the root user, and the
root user won't be able to find the libraries):

::

  pip install --user .


In the later case, you might need to take extra steps to have the pingboard
available to you (i.e. add "$HOME/.local/bin" to your PATH)

Development:
============
If you want to have a copy you can hack on, organise yourself a virtualenv
environment to work in, then install with the -e flag:

::

  pip install -e .

Once you've one that, install the test dependencies so you can run the test
suite:

::

  pip install -r requirements_test.txt
