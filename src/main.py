import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("MuninnMonitor")
layout = QVBoxLayout()
label = QLabel("Press [Crow] to Crow!")
layout.addWidget(label)
window.setLayout(layout)
window.show()
app.exec()



