def get_xvalue(line, y_min, y_max):
    for x1, y1, x2, y2 in line:
        slope = (y2 - y1) / (x2 - x1)
        y_intercept = y1 - (slope * x1)

        x_min = int((y_min - y_intercept) / slope)
        x_max = int((y_max - y_intercept) / slope)

    return x_min, x_max

def get_average_line(lines):
    return [list(map(int, np.average(lines, axis=0)[0]))]

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

            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

    SOLIDLINE_COLOR = [0, 255, 0]
    SOLIDLINE_THICKNESS = 12

    if left_lines:
        left_average_line = get_average_line(left_lines)
        x_min, x_max = get_xvalue(left_average_line, y_min, y_max)

        cv2.line(img, (x_min, y_min), (x_max, y_max), SOLIDLINE_COLOR, SOLIDLINE_THICKNESS)
    if right_lines:
        right_average_line = get_average_line(right_lines)
        x_min, x_max = get_xvalue(right_average_line, y_min, y_max)

        cv2.line(img, (x_min, y_min), (x_max, y_max), SOLIDLINE_COLOR, SOLIDLINE_THICKNESS)
