import cv2
import numpy as np

img = cv2.imread("mountain2.jpg")
clone = img.copy()

drawing = False 
ix,iy = -1,-1
ex,ey = -1,-1

color = (0, 0, 0)

def nothing(x):
    pass

def get_color_from_trackbar(val):
    h = int((val / 255) * 179)
    s = 255
    v = 255
    hsv_color = np.uint8([[[h, s, v]]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr_color[0]), int(bgr_color[1]), int(bgr_color[2]))

def draw_rectangle(event,x,y,flags,param):
    global ix, iy, ex, ey, drawing, img, clone, color
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = clone.copy()
            ex, ey = x,y
            overlay = img.copy()
            x1, x2 = sorted([ix, ex])
            y1, y2 = sorted([iy, ey])

            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)

            alpha = 0.4
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

            text = f"Mouse Positon ({ix},{iy}) - ({ex},{ey}) - Color BGR: {color}"
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        overlay = img.copy()
        x1, x2 = sorted([ix, ex])
        y1, y2 = sorted([iy, ey])

        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)

        alpha = 0.4
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        text = "Mouse Positon ({ix},{iy}) - ({ex},{ey}) - Color BGR: {color}"
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                     0.7, (255, 255, 255), 2)

cv2.namedWindow('image')
cv2.createTrackbar('Color','image',0,255,nothing)

cv2.setMouseCallback('image',draw_rectangle)

while True:
    val = cv2.getTrackbarPos('Color', 'image')
    color = get_color_from_trackbar(val)

    if not drawing:
        img = clone.copy()
        if ix != -1 and iy != -1 and ex != -1 and ey != -1:
            overlay = img.copy()
            x1, x2 = sorted([ix, ex])
            y1, y2 = sorted([iy, ey])
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)

            alpha = 0.4
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            text = f"Mouse Positon ({ix},{iy}) - ({ex},{ey}) - Color BGR: {color}"
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
            
    cv2.imshow("image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()

