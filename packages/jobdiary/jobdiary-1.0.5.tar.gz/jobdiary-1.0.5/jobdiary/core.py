import datetime
from pathlib import Path
import pprint
import sys
from tinydb import Query, TinyDB
from huepy import *
from jobdiary.texts import usage
from jobdiary import __version__


db = TinyDB(str(Path.home().joinpath("jobdiary.json")))
pp = pprint.PrettyPrinter(indent=4)


def decode_args(args, encoding=None):
    """
    Convert all bytes args to str
    by decoding them using stdin encoding.
    """
    return [
        arg.decode(encoding)
        if type(arg) == bytes else arg
        for arg in args
    ]


def can_start(entries):
    starts_and_stops = [e for e in entries if (e['type'] == 'start') |
                        (e['type'] == 'end')]
    return len(starts_and_stops) % 2 == 0


def can_stop(entries):
    starts_and_stops = [e for e in entries if (e['type'] == 'start') |
                        (e['type'] == 'end')]
    return len(starts_and_stops) % 2 != 0


def can_change(entries):
    return can_stop(entries)


def start(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        if can_start(result['entries']):
            result['entries'].append({'type': 'start',
                                      'time': str(now.time())})
            db.update(result)
        else:
            return bad("unable to start")
    else:
        db.insert({'day': str(now.date()),
                   'entries': [{'type': 'start',
                                'time': str(now.time())}]
                   })
    return run("started!")


def stop(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        if can_stop(result['entries']):
            result['entries'].append({'type': 'end', 'time': str(now.time())})
            db.update(result)
            return run("stopped")
        return bad("unable to stop")
    else:
        return bad("no daily entry found")


def project(args):
    if len(args) == 0:
            return bad("Error: empty project")
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        if can_change(result['entries']):
            result['entries'].append({'type': 'project',
                                      'time': str(now.time()),
                                      'project': args[0]})
            if len(args) > 1:
                result['entries'].append({'type': 'task',
                                          'time': str(now.time()),
                                          'task': args[1]})
            db.update(result)
            return good("Project : " + args[0])
        return bad("unable add entry")
    else:
        return bad("no daily entry found")


def task(args):
    if len(args) == 0:
            return bad("Error: empty task")
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        if can_change(result['entries']):
            result['entries'].append({'type': 'task',
                                      'time': str(now.time()),
                                      'task': args[0]})
            db.update(result)
            return good("Task : " + args[0])
        return bad("unable add entry")
    else:
        return bad("no daily entry found")


def date_is_in_calendar_week(date_string, week_number):
    return (datetime.datetime.strptime(date_string, "%Y-%m-%d")
            .date().isocalendar()[1] == int(week_number))


def report(args):
    now = datetime.datetime.now()
    target_date = now.date()
    entry = Query()
    if len(args) != 0:
        if "-m" in args:
            target_date = ("^" +
                           (datetime.datetime.strptime(args[1], "%m.%Y")
                            .strftime("%Y-%m")) +
                           "*")
        elif "-w" in args:
            return format_results(
                db.search(entry.day.test(date_is_in_calendar_week, args[1])))
        else:
            target_date = (datetime.datetime.strptime(args[0], "%d.%m.%Y")
                           .strftime("%Y-%m-%d"))
    else:
        target_date = now.date()

    return format_results(db.search(entry.day.matches(str(target_date))))


def format_results(results):
    if len(results) > 0:
        return pp.pformat(list(result for result in results))
    else:
        return bad("no entry found")


def main(args=sys.argv[1:]):
    args = decode_args(args)

    include_debug_info = '--debug' in args

    if (len(args) == 0) | ("--help" in args):
        return usage()

    if "--version" in args:
        return __version__

    if include_debug_info:
        print(orange(str(Path.home().joinpath("jobdiary.json"))))
        print(args)

    commands = {
        "start": start,
        "stop": stop,
        "project": project,
        "task": task,
        "report": report
    }

    func = commands.get(args[0], lambda x: """
Invalid command.
Use --help for commands description""")

    return func(args[1:])
