from Domain.ProgramSettings import ProgramSettings
from Service.Service import Service

try:
	settings = ProgramSettings("settings.properties")
except Exception as e:
	print(e)
	print("Press Enter to continue . . .")
	input()
	import sys
	sys.exit(0)

if settings["UI"] == "Console":
    from ConsoleUI import ConsoleUI
    ConsoleUI(Service(settings)).start()
elif settings["UI"] == "Light":
    from GUI import GUI
    GUI(Service(settings)).start()
elif settings["UI"] == "Dark":
    from GUIDark import GUI
    GUI(Service(settings)).start()