"""
I am responsible for implementing a class that can be used programatically
to make CSV files that Moodle can use upload users.

Moodle's CSV files for upload specification:
are specified here: http://docs.moodle.org/23/en/Upload_users#File_formats_for_upload_users_file

Moodle's CSV files have some challenges:
  * There has to be an equal amount of columns in each row
  * Empty columns in a row is defined as an empty string, so two commas next to each other means null
  * No row can end with a comma

Moodle's import software asks the CSV file to define an enrollment like this:
  * course1 and group1 and cohort1 (where 1 can be any integer) all refer to the same enrollment
  * Below, I call such columns 'dynamic headers'

That logically means that I must:
  * Output in a way that right-shifts dynamic headers
  * To do that, I must keep tabs on the maximum number of items for any those headers (columns)
  * To do that, make sure you keep your rows in line

Idioms:
  * Init the class with no parameters
  * Call build_headers with string of headers
  * Indicate dynamic headers by ENDING WITH AN UNDERSCORE:
        output_file = MoodleCSVFile()
        output_file.build_headers(['username', 'course_', 'cohort_'])
  * Get a row from the class's factory method
  * Build the row's basic columns
        row = output_file.factory()
        row.build_username('Joe Smith')
        row.build_passport('changeme')
  * Build the courses USING AN UNDERSCORE
        row.build_course_(['loves and misses', 'bun', 'ny'])
        row.build_cohort_(['howdy'])
  * Finally, add the row
        output_file.add_row(row)
  * Output
        print(output_file.output())

"""

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

import os
def my_path():
    """ Used to help with debugging """
    return os.path.realpath(__file__)

class moodle_csv_row:
    """
    Represents a row in the file
    Keeps track of how many entries per each header
    So that when you output as CSV all the columns add up to the same number
    """
    
    error_msg_1 = strng("Cannot use strings with dynamic headers, pass list instead. Find more documentation at {path_to_here}",
                        path_to_here = my_path())
    error_msg_2 = strng("Cannot use list with static headers, pass string instead. {newline}{tab}Did you forget to add an underscore when you called the build method??{newline}{tab}Find more documentation at {path_to_here}", path_to_here = my_path())

    
    def __init__(self, header_list):
        self.header_list = header_list
        self.content = {}
        for key in header_list:
            self.content[key] = []

    def build(self, name, objects):
        if isinstance(objects, str):
            if name.endswith('_'):
                raise PSI_Error(self.error_msg_1)
            self.content[name] = [objects]
        elif isinstance(objects, list):
            if not name.endswith('_'):
                raise PSI_Error(self.error_msg_2)
            self.content[name].extend(objects)
        else:
            print(name)
            print(objects)
            raise ValueError("What on earth did you pass?")
        return self

    def build_(self, objects):
            return self.build(self.name, objects)

    def __getattr__(self, name):
        if name.startswith('build_'):
            self.name = name[6:]
            return self.build_
        else:
            return self.__dict__[name]

    def __getitem__(self, name):
        return self.content[name]

    def output(self, max_dict):
        out = []
        for header in self.header_list:
            max = max_dict[header]
            l   = len(self.content[header])
            if l < max:
                for i in range(0, max-l):
                    out.append("")
            out.extend(self.content[header])
        return ",".join(out)

class MoodleCSVFile:
    """
    Programatically create comma-seperated value files that Moodle can use to update itself
    Specification defined at http://docs.moodle.org/23/en/Upload_users#File_formats_for_upload_users_file
    """
    def __init__(self, path=''):
        self.rows = []
        self.header_info = {}   # keeps track of maximum entries per header
        self.header_list = []   # the header list
        self.path = path if path else None

    def add_row(self, r):
        """
        Adds row, and updates header_info so we know how many of them we have to account for
        """
        self.rows.append(r)
        for header in self.header_info.keys():
            this = r[header]
            if not isinstance(this, list):
                continue
            now_max = self.header_info[header]
            if now_max < len(this):
                self.header_info[header] = len(this)

    def factory(self):
        return moodle_csv_row(self.header_list)

    def build_headers(self, objects):
        for o in objects:
            self.header_info[o] = 0
        self.header_list.extend(objects)

    def output(self):
        """
        Writes the data to the file if self.path is defined
        Also returns the data (so you can print to stdout)
        """
        # out is just the header information
        out = []
        for header in self.header_list:
            max = self.header_info[header]
            if not max:
                out.append(header)
            else:
                if header.endswith('_'):
                    for t in range(1, max+1):
                        out.append( header[:-1] + str(t) )
                else:
                    out.append( header )
        # s is the string to pass to the file
        s = ",".join(out) + '\n'
        s += "\n".join([r.output(self.header_info) for r in self.rows])
        if self.path:
            with open(self.path, 'w') as f:
                f.write(s)
        return s

if __name__ == "__main__":

    output_file = MoodleCSVFile()
    output_file.build_headers(['username', 'profile_field_blah', 'course_', 'cohort_'])

    row = output_file.factory()
    row.build_username('Adam Morris')
    row.build_profile_field_blah('boob')
    row.build_course_(['loves and misses', 'bun', 'ny'])
    row.build_cohort_(['howdy'])
    output_file.add_row(row)

    row = output_file.factory()
    row.build_username('Adam Morris')
    row.build_profile_field_blah('blah')
    row.build_course_(['Bunny', 'Ah'])
    row.build_cohort_(['no', 'yes', 'effing'])
    output_file.add_row(row)

    print(output_file.output())
