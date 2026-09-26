import sys
import multiprocessing as mp
import time
from queue import Empty
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np

#recibir datos y graficarlos
def gui_process(queue, stop_event):
    x_data = []
    y_data = []
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("MuninnMonitor")
    layout = QVBoxLayout()
    container = QWidget()

    container.setLayout(layout)
    label = QLabel("w8ting")
    window.setLayout(layout)
    layout.addWidget(label)
    
    window.setCentralWidget(container)
    plot_widget = pg.PlotWidget()
    layout.addWidget(plot_widget)
    curve = plot_widget.plot(pen=None, symbol="o", symbolSize=8, symbolBrush="b")
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
            label.setText("Press [Crow] "+ str(item[0]) +" to Crow! "+ str(item[1]))
            x = item[0]
            y = item[1]
            x_data.append(x)
            y_data.append(y)
            curve.setData(x_data, y_data)
        
    app.aboutToQuit.connect(stop_event.set)
    timer = QTimer()
    timer.timeout.connect(check_queue)
    timer.start(250)
    sys.exit(app.exec())


if __name__ == "__main__":
    np.random.seed(67)
    X = np.linspace(0, 1, 100)
    w = 1.5
    b = 0.25
    noise = np.random.normal(1, 0.025, size=X.shape)
    y = w*X+b+noise

    q = mp.Queue()
    stop_event = mp.Event()
    w = mp.Process(target=gui_process, args=(q, stop_event))
    w.start()
    for a,b in np.nditer([X, y]):
        if stop_event.is_set():
            break
        data = [a,b]
        q.put(data)
        time.sleep(1)
    q.put(None)
    w.join()
    q.close()
    q.join_thread()
