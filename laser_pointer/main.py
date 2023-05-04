from calibrate import Calibrate
from panel import Panel

from Integra_Diniz_Giordan import (
    laser_coordinate,
    draw_laser,
    visualize_camera,
    warp_point,
)
import cv2 as cv
import numpy as np
import time

matCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhomatCam.npy"
)
distorCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhodistorCam.npy"
)

visualize_camera()

calibrate = Calibrate(1, matCam, distorCam)
M, old_points = calibrate.run()
panel = Panel().create_panel()

# Inicializa a câmera indicando o numero do dispositivo de captura da imagem
# (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
cam = cv.VideoCapture(1, cv.CAP_DSHOW)
default_color = (0, 0, 0)
cv.namedWindow("Draw", cv.WINDOW_NORMAL)
cv.setWindowProperty("Draw", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

cv.moveWindow("Draw", 1920, 0)

# Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
# Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
k = 0
aux = 0
while 1:
    # Adquira uma imagem
    Sucesso, img = cam.read()
    imgCorrigida = calibrate.correct_distortion(img)

    # A variável Sucesso conterá True se a aquisição for bem-sucedida
    if Sucesso == True:
        # Espere por 10 ms que o usuário pressione uma tecla
        k = cv.waitKey(1)
        X, Y = laser_coordinate(imgCorrigida, old_points)
        x, y = warp_point(X, Y, M)
        if aux == 0:
            color = Panel().execute_button(x, y, panel, default_color)
            draw = draw_laser(panel, x, y, color)
        else:
            color = Panel().execute_button(x, y, draw, color)
            draw = draw_laser(draw, x, y, color)
        # cv.resize(draw, (1024, 768))
        cv.imshow("Draw", draw)
        if aux == 0:
            time.sleep(1)
        aux += 1
    # Se o Esc for pressionado (codigo 27) interrompa o loop
    if k == 27:
        break


cv.destroyAllWindows()
# É uma boa pratica desalocar a camera antes de encerrar o programa
cam.release()
