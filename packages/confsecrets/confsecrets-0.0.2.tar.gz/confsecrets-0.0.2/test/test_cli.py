from base64 import b64decode
from unittest import TestCase

from confsecrets.cli import main_guts, parse_args


def test_newsalt_raw(capsys):
    main_guts('confsecrets', ['newsalt', '--raw'])
    captured = capsys.readouterr()
    assert len(captured.err)==0
    new_salt = eval(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8


def test_newsalt_base64(capsys):
    main_guts('confsecrets', ['newsalt'])
    captured = capsys.readouterr()
    assert len(captured.err)==0
    new_salt = b64decode(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8
