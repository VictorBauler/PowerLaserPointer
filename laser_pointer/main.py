from calibrate import Calibrate

from Integra_Diniz_Giordan import (
    panel_creation,
    laser_coordinate,
    button_function,
    draw_laser,
)
import cv2 as cv
import numpy as np

cam = cv.VideoCapture(1, cv.CAP_DSHOW)

# Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
# Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
k = 0
contagem = 1
while 1:
    # Adquira uma imagem
    Sucesso, img = cam.read()

    # A variável Sucesso conterá True se a aquisição for bem-sucedida
    if Sucesso == True:
        cv.imshow("Imagem", img)
        # Espere por 10 ms que o usuário pressione uma tecla
        k = cv.waitKey(10)
        # Se o Esc for pressionado (codigo 27) interrompa o loop
    if k == 27:
        break
cv.destroyAllWindows()
cam.release()
matCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhomatCam.npy"
)
distorCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhodistorCam.npy"
)

calibrate = Calibrate(1, matCam, distorCam)
M, old_points = calibrate.run()
red = (0, 0, 255)

panel_creation()

# Inicializa a câmera indicando o numero do dispositivo de captura da imagem
# (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
cam = cv.VideoCapture(1, cv.CAP_DSHOW)

# Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
# Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
k = 0
contagem = 1
while 1:
    # Adquira uma imagem
    Sucesso, img = cam.read()
    imgCorrigida = calibrate.correct_distortion(img)

    # A variável Sucesso conterá True se a aquisição for bem-sucedida
    if (Sucesso == True) and contagem > 1:
        coords = laser_coordinate(img, lastImg, old_points)
        # Desenha o laser na imagem e retorna a imagem desenhada
        # A imagem passada pra função draw_laser deve ser apenas a imagem do projetor
        # A cor passada pra função draw_laser deve ser definida conforme a função do botão selecionado
        imgLaser = draw_laser(img, coords[0], coords[1], red)

        imgCorrigida = calibrate.correct_distortion(imgLaser)

        cv.imshow("Imagem", imgCorrigida)
        # Espere por 10 ms que o usuário pressione uma tecla
        k = cv.waitKey(10)
        # Se o Esc for pressionado (codigo 27) interrompa o loop
    if k == 27:
        break
    elif (k == 43) or (k == 13):
        cv.imwrite("LaserPointer.png", imgCorrigida)

    lastImg = imgCorrigida
    contagem += 1

k = cv.waitKey(-1)
cv.destroyAllWindows()

# É uma boa pratica desalocar a camera antes de encerrar o programa
cam.release()

# new_image = cv.warpPerspective(frame,M,(comprimento,altura))
