import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler





# 监控所有文件和目录变化，包括新增、修改、删除、移动
class AllFilesHandler(FileSystemEventHandler):
    def on_created(self, event):
        type_ = "目录" if event.is_directory else "文件"
        print(f"[新增] {type_}: {event.src_path}")

    def 