import argparse

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static
from rich_pixels import Pixels
from PIL import Image, ImageSequence


class ImageViewer(Static):
    frame_index: reactive[int] = reactive(0)

    def __init__(self, image_path: str):
        super().__init__()
        self.image_path = image_path
        self.frames: list[Image.Image] = []

    def on_mount(self) -> None:
        im = Image.open(self.image_path)
        self.frames = [
            frame.copy().resize((50, 50)) for frame in ImageSequence.Iterator(im)
        ]

        self.update(Pixels.from_image(self.frames[0]))

        duration = im.info.get("duration", 100) / 1000
        self.set_interval(duration, self.next_frame)

    def next_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % len(self.frames)

    def watch_frame_index(self, frame_index: int) -> None:
        self.update(Pixels.from_image(self.frames[frame_index]))


class ConsoleImageViewer(App):
    """A Textual app to view pictures in console."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, image_path: str):
        super().__init__()
        self.image_path = image_path

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ImageViewer(self.image_path)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View images in console.")
    parser.add_argument("-i", "--image", type=str, required=True, help="Image path")
    args = parser.parse_args()

    app = ConsoleImageViewer(args.image)
    app.run()
