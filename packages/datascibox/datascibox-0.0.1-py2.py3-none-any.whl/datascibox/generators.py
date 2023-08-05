def odds(stream):
    for x in stream:
        if x%2==1:
            yield x

def evens(stream):
    for x in stream:
        if x%2==0:
            yield x

def range_2d(width, height):
    """Produce a stream of 2-D coordinates
    """
    for y in range(height):
        for x in range(width):
            yield x, y
