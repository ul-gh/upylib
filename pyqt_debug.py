import sys
import types
from functools import wraps
from PyQt5.QtCore import pyqtSlot

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


def debug_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

