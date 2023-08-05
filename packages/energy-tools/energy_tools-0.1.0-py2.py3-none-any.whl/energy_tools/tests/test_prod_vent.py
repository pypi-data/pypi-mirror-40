def test_facteur_utilisation():
    from energy_tools.prod_vent import facteur_utilisation

    P = 4.2  # MW
    heures = [571, 1264, 713, 730, 344, 341, 565, 329, 315, 315, 1431, 1847]
    mw = [
        0.000,
        0.210,
        0.630,
        1.050,
        1.470,
        1.890,
        2.310,
        2.730,
        3.150,
        3.570,
        3.990,
        4.200,
    ]
    ans = facteur_utilisation(heures, mw, P)
    assert round(ans, 3) == 0.555


def test_facteur_de_pertes():
    from energy_tools.prod_vent import facteur_pertes

    P = 4.2  # MW
    heures = [571, 1264, 713, 730, 344, 341, 565, 329, 315, 315, 1431, 1847]
    mw = [
        0.000,
        0.210,
        0.630,
        1.050,
        1.470,
        1.890,
        2.310,
        2.730,
        3.150,
        3.570,
        3.990,
        4.200,
    ]
    ans = facteur_pertes(heures, mw, P)
    assert round(ans, 3) == 0.460


def test_calc_mwh():
    from energy_tools.prod_vent import calc_mwh

    heures = [571, 1264, 713, 730, 344, 341, 565, 329, 315, 315, 1431, 1847]
    mw = [
        0.000,
        0.210,
        0.630,
        1.050,
        1.470,
        1.890,
        2.310,
        2.730,
        3.150,
        3.570,
        3.990,
        4.200,
    ]
    ans = calc_mwh(heures, mw)
    mwh = [0.00, 0.27, 0.45, 0.77, 0.51, 0.64, 1.31, 0.90, 0.99, 1.12, 5.71, 7.76]
    assert ans == mwh
