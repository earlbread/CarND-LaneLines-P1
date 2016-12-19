def process_pipeline(image):
    imshape = image.shape

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    yellow = cv2.inRange(hsv, (20, 50, 50), (50, 255, 255))
    white = cv2.inRange(hsv, (0, 0, 180), (255, 25, 255))

    gray = cv2.bitwise_or(yellow, white)

    KERNEL_SIZE  = 7  # Kernel size for Gaussian blur
    blurred_gray = gaussian_blur(gray, KERNEL_SIZE)

    LOW_THRESHOLD  = 50  # Low threshold for canny
    HIGH_THRESHOLD = 150  # High threshold for canny

    canny_image = canny(blurred_gray, LOW_THRESHOLD, HIGH_THRESHOLD)

    # Region to mask
    X_LEFT_BOTTOM  = int((imshape[1] / 20) * 2)
    X_LEFT_TOP     = int((imshape[1] / 20) * 8)
    X_RIGHT_TOP    = int((imshape[1] / 20) * 13)
    X_RIGHT_BOTTOM = int((imshape[1] / 20) * 19)

    Y_TOP          = int((imshape[0] / 3) * 2)
    Y_BOTTOM       = imshape[0]

    vertices = np.array([[(X_LEFT_BOTTOM,Y_BOTTOM),
                          (X_LEFT_TOP, Y_TOP),
                          (X_RIGHT_TOP, Y_TOP),
                          (X_RIGHT_BOTTOM, Y_BOTTOM)]], dtype=np.int32)

    selected_image = region_of_interest(canny_image, vertices)

    # Parameters for Hough transfrom
    RHO          = 2
    THETA        = np.pi / 180
    THRESHOLD    = 40
    MIN_LINE_LEN = 5
    MAX_LINE_GAP = 30

    hough_image = hough_lines(selected_image, RHO, THETA, THRESHOLD, MIN_LINE_LEN, MAX_LINE_GAP)
    result = weighted_img(hough_image, image)

    cv2.polylines(result, vertices, True, [0, 255, 0], thickness=2, lineType=8, shift=0)

    return result
