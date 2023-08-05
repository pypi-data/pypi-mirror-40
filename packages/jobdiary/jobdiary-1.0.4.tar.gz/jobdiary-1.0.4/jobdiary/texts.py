def usage():
    text = """
    jd <command> [options]

Command list:
start : start a diary page
stop : stop a diary page
project : set the current project (options: "<project_name>")
task : set the current task (options: "<task_name>")
report : show a diary report (options: <dd.mm.yyyy>, -m <mm.yyyy>, -w <week>)

    """
    return text
