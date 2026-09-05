import sys
import multiprocessing as mp
import time
from queue import Empty
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer


def gui_process(queue, stop_event):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("MuninnMonitor")
    layout = QVBoxLayout()
    label = QLabel("w8ting")
    window.setLayout(layout)
    layout.addWidget(label)
    window.show()
    def check_queue():
        while True:
            try:
                item = queue.get_nowait()
            except Empty:
                break
            if item is None:
                        app.quit()
                        return
            label.setText("Press [Crow] "+ str(item) +" to Crow!")
        
    app.aboutToQuit.connect(stop_event.set)
    timer = QTimer()
    timer.timeout.connect(check_queue)
    timer.start(250)
    sys.exit(app.exec())


if __name__ == "__main__":
    
    q = mp.Queue()
    stop_event = mp.Event()
    w = mp.Process(target=gui_process, args=(q, stop_event))
    w.start()
    for i in range(100):
        if stop_event.is_set():
            break
        q.put(i)
        time.sleep(1)
    q.put(None)
    w.join()
    q.close()
    q.join_thread()
