import campy.campy as cam
import cv2

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

my_cam = cam.camera()
img, first_timestamp = my_cam.getFrame()

while True:
    img, timestamp = my_cam.getFrame()
    height, width, z = img.shape
    cv2.putText(img, str(round((timestamp - first_timestamp)/1e9, 4)) + ' seconds', (10, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(img, str('Press Q to Quit'), (width - 300, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('image', img)

    # Q to Quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

my_cam.stopCam()