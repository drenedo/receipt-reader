from craft import Box, unify


def test_unify_all():
    boxes = [Box(0, 100, 0, 200),
             Box(0, 100, 300, 400),
             Box(0, 100, 500, 600),
             Box(0, 100, 700, 800),
             Box(0, 100, 900, 1000),
             Box(0, 100, 0, 1200)]

    unifed = unify(boxes)

    assert len(unifed) == 1
    assert unifed[0].x1 == 0 and unifed[0].x2 == 100 and unifed[0].y1 == 0 and unifed[0].y2 == 1200


def test_unify_partial():
    boxes = [Box(0, 100, 0, 200),
             Box(0, 100, 300, 400),
             Box(0, 100, 500, 600),
             Box(0, 100, 700, 800),
             Box(0, 100, 900, 1000),
             Box(0, 100, 199, 1200)]

    unifed = unify(boxes)

    assert len(unifed) == 1
    assert unifed[0].x1 == 0 and unifed[0].x2 == 100 and unifed[0].y1 == 0 and unifed[0].y2 == 1200