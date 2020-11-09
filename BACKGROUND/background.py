import cv2
import numpy as np
import matplotlib.pyplot as plt

def remove_bg(
    path,
    BLUR = 21,
    CANNY_THRESH_1 = 10,
    CANNY_THRESH_2 = 200,
    MASK_DILATE_ITER = 10,
    MASK_ERODE_ITER = 10,
    MASK_COLOR = (0.0,0.0,1.0),
    ):
    # 画像を読み込む
    img = cv2.imread(path)
    # グレー変換
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # エッジ検出
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # エッジだけの描画
    plt.imshow(edges,cmap = 'gray')
    plt.show()

    # 輪郭の取得 最も長い輪郭を採用
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # マスク作成
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # マスクのスムージング処理
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, kernel, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    # マスクと背景の合成
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    c_blue, c_green, c_red = cv2.split(img)
    
    img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))


    plt.imshow(img_a)
    plt.show()
    return img_a


def img_save(img_fin):
    # 画像を保存
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(img_fin)
    fig.savefig('sample/create/fin2.jpg')

if __name__ == '__main__':
    img_fin = remove_bg(    
    path = 'sample/img/sample8.jpg',
    BLUR = 21,
    CANNY_THRESH_1 = 100,
    CANNY_THRESH_2 = 200,
    MASK_DILATE_ITER = 10,
    MASK_ERODE_ITER = 13,
    )
    img_save(img_fin)