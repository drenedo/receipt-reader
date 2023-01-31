from craft import Box, chop_big_boxes


def test_not_chopped_lines():
    boxes = [Box(0, 100, 0, 200),
             Box(0, 100, 300, 400),
             Box(0, 100, 500, 600),
             Box(0, 100, 700, 800),
             Box(0, 100, 900, 1000),
             Box(0, 100, 1100, 1200)]

    chopped = chop_big_boxes(boxes)

    assert len(chopped) == 6


def test_chopped_lines():
    boxes = [Box(0, 100, 100, 200),
             Box(0, 100, 300, 400),
             Box(0, 100, 500, 600),
             Box(0, 100, 700, 800),
             Box(0, 100, 900, 1000),
             Box(5, 20, 400, 1200)]

    chopped = chop_big_boxes(boxes)

    assert len(chopped) == 9
    # assert chopped[6].x1 == 0 and chopped[6].x2 == 100 and chopped[6].y1 == 500 and chopped[6].y2 == 600
    # assert chopped[7].x1 == 0 and chopped[7].x2 == 100 and chopped[7].y1 == 700 and chopped[7].y2 == 800
    # assert chopped[8].x1 == 0 and chopped[8].x2 == 100 and chopped[8].y1 == 900 and chopped[8].y2 == 1000
