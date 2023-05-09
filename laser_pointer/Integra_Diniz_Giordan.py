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
y_panel = 720  # 360
x_panel = 1280  # 640


# função para chamar os valores do dicionário de forma simplificada
def bxy(b_name, pos_idx):
    global x_panel, y_panel

    # Coordenadas verticais dos botões
    y_button1 = round(
        y_panel - (0.1 * y_panel * 0.2)
    )  # 20% do menu de ferramentas espaço em branco abaixo dos botões
    y_button2 = round(
        y_panel - (0.1 * y_panel * 0.82)
    )  # 62% é o tamanho do botão abaixo do espaçamento

    # Definição dos tamanhos dos espaçamentos e dos botões
    x_space_f = round(x_panel * 0.04)  # 4% do painel
    x_space_c = round(x_panel * 0.02)  # 2% do painel
    button_width_f = round(x_panel * 0.10)  # 10% do painel
    button_width_c = round(x_panel * 0.145)  # 14.5% do painel

    # Criação de dicionário com coordenadas x e y dos botões

    # definição dos parâmetros iniciais
    button_x = round(x_space_f)
    button_positions = [
        "Reset",
        "Red",
        "Blue",
        "Green",
        "Erase",
        "Save",
    ]  # 7 buttons slots
    button_xs = []  # x coordinates of each button
    button_positions_dict = {}  # dictionary to store button positions

    # loop para armazenamento dos valores no dicionário
    for i in range(len(button_positions)):
        button_xs.append(button_x)

        if i == 0:  # tamanho do primeiro botão
            button_positions_dict[button_positions[i]] = (
                (button_x, y_button1),
                (button_x + button_width_f, y_button2),
            )
            button_x += button_width_f + x_space_f

        elif i == (len(button_positions) - 1):  # tamanho do último botão
            button_positions_dict[button_positions[i]] = (
                (button_x, y_button1),
                (button_x + button_width_f, y_button2),
            )
            button_x += button_width_f + x_space_f

        elif i == (len(button_positions) - 2):  # ultimo botão de cor
            button_positions_dict[button_positions[i]] = (
                (button_x, y_button1),
                (button_x + button_width_c, y_button2),
            )
            button_x += button_width_c + x_space_f

        else:  # tamanho dos botões intermediários (cores)
            button_positions_dict[button_positions[i]] = (
                (button_x, y_button1),
                (button_x + button_width_c, y_button2),
            )
            button_x += (
                button_width_c + x_space_c
            )  # cada botão será separado por um espaço (button_width)

        button_x = round(button_x)

    return button_positions_dict[b_name][pos_idx]


