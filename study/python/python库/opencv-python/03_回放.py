import cv2


def play_video(file_path):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("无法打开视频文件：", file_path)
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("播放结束")
            break

        cv2.imshow("Video Playback - 按 q 退出", frame)

        # 这里可以稍微大一点的延时，模拟接近原始 fps
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    play_video("camera_20240101_120000.mp4")  # 换成你实际录出来的文件名
