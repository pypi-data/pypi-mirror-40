supported_backends = [
    "tkinter",
]


class NoBackend(BaseException):
    def __init__(self):
        super().__init__(
            "There is no supported graphical backend installed.\n" +
            "Try to install one of those:\n" +
            "\n".join("- " + back for back in supported_backends)
        )

try:
    import tkinter as tk
    have_tk = True
except ImportError:
    have_tk = False 

if have_tk:
    from .backend_tk import Backend
else:
    raise NoBackend()
