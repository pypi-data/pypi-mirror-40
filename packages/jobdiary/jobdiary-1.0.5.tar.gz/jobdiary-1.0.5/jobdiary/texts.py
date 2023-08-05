def usage():
    text = """
    jd <command> [parameters]

Command list:
start : start a diary page
stop : stop a diary page
project : set the current project and task (parameters: "<project_name>"* "task_name")
task : set the current task (parameters: "<task_name>"*)
report : show a diary report (parameters: <dd.mm.yyyy> or -m <mm.yyyy> or -w <week>)

(*) = Required parameters
    """
    return text
