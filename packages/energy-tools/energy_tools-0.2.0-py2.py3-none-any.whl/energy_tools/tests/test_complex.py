from math import sqrt

builtin_complex = complex
from energy_tools.complex import complex


def test_init():
    assert complex(1, 2) == builtin_complex(1, 2)


def test_phase_simple():
    assert complex(1, 1).phase == 45


def test_phase_quadran_1():
    assert complex(1 + 1j).phase == 45.0


def test_phase_quadran_2():
    assert complex(-1 + 1j).phase == 135.0


def test_phase_quadran_3():
    assert complex(-1 - 1j).phase == 225.0


def test_phase_quadran_4():
    assert complex(1 - 1j).phase == 315.0


def test_phase_0_degres():
    assert complex(1 + 0j).phase == 0.0


def test_phase_90_degres():
    assert complex(0 + 1j).phase == 90.0


def test_phase_180_degres():
    assert complex(-1 + 0j).phase == 180.0


def test_phase_270_degres():
    assert complex(0 - 1j).phase == 270.0


def test_phase_entier_positif():
    assert complex(2).phase == 0.0


def test_phase_decimal_negatif():
    assert complex(-2.12).phase == 180.0


def test_module():
    assert complex(1, 1).module == sqrt(2)
