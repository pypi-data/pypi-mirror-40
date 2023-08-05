from . files import *


def process_image(fn, debug=False):

    #  Read image from file
    img = cv.imread(fn, 0)
    if img is None:
        print("Failed to load", fn)
        return None

    #  Locate chessboard corners in images
    found, corners = cv.findChessboardCorners(img, pattern_size)
    if found:
        term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.001)
        cv.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

    #  Debug: Draw chessboard on image
    if debug:
        vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        cv.drawChessboardCorners(vis, pattern_size, corners, found)
        _path, name, _ext = splitfn(fn)
        outfile = os.path.join(_path, name + '_chess.png')
        cv.imwrite(outfile, vis)

    #  Return None if the chessboard is not founf
    if not found:
        print('Chessboard not found')
        return None

    #  Print status
    print('{}... OK'.format(fn))

    return (corners.reshape(-1, 2), pattern_points)
