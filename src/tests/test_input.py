from src.scale_inator.main import readinput
import re


def cleantemp():
    from shutil import rmtree
    rmtree(path)


def set_env():
    from atexit import register
    from os import environ
    from tempfile import mkdtemp
    global path
    path = mkdtemp()
    register(cleantemp)
    environ["XDG_DATA_HOME"] = path


def test_input_quit(capsys, main_setup, monkeypatch):
    arguments = main_setup
    monkeypatch.setattr('builtins.input', lambda _: 'q')
    readinput(arguments)
    captured = capsys.readouterr()
    assert captured.out == "Quitting...\n"


def test_input_scam_detection(capsys, main_setup, monkeypatch):
    arguments = main_setup
    inputs = iter(["20", "20"])
    monkeypatch.setattr('builtins.input', lambda msg: next(inputs))
    try:
        readinput(arguments)
    except StopIteration:
        captured = capsys.readouterr()
        assert re.search("SAME AS PREVIOUS,\nNOT ACCEPTED.\n", captured.out)


def test_input_csv(main_setup, monkeypatch):
    arguments = main_setup
    set_env()
    num_list = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    iterate = iter(list(map(str, num_list))+["q"])

    monkeypatch.setattr('builtins.input', lambda msg: next(iterate))
    readinput(arguments)

    from src.scale_inator.data import get_csv_name, xdg_data_dir
    from datetime import datetime
    from os import path as ospath

    csvfile = open(ospath.join(xdg_data_dir(), get_csv_name()), "r")
    for num in num_list:
        assert re.match(
            ("[0-9.]*,{},{},{}").format(
                int(num),
                ((int(num)-1)//20)+1,
                datetime.now().strftime("%d.%m.%Y")
            ),
            csvfile.readline()
        )
