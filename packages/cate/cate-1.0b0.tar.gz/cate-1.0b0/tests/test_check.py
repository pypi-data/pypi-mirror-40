# -*- coding: utf-8 -*-

import pytest
from cate import check


# pylint: disable=missing-docstring
class TestCheck:
    TEST_MATRICES = {
        '2x2_fail_square': ((0, 0), (0, )),
        '2x3_fail_square': ((0, 1, 2), (3, 4, 5)),
        '3x3_fail_symmetric': ((-1, 0, -1), (-1, 0, 0), (-1, 0, 1)),
        '2x2_fail_diagonal': ((0, 0), (0, 2)),
        '4x4_fail_neighbors': ((3, 2, 2, 3), (2, 2, 2, 3), (2, 2, 3, 4), (3, 3, 4, 4)),
        '4x4_fail_final-position': ((0, 0, 0, -1), (0, 1, 0, 0), (0, 0, 0, -1), (-1, 0, -1, -1)),
        '2x2-0_fail_submatrix': ((0, 1), (1, 1)),
        '2x2-1_fail_submatrix': ((1, 2), (2, 2)),
        '2x2-2_fail_submatrix': ((-1, -1), (-1, -2)),
        '3x3_fail_submatrix': ((-1, -1, -1), (-1, -2, -2), (-1, -2, -3)),
        '4x4_fail_planarity': ((0, 0, 0, 0), (0, 1, 0, -1), (0, 0, 0, -1), (0, -1, -1, -1)),
        '2x2_ok': ((0, 0), (0, 1)),
        '4x4_ok': ((-1, -1, -1, -1), (-1, 0, 0, 0), (-1, 0, 1, 1), (-1, 0, 1, 2)),
    }

    @pytest.mark.parametrize('input_', (
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_is_square(self, input_):
        assert check.is_square(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x2_fail_square',
        '2x3_fail_square',
    ))
    def test_ko_is_square(self, input_):
        assert not check.is_square(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_is_symmetric(self, input_):
        assert check.is_symmetric(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '3x3_fail_symmetric',
    ))
    def test_ko_is_symmetric(self, input_):
        assert not check.is_symmetric(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '3x3_fail_symmetric',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_diagonal_criterion(self, input_):
        assert check._diagonal_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
    ))
    def test_ko_diagonal_criterion(self, input_):
        assert not check._diagonal_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_neighbors_criterion(self, input_):
        assert check._neighbors_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
    ))
    def test_ko_neighbors_criterion(self, input_):
        assert not check._neighbors_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_final_position_criterion(self, input_):
        assert check._final_position_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
    ))
    def test_ko_final_position_criterion(self, input_):
        assert not check._final_position_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_is_continuous(self, input_):
        assert check.is_continuous(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
    ))
    def test_ko_is_continuous(self, input_):
        assert not check.is_continuous(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x3_fail_square',
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_final-position',
        '4x4_fail_planarity',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_submatrix_criterion(self, input_):
        assert check._submatrix_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '4x4_fail_neighbors',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
    ))
    def test_ko_submatrix_criterion(self, input_):
        assert not check._submatrix_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2_fail_diagonal',
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_planarity_criterion(self, input_):
        assert check._planarity_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '4x4_fail_planarity',
    ))
    def test_ko_planarity_criterion(self, input_):
        assert not check._planarity_criterion(self.TEST_MATRICES[input_])  # pylint: disable=protected-access

    @pytest.mark.parametrize('input_', (
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_is_deterministic(self, input_):
        assert check.is_deterministic(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
    ))
    def test_ko_is_deterministic(self, input_):
        assert not check.is_deterministic(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x2_ok',
        '4x4_ok',
    ))
    def test_valid_is_linking(self, input_):
        assert check.is_linking(self.TEST_MATRICES[input_])

    @pytest.mark.parametrize('input_', (
        '2x3_fail_square',
        '3x3_fail_symmetric',
        '2x2_fail_diagonal',
        '4x4_fail_neighbors',
        '4x4_fail_final-position',
        '2x2-0_fail_submatrix',
        '2x2-1_fail_submatrix',
        '2x2-2_fail_submatrix',
        '3x3_fail_submatrix',
        '4x4_fail_planarity',
    ))
    def test_ko_is_linking(self, input_):
        assert not check.is_linking(self.TEST_MATRICES[input_])
