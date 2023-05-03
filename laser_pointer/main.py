from calibrate import Calibrate

from Integra_Diniz_Giordan import (
    panel_creation,
    laser_coordinate,
    button_function,
    draw_laser,
    visualize_camera,
    aquire_image,
    warp_point,
    bxy,
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
panel = panel_creation()
# camera = aquire_image(1, calibrate)
# X, Y = laser_coordinate(camera, old_points)
# x, y = warp_point(X, Y, M)
# color = button_function(x, y, panel)
# draw = draw_laser(panel, x, y, color)
# cv.destroyAllWindows()

# Inicializa a câmera indicando o numero do dispositivo de captura da imagem
# (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
cam = cv.VideoCapture(1, cv.CAP_DSHOW)
default_color = (0, 0, 0)
cv.namedWindow("Draw", cv.WINDOW_NORMAL)
cv.setWindowProperty("Draw", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

cv.moveWindow("Draw", 1920, 0)

# print("Red:")
# print(f"x1 :{bxy('Red', 0)[0]}", f"x2 :{bxy('Red', 1)[0]}")
# print(f"y1 :{bxy('Red', 0)[1]}", f"y2 :{bxy('Red', 1)[1]}")
# print("Blue")
# print(f"x1 :{bxy('Blue', 0)[0]}", f"x2 :{bxy('Blue', 1)[0]}")
# print(f"y1 :{bxy('Blue', 0)[1]}", f"y2 :{bxy('Blue', 1)[1]}")

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
            color = button_function(x, y, panel, default_color)
            draw = draw_laser(panel, x, y, color)
        else:
            color = button_function(x, y, draw, color)
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

# while 1:
#     cv.imshow("Draw", draw)
#     X, Y = laser_coordinate(camera, old_points)
#     x, y = warp_point(X, Y, M)
#     color = button_function(x, y, panel)
#     draw = draw_laser(panel, x, y, color)
#     k = cv.waitKey(10)
#     if k == 27:
# break

# cv.destroyAllWindows()
# # É uma boa pratica desalocar a camera antes de encerrar o programa
# cv.VideoCapture(1, cv.CAP_DSHOW).release()
