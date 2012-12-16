"""
Responsible for abstract class PSI_Importer_Manager
Takes a bunch of objects and keeps them around in memory
Basic filtering tools provided
"""

class PSI_Importer_Objects:
    """
    Represents the objects
    """
    def __init__(self, klass=None):
        self.klass = klass

    def make_new(self):
        return self.klass()

    def add(self, obj):
        self.append(obj)


class PSI_Importer_Manager:
    """
    Manages the import process
    """
    def __init__(self, factory_class=None):
        """        
        @param factory_class is the object that implements 
        """
        self.objects = PSI_Importer_Objects(factory_class)
        self.define(localhost=True, file_based=True)

    def define(self, localhost=True, file_based=True):
        pass

    def go(self):
        pass
        

if __name__ == "__main__":

    """
    Provides some basic testing tools here
    """
    
