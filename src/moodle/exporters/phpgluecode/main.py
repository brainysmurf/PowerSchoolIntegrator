file_name = 'phpclimoodle.php'

if __name__ == "__main__":
    import os
    path = os.path.realpath(__file__)
    path = os.path.split(path)[0]
    if not file_name in os.listdir(path):
        print("** Change the file_name variable here! **")
        print("** Moodle direct integration won't work otherwise! **")
