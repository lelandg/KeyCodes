import pygame
import sys
from _version import __version__

__author__ = "Your Name"
__license__ = "MIT"

from IPython.core.page import esc_re

modifier_keys = [
    pygame.K_LSHIFT, pygame.K_RSHIFT,  # Left/Right Shift
    pygame.K_LCTRL, pygame.K_RCTRL,  # Left/Right Control
    pygame.K_LALT, pygame.K_RALT,  # Left/Right Alt
    pygame.K_CAPSLOCK,  # Caps Lock
    pygame.K_NUMLOCK,  # Num Lock
    pygame.K_LMETA, pygame.K_RMETA  # Left/Right Meta (Command/Windows)
]

class KeyCodeViewer:
    def __init__(self):
        # Initialize pygame
        self.show_key_up = False
        pygame.init()

        # Set up display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Key Code Viewer")

        # Set up fonts and colors
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (30, 30, 30)
        self.text_color = (200, 200, 200)

        # List to display key events
        self.key_events = []
        self.max_events = 19

        # ESC key counter
        self.esc_counter = 0
        self.running = True
        self.modifiers = []

    def add_event(self, event_text):
        """Add a key event to the list and maintain max length."""
        self.key_events.append(event_text)
        if len(self.key_events) > self.max_events:
            self.key_events.pop(0)

    def reset_esc_counter(self):
        """Reset the ESC key counter."""
        self.esc_counter = 0

    def render_text(self, text, x, y):
        """Render text on the screen."""
        label = self.font.render(text, True, self.text_color)
        self.screen.blit(label, (x, y))

    def is_modifier_key(self, key):
        """Determine if the given key is a modifier key."""
        modifier_keys = [
            pygame.KMOD_SHIFT,
            pygame.KMOD_CTRL,
            pygame.KMOD_ALT,
            # pygame.KMOD_CAPS,
            pygame.KMOD_META,  # Windows/Command key
            # pygame.KMOD_NUM  # Num lock
        ]
        mods = pygame.key.get_mods()
        return (mods & key) != 0

    def is_modifier_key_name(self, key_name):
        """Determine if the given key name is a modifier key."""
        return key_name.lower() in ["right shift", "right ctrl", "right alt", "right meta", "left shift", "left ctrl", "left alt", "left meta"]

    def get_active_modifiers(self, mods):
        """Check which modifier keys are active."""
        active_mods = []  # List to store active modifiers
        if mods & pygame.KMOD_SHIFT:
            active_mods.append("Shift")
        if mods & pygame.KMOD_CTRL:
            active_mods.append("Ctrl")
        if mods & pygame.KMOD_ALT:
            active_mods.append("Alt")
        if mods & pygame.KMOD_CAPS:
            active_mods.append("Caps Lock")
        if mods & pygame.KMOD_NUM:
            active_mods.append("Num Lock")
        if mods & pygame.KMOD_META:
            active_mods.append("Meta (Command/Windows)")
        return active_mods

    def main_loop(self):
        """Main game loop to capture key events."""
        esc_counter = 0
        while self.running:
            self.screen.fill(self.bg_color)

            # Event checking
            for event in pygame.event.get():
                # if event.type == pygame.QUIT:
                #     esc_counter += 1
                #     print(f"Quit event detected. esc_counter: {esc_counter}")
                #     if esc_counter >= 2:
                #         # self.running = False
                #         break
                # else:
                #     esc_counter = 0

                if event.type == pygame.KEYDOWN:
                    modifiers = self.get_active_modifiers(event.mod)
                    if event.key in modifier_keys:
                        key_name = ""
                    else:
                        key_name = pygame.key.name(event.key)
                    if modifiers:
                        if key_name == "":
                            self.add_event(f"Key Down: {"+".join(modifiers)} (Code: {event.key})")
                        else:
                            self.add_event(f"Key Down: {"+".join(modifiers + [key_name])} (Code: {event.key})")
                    else:
                        self.add_event(f"Key Down: {key_name} (Code: {event.key})")

                    # ESC key logic
                    if event.key == pygame.K_ESCAPE:
                        self.esc_counter += 1
                        if self.esc_counter >= 2:
                            self.running = False
                            break
                    else:
                        self.reset_esc_counter()

                elif event.type == pygame.KEYUP:
                    if self.show_key_up:
                        self.add_event(f"Key Up: {key_name} (Code: {event.key})")

                if event.type != pygame.KEYDOWN:
                    break
                # Display key events
                y_offset = 20

                for idx, event_text in enumerate(self.key_events):
                    if idx == 0:
                        print(f"Processing {len(self.key_events)} key events")
                    self.render_text(event_text, 20, y_offset + (idx * 30))
                    print(event_text)
                # self.key_events.clear()

                # Update screen
                pygame.display.flip()



        pygame.quit()
        sys.exit()


def main():
    print (f"Running Pygame Key Code Viewer version {__version__}")
    viewer = KeyCodeViewer()
    viewer.main_loop()


if __name__ == "__main__":
    main()