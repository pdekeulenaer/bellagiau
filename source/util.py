from pymunk.vec2d import Vec2d


SCALE_PX_TO_M = 50 #defines how many pixels go in 1 meter
FRAMES_PER_SECOND = 60

def get_pixels_from_meters(meters):
    return meters * SCALE_PX_TO_M

def get_pxspeed_from_kph(km_per_hour):
    # convert kph to m/s
    meters_per_second = (km_per_hour * 1000.0) / 3600.0
    pixels_per_second = get_pixels_from_meters(meters_per_second)
    # pixels_per_frame = pixels_per_second / FRAMES_PER_SECOND
    return pixels_per_second

def get_vector_difference(x,y, x2,y2):
    return (Vec2d(x,y)-Vec2d(x2,y2))

def is_in_range(value, start, end):
    return (value >= start and value <= end)

def is_in_range(value, range_list):
    assert(len(range_list) == 2)
    return is_in_range(value, range_list[0], range_list[1])

def show_figures():
    print("Parcours for 1km: ", get_pixels_from_meters(1000))
    print("Starting speed 40km/h", get_pxspeed_from_kph(40))
    print("Pixelsize for asset", get_pixels_from_meters(1.75))

