from Domain.ProgramSettings import ProgramSettings
from Service.Service import Service

settings = ProgramSettings("settings.properties")

if settings["UI"] == "Console":
    from ConsoleUI import ConsoleUI
    ConsoleUI(Service(settings)).start()
elif settings["UI"] == "Light":
    from GUI import GUI
    GUI(Service(settings)).start()
elif settings["UI"] == "Dark":
    from GUIDark import GUI
    GUI(Service(settings)).start()
