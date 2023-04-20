# Importe as bibliotecas necessárias
import numpy as np
import cv2

# Correção da distorção da imagem:
# O programa abaixo usa as matrizes matCam e distorCam previamente calculadas
# para corrigir as distorções da lente da câmera (almofada/barril) na imagem especificada.
# As matrizes matCam e distorCam são lidas de arquivo
# Definir caminho dos arquivos:
# Defina o Caminho para a pasta onde estão os arquivos matCam e distorCam
# Caminho = r"C:\Users\giord\OneDrive\Documentos\Aula\Visao_Comp\Trabalho"
# Lendo arquivos das matrizes da câmera e dos coeficientes que corrigem as distorções da lente:
# matCam = np.load(rf"{Caminho}\TrabalhomatCam.npy")
# distorCam = np.load(rf"{Caminho}\TrabalhodistorCam.npy")

# Create the colors to be called when applied the button's function
red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# This function draws in the laser in the image
# image: image from camera to be updated
# color: color to be drawn based on the buttons


def draw_laser(image, color, old_points):
    image = image[
        int(old_points[0][1]) : int(old_points[3][1]),
        int(old_points[0][0]) : int(old_points[3][0]),
    ]
    # first, tranforms the image to HSV
    cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # create the mask for saturated color: a mask is the same size as our image, but has only two pixel values: 0 and 255
    mask = np.zeros(image.shape[:2], dtype="uint8")
    lower = np.array([240, 240, 240])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(image, lower, upper)

    # Calculate the centroid of the mask to have the position of just one pixel
    # Calculate moments of binary image
    M = cv2.moments(mask)
    if M["m00"] != 0:
        # Calculate x,y coordinate of centroid
        X = int(M["m10"] / M["m00"])
        Y = int(M["m01"] / M["m00"])
        imagem = cv2.circle(image, (X, Y), radius=2, color=color, thickness=-1)
    else:
        imagem = image

    return imagem


# Inicializa a câmera indicando o numero do dispositivo de captura da imagem
# (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
# cam = cv2.VideoCapture(0)

# # Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
# # Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
# k = 0
# contagem = 1
# while 1:
#     # Adquira uma imagem
#     Sucesso, img = cam.read()
#     # A variável Sucesso conterá True se a aquisição for bem-sucedida
#     if Sucesso == True:
#         # Desenha o laser na imagem e retorna a imagem desenhada
#         # A imagem passada pra função draw_laser deve ser apenas a imagem do projetor
#         # A cor passada pra função draw_laser deve ser definida conforme a função do botão selecionado
#         cv2.imshow("imagem", draw_laser(img, red))
#         # Espere por 10 ms que o usuário pressione uma tecla
#         k = cv2.waitKey(10)
#         # Se o Esc for pressionado (codigo 27) interrompa o loop
#     if k == 27:
#         break

# k = cv2.waitKey(-1)
# cv2.destroyAllWindows()

# # É uma boa pratica desalocar a camera antes de encerrar o programa
# cam.release()
