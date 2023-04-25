import cv2
import numpy as np

# Define variables for selected color and saved image
color = (0, 0, 0)
saved_img = None


# Define a function to handle mouse events
def mouse_callback(x, y):  # substituir por função do laser
    global color, saved_img

    if x_r1 <= x <= x_r2 and y_r1 <= y <= y_r2:
        color = (0, 0, 255)  # Red button selected
    elif x_b1 <= x <= x_b2 and y_b1 <= y <= y_b2:
        color = (255, 0, 0)  # Blue button selected
    elif x_g1 <= x <= x_g2 and y_g1 <= y <= y_g2:
        color = (0, 255, 0)  # Green button selected
    elif x_res1 <= x <= x_res2 and y_res1 <= y <= y_res2:
        panel = np.zeros((x_panel, y_panel, 3), np.uint8)  # Clear panel
    elif x_sav1 <= x <= x_sav2 and y_sav1 <= y <= y_sav2:
        saved_img = img.copy()  # save current image
        cv2.imwrite("saved_image.jpg", saved_img)  # Save image to directory


# Function for creation of the Panel
def panel_creation():
    # Create a blank panel for writing (16:9)
    y_panel = 675  # 720
    x_panel = 1200  # 1280
    panel = np.zeros((y_panel, x_panel, 3), np.uint8)  # creation of the panel

    # Draw line to separate buttons from writing area
    y_line = round(
        y_panel - 0.1 * y_panel
    )  # 10% do painel inferior é para o menu de ferramentas
    cv2.line(panel, (0, y_line), (1200, y_line), (255, 255, 255), 2)

    # Draw color selection buttons on panel

    # definição do y dos botões
    y_button1 = round(
        y_panel - (0.1 * y_panel * 0.2)
    )  # 20% do menu de ferramentas espaço em branco abaixo dos botões
    y_button2 = round(
        y_panel - (0.1 * y_panel * 0.82)
    )  # 62% é o tamanho do botão abaixo do espaçamento
    # definição do x dos botões
    x_r1, y_r1 = 395, round(y_button1)
    x_r2, y_r2 = 525, round(y_button2)
    x_b1, y_b1 = 535, round(y_button1)
    x_b2, y_b2 = 665, round(y_button2)
    x_g1, y_g1 = 675, round(y_button1)
    x_g2, y_g2 = 805, round(y_button2)

    # Criação dos botões
    cv2.rectangle(
        panel, (x_r1, y_r1), (x_r2, y_r2), (0, 0, 255), -1
    )  # Red button  / (top left corner) (bottom right corner)
    cv2.rectangle(
        panel, (x_b1, y_b1), (x_b2, y_b2), (255, 0, 0), -1
    )  # Blue button
    cv2.rectangle(
        panel, (x_g1, y_g1), (x_g2, y_g2), (0, 255, 0), -1
    )  # Green button
    # Definição dos botões reset e Save
    x_res1, y_res1 = 10, round(y_button1)
    x_res2, y_res2 = 160, round(y_button2)
    x_sav1, y_sav1 = 1000, 620
    x_sav2, y_sav2 = 1150, 660

    # Criação dos botões de reset e save
    cv2.rectangle(
        panel, (x_res1, y_res1), (x_res2, y_res2), (255, 255, 255), -1
    )  # Reset button
    cv2.rectangle(
        panel, (x_sav1, y_sav1), (x_sav2, y_sav2), (255, 255, 255), -1
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

    # Display panel and wait for mouse events
    cv2.imshow("Panel", panel)
    cv2.setMouseCallback(
        "Panel", mouse_callback
    )  # Substituir pelo deslocamento do laser

    # Loop through frames from camera and draw laser pointer position
    #    cap = cv2.VideoCapture(0)
    #    while True:
    #        ret, img = cap.read()
    #        if not ret:
    #            break

    # Draw laser pointer position on image
    # ...

    # Display image and wait for key press
    #        cv2.imshow("Image", img)
    #        key = cv2.waitKey(1)
    #        if key == 27: # If ESC key is pressed, break loop
    #            break

    # Release camera and destroy windows
    #    cap.release()
    while True:
        cv2.imshow("Panel", panel)
        key = cv2.waitKey(1)
        if key == 27:  # If ESC key is pressed, break loop
            break
    cv2.destroyAllWindows()


panel_creation()
