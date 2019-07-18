import sys
from traceback import format_exception
import types
from functools import wraps
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMessageBox

from pyqt_debug import patch_pyqt_event_exception_hook

class Test(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("hello")
        self.clicked.connect(self.buttonClicked)

    def buttonClicked(self, checked):
        print("clicked")
        raise Exception("wow")

class MyApp(QApplication):
    def notify(self, obj, event):
        isex = False
        try:
            return QApplication.notify(self, obj, event)
        except Exception:
            isex = True
            print("Unexpected Error")
            print(format_exception(*sys.exc_info()))
            return False
        finally:
            if isex:
                self.quit()

app = MyApp(sys.argv)

patch_pyqt_event_exception_hook(app)

t=Test()
t.show()

# Some boilerplate in case this is run from an IPython shell
try:
    from IPython import get_ipython
    ipy_inst = get_ipython()
    if ipy_inst is None:
        app.exec_()
    else:
        ipy_inst.run_line_magic("gui", "qt5")
except ImportError:
    app.exec_()
