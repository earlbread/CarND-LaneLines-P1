def get_average_line(lines):
    return [list(map(int, np.average(lines, axis=0)[0]))]

def get_xvalue(line, y_min, y_max):
    for x1, y1, x2, y2 in line:
        slope = (y2 - y1) / (x2 - x1)
        y_intercept = y1 - (slope * x1)

        x_min = int((y_min - y_intercept) / slope)
        x_max = int((y_max - y_intercept) / slope)

    return x_min, x_max

def get_xvalue_from_lines(lines, y_min, y_max):
    average_line = get_average_line(lines)
    return get_xvalue(average_line, y_min, y_max)

prev_left = []
prev_right = []

def clear_prev_lines():
    prev_left.clear()
    prev_right.clear()

def first_order_filter(prev_line, next_line):
    ALPHA  = 0.2
    for i in range(len(next_line)):
        next_line[i] = int(prev_line[i] * (1 - ALPHA) + next_line[i] * ALPHA)

def draw_solid_line(img, lines, prev_line, y_min, y_max):
    SOLIDLINE_COLOR = [0, 255, 0]
    SOLIDLINE_THICKNESS = 12

    next_line = []
    solid_line = []
    if lines:
        x_min, x_max = get_xvalue_from_lines(lines, y_min, y_max)
        next_line = [x_min, y_min, x_max, y_max]

        if prev_line:
            first_order_filter(prev_line, next_line)
        prev_line = next_line

    if next_line:
        solid_line = next_line
    elif prev_line:
        solid_line = prev_line

    if solid_line:
        x1, y1, x2, y2 = solid_line
        cv2.line(img, (x1, y1), (x2, y2), SOLIDLINE_COLOR, SOLIDLINE_THICKNESS)

    return solid_line


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    x_size = img.shape[1]
    x_half = x_size / 2

    y_size = img.shape[0]

    left_lines = []
    right_lines = []

    y_max = img.shape[0]
    y_min = int((y_size / 3) * 2);

    SLOPE_MIN = 0.4
    SLOPE_MAX = 2

    for line in lines:
        for x1,y1,x2,y2 in line:
            # If x1 == x2, slope is infinite
            if x1 == x2:
                continue

            slope = (y2 - y1) / (x2 - x1)

            # Remove noises
            if abs(slope) < SLOPE_MIN or abs(slope) > SLOPE_MAX:
                continue

            if slope < 0:
                if x1 < x_half and x2 < x_half:
                    left_lines.append(line)
            else:
                if x1 > x_half and x2 > x_half:
                    right_lines.append(line)

    global prev_left
    global prev_right

    prev_left = draw_solid_line(img, left_lines, prev_left, y_min, y_max)
    prev_right = draw_solid_line(img, right_lines, prev_right, y_min, y_max)

