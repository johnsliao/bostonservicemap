import sys
import pandas

from PIL import Image
from config import MIN_LAT, MIN_LON, MAX_LAT, MAX_LON, CANVAS_X, CANVAS_Y

def ll_to_pixel(lat, lon):
    x_frac = (MAX_LAT - lat) / (MAX_LAT - MIN_LAT)
    y_frac = (MAX_LON - lon) / (MAX_LON - MIN_LON)

    x = x_frac * CANVAS_X
    y = y_frac * CANVAS_Y

    return x, y

def load_ll(fname):
    points = []

    data = pandas.read_csv(fname)

    for row in range(len(data.index)):
        lat, lon = data['LATITUDE'][row], data['LONGITUDE'][row]

        points.append([float(lat), float(lon)])

    return points

def main(fname):
    points = load_ll(fname)

    I = Image.new('RGBA', (CANVAS_X, CANVAS_Y))
    IM = I.load()

    for lat, lon in points:
        x, y = ll_to_pixel(lat, lon)
        print x, y

        for x1, y1 in [(x,y),
                       (x+1,y+1),
                       (x-1,y-1),
                       (x-1,y+1),
                       (x+1, y-1),
                       (x+2,y+2),
                       (x-2,y-2),
                       (x-2,y+2),
                       (x+2, y-2)]:
                if 0 <= x1 < CANVAS_X and 0 <= y1 < CANVAS_Y:
                    print 'Adding to canvas'
                    IM[x1,y1] = (0,0,0)

    I.save("./bostonservicemap/sample_data/sample.png", "PNG")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '''Usage
                draw_dots_at_requests.py <service_requests.csv>'''
    else:
        fname = sys.argv[1]
        main(fname)