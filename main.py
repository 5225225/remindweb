import os
import bottle
import subprocess

MSG_SUCCESS = """
<meta http-equiv="refresh" content="5; url=/">
<h3>Your calendar item has been successfully added</h3>
"""

fname = os.path.expanduser("~/.config/remind/web.rem")


@bottle.get("/")
def web_root():
    tpl = bottle.SimpleTemplate(open("main.html").read())

    calendar = subprocess.check_output(
        "remind -w120,3,0 -c3m -b1 ~/.config/remind",
        shell=True)

    return tpl.render(calendar=calendar)


@bottle.post("/add-easy")
def web_post():
    date_spec = bottle.request.forms.get("date_spec")
    delta = bottle.request.forms.get("delta")
    repeat = bottle.request.forms.get("repeat")
    at = bottle.request.forms.get("at")
    tdelta = bottle.request.forms.get("tdelta")
    expiry_date = bottle.request.forms.get("expiry_date")
    start_date = bottle.request.forms.get("start_date")
    duration = bottle.request.forms.get("duration")
    msg = bottle.request.forms.get("msg")

    print(date_spec)
    print(delta)
    print(repeat)
    print(at)
    print(tdelta)
    print(expiry_date)
    print(start_date)
    print(duration)
    print(msg)

    command = []

    command.append("REM")

    if date_spec:
        command.append(date_spec)
    else:
        return "<b>date_spec REQURED. ITEM NOT ADDED</b>"

    if delta:
        command.append("+" + str(delta))

    if repeat:
        command.append("*" + str(repeat))

    if at:
        command.append("AT")
        command.append(at)

    if tdelta:
        if at:
            command.append("+" + tdelta)
        else:
            return "<b>tdelta REQURES at. ITEM NOT ADDED</b>"

    if start_date:
        command.append("FROM")
        command.append(start_date)

    if expiry_date:
        command.append("UNTIL")
        command.append(expiry_date)

    if duration:
        command.append("DURATION")
        command.append(duration)

    if msg:
        command.append("MSG")
        command.append(msg)
    else:
        return "<b>msg REQUIRED. ITEM NOT ADDED</b>"

    toadd = " ".join(command) + "\n"

    with open(fname, "a") as f:
        f.write(toadd)

    return MSG_SUCCESS


@bottle.post("/add-raw")
def web_raw_post():
    toadd = bottle.request.forms.get("rem_command")
    with open(fname, "a") as f:
        f.write(toadd)

    return MSG_SUCCESS


@bottle.route('/static/<path:path>')
def web_static(path):
    return bottle.static_file(
        path,
        root=os.path.expanduser("~/src/remindweb/static"))


bottle.run(host="", port=8888)
