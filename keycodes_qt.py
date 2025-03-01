import sys

from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget, QLabel, QPushButton

from _version import __version__

__author__ = "Leland Green"
__license__ = "CC0-1.0"


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Instructions.")
        self.resize(300, 200)

        # Help message as a QLabel
        help_text = QLabel("Press a key and note the returned value.\n\n"
                           "Press F1 for help. (This screen.)\n\n"
                           "Press Esc twice to quit. (Or three times from this dialog.)")
        help_text.setWordWrap(True)  # Enable text wrapping
        # help_text.setAlignment(Qt.AlignCenter)
        # help_text.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc; }")
        font = QFont()
        font.setPointSize(12)
        help_text.setFont(font)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Dialog layout
        layout = QVBoxLayout()
        layout.addWidget(help_text)
        layout.addWidget(help_text)
        layout.addWidget(close_button)
        self.setLayout(layout)


class KeyCodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keycodes - <Esc> twice to quit.")
        self.setGeometry(0, 0, 400, 500)

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

    def sanitize_string(self, value):
        """Sanitize strings to avoid UnicodeEncodeError."""
        try:
            return str(value).encode("utf-8", errors="replace").decode("utf-8")
        except Exception:
            return "<invalid>"

    def add_label(self, name, value):
        """Add a label to the layout and scroll to the bottom."""
        # sanitized_name = self.sanitize_string(name)
        # sanitized_value = self.sanitize_string(value)
        # label = QLabel(f"<span style='color: purple;'>{sanitized_name}</span>: <span style='color: blue;'>{sanitized_value}</span>")
        # print(f"Key pressed: {sanitized_name} ({sanitized_value})")
        label = QLabel(f"<span style='color: purple;'>{name.replace('<','&lt;').replace('>','&gt;')}</span> : <span style='color: blue;'>{value}</span>")
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 0px; border: 0px solid #ccc; }")
        label.setToolTip(f"Key pressed: {name} ({value})")

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
        key_name = event.text()

        # print(f"Key pressed: {key_name} ({key})")

        # Initialize a list to store active modifiers
        modifiers = []

        # Check for specific modifiers
        if event.modifiers() & Qt.ControlModifier:
            modifiers.append("Ctrl")
        if event.modifiers() & Qt.AltModifier:
            modifiers.append("Alt")
        if event.modifiers() & Qt.ShiftModifier:
            modifiers.append("Shift")

        if len(modifiers) > 0:
            key_name = QKeySequence(key).toString(QKeySequence.NativeText)
        # print(f"Key pressed: {key_name} ({key})")
        # Handle Escape key to exit
        if key == Qt.Key_Escape:
            key_name = "<Esc>"
            self.esc_counter += 1
            # print("<Esc> pressed. Press again to quit.")
            if self.esc_counter >= 2:
                self.running = False
                self.close()
                QApplication.instance().quit()  # Exit the main Qt application loop
        else:
            self.reset_esc_counter()

        if key in [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta] and not key_name:
            key_name = "+".join(modifiers)
        elif not key_name:
            key_name = QKeySequence(key).toString()


        # if key_name:
        if not key in [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta]:
            modifiers.append(key_name)
        if len(modifiers) > 0:
            self.add_label("+".join(modifiers), key)
        else:
            self.add_label(key_name, key)

        if key == Qt.Key_F1:
            help_dialog = HelpDialog()
            help_dialog.exec()

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


def main():
    print(f"Keycodes Viewer v{__version__}")
    # Print instructions for user
    print("Press <Esc> twice to quit.")

    # Launch PyQt5 window
    app = QApplication(sys.argv)
    window = KeyCodeWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
