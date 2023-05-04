# Importe as bibliotecas necessárias
import numpy as np
import cv2
from calibrate import Calibrate
from panel import Panel


def visualize_camera():
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
    # Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
    k = 0
    while 1:
        # Adquira uma imagem
        Sucesso, img = cam.read()

        # A variável Sucesso conterá True se a aquisição for bem-sucedida
        if Sucesso == True:
            cv2.imshow("Imagem", img)
            # Espere por 10 ms que o usuário pressione uma tecla
            k = cv2.waitKey(10)
            # Se o Esc for pressionado (codigo 27) interrompa o loop
        if k == 27:
            break
    cv2.destroyAllWindows()
    cam.release()


def aquire_image(camera, calibration):
    # Inicializa a câmera indicando o numero do dispositivo de captura da imagem
    # (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
    cam = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

    # Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
    # Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
    k = 0
    while 1:
        # Adquira uma imagem
        Sucesso, img = cam.read()
        imgCorrigida = calibration.correct_distortion(img)

        # A variável Sucesso conterá True se a aquisição for bem-sucedida
        if Sucesso == True:
            # Espere por 10 ms que o usuário pressione uma tecla
            k = cv2.waitKey(10)
            return imgCorrigida
        # Se o Esc for pressionado (codigo 27) interrompa o loop
        if k == 27:
            break

    k = cv2.waitKey(-1)
    cv2.destroyAllWindows()
    # É uma boa pratica desalocar a camera antes de encerrar o programa
    cam.release()


# This function identifies the laser and calculate the x and y coordinates
def laser_coordinate(image, old_points):
    # create the mask for saturated color: a mask is the same size as our image, but has only two pixel values: 0 and 255
    black = np.zeros(image.shape, dtype="uint8")
    old_points_copy = old_points.copy()
    old_points_copy = old_points_copy.astype(int)
    old_2 = old_points_copy[2].copy()
    old_points_copy[2] = old_points_copy[3]
    old_points_copy[3] = old_2
    projector = cv2.fillPoly(
        black, pts=[old_points_copy], color=(255, 255, 255)
    )
    # apply the mask to the image
    masked = cv2.bitwise_and(image, projector)

    # tranforms the image to HSV
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 254])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("mask", mask)
    # retangulo = cv2.rectangle(mask, old_points[0], old_points[2], (0, 80, 0), 2)
    # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    # cv2.imshow("mask", retangulo)

    # Calculate the centroid of the mask to have the position of just one pixel
    # Calculate moments of binary image
    M = cv2.moments(mask)
    if M["m00"] != 0:
        # Calculate x,y coordinate of centroid
        X = int(M["m10"] / M["m00"])
        Y = int(M["m01"] / M["m00"])
    else:
        X = 0
        Y = 0
    return (X, Y)


def warp_point(x, y, M):
    d = M[2, 0] * x + M[2, 1] * y + M[2, 2]

    return (
        int((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d),  # x
        int((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d),  # y
    )


# This function draws in the laser in the image
# image: image from camera to be updated
# x: laser x coordinate
# y: laser y coordinate
# color: color to be drawn based on the buttons
# y_panel: panel size
def draw_laser(image, x, y, color):
    global y_panel
    if color == (0, 0, 0):
        if y < round(y_panel - 0.13 * y_panel):
            imagem = cv2.circle(
                image, (x, y), radius=30, color=color, thickness=-1
            )
        else:
            imagem = image
    elif y < round(y_panel - 0.1 * y_panel):
        imagem = cv2.circle(image, (x, y), radius=5, color=color, thickness=-1)
    elif color == (1, 1, 1):
        imagem = Panel().create_panel()
    else:
        imagem = image
    return imagem
