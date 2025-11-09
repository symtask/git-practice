import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinterdnd2 import *
from PIL import Image
import os

class ImageGridCombiner:
    def __init__(self, root):
        self.root = root  # ← 二重定義やめる！
        self.root.title("画像グリッド結合くん")
        self.images = []
        self.setup_ui()

    def setup_ui(self):
        # 画像選択（ドロップラベル）
        self.drop_label = tk.Label(self.root, text="ここをクリックまたは画像をドロップ", bg="#dddddd", width=50, height=4)
        self.drop_label.pack(pady=10)
        self.drop_label.bind("<Button-1>", self.select_files)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.drop_files)

        # 縦枚数（2～6）
        tk.Label(self.root, text="縦の画像枚数：").pack()
        self.rows_var = tk.IntVar(value=2)
        ttk.Combobox(self.root, textvariable=self.rows_var, values=[2, 3, 4, 5, 6], state="readonly").pack()

        # 横枚数（2～6）
        tk.Label(self.root, text="横の画像枚数：").pack()
        self.cols_var = tk.IntVar(value=5)
        ttk.Combobox(self.root, textvariable=self.cols_var, values=[2, 3, 4, 5, 6], state="readonly").pack()

        # アスペクト比選択
        tk.Label(self.root, text="アスペクト比：").pack()
        self.aspect_ratio_var = tk.StringVar(value="3:2")
        tk.Radiobutton(self.root, text="1:1 (400x400)", variable=self.aspect_ratio_var, value="1:1").pack()
        tk.Radiobutton(self.root, text="3:2 (600x400)", variable=self.aspect_ratio_var, value="3:2").pack()

        # 実行ボタン
        tk.Button(self.root, text="画像を結合して保存", command=self.combine_and_save).pack(pady=20)

    def select_files(self, event=None):
        filepaths = filedialog.askopenfilenames(filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.webp")])
        if filepaths:
            self.images = [Image.open(f).convert("RGB") for f in filepaths]
            self.drop_label.config(text=f"{len(self.images)} 枚の画像を読み込みました")

    def drop_files(self, event):
        filepaths = self.root.splitlist(event.data)
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        filtered_files = [f for f in filepaths if os.path.splitext(f.lower())[1] in valid_extensions]
        if filtered_files:
            self.images = [Image.open(f).convert("RGB") for f in filtered_files]
            self.drop_label.config(text=f"{len(self.images)} 枚の画像を読み込みました")

    def combine_and_save(self):
        if not self.images:
            messagebox.showerror("エラー", "画像を選択してください")
            return

        cols = self.cols_var.get()
        rows = self.rows_var.get()
        max_images = cols * rows
        images = self.images[:max_images]

        if len(self.images) > max_images:
            messagebox.showwarning("注意", f"{len(self.images)} 枚読み込みましたが、{max_images} 枚まで使用します。")
        elif len(self.images) < max_images:
            messagebox.showwarning("注意", f"{max_images} 枚必要ですが、{len(self.images)} 枚しかありません。空白で埋めます。")

        # アスペクト比に基づくターゲットサイズ
        aspect_ratio = self.aspect_ratio_var.get()
        if aspect_ratio == "1:1":
            target_width = 400
            target_height = 400
            target_ratio = 1.0
        else:  # 3:2
            target_width = 400
            target_height = 600
            target_ratio = 1.5

        processed_images = []
        for img in images:
            img_width, img_height = img.size
            img_ratio = img_height / img_width

            # アスペクト比を保ちつつリサイズ
            if img_ratio > target_ratio:  # 縦長
                scale = target_height / img_height
                new_width = int(img_width * scale)
                new_height = target_height
            else:  # 横長または適切
                scale = target_width / img_width
                new_width = target_width
                new_height = int(img_height * scale)

            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # ターゲットサイズのキャンバスに中央配置
            canvas = Image.new("RGB", (target_width, target_height), color=(255, 255, 255))
            x_offset = (target_width - new_width) // 2
            y_offset = (target_height - new_height) // 2
            canvas.paste(resized, (x_offset, y_offset))
            processed_images.append(canvas)

        # 空白を埋めるためにダミー画像を追加
        while len(processed_images) < max_images:
            processed_images.append(Image.new("RGB", (target_width, target_height), color=(255, 255, 255)))

        # 結合画像サイズ（縦×横を正しく）
        total_height = rows * target_height
        total_width = cols * target_width
        new_img = Image.new("RGB", (total_width, total_height), color=(255, 255, 255))

        # 配置
        for index, img in enumerate(processed_images):
            x = (index % cols) * target_width
            y = (index // cols) * target_height
            new_img.paste(img, (x, y))

        # 保存先選択
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG 画像", "*.jpg"), ("PNG 画像", "*.png"), ("WEBP 画像", "*.webp")],
            initialfile="結合画像.jpg"
        )
        if save_path:
            new_img.save(save_path)
            messagebox.showinfo("保存完了", f"保存しました：\n{save_path}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageGridCombiner(root)
    root.mainloop()
