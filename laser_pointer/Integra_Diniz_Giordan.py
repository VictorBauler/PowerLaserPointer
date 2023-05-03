# Importe as bibliotecas necessárias
import numpy as np
import cv2
from calibrate import Calibrate


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


# Create a blank panel for writing (16:9)
y_panel = 768  # 720
x_panel = 1024  # 1280

# Define the buttons position
# definição do y dos botões
y_button1 = round(
    y_panel - (0.1 * y_panel * 0.2)
)  # 20% do menu de ferramentas espaço em branco abaixo dos botões
y_button2 = round(
    y_panel - (0.1 * y_panel * 0.82)
)  # 62% é o tamanho do botão abaixo do espaçamento
# definição do x dos botões
x_r1, y_r1 = 395, 600  # round(y_button1)
x_r2, y_r2 = 525, 600  # round(y_button2)
x_b1, y_b1 = 535, 600  # round(y_button1)
x_b2, y_b2 = 665, 600  # round(y_button2)
x_g1, y_g1 = 675, 600  # round(y_button1)
x_g2, y_g2 = 805, 600  # round(y_button2)
x_res1, y_res1 = 10, round(y_button1)
x_res2, y_res2 = 160, round(y_button2)
x_sav1, y_sav1 = 1000, 620
x_sav2, y_sav2 = 1150, 660


# Function for creation of the Panel
def panel_creation():
    global x_panel, y_panel, x_r1, y_r1, x_r2, y_r2, x_b1, y_b1, x_b2, y_b2, x_g2, y_g2, x_res1, y_res1, x_res2, y_res2, x_sav1, y_sav1, x_sav2, y_sav2

    panel = np.zeros((y_panel, x_panel, 3), np.uint8)  # creation of the panel

    # Draw line to separate buttons from writing area
    y_line = round(
        y_panel - 0.1 * y_panel
    )  # 10% do painel inferior é para o menu de ferramentas
    cv2.line(panel, (0, y_line), (1200, y_line), (12, 12, 12), 2)

    # Draw color selection buttons on panel

    x_r1, y_r1, round(y_button1)
    x_r2, y_r2, round(y_button2)
    x_b1, y_b1, round(y_button1)
    x_b2, y_b2, round(y_button2)
    x_g1, y_g1, round(y_button1)
    x_g2, y_g2, round(y_button2)

    # Criação dos botões
    cv2.rectangle(
        panel, (x_r1, y_r1), (x_r2, y_r2), (0, 0, 15), -1
    )  # Red button  / (top left corner) (bottom right corner)
    cv2.rectangle(
        panel, (x_b1, y_b1), (x_b2, y_b2), (0, 15, 0), -1
    )  # Blue button
    cv2.rectangle(
        panel, (x_g1, y_g1), (x_g2, y_g2), (15, 0, 0), -1
    )  # Green button
    # Definição dos botões reset e Save
    x_res1, y_res1, round(y_button1)
    x_res2, y_res2, round(y_button2)

    # Criação dos botões de reset e save
    cv2.rectangle(
        panel, (x_res1, y_res1), (x_res2, y_res2), (30, 30, 30), -1
    )  # Reset button
    cv2.rectangle(
        panel, (x_sav1, y_sav1), (x_sav2, y_sav2), (30, 30, 30), -1
    )  # Save button
    # Texto dos botões reset e save (com alinhamento)

    res_text_size = cv2.getTextSize("Reset", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[
        0
    ]
    res_text_x = x_res1 + (x_res2 - x_res1 - res_text_size[0]) // 2
    res_text_y = y_res1 + (y_res2 - y_res1 + res_text_size[1]) // 2

    sav_text_size = cv2.getTextSize("Save", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[
        0
    ]
    sav_text_x = x_sav1 + (x_sav2 - x_sav1 - sav_text_size[0]) // 2
    sav_text_y = y_sav1 + (y_sav2 - y_sav1 + sav_text_size[1]) // 2

    cv2.putText(
        panel,
        "Reset",
        (res_text_x, res_text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (30, 30, 30),
        2,
    )  # Reset text
    cv2.putText(
        panel,
        "Save",
        (sav_text_x, sav_text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (30, 30, 30),
        2,
    )  # Save text

    return panel


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

    lower = np.array([0, 0, 220])
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


# Define a function to handle the buttons
def button_function(x, y, img, color):
    global x_panel, y_panel, x_r1, y_r1, x_r2, y_r2, x_b1, y_b1, x_b2, y_b2, x_g2, y_g2, x_res1, y_res1, x_res2, y_res2, x_sav1, y_sav1, x_sav2, y_sav2
    if x_r1 <= x <= x_r2 and y_r1 <= y <= y_r2:
        color = (0, 0, 255)  # Red button selected
    elif x_b1 <= x <= x_b2 and y_b1 <= y <= y_b2:
        color = (255, 0, 0)  # Blue button selected
    elif x_g1 <= x <= x_g2 and y_g1 <= y <= y_g2:
        color = (0, 255, 0)  # Green button selected
    elif x_res1 <= x <= x_res2 and y_res1 <= y <= y_res2:
        color = (1, 1, 1)  # Reset
    elif x_sav1 <= x <= x_sav2 and y_sav1 <= y <= y_sav2:
        color = color
        saved_img = img.copy()  # save current image
        cv2.imwrite("saved_image.jpg", saved_img)  # Save image to directory
    else:
        color = color
    return color


# This function draws in the laser in the image
# image: image from camera to be updated
# x: laser x coordinate
# y: laser y coordinate
# color: color to be drawn based on the buttons
# y_panel: panel size
def draw_laser(image, x, y, color):
    global y_panel
    if y < round(y_panel - 0.1 * y_panel):
        imagem = cv2.circle(image, (x, y), radius=2, color=color, thickness=-1)
    elif color == (1, 1, 1):
        imagem = panel_creation()
    else:
        imagem = image
    return imagem
