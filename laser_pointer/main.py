from calibrate import Calibrate

from Integra_Diniz_Giordan import (
    panel_creation,
    laser_coordinate,
    button_function,
    draw_laser,
    visualize_camera,
    aquire_image,
    warp_point
)
import cv2 as cv
import numpy as np



matCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhomatCam.npy"
)
distorCam = np.load(
    r"D:\Jupyther\UFSC\Visao Computacional\PowerLaserPointer\laser_pointer\TrabalhodistorCam.npy"
)

visualize_camera()

calibrate = Calibrate(1, matCam, distorCam)
M, old_points = calibrate.run()
cv.namedWindow("panel")
panel = panel_creation()
cv.imshow("panel", panel)
camera = aquire_image(1)
X,Y = laser_coordinate(camera, old_points)
x,y = warp_point(X, Y, M)
color = button_function(x, y, panel)
draw = draw_laser(panel, x, y, color)
cv.destroyAllWindows()

while 1:
    cv.imshow("Draw", draw)
    X,Y = laser_coordinate(camera, old_points)
    x,y = warp_point(X, Y, M)
    color = button_function(x, y, panel)
    draw = draw_laser(panel, x, y, color)
    k = cv.waitKey(10)
    if k == 27:
        break

cv.destroyAllWindows()
# É uma boa pratica desalocar a camera antes de encerrar o programa
cv.VideoCapture(1, cv.CAP_DSHOW).release()
    







