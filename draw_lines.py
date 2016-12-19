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

    for line in lines:
        for x1,y1,x2,y2 in line:
            # If x1 == x2, slope is infinite
            if x1 == x2:
                continue

            slope = (y2 - y1) / (x2 - x1)

            # Remove noises
            if abs(slope) < 0.4 or abs(slope) > 2:
                continue

            if slope < 0:
                if x1 > x_half or x2 > x_half:
                    continue
            else:
                if x1 < x_half or x2 < x_half:
                    continue

            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
