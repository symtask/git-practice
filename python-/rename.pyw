import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

class RenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("リネーム")
        self.root.geometry("300x300")
        self.root.configure(bg="#e0f7fa")  # 爽やかな薄いブルー

        self.files = []

        # ドロップ用ラベル
        self.label = tk.Label(root, text="ここに画像をドロップ", bg="#b2ebf2", relief="ridge",
                              width=25, height=5, wraplength=180)
        self.label.pack(pady=(20, 10))
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind("<<Drop>>", self.drop)

        # 実行ボタン（非表示から開始）
        self.run_button = tk.Button(root, text="実行", command=self.rename_images, state="disabled",
                                    bg="#00bcd4", fg="white", width=15)
        self.run_button.pack(pady=(10, 5))

        # ドロップ完了メッセージ（初期は空白）
        self.status = tk.Label(root, text="", bg="#e0f7fa", fg="gray")
        self.status.pack(pady=(5, 10))

    def drop(self, event):
        self.files = self.root.tk.splitlist(event.data)
        self.status.config(text=f"{len(self.files)} ファイルをドロップしました")
        self.run_button.config(state="normal")

    def rename_images(self):
        for i, file_path in enumerate(self.files):
            folder = os.path.dirname(file_path)
            ext = os.path.splitext(file_path)[1]
            new_name = f"img_{i+1:02d}{ext}"
            new_path = os.path.join(folder, new_name)

            if not os.path.exists(new_path):  # 上書き防止
                os.rename(file_path, new_path)

        self.status.config(text="リネーム完了しました！")
        self.run_button.config(state="disabled")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = RenameApp(root)
    root.mainloop()
