import numpy as np
import cv2 as cv
import time


class Calibrate:
    """Class to calibrate the camera"""

    CALIBRATE_WHITE_PATH = r"imagens\calibrate_white.png"
    CALIBRATE_BLACK_PATH = r"imagens\calibrate_black.png"
    CALIBRATE_GRAY_PATH = r"imagens\calibrate_gray.png"

    def __init__(self, cam, matCam, distorCam):
        self.cam = cam
        self.matCam = matCam
        self.distorCam = distorCam

    def find_edge(self, whiteImg, blackImg):
        """Finds the edge of the projector in the image taken by the camera

        Parameters:
            whiteImg (numpy.ndarray): image taken with the projector with a white background
            blackImg (numpy.ndarray): image taken with the projector with a black background

        Returns:

        """

        diff = cv.absdiff(blackImg, whiteImg)
        cv.imwrite("diff.png", diff)

        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        cv.imwrite("gray.png", gray)

        threshold, thresh = cv.threshold(
            gray, 50, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
        )
        cv.imwrite("thresh.png", thresh)

        # cv.imwrite("./screenshots/calibrate_thresh.png", thresh)
        # cv.imshow("thresh", thresh)
        # Achar contornos
        contours, hier = cv.findContours(
            thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE
        )

        # Calcular maior contorno

        try:
            cnt = contours[0]
            for cont in contours:
                epsilon = 0.01 * cv.arcLength(cont, True)
                approx = cv.approxPolyDP(cont, epsilon, True)
                if (cv.contourArea(cont) > cv.contourArea(cnt)) and (
                    len(approx) == 4
                ):
                    cnt = cont

            # Aproximar maior contorno por um polígono
            epsilon = 0.01 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)

            # Desenhar contorno do polígono na imagem
            mask_draw = thresh.copy()
            mask_draw = cv.cvtColor(mask_draw, cv.COLOR_GRAY2BGR)
            contours_generated = cv.drawContours(
                mask_draw, [approx], -1, (0, 0, 255), 3
            )
            print(f"Número de pontos do polígono: {len(approx)}")
            return approx, cnt, contours_generated
        except Exception as e:
            raise e
            pass

    def find_coordinates(self, approx):
        points = []
        for coord in approx:
            points.append(coord[0])
        points = np.float32(points)
        old_points = [[0, 0], [0, 0], [0, 0], [0, 0]]

        for point in points:
            if np.sum(point) == min(map(np.sum, points)):
                old_points[0] = point
            elif np.sum(point) == max(map(np.sum, points)):
                old_points[3] = point
            elif point[1] / (point[0] + 1) == max(
                map(lambda x: x[1] / (x[0] + 1), points)
            ):
                old_points[2] = point
            else:
                old_points[1] = point
            old_points = np.float32(old_points)
        return old_points

    def get_calibration_image(self, cap, path):
        """Gets the image to calibrate the camera

        Parameters:
            cap (cv.VideoCapture): camera
            path (str): path of the image

        Returns:
            numpy.ndarray: image
        """

        self.show_image(path)
        time.sleep(2)

        status, frame = cap.read()

        aux = 0
        while cap.isOpened() and aux < 30:
            status, frame = cap.read()
            aux += 1

        # Calibrar imagem
        img_mean = self.correct_distortion(frame)

        cv.destroyAllWindows()

        if path == self.CALIBRATE_WHITE_PATH:
            cv.imwrite("img_mean_white.png", img_mean)
        elif path == self.CALIBRATE_BLACK_PATH:
            cv.imwrite("img_black_mean.png", img_mean)

        return img_mean

    def calculate_transformation_matrix(self, old_points):
        """Calculates the transformation matrix"""

        # image = cv.imread(self.CALIBRATE_WHITE_PATH)
        # comprimento, altura = image.shape[1], image.shape[0]
        comprimento, altura = 1024, 768

        new_points = np.float32(
            [[0, 0], [comprimento, 0], [0, altura], [comprimento, altura]]
        )

        M = cv.getPerspectiveTransform(old_points, new_points)

        return M

    def show_image(self, path):
        """Shows the image in full screen"""

        cv.namedWindow("calibration", cv.WINDOW_NORMAL)
        cv.setWindowProperty(
            "calibration", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN
        )
        image = cv.imread(path)
        cv.imshow("calibration", image)
        cv.waitKey(100)

    def correct_distortion(self, image):
        """Corrects the distortion of the camera lens in the image

        Parameters:
            image (numpy.ndarray): image to be corrected

        Returns:
            numpy.ndarray: image corrected
        """

        h, w = image.shape[:2]

        newcameramtx, roi = cv.getOptimalNewCameraMatrix(
            self.matCam, self.distorCam, (w, h), 1, (w, h)
        )
        imgCorr = cv.undistort(
            image, self.matCam, self.distorCam, None, newcameramtx
        )
        x, y, w, h = roi

        imgCorrigida = imgCorr[y : y + h, x : x + w]

        return imgCorrigida

    def run(self):
        """Runs the calibration process"""

        video_cap = cv.VideoCapture(self.cam, cv.CAP_DSHOW)

        whiteImg = self.get_calibration_image(
            video_cap, self.CALIBRATE_WHITE_PATH
        )
        time.sleep(2)
        blackImg = self.get_calibration_image(
            video_cap, self.CALIBRATE_BLACK_PATH
        )

        approx, cnt, countours_generated = self.find_edge(whiteImg, blackImg)

        old_points = self.find_coordinates(approx)

        print(old_points)
        print(old_points[0][1])
        M = self.calculate_transformation_matrix(old_points)

        cv.imshow("projetor", countours_generated)
        cv.waitKey(0)

        video_cap.release()

        return M, old_points


if __name__ == "__main__":
    matCam = np.load(
        r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhomatCam.npy"
    )
    distorCam = np.load(
        r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhodistorCam.npy"
    )

    calibrate = Calibrate(1, matCam, distorCam)

    M = calibrate.run()

    (
        "sahuashudasuhshudashdaduasduasdhuadw",
        "sauhsausahsusahusauhdasuhdashdasuhasasdas",
        "sahusahusahuashusauashusahsauh",
    )
