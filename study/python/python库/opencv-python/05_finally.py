import cv2
from datetime import datetime
from typing import Tuple, Optional


class CameraRecorder:
    def __init__(
        self,
        camera_index: int = 0,
        output_file: Optional[str] = None,
        fps: float = 20.0,
        codec: str = "mp4v",
        frame_size: Optional[Tuple[int, int]] = None,
    ):
        self.camera_index = camera_index
        self.output_file = output_file or datetime.now().strftime("camera_%Y%m%d_%H%M%S.mp4")
        self.fps = fps
        self.codec = codec
        self.frame_size = frame_size

        self.cap = None
        self.out = None

    def open(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("摄像头打开失败")

        if self.frame_size is None:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.frame_size = (width, height)

        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self.out = cv2.VideoWriter(self.output_file, fourcc, self.fps, self.frame_size)

        if not self.out.isOpened():
            self.cap.release()
            raise RuntimeError("视频文件创建失败")

    def run(self):
        print(f"开始录制，输出文件：{self.output_file}，按 q 停止")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("读取摄像头失败")
                break

            # 可以在这里对 frame 做一些统一处理，比如翻转
            # frame = cv2.flip(frame, 1)  # 1 为左右镜像

            if (frame.shape[1], frame.shape[0]) != self.frame_size:
                frame = cv2.resize(frame, self.frame_size)

            self.out.write(frame)
            cv2.imshow("CameraRecorder - 按 q 停止", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def close(self):
        if self.cap is not None:
            self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recorder = CameraRecorder()
    try:
        recorder.open()
        recorder.run()
    finally:
        recorder.close()
