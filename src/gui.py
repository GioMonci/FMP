"""Tkinter interface for the FMP image converter."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from .main import convert_to_png, default_output_path
except ImportError:
    from main import convert_to_png, default_output_path


class ConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("FMP Image Converter")
        self.root.resizable(False, False)

        self.source_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status = tk.StringVar(value="Choose an image to begin.")

        frame = ttk.Frame(root, padding=20)
        frame.grid(sticky="nsew")

        ttk.Label(frame, text="Input image").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.source_path, width=52).grid(
            row=1, column=0, padx=(0, 8), pady=(4, 12)
        )
        ttk.Button(frame, text="Browse", command=self.choose_source).grid(
            row=1, column=1, pady=(4, 12)
        )

        ttk.Label(frame, text="Output PNG").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.output_path, width=52).grid(
            row=3, column=0, padx=(0, 8), pady=(4, 16)
        )
        ttk.Button(frame, text="Save as", command=self.choose_output).grid(
            row=3, column=1, pady=(4, 16)
        )

        ttk.Button(frame, text="Convert to PNG", command=self.convert).grid(
            row=4, column=0, columnspan=2
        )
        ttk.Label(frame, textvariable=self.status).grid(
            row=5, column=0, columnspan=2, pady=(12, 0)
        )

    def choose_source(self) -> None:
        selected = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.webp *.svg *.bmp *.gif *.tif *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if selected:
            self.source_path.set(selected)
            self.output_path.set(str(default_output_path(selected)))
            self.status.set("Ready to convert.")

    def choose_output(self) -> None:
        selected = filedialog.asksaveasfilename(
            title="Save PNG as",
            initialdir=default_output_path("image").parent,
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
        )
        if selected:
            self.output_path.set(selected)

    def convert(self) -> None:
        source = self.source_path.get().strip()
        destination = self.output_path.get().strip() or None

        if not source:
            messagebox.showwarning("Missing image", "Choose an image to convert.")
            return

        try:
            output = convert_to_png(source, destination)
        except Exception as error:
            self.status.set("Conversion failed.")
            messagebox.showerror("Conversion failed", str(error))
            return

        self.output_path.set(str(output))
        self.status.set(f"Saved: {output}")
        messagebox.showinfo("Conversion complete", f"Saved PNG to:\n{output}")


def main() -> None:
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
