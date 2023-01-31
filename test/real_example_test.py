from ocr import scan, Result


def test_lidl_receipt():
    result: Result = scan("./imgs/receipt_lidl.jpeg")

    lines = result.get_lines()
    assert len(lines) == 18
    assert lines[0].get_text() == "X4.00"
    assert lines[1].get_text() == "LIDL SUPERMERCADOS S.A.U."
    assert lines[2].get_text() == "C/ CONDESA MENCIA S/N (G3)"
    assert lines[3].get_text() == "09006BURGOS"
    assert lines[4].get_text() == "NIF A60195278"
    assert lines[5].get_text() == "WWW.LIDL.ES"
    assert lines[6].get_text() == "EUR"
    assert lines[7].get_text() == "SWEET CORNER/LADRILLOS T 1.09 B"
    assert lines[8].get_text() == "CROWNFIELD/COPOS DE 0,65X 3 1.95 B"
    assert lines[9].get_text() == "TOTAL 3.04"
    assert lines[10].get_text() == "ENTREGADO 5.05"
    assert lines[11].get_text() == "CAMBIO -2,01"
    assert lines[12].get_text() == "IVAX IVA P NETO = PVP"
    assert lines[13].get_text() == "B 10 % 0.28 2.76 3.04"
    assert lines[14].get_text() == "SUMA 0.28 2.76 3.04"
    assert lines[15].get_text() == "REGISTRATE EN LIDL PLUS Y AHORRA"
    assert lines[16].get_text() == "EN TUS PROXIMAS COMPMAS"
    assert lines[17].get_text() == "0471"


def test_tifer_receipt():
    result: Result = scan("./imgs/receipt_tifer.jpg")

    lines = result.get_lines()
    assert len(lines) == 10
    assert lines[0].get_text() == "TIFER"
    assert lines[1].get_text() == "LECHE GAZA ENTERA BRIK LITRO"
    assert lines[2].get_text() == "18X0.94 16.92"
    assert lines[3].get_text() == "PATAT,RUFFLES SALERO 160 GR 1,62"
    assert lines[4].get_text() == "PASTA GALLO HELICES VEGET.450G 1,59"
    assert lines[5].get_text() == "MERMELADA HELIOS FRESA 340 GR. 1,89"
    assert lines[6].get_text() == "PIMIENTO ROJO CAT.1@ 1.78"
    assert lines[7].get_text() == "TOTAL 23.80E"
    assert lines[8].get_text() == "IMP."
    assert lines[9].get_text() == "3,19 10% 0.32"


def test_alcampo_receipt():
    result: Result = scan("./imgs/receipt_alcampo.jpg")

    lines = result.get_lines()
    assert len(lines) == 25
    assert lines[0].get_text() == "AL CAMPO BURGOS"
    assert lines[1].get_text() == "FACTURA SIMPLIFICADA"
    assert lines[2].get_text() == "YOGUR NATURAL 4.29 B"
    assert lines[3].get_text() == "DORADA RACION 13.60 B"
    assert lines[4].get_text() == "REF:2073514013604"
    assert lines[5].get_text() == "PLUMAS INTEG.450 1,31 F"
    assert lines[6].get_text() == "PLUMAS INTEG.450 1,31 F"
    assert lines[7].get_text() == "MACARRON DE GUIS 1,66 F"
    assert lines[8].get_text() == "SPAGHETTI INT 450 SPAGHET INR +25% 1.69 F"
    assert lines[9].get_text() == "TOMATE CANARIO 1,87 E"
    assert lines[10].get_text() == "PECHUGA DE POLLO 3,94 B 3,94 B"
    assert lines[11].get_text() == "REF:2042229003941"
    assert lines[12].get_text() == "CALABACIN GRANEL .70 E"
    assert lines[13].get_text() == "PIMIENTO ITALIAN .22 E"
    assert lines[14].get_text() == "CHAMPINON PIE CO 49 E"
    assert lines[15].get_text() == "HARINA TRIG.FUER 1.63 E"
    assert lines[16].get_text() == "CREMA DENTAL 4.62 A"
    assert lines[17].get_text() == "Q.MEZCLA SEMICUR 3.86 E"
    assert lines[18].get_text() == "HUEVOS CLASE L 2.68 E"
    assert lines[19].get_text() == "EX HUEVOS L DAGU TOT 47.72 1"
    assert lines[20].get_text() == "E TARJETA 47.72"
    assert lines[21].get_text() == "E CAMBIO .00"
    assert lines[22].get_text() == "NUM. TOTAL ART VENDIDOS 17"
    assert lines[23].get_text() == "IMP. % BASE CUOTA"
    assert lines[24].get_text() == "===="
