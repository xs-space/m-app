import cv2
from datetime import datetime


def record_with_timestamp(camera_index=0, output_file="record_with_ts.mp4"):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("摄像头打开失败")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, 20.0, frame_size)

    print("开始录制（带时间戳），按 q 停止")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("读取失败")
            break

        # 在左上角画一个时间戳
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            frame,  # 要画字的图像
            now,  # 文本
            (10, 30),  # 坐标（x, y）
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
            0.8,  # 字号
            (0, 255, 0),  # 颜色 (B, G, R)
            2,  # 线宽
        )

        out.write(frame)
        cv2.imshow("Recording with timestamp - 按 q 停止", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("录制结束")


if __name__ == "__main__":
    record_with_timestamp()
