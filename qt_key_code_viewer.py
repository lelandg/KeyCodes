import sys

from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget, QLabel

__version__ = "0.1.0"
__author__ = "Leland Green"
__license__ = "CC0-1.0"

class KeyCodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keycodes Viewer")
        self.setGeometry(0, 0, 300, 500)

        # Set scrollable area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scrollbar = self.scroll_area.verticalScrollBar()

        container_widget = QWidget()
        self.layout = QVBoxLayout(container_widget)
        # Extract all key name and value pairs from Qt
        qt_key_definitions = {name: value for name, value in vars(Qt).items() if name.startswith("Key_")}

        # Sort by value for a clean output
        sorted_qt_keys = sorted(qt_key_definitions.items(), key=lambda x: x[1])

        self.loading = True
        # Print all key names and their values
        for key_name, key_value in sorted_qt_keys:
            self.add_label(key_name, key_value)
        self.loading = False
        self.scroll_area.setWidget(container_widget)
        self.setCentralWidget(self.scroll_area)
        self.scrollbar.setValue(self.scrollbar.maximum())

        self.running = True
        self.esc_counter = 0
        self.center_window()

        # Install an event filter on the scroll area
        self.scroll_area.installEventFilter(self)

    def scroll_to_last(self):
        if self.scrollbar:  # Ensure the scrollbar is still valid
            self.scrollbar.setValue(self.scrollbar.maximum())  # Scroll to the bottom.

    def center_window(self):
        """Centers the main window on the screen."""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def add_label(self, name, value):
        """Add a label to the layout and scroll to the bottom."""
        label = QLabel(f"<span style='color: purple;'>{name}</span>: <span style='color: blue;'>{value}</span>")
        print(f"Key pressed: {name} ({value})")
        self.layout.addWidget(label)
        if not self.loading:
            # Use QTimer instead of threading.Timer
            QTimer.singleShot(50, self.scroll_to_last)  # Delay in milliseconds

    def reset_esc_counter(self):
        self.esc_counter = 0

    def keyPressEvent(self, event):
        """Override the default key press event."""
        key = event.key()
        key_name = QKeySequence(key).toString()
        # Handle Escape key to exit
        if key == Qt.Key_Escape:
            self.esc_counter += 1
            print("<Esc> pressed. Counter:", self.esc_counter)
            if self.esc_counter >= 2:
                self.running = False
                self.close()
                QApplication.instance().quit()  # Exit the main Qt application loop
        else:
            self.reset_esc_counter()

        # Handle other keys
        self.processKey(key)
        event.accept()  # Ensure the event isn't processed further.

    def eventFilter(self, obj, event):
        """Filter events to intercept key presses."""
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if obj == self.scroll_area and event.type() == event.KeyPress:
                self.keyPressEvent(event)

            # Optionally, log or pre-process key events here
            # Example: Pass scrolling keys directly to keyPressEvent
            if key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
                return super().eventFilter(obj, event)  # Let the event be handled normally.

            # Otherwise indicate that the event is handled here
            # To avoid redundant processing
            return True

        return super().eventFilter(obj, event)

    def processKey(self, key):
        """Handle non-scrolling key inputs."""
        # Your logic for handling keys goes here
        key_name = QKeySequence(key).toString()
        if key_name:
            self.add_label(key_name, key)
        else:
            self.add_label(f"Key_{key}", "<not configured>")


def main():
    # Print instructions for user
    print("Press <Esc> twice to quit.")

    # Launch PyQt5 window
    app = QApplication(sys.argv)
    window = KeyCodeWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
