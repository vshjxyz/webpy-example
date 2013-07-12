webpy-example
=============

just an (old) example of a simple application written in web.py

To make it work just launch this (possibly) inside a virtualenv

`pip install -r requirements.txt`

then just launch the server with

`python web.py`

and go to http://0.0.0.0:8080

You'll be able to
* Print to console an ordered list of words (fetched from a remote url and then ordered)
* Print to the interface that ordered list (watch out if the list is too long)
* Write the ordered list to disk and being able to download it
* Send the ordered list to a gist (watch out the dimensions of the list)
* Send the ordered list by mail (it should work only if you have a SMTP server up on localhost)
