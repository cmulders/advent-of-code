import collections

def create_layes(pixels, width, height):
    layer_size = width*height
    if len(pixels) % layer_size != 0:
        raise ValueError
    
    return [
        pixels[start:start+layer_size]
        for start in range(0, len(pixels), layer_size)
    ]

def find_fewest_zeros(layers):
    counters = [collections.Counter(l) for l in layers]
    zeros = [c[0] for c in counters]
    
    return layers[zeros.index(min(zeros))]

def calculate_one_two_hash(layer):
    counted = collections.Counter(layer)

    return counted[1] * counted[2]

def render(layers):
    
    def render_pixel(vals):
        for val in vals:
            if val != 2:
                return val
        return 2

    pixels = list(map(render_pixel, zip(*layers)))
    
    return pixels