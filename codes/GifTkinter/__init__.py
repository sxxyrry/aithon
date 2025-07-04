import tkinter as tk
import time
import _tkinter
from PIL import Image, ImageTk

class AnimatedGif:
    def __init__(self, root: tk.Toplevel, file_path: str, is_loop: bool = False):
        self.root: tk.Toplevel = root
        self.master = tk.Frame(root)
        self.master.pack()  # 确保Frame被正确布局
        self.file_path: str = file_path
        self.frames: list[ImageTk.PhotoImage] = []
        self.durations: list[int] = []  # 存储每一帧的延迟时间
        self.frame_index = 0
        self.is_loop: bool = is_loop
        self.load_frames()
        self.label = tk.Label(self.master)
        self.label.pack()
    def load_frames(self):
        img = Image.open(self.file_path)
        try:
            while True:
                frame = img.copy()
                photo_image = ImageTk.PhotoImage(frame)
                self.frames.append(photo_image)
                self.durations.append(img.info.get('duration', 100))  # 默认延迟为100ms
                img.seek(len(self.frames))
        except EOFError:
            return

    def start(self):
        try:
            self.update_image()
        except _tkinter.TclError:  # 如果图片已经播放完毕，则停止播放
            return

    def update_image(self):
        if not self.frames:  # 防止空帧导致错误
            return
        img: ImageTk.PhotoImage = self.frames[self.frame_index]
        self.label.config(image=img)
        self.label.image = img  # type: ignore # 避免垃圾回收
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.update()
        if not self.is_loop and self.frame_index == 0:  # 如果不循环且回到第一帧则停止
            return
        # self.root.after(self.durations[self.frame_index - 1], self.update_image)
        time.sleep(self.durations[self.frame_index - 1] / 1000)
        # self.root.after(0, self.update_image)
        self.update_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Animated Gif")
    gif_path = "path_to_your_animated_gif.gif"  # 替换为你的GIF文件路径
    animated_gif = AnimatedGif(root, gif_path, is_loop=True)  # type: ignore # 设置是否循环播放
    root.mainloop()
