# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

def ipython_pyqt_boilerplate(app: QApplication) -> None:
    """When running from ipython shell, use its Qt GUI event loop
    integration. Otherwise, start pyqt event loop via app.exec_()
    """
    try:
        from IPython import get_ipython
        ipy_inst = get_ipython()
        if ipy_inst is not None:
            ipy_inst.run_line_magic("gui", "qt5")
            ipy_inst.run_line_magic("matplotlib", "qt5")
    except ImportError:
        ipy_inst = None
    if ipy_inst is None:
        sys.exit(app.exec_())

def get_qobj_base_state(instance: object) -> dict:
    """Returns attributes of given class instance which
    do not themselves inherit from QObject.

    This is needed for using the pickle module.
    """
    state = vars(self).items()
    return {key: val for key, val in state if not isinstance(val, QObject)}

