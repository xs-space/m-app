import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# 监控所有文件和目录变化，包括新增、修改、删除、移动
class AllFilesHandler(FileSystemEventHandler):

    def on_created(self, event):
        type_ = "目录" if event.is_directory else "文件"
        print(f"[新增] {type_}: {event.src_path}")

    def on_modified(self, event):
        type_ = "目录" if event.is_directory else "文件"
        print(f"[修改] {type_}: {event.src_path}")

    def on_deleted(self, event):
        type_ = "目录" if event.is_directory else "文件"
        print(f"[删除] {type_}: {event.src_path}")

    def on_moved(self, event):
        type_ = "目录" if event.is_directory else "文件"
        print(f"[移动] {type_}: {event.src_path} -> {event.dest_path}")


if __name__ == "__main__":
    path = r"E:\workspace\temp"  # 需要监控的目录
    event_handler = AllFilesHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  # 这里要把参数recursive=True，这样可以监控子目录
    observer.start()
    print(f"正在监控 {path} 及子目录下所有文件和目录的变化...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
