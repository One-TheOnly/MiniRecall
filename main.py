import os
import threading
import time

import schedule
from PIL import ImageGrab
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='screenshots')
screenshots_folder = app.static_folder


def capture_screenshot():
    screenshot_name = f"screenshot_{time.strftime('%Y-%m-%d_%H-%M-%S')}.png"
    screenshot_path = os.path.join(screenshots_folder, screenshot_name)
    ImageGrab.grab().save(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")


def screenshot_job():
    capture_screenshot()
    # 这里不需要在函数内部调用schedule.every()，因为我们在外部已经设置了  


def run_scheduled_screenshots():
    # 配置截图间隔时间（例如：每30分钟）
    schedule.every(10).minutes.do(screenshot_job)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_flask_server():
    # 确保截图目录存在  
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
    app.run(debug=False, threaded=True)  # 开启多线程模式以支持同时处理多个请求


@app.route('/')
def index():
    # 获取截图文件名列表
    screenshot_files = [f for f in os.listdir(app.static_folder) if f.endswith('.png')]
    screenshot_files.reverse()
    return render_template('index.html', screenshots=screenshot_files)


@app.route('/screenshots/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == "__main__":
    # 立即执行一次截图
    capture_screenshot()

    # 创建并启动截图任务的线程  
    screenshot_thread = threading.Thread(target=run_scheduled_screenshots)
    screenshot_thread.start()

    # 创建并启动Flask服务器的线程（实际上，Flask的app.run()已经是一个阻塞调用，但在这里我们假设它支持多线程）  
    # 注意：由于Flask的app.run()是阻塞的，这里实际上不需要另一个线程（除非你想在后台运行Flask）  
    # 但为了符合您的要求并保持示例的完整性，我将其保留在注释中  
    # flask_thread = threading.Thread(target=run_flask_server)  
    # flask_thread.start()  

    # 直接运行Flask服务器（这将阻塞主线程）  
    run_flask_server()

    # 注意：上面的代码实际上不会同时运行截图任务和Flask服务器，因为run_flask_server()会阻塞。  
    # 如果您想要两者都运行，并且想要在主线程中控制它们，您可能需要考虑使用其他方法，  
    # 如使用多进程（multiprocessing）或异步框架（如FastAPI与Uvicorn）。  
    # 但对于简单的用例，上面的代码（取消注释flask_thread部分）应该足够。