# Function for creation of the Panel
def panel_creation():
    global x_panel, y_panel
    panel = np.zeros((y_panel, x_panel, 3), np.uint8)  # creation of the panel

    # Draw line to separate buttons from writing area
    y_line = round(
        y_panel - 0.1 * y_panel
    )  # 10% do painel inferior é para o menu de ferramentas
    cv2.line(panel, (0, y_line), (x_panel, y_line), (15, 15, 15), 2)

    # Coordenadas verticais dos botões
    y_button1 = round(
        y_panel - (0.1 * y_panel * 0.2)
    )  # 20% do menu de ferramentas espaço em branco abaixo dos botões
    y_button2 = round(
        y_panel - (0.1 * y_panel * 0.82)
    )  # 62% é o tamanho do botão abaixo do espaçamento

    # Definição dos tamanhos dos espaçamentos e dos botões
    x_space_f = round(x_panel * 0.04)  # 4% do painel
    x_space_c = round(x_panel * 0.02)  # 2% do painel
    button_width_f = round(x_panel * 0.10)  # 10% do painel
    button_width_c = round(x_panel * 0.145)  # 14.5% do painel

    # Criação de dicionário com coordenadas x e y dos botões

    # # definição dos parâmetros iniciais
    # button_x = round(x_space_f)
    # button_positions = [
    #     "Reset",
    #     "Red",
    #     "Blue",
    #     "Green",
    #     "Erase",
    #     "Save",
    # ]  # 7 buttons slots
    # button_xs = []  # x coordinates of each button
    # button_positions_dict = {}  # dictionary to store button positions

    # # loop para armazenamento dos valores no dicionário
    # for i in range(len(button_positions)):
    #     button_xs.append(button_x)

    #     if i == 0:  # tamanho do primeiro botão
    #         button_positions_dict[button_positions[i]] = (
    #             (button_x, y_button1),
    #             (button_x + button_width_f, y_button2),
    #         )
    #         button_x += button_width_f + x_space_f

    #     elif i == (len(button_positions) - 1):  # tamanho do último botão
    #         button_positions_dict[button_positions[i]] = (
    #             (button_x, y_button1),
    #             (button_x + button_width_f, y_button2),
    #         )
    #         button_x += button_width_f + x_space_f

    #     elif i == (len(button_positions) - 2):  # ultimo botão de cor
    #         button_positions_dict[button_positions[i]] = (
    #             (button_x, y_button1),
    #             (button_x + button_width_c, y_button2),
    #         )
    #         button_x += button_width_c + x_space_f

    #     else:  # tamanho dos botões intermediários (cores)
    #         button_positions_dict[button_positions[i]] = (
    #             (button_x, y_button1),
    #             (button_x + button_width_c, y_button2),
    #         )
    #         button_x += (
    #             button_width_c + x_space_c
    #         )  # cada botão será separado por um espaço (button_width)

    #     button_x = round(button_x)

    # exemplo: bxy('Green',0) = (g_x1,g_y1) // bxy('Green',1) = (g_x2,g_y2)

    # Criação dos Retângulos dos botões com valores do dicionário
    cv2.rectangle(
        panel, bxy("Reset", 0), bxy("Reset", 1), (95, 95, 95), -1
    )  # Reset button

    cv2.rectangle(
        panel, bxy("Green", 0), bxy("Green", 1), (0, 70, 0), -1
    )  # Green button
    cv2.rectangle(
        panel, bxy("Blue", 0), bxy("Blue", 1), (70, 0, 0), -1
    )  # Blue button
    cv2.rectangle(
        panel, bxy("Red", 0), bxy("Red", 1), (0, 0, 100), -1
    )  # Red button  / (top left corner) (bottom right corner)
    cv2.rectangle(
        panel, bxy("Erase", 0), bxy("Erase", 1), (35, 35, 35), -1
    )  # Erase button (black color)

    cv2.rectangle(
        panel, bxy("Save", 0), bxy("Save", 1), (95, 95, 95), -1
    )  # Save button

    # Adição de texto aos botões (Reset ; Save ; Erase)

    res_text_size = cv2.getTextSize("Reset", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[
        0
    ]  # returns tuple with text x_size,y_size
    # res_text_x = x_res1 + (x_res2 - x_res1 - res_text_size[0]) // 2
    # res_text_y = y_res1 + (y_res2 - y_res1 + res_text_size[1]) // 2
    res_text_x = (
        bxy("Reset", 0)[0]
        + (bxy("Reset", 1)[0] - bxy("Reset", 0)[0] - res_text_size[0]) // 2
    )  # define posição x do texto em função do botão
    res_text_y = (
        bxy("Reset", 0)[1]
        + (bxy("Reset", 1)[1] - bxy("Reset", 0)[1] + res_text_size[1]) // 2
    )  # define posição y do texto em função do botão

    sav_text_size = cv2.getTextSize("Save", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[
        0
    ]
    sav_text_x = (
        bxy("Save", 0)[0]
        + (bxy("Save", 1)[0] - bxy("Save", 0)[0] - sav_text_size[0]) // 2
    )
    sav_text_y = (
        bxy("Save", 0)[1]
        + (bxy("Save", 1)[1] - bxy("Save", 0)[1] + sav_text_size[1]) // 2
    )
# Define posição do texto 'erase'
    era_text_size = cv2.getTextSize("Borracha", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    era_text_x = bxy('Erase',0)[0] + (bxy('Erase',1)[0] - bxy('Erase',0)[0] - era_text_size[0]) // 2
    era_text_y = bxy('Erase',0)[1] + (bxy('Erase',1)[1] - bxy('Erase',0)[1] + era_text_size[1]) // 2
    
    
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
    cv2.putText(panel, "Borracha", (era_text_x, era_text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (95, 95, 95), 2) # Erase text
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


# Define a function to handle the buttons
def button_function(x, y, img, color_input):
    # print(f"x :{x}", f"y :{y}")

    if (
        bxy("Red", 0)[0] <= x <= bxy("Red", 1)[0]
        and bxy("Red", 1)[1] <= y <= bxy("Red", 0)[1]
    ):
        color = (0, 0, 100)  # Red button selected
        radius = 2
    elif (
        bxy("Blue", 0)[0] <= x <= bxy("Blue", 1)[0]
        and bxy("Blue", 1)[1] <= y <= bxy("Blue", 0)[1]
    ):
        color = (70, 0, 0)  # Blue button selected
        radius = 2
    elif (
        bxy("Green", 0)[0] <= x <= bxy("Green", 1)[0]
        and bxy("Green", 1)[1] <= y <= bxy("Green", 0)[1]
    ):
        color = (0, 70, 0)  # Green button selected
        radius = 2
    elif (
        bxy("Erase", 0)[0] <= x <= bxy("Erase", 1)[0]
        and bxy("Erase", 1)[1] <= y <= bxy("Erase", 0)[1]
    ):
        color = (0, 0, 0)  # Erase button selected
        radius = 5
    elif (
        bxy("Reset", 0)[0] <= x <= bxy("Reset", 1)[0]
        and bxy("Reset", 1)[1] <= y <= bxy("Reset", 0)[1]
    ):
        color = (1, 1, 1)  # Reset color
    elif (
        bxy("Save", 0)[0] <= x <= bxy("Save", 1)[0]
        and bxy("Save", 1)[1] <= y <= bxy("Save", 0)[1]
    ):
        saved_img = img.copy()  # save current image
        cv2.imwrite("saved_image.jpg", saved_img)  # Save image to directory
        color = color_input
    else:
        color = color_input

    # print(color)
    return color  # radius (?)


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
        imagem = panel_creation()
    else:
        imagem = image
    return imagem
