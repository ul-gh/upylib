import sys
import types
import logging
import traceback
from functools import wraps
from traceback import format_exception
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

def logExceptionSlot(*args, logger=None, catch=Exception, default_value=None):
    """Catch all exceptions from this decorated function
    and send to the specified logger instance.

    This creates a pyqtSlot with *args.

    Arguments:
    *args:  any valid types for the pyqtSlot
    catch:  Type of the exception to catch, defaults to any exception
    default_value: Optional value to be returned on exception
    """
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @pyqtSlot(*args)
    def slotdecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except catch as e:
                logger = logging.getLogger(f"{wrapper.__module__}")
                text = (f"\nIn pyqtSlot: {wrapper.__name__}\n"
                        f"Uncaught exception of {type(e)} occurred:\n")
                text += "\n".join(
                        traceback.format_exception(Exception, e, e.__traceback__)
                        )
                logger.critical(text)
                return default_value
        return wrapper
    return slotdecorator


def patch_pyqt_event_exception_hook(app):
    """Monkey-patch sys.excepthook /inside/ a PyQt event, e.g. for handling
    exceptions occuring in pyqtSlots.
    """
    def new_except_hook(etype, evalue, tb):
        text = "".join(format_exception(etype, evalue, tb))
        print(text)
        QMessageBox.critical(None, "Error", text)

    def patch_excepthook():
        sys.excepthook = new_except_hook

    t = QTimer()
    t.setSingleShot(True)
    t.timeout.connect(patch_excepthook)
    t.start()
    app.EVENT_PATCHING_TIMER = t


def debug_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

