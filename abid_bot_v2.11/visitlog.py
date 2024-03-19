# Visit 3.1.4 log file
ScriptVersion = "3.1.4"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
