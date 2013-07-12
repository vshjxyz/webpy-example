import contextlib
import json
import mailer
import os
import random
import string
import urllib
import web

# Random url, change it to any url that has a list of unordered words in plain text
ADDRESS = 'http://svn.pietdepsi.com/repos/projects/zyzzyva/trunk/data/words/North-American/OWL.txt'
TMP_FOLDER = 'tmp/'
TMP_EXTENSION = 'txt'
# Defining urls for web.py
URLS = (
    '/', 'index',
    '/consolelist', 'ConsoleList',
    '/printlist', 'PrintList',
    '/getlist/(.*)', 'GetList',
    '/writelist', 'WriteList',
    '/emaillist', 'EmailList',
    '/gistlist', 'GistList',
)
# Creating web.py instance app and renderer to point on templates dir
app = web.application(URLS, globals())
render = web.template.render('templates')


def get_ordered_list(separator):
    """
    Main function of the program, it takes a string called separator to
    return the list of ordered words in a proper way
    """
    # Using the with command with contextlib in order to have a conection close in any case
    with contextlib.closing(urllib.urlopen(ADDRESS)) as response:
        # Reading words, stripping them and splitting to have a list
        words = response.read().strip().split()
        # Sorting the words in the list
        words.sort(key=str.lower)
        # Checking if the separator is a valid string
        if not isinstance(separator, str):
            raise web.InternalError('Separator character is not a String')
        # Returning the words ordered and joined with the separator
        return separator.join(words)


def get_full_path_list(name):
    """
    Returns the full path for the temporary files (in order to generate or download them)
    """
    return os.path.join(TMP_FOLDER, '%s.%s' % (name, TMP_EXTENSION))


class index:
    """
    Handles the index (/) request rendering the main interface (according to web.py)
    """
    def GET(self):
        return render.interface()


class ConsoleList:
    """
    Calls the main method and prints out the result in the python console
    """
    def GET(self):
        print get_ordered_list('\n')


class PrintList:
    """
    Calls the main method and returns the result with web.py interface (will be handled by interface.js)
    """
    def GET(self):
        return get_ordered_list('<br />')


class WriteList:
    """
    Writes the list to disk in TMP_FOLDER with a random name, returns the random name to the script
    """
    def GET(self):
        # Getting the ordered list
        ordered_list = get_ordered_list('\n')
        # Creating a random name of 15 characters
        random_name = ''.join(random.choice(string.letters) for i in xrange(15))
        # Get the full path of the new file to write
        full_path = get_full_path_list(random_name)
        # Check if the path exists and creates it if it doesn't
        if not os.path.exists(TMP_FOLDER):
            os.makedirs(TMP_FOLDER)
        # Write the files and returns his name
        with open(full_path, 'w') as f:
            f.write(ordered_list)
            f.close()
        return random_name


class GetList:
    """
    Method/class to be called when the user wants to download the written file (written with the writeList method/class)
    """
    def GET(self, filename):
        # Checks if filename (which is a parameter passed in the link) exists in the TMP_FOLDER
        # If it doesn't, an error is returned
        full_path = get_full_path_list(filename)
        if (not os.path.exists(full_path)):
            web.NotFound('File not found in %s' % full_path)
        else:
            # If the file exists, prepares the headers for the response
            web.header("Content-Disposition", "attachment; filename=%s" % filename)
            web.header("Content-Type", TMP_EXTENSION)
            web.header('Transfer-Encoding','chunked')
            # Opens the file with a buffer and returns it
            f = open(full_path, 'rb')
            while True:
                buf = f.read(1024 * 8)
                if not buf:
                    # Exits when the buffer is empty
                    break
                yield buf


class EmailList:
    """
    Uses the mailer library to connect to a SMTP server and send a mail with the result of the operation
    """
    def GET(self):
        # Setting up mailer to send the email
        email_to = "yours@example.com"
        message = mailer.Message()
        message.From = "me@example.com"
        message.To = email_to
        message.Subject = "Ordered list"
        message.Body = get_ordered_list('\n')

        # mailer_instance = mailer.Mailer('smtp.example.com') Actually doesn't work because there's no smtp server configured
        # mailer_instance.send(message) Send the message
        # I return the email
        return email_to


class GistList:
    """
    Using the Gist api, I use this method/class to send a JSON with the result into a public gist
    returning the html link to the gist
    """
    def GET(self):
        # Setting up the JSON to be used in the call
        params = json.dumps({
            'description': 'test web.py',
            'public': True,
            'files': {
                'test.txt': {
                    'content': get_ordered_list('\n')
                }
            }
        })
        # Using contextlib to be sure that the connection will be closed
        with contextlib.closing(urllib.urlopen("https://api.github.com/gists", params)) as response:
            # Parsing the response into a dictionary
            json_response = json.loads(response.read())
        # Checking if the response code is correct and if the html_url is inside the response
        if response.code != 201 or 'html_url' not in json_response:
            web.badrequest()
        # Returning the html_url
        return json_response['html_url']


if __name__ == "__main__":
    app.run()
