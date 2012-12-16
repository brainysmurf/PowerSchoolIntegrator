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

from exporters.connections import FileSystemConnection, DatabaseConnection, Credentials

class PSIMoodleDatabaseConnection(DatabaseConnection):
    pass

class PSIMoodleFileSystemConnection(FileSystemConnection):

    def __init__(self, credentials, code_directory=None):
        """
        I set attributes accordingly
        I also upload the php command line tool to the right place
        """
        if not code_directory:
            code_directory = input(strng("Enter the path to the www folder on the machine.{newline}Usually it's something like /var/www/moodle{newline}{colon}{space}"))
        self.code_directory = code_directory
        from moodle.exporters.phpgluecode.main import file_name   # get the filename of the php glue code
        self.cli_tool_path = os.path.join(code_directory, 'admin', file_name)
        self.upload(self.cli_tool_path)

class PSIMoodleManualIntegrator:
    """
    Provides manual integration:
        * Uses php code which is uploaded to the admin/cli/ folder
            * There are other ways to integrate manual accounts, but that's by far the most powerful way
            * Works by making system calls directly and does what moodle does when commands are instigated from the front-end
            * Main benefit for K-12 schools is that parent account integration is easy this way
        * Can export csv file for upload users feature
            * Requires more manual work
            * Could be useful to sysadmins familiar with grep tool who want a way to check what enrollments are in one file

    Manual Integration:
        * The accounts, username, passwords, enrollments are stored in moodle database
    """
    def __init__(self, database=None, system=None):
        """
        Initialize the database and system connections
        Parameters:
            database and system can be a Credentials object (imported above)
            or objects that have a username and password attribute
        """
        if database:
            database = PSIMoodleDatabaseConnection(database)
        if system:
            system = PSIMoodleFileSystemConnection(system)
        self.database = database
        self.system   = system

if __name__ == "__main__":

    Moodle = PSIMoodleManualIntegrator(database=Credentials('amorris', 'brainysmurf'),
                                 system=Credentials('root', 'password'))
