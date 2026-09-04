import itertools
import sys
import threading
import time


class Loader:
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(
            target=self._animate,
            daemon=True,
        )
        self.thread.start()

    def _animate(self):
        spinner = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )

        while self.running:
            sys.stdout.write(
                f"\r{next(spinner)} {self.message}"
            )
            sys.stdout.flush()
            time.sleep(0.1)

    def stop(self, success=True):
        self.running = False

        if self.thread:
            self.thread.join(timeout=1)

        status = "✓" if success else "✗"

        sys.stdout.write(
            f"\r{status} {self.message}\n"
        )
        sys.stdout.flush()