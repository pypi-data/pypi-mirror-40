# -*- coding: utf-8 -*-

import itertools
import pytest
from cate import cli
import helpers


@pytest.fixture
def parser():
    return cli._create_parser()


class TestArgumentsParsing:
    def test_missing_matrix(self, parser, capsys):
        with pytest.raises(SystemExit):
            parser.parse_args([])
        stderr = capsys.readouterr().err
        assert 'error: the following arguments are required: matrix' in stderr

    @helpers.dict_parametrize('args', {
        'short': ['-x'],
        'long': ['--wrong-long'],
        'mixed': ['-x', '--wrong-long'],
    })
    def test_unknown_arguments(self, parser, capsys, args):
        with pytest.raises(SystemExit):
            parser.parse_args(args + ['matrix'])
        stderr = capsys.readouterr().err
        assert 'error: unrecognized arguments:' in stderr

    @helpers.dict_parametrize('scale', {
        'non_float': 'ImNoFloat',
        'NaN': 'NaN',
        'infinity': 'Inf',
        'too_small': '0.1',
        'too_big': '10',
    })
    def test_invalid_scale(self, parser, capsys, scale):
        with pytest.raises(SystemExit):
            parser.parse_args(['-s', scale, 'matrix'])
        stderr = capsys.readouterr().err
        assert 'cate: error: argument -s/--scale:' in stderr

    @pytest.mark.parametrize('argname', ['-o', '--output', '-s', '--scale'])
    def test_missing_argvalue(self, parser, capsys, argname):
        with pytest.raises(SystemExit):
            parser.parse_args([argname])
        stderr = capsys.readouterr().err
        assert 'cate: error: argument ' in stderr
        assert ': expected one argument' in stderr

    @pytest.mark.parametrize('combination', itertools.product(
        ('', '-s 1.0', '--scale 1.0'),
        ('', '-t', '--complete-flow'),
        ('', '-c', '--no-color'),
        ('', '-o template.svg', '--output template.svg'),
    ))
    def test_valid_combinations(self, parser, combination):
        args = ' '.join(combination).split()  # needed for arguments with a value
        parser.parse_args(args + ['matrix'])
