from craft import Box, get_overlapped_percent


def test_not_chopped_lines():
    box1 = Box(0, 50, 0, 70)
    box2 = Box(10, 150, 10, 170)
    percentage_overlapped = get_overlapped_percent(box1, box2)

    assert percentage_overlapped == 68


def test_not_chopped_lines():
    box1 = Box(143, 460, 286, 324)
    box2 = Box(143, 461, 287, 324)
    percentage_overlapped = get_overlapped_percent(box1, box2)

    assert percentage_overlapped == 102


def test_not_chopped_lines_2():
    box1 = Box(226, 692, 363, 387)
    box2 = Box(228, 690, 379, 395)
    percentage_overlapped = get_overlapped_percent(box1, box2)

    assert percentage_overlapped == 50