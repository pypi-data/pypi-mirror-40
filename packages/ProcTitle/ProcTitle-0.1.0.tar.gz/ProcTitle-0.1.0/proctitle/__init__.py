import setproctitle

class ProcTitle:
    def __init__(self, title):
        self.title = title

    def __enter__(self):
        self.orig_title = setproctitle.getproctitle()
        setproctitle.setproctitle(self.title)

    def __exit__(self, type, value, traceback):
        setproctitle.setproctitle(self.orig_title)
