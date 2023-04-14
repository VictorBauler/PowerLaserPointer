# Importe as bibliotecas necessárias
import numpy as np
import cv2

# Correção da distorção da imagem:
# O programa abaixo usa as matrizes matCam e distorCam previamente calculadas
# para corrigir as distorções da lente da câmera (almofada/barril) na imagem especificada.
# As matrizes matCam e distorCam são lidas de arquivo
# Definir caminho dos arquivos:
# Defina o Caminho para a pasta onde estão os arquivos matCam e distorCam
Caminho = r"C:\Users\giord\OneDrive\Documentos\Aula\Visao_Comp\Trabalho"
# Lendo arquivos das matrizes da câmera e dos coeficientes que corrigem as distorções da lente:
matCam = np.load(rf"{Caminho}\TrabalhomatCam.npy")
distorCam = np.load(rf"{Caminho}\TrabalhodistorCam.npy")


# Função que corrigem a distorção da imagem:
def corrige_distorcao(imagem):
    # Encontre as dimensões da imagem
    h, w = img.shape[:2]
    # Otimize a matriz da câmera
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        matCam, distorCam, (w, h), 1, (w, h)
    )
    # Corrija a distorção da imagem
    imgCorr = cv2.undistort(img, matCam, distorCam, None, newcameramtx)
    # é possível recortar a imagem distorcida para evitar regiões pretas
    # use os limites defindos pela roi (region of interest)
    x, y, w, h = roi
    # Recorte as bordas irregulares
    imgCorrigida = imgCorr[y : y + h, x : x + w]
    ## cv2.namedWindow('ImagemCorrigida')
    # cv2.namedWindow('ImagemCorrigida')
    ## Mostra imagem corrigida
    # cv2.imshow('ImagemCorrigida', imgCorrigida)
    return imgCorrigida


# Identifica o laser e retorna a mascará:
def laser_position(imagem):
    # a mask is the same size as our image, but has only two pixel values: 0 and 255

    # transformar imagem em hsv
    cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    mask = np.zeros(imagem.shape[:2], dtype="uint8")

    # treshold (à definir com testes):
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 0, 240])
    upper1 = np.array([10, 255, 255])
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160, 0, 240])
    upper2 = np.array([179, 255, 255])

    lower_mask = cv2.inRange(imagem, lower1, upper1)
    upper_mask = cv2.inRange(imagem, lower2, upper2)

    mask = lower_mask + upper_mask

    # Calculate the centroid of the mask to have the position of just one pixel
    # Calculate moments of binary image
    M = cv2.moments(mask)
    # Calculate x,y coordinate of centroid
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return (cX, cY)


# Inicializa a câmera indicando o numero do dispositivo de captura da imagem
# (geralmente 0 funciona quando só ha uma câmera em uso. Use 1 para uma segunda câmera etc)
cam = cv2.VideoCapture(1)

# Para mostrar uma imagem ao vivo, adquira sequencialmente várias imagens
# Para isso, inicie um loop sem fim até que a tecla Esc (codigo 27) seja pressionada
k = 0
contagem = 1
while 1:
    # Adquira uma imagem
    Sucesso, img = cam.read()
    # A variável Sucesso conterá True se a aquisição for bem-sucedida
    if Sucesso:
        corrige_distorcao(img)

    # Espere por 10 ms que o usuário pressione uma tecla
    k = cv2.waitKey(10)
    # Se o Esc for pressionado (codigo 27) interrompa o loop
    if k == 27:
        break

k = cv2.waitKey(-1)
cv2.destroyAllWindows()

# É uma boa pratica desalocar a camera antes de encerrar o programa
cam.release()
