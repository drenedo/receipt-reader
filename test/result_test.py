from ocr import Result, Coord, TextCoordinates


def test_line_result():
    results = Result([TextCoordinates("LIFER",Coord(401, 235), Coord(844,477)),
        TextCoordinates("LECHE GAZA ENTERA BRIK LITRO",Coord(46,685), Coord(804 ,745)),
        TextCoordinates("16.92",Coord(993,746), Coord(1136,798)),
        TextCoordinates("18X0.94",Coord(50, 755), Coord(249 ,831)),
        TextCoordinates("ITEM",Coord(1001, 800), Coord(1132,818)),
        TextCoordinates("1.04",Coord(1023, 837), Coord(1142,887)),
        TextCoordinates("PAIAT, KUFFLES SALERO IOU GR",Coord(44, 842), Coord(785 ,892)),
        TextCoordinates("-",Coord(789,875), Coord(798 ,886)),
        TextCoordinates("1.59",Coord(1023, 903), Coord(1142,953)),
        TextCoordinates("PASIA GALLU HELICES VEGET.4300", Coord(42, 908), Coord(863 ,954)),
        TextCoordinates("MERMELADA HELIUS FRESA 340 UR.", Coord(44, 977), Coord(856 ,1030)),
        TextCoordinates("1.89",Coord(1029, 966), Coord(1141,1019)),
        TextCoordinates(":",Coord(845,1002), Coord(855 ,1013)),
        TextCoordinates("1.78",Coord(1030, 1035), Coord(1144,1088)),
        TextCoordinates("PIMIENTO RUJO CAL.LE",Coord(42, 1045), Coord(601 ,1091)),
        TextCoordinates("23.80E",Coord(945,1225), Coord(1197,1321)),
        TextCoordinates("TOTAL",Coord(47, 1251), Coord(256 ,1331)),
        TextCoordinates("IMP",Coord(871,1365), Coord(953 ,1427)),
        TextCoordinates("D. IMP.",Coord(50, 1400), Coord(215 ,1435)),
        TextCoordinates("10.70",Coord(281,1400), Coord(414 ,1430)),
        TextCoordinates("+ YA",Coord(555,1400), Coord(630 ,1416)),
        TextCoordinates("MM",Coord(691,1400), Coord(738 ,1407)),
        TextCoordinates("***",Coord(1044, 1400), Coord(1143,1411)),
        TextCoordinates("1,51",Coord(307, 1450), Coord(414 ,1487)),
        TextCoordinates("0.70",Coord(688, 1450), Coord(736 ,1468)),
        TextCoordinates("0.00",Coord(1031, 1450), Coord(1145,1480)),
        TextCoordinates("10%",Coord(661, 1500), Coord(742 ,1543)),
        TextCoordinates("0.32",Coord(1033, 1500), Coord(1151,1556)),
        TextCoordinates("3,19",Coord(301, 1504), Coord(422 ,1562))])

    lines = results.get_lines()

    assert len(lines) == 11
    assert lines[7].get_text() == "TOTAL 23.80E"
