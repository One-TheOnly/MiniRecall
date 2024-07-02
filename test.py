import os
import threading
import time

from flask import Flask

app = Flask(__name__, static_folder='screenshots')
screenshots_folder = app.static_folder


def run_scheduled_screenshots():
    thread_name = threading.current_thread().name
    process_id = os.getpid()
    print(
        f"##########{time.strftime('%Y-%m-%d_%H-%M-%S')}启动定时截图, Thread Name: {thread_name}, Process ID: {process_id}")


def run_flask_server():
    # 确保截图目录存在
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
    app.run(debug=False, use_reloader=False, threaded=True)  # 开启多线程模式以支持同时处理多个请求


if __name__ == "__main__":
    # 创建并启动截图任务的线程
    screenshot_thread = threading.Thread(target=run_scheduled_screenshots)
    screenshot_thread.start()
    # flask_thread.start()

    # 直接运行Flask服务器（这将阻塞主线程）
    run_flask_server()
