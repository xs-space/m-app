import cv2
from datetime import datetime


def record_camera(camera_index=0, output_file=None, fps=20.0, frame_size=None):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("摄像头打开失败")
        return

    # 如果没指定输出文件名，就用时间戳来生成一个
    if output_file is None:
        output_file = datetime.now().strftime("camera_%Y%m%d_%H%M%S.mp4")

    # 获取摄像头的宽高
    if frame_size is None:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)

    # fourcc 指定视频编码格式，不同系统可能要试几个
    # 'mp4v' 生成 mp4，一般还算通用
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    if not out.isOpened():
        print("视频文件创建失败，检查路径和编码格式")
        cap.release()
        return

    print(f"开始录制，保存到：{output_file}，按 q 停止")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("读取摄像头失败，中断录制")
            break

        # 如果摄像头分辨率和 frame_size 不一致，调整一下大小
        if (frame.shape[1], frame.shape[0]) != frame_size:
            frame = cv2.resize(frame, frame_size)

        # 写入这一帧到视频文件
        out.write(frame)

        # 一边录一边预览
        cv2.imshow("Recording - 按 q 停止", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("录制结束")


if __name__ == "__main__":
    record_camera()
