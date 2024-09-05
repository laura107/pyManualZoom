import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class LiveViewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live View with Zoom")
        self.root.geometry("800x600")

        self.cap = cv2.VideoCapture(1)
        self.zoom_level = 1
        self.zoom_center = (0.5, 0.5)

        self.camera_label = Label(root)
        self.camera_label.pack(expand=True, fill=tk.BOTH)

        self.zoom_in_button = Button(root, text="+ Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.zoom_out_button = Button(root, text="- Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_frame()

    def apply_zoom(self, frame):
        """Apply zoom to the frame based on the current zoom level."""
        if self.zoom_level == 1:
            return frame

        height, width = frame.shape[:2]
        center_x, center_y = int(width * self.zoom_center[0]), int(height * self.zoom_center[1])
        scale = self.zoom_level

        new_width, new_height = int(width / scale), int(height / scale)

        left = max(center_x - new_width // 2, 0)
        top = max(center_y - new_height // 2, 0)
        right = min(center_x + new_width // 2, width)
        bottom = min(center_y + new_height // 2, height)

        cropped_frame = frame[top:bottom, left:right]
        zoomed_frame = cv2.resize(cropped_frame, (width, height), interpolation=cv2.INTER_LINEAR)

        return zoomed_frame

    def refresh_frame(self):
        """Refreshes the camera frame displayed on the UI."""
        ret, frame = self.cap.read()
        if ret:
            frame = self.apply_zoom(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame)
            frame_image = ImageTk.PhotoImage(image=frame_image)

            self.camera_label.configure(image=frame_image)
            self.camera_label.image = frame_image

        self.root.after(10, self.refresh_frame)

    def zoom_in(self):
        """Increase zoom level."""
        self.zoom_level *= 1.1
        print(f"Zoom level: {self.zoom_level}")

    def zoom_out(self):
        """Decrease zoom level."""
        self.zoom_level /= 1.1
        print(f"Zoom level: {self.zoom_level}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveViewApp(root)
    root.mainloop()
