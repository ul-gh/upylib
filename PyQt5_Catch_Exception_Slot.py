import sys
import traceback
import types
from functools import wraps
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMessageBox

def pyqtCatchExceptionSlot(*args, catch=Exception, on_exception_emit=None):
    """This is a decorator for pyqtSlots where an exception
    in user code is caught, printed and a optional pyqtSignal with
    signature pyqtSignal(Exception, str) is emitted when that happens.

    Arguments:
    *args:  any valid types for the pyqtSlot
    catch:  Type of the exception to catch, defaults to any exception
    on_exception_emit:  name of a pyqtSignal to be emitted
    """
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @pyqtSlot(*args)
    def slotdecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args)
            except catch as e:
                print(f"In pyqtSlot: {wrapper.__name__}:\n"
                      f"Caught exception: {e.__repr__()}")
                if on_exception_emit is not None:
                    # args[0] is instance of bound signal
                    pyqt_signal = getattr(args[0], on_exception_emit)
                    pyqt_signal.emit(e, wrapper.__name__)
        return wrapper
    return slotdecorator


class Test(QPushButton):
    exceptionOccurred = pyqtSignal(Exception, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("hello")
        self.clicked.connect(self.buttonClicked)
        self.exceptionOccurred.connect(self.on_exceptionOccurred)

    @pyqtSlot(Exception, str)
    def on_exceptionOccurred(self, exception, slot_name):
        QMessageBox.critical(self, "Uncaught exception in pyqtSlot!",
                             f"In pyqtSlot: {slot_name}:\n"
                             f"Caught exception: {exception.__repr__()}")

    @pyqtCatchExceptionSlot("bool", on_exception_emit="exceptionOccurred")
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
            print(traceback.format_exception(*sys.exc_info()))
            return False
        finally:
            if isex:
                self.quit()

app = MyApp(sys.argv)

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
