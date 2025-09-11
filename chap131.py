import cv2
import numpy as np

def nothing(x):
    pass

img_origin = cv2.imread('mountain1.jpg')
img = img_origin.copy()
font = cv2.FONT_HERSHEY_SIMPLEX
drawing = False
mode = True
ix, iy = -1, -1

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img

    temp = img.copy()  # 그림은 임시 이미지로
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        # 텍스트는 항상 temp에 표시
        txt = f'Mouse Position({x},{y}) {img[y, x]}'
        cv2.putText(temp, txt, (30,30), font, 1, (255,255,255), 2, cv2.LINE_AA)

        # 드래그 중 네모/원도 temp에 그림
        if drawing:
            if mode:
                cv2.rectangle(temp, (ix, iy), (x, y), (0,0,255), -1)
            else:
                cv2.circle(temp, (x, y), 5, (0,0,255), -1)

        cv2.imshow('image', temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # 드래그 끝나면 실제 img에 그림 확정
        if mode:
            cv2.rectangle(img, (ix, iy), (x, y), (0,0,255), -1)
        else:
            cv2.circle(img, (x, y), 5, (0,0,255), -1)

cv2.namedWindow('image')
cv2.createTrackbar('R','image',0,255,nothing)
cv2.setMouseCallback('image', draw_circle)

while True:
    r = cv2.getTrackbarPos('R','image')
    print(r)

    # 항상 텍스트는 현재 마우스 위치 기준으로 표시
    # 하지만 실시간 드래그 중이면 draw_circle에서 이미 imshow 호출
    if not drawing:
        temp = img.copy()
        x, y = cv2.getWindowImageRect('image')[:2]  # 마우스 좌표 직접 가져오기 어렵지만, 여기선 생략 가능
        # 단순히 img만 보여줌
        cv2.imshow('image', temp)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()


"""
cv2.namedWindow('image')
img[100:200,100:200,2] = 255


while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows() 
"""