import cv2
import numpy as np


class Panel:
    """Class to create the panel with the buttons"""

    def __init__(self, x_panel=1280, y_panel=720):
        self.x_panel = x_panel
        self.y_panel = y_panel

    def calculate_buttons_coordinates(self, button_positions):
        # TODO : Quebrar em funções menores

        button_coordinates_dict = {}

        # Coordenadas verticais dos botões
        y_button1 = round(
            self.y_panel - (0.1 * self.y_panel * 0.2)
        )  # 20% do menu de ferramentas espaço em branco abaixo dos botões
        y_button2 = round(
            self.y_panel - (0.1 * self.y_panel * 0.82)
        )  # 62% é o tamanho do botão abaixo do espaçamento

        # Definição dos tamanhos dos espaçamentos e dos botões
        x_space_f = round(self.x_panel * 0.04)  # 4% do painel
        x_space_c = round(self.x_panel * 0.02)  # 2% do painel
        button_width_f = round(self.x_panel * 0.10)  # 10% do painel
        button_width_c = round(self.x_panel * 0.145)  # 14.5% do painel
        button_x = round(x_space_f)

        for enum, button in button_positions:
            if (enum == 0) or (
                enum == (len(button_positions) - 1)
            ):  # tamanho do primeiro botão ou último
                button_coordinates_dict[button] = (
                    (button_x, y_button1),
                    (button_x + button_width_f, y_button2),
                )
                button_x += button_width_f + x_space_f

            elif enum == (len(button_positions) - 2):  # ultimo botão de cor
                button_coordinates_dict[button] = (
                    (button_x, y_button1),
                    (button_x + button_width_c, y_button2),
                )
                button_x += button_width_c + x_space_f

            else:  # tamanho dos botões intermediários (cores)
                button_coordinates_dict[button] = (
                    (button_x, y_button1),
                    (button_x + button_width_c, y_button2),
                )
                button_x += (
                    button_width_c + x_space_c
                )  # cada botão será separado por um espaço (button_width)

            button_x = round(button_x)

        self.button_coordinates_dict = button_coordinates_dict

    def button_coordinates(self, button_name, pos_index):
        return self.button_coordinates_dict[button_name][pos_index]

    def create_button(self, button_name, button_color, button_text=None):
        """_summary_

        Parameters
        ----------
        button_coordinates : _type_
            _description_
        button_color : _type_
            _description_
        button_name : _type_, optional
            _description_, by default None
        """
        cv2.rectangle(
            self.panel,
            self.button_coordinates(button_name, 0),
            self.button_coordinates(button_name, 1),
            button_color,
            -1,
        )

        # check if button has text
        if button_text is not None:
            # returns tuple with text x_size,y_size
            text_size = cv2.getTextSize(
                button_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )[0]

            # res_text_x = x_res1 + (x_res2 - x_res1 - res_text_size[0]) // 2
            # res_text_y = y_res1 + (y_res2 - y_res1 + res_text_size[1]) // 2

            res_text_x = (
                self.button_coordinates(button_name, 0)[0]
                + (
                    self.button_coordinates(button_name, 1)[0]
                    - self.button_coordinates(button_name, 0)[0]
                    - text_size[0]
                )
                // 2
            )
            res_text_y = (
                self.button_coordinates(button_name, 1)[1]
                + (
                    self.button_coordinates(button_name, 1)[1]
                    - self.button_coordinates(button_name, 0)[1]
                    + text_size[1]
                )
                // 2
            )

            cv2.putText(
                self.panel,
                button_text,
                (res_text_x, res_text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (30, 30, 30),
                2,
            )

    def execute_button(self, x, y, img, color_input):
        # TODO Tentar reescrever essa função para ficar mais simples

        if (
            self.button_coordinates("Red", 0)[0]
            <= x
            <= self.button_coordinates("Red", 1)[0]
            and self.button_coordinates("Red", 1)[1]
            <= y
            <= self.button_coordinates("Red", 0)[1]
        ):
            color = (0, 0, 100)  # Red button selected
        elif (
            self.button_coordinates("Blue", 0)[0]
            <= x
            <= self.button_coordinates("Blue", 1)[0]
            and self.button_coordinates("Blue", 1)[1]
            <= y
            <= self.button_coordinates("Blue", 0)[1]
        ):
            color = (70, 0, 0)  # Blue button selected
        elif (
            self.button_coordinates("Green", 0)[0]
            <= x
            <= self.button_coordinates("Green", 1)[0]
            and self.button_coordinates("Green", 1)[1]
            <= y
            <= self.button_coordinates("Green", 0)[1]
        ):
            color = (0, 70, 0)  # Green button selected

        elif (
            self.button_coordinates("Erase", 0)[0]
            <= x
            <= self.button_coordinates("Erase", 1)[0]
            and self.button_coordinates("Erase", 1)[1]
            <= y
            <= self.button_coordinates("Erase", 0)[1]
        ):
            color = (0, 0, 0)  # Erase button selected
        elif (
            self.button_coordinates("Reset", 0)[0]
            <= x
            <= self.button_coordinates("Reset", 1)[0]
            and self.button_coordinates("Reset", 1)[1]
            <= y
            <= self.button_coordinates("Reset", 0)[1]
        ):
            color = (1, 1, 1)  # Reset color
        elif (
            self.button_coordinates("Save", 0)[0]
            <= x
            <= self.button_coordinates("Save", 1)[0]
            and self.button_coordinates("Save", 1)[1]
            <= y
            <= self.button_coordinates("Save", 0)[1]
        ):
            saved_img = img.copy()  # save current image
            cv2.imwrite(
                "saved_image.jpg", saved_img
            )  # Save image to directory
            color = color_input
        else:
            color = color_input

        return color

    def create_panel(self):
        self.panel = np.zeros((self.y_panel, self.x_panel, 3), np.uint8)
        # Draw line to separate buttons from writing area
        y_line = round(
            self.y_panel - 0.1 * self.y_panel
        )  # 10% do painel inferior é para o menu de ferramentas
        cv2.line(
            self.panel, (0, y_line), (self.x_panel, y_line), (15, 15, 15), 2
        )

        button_positions = [
            "Reset",
            "Red",
            "Blue",
            "Green",
            "Erase",
            "Save",
        ]

        self.calculate_buttons_coordinates(button_positions=button_positions)

        # Criação dos Retângulos dos botões com valores do dicionário
        self.create_button("Reset", (95, 95, 95), "Reset")
        self.create_button("Red", (0, 0, 100))
        self.create_button("Blue", (70, 0, 0))
        self.create_button("Green", (0, 70, 0))
        self.create_button("Erase", (0, 0, 0))
        self.create_button("Save", (255, 255, 255), "Save")

        return self.panel
