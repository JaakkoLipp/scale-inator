from src.scale_inator.main import readinput
import pytest
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


def randlist(lngth, **kwargs):
    lst = kwargs.get("lst", None)
    if lst is None:
        from sys import setrecursionlimit

        # lowering this will lead to A) RecursionError B) a hang
        setrecursionlimit(10**5)

        if type(lngth) is not int:
            raise TypeError("Length is not an integer")
        if lngth == 0:
            return []
        if lngth > 10000:
            # Segmentation fault with larger values
            raise OverflowError("Length too large to handle")

        return randlist(lngth, lst=[])
    else:
        from random import uniform
        if lngth == 0:
            return lst

        def create_rand_num():
            rand = round(uniform(1, 100))
            if len(lst) > 0 and rand == lst[-1]:
                return create_rand_num()
            return rand
        return randlist(lngth-1, lst=lst+[create_rand_num()])


@pytest.mark.timeout(1)
def test_input_quit(capsys, main_setup, monkeypatch):
    arguments = main_setup
    monkeypatch.setattr('builtins.input', lambda _: 'q')
    readinput(arguments)
    captured = capsys.readouterr()
    assert captured.out == "Quitting...\n"


@pytest.mark.timeout(1)
def test_input_scam_detection(capsys, main_setup, monkeypatch):
    arguments = main_setup
    inputs = iter(["20", "20"])
    monkeypatch.setattr('builtins.input', lambda msg: next(inputs))
    try:
        readinput(arguments)
    except StopIteration:
        captured = capsys.readouterr()
        assert re.search("SAME AS PREVIOUS,\nNOT ACCEPTED.\n", captured.out)


@pytest.mark.timeout(2)
def test_input_csv(main_setup, monkeypatch):
    arguments = main_setup
    set_env()
    num_list = randlist(10000)
    print(num_list)
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
                num,
                ((num-1)//20)+1,
                datetime.now().strftime("%d.%m.%Y")
            ),
            csvfile.readline()
        )
