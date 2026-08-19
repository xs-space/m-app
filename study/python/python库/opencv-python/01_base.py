import cv2


def preview_camera(camera_index=0):
    # 1. 打开摄像头，0 通常是默认摄像头，笔记本就是内置摄像头
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("摄像头打开失败，检查一下摄像头是否被占用，或者 camera_index 写错了")
        return

    while True:
        # 2. 读取一帧图像
        ret, frame = cap.read()

        if not ret:
            print("读取摄像头画面失败，可能是摄像头断开了")
            break

        # 3. 在窗口中显示这一帧
        cv2.imshow("Camera Preview - 按 q 退出", frame)

        # 4. 等待键盘事件，参数是等待毫秒数
        #   如果 1ms 内按下 q，就退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 5. 释放摄像头资源，关闭窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    preview_camera()
