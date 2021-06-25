from src.scale_inator.main import readinput
import re


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
