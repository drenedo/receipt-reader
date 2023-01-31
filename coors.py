

def get_coordinates(prediction):
    """
    it returns x1, x2, y1 and y2 from coordinates from prediction
    """
    return int(prediction[0][0]), int(prediction[2][0]), int(prediction[0][1]), int(prediction[2][1])