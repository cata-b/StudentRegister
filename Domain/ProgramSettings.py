import javaproperties

class ProgramSettings():
    def __init__(self, file):
        PossibleKeys = ["repository", "students", "disciplines", "grades", "UI", "debuglists", "db_connection_string"]
        PossibleRepos = ["inmemory", "txt", "pickle", "json", "db"]
        PossibleUIs = ["Console", "Light", "Dark"]
        PossibleDBGList = ["True", "False"]
        r = None
        self._data = {}
        try:
            r = open(file, 'r')
        except:
            raise FileNotFoundError("%s not found." % file)
        try:
            data = javaproperties.load(r)
            for key in data.keys():
                PossibleKeys.remove(key)
            if len(PossibleKeys) != 0:
                raise Exception
            if data["repository"] not in PossibleRepos or\
               data["UI"] not in PossibleUIs or\
               data["debuglists"] not in PossibleDBGList:
                raise Exception
            self._data = data
        except:
            raise SyntaxError("%s is in a wrong format." % file)
    def __getitem__(self, key):
        return self._data[key]