# This is PSI standard boilerplate import idiom, if you don't understand it, never mind it
# This allows us to run each .py file by calling it from within its parent directory
# (Which is useful for simple debugging and setup procedures)
# Also imports the most common routines (from utils import *)
if __name__ == "__main__":
    import sys
    import os
    print("*** Running as main, dry run ***")
    path = os.path.realpath(__file__)
    # let's find the path to this app's src parent folder
    src_path = None
    while not path == '/':
        path = os.path.split(path)[0]
        if not '__init__.py' in os.listdir(path):
            # src doesn't have an __init__.py file by definition
            src_path = path
            break
    # couldn't find it?
    if not src_path:
        raise ImportError("Could not set up file to import the right tools...")
    sys.path.insert(0, src_path)
# now import the basic necessary utilities we need to run right
from utils import *
# End standard boilerplate

class Credentials:
    """ Just an object that holds credential information """
    def __init__(self, username, password):
        self.username = username
        self.password = password

class FileSystemConnection:
    """
    I am a base class for file system connection to tools
    I use scp to copy files over. Pretty boring stuff.
    """
    def __init__(self):
        print('hi')

    def upload(self, path):
        print(strng("Uploading...", path))

class DatabaseConnection:
    """
    I am a base class for database connections to tools
    """
    def __init__(self, 
                 username,
                 password,
                 kind: 'Only postgres available right now' = 'postgres'):
        self.kind = kind
        self.credentials = Credentials(username, password)
        print(strng("Passed {username} with password {password} to {kind} database", self.credentials, kind=self.kind))


if __name__ == "__main__":

    pass
