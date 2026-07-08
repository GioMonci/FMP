"""Tkinter interface for the FMP image converter."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from .main import convert_to_png, default_output_path
except ImportError:
    from main import convert_to_png, default_output_path


BACKGROUND = "#f4f7fb"
CARD = "#ffffff"
TEXT = "#172033"
MUTED = "#687386"
PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
BORDER = "#dbe3ef"
SUCCESS = "#15803d"
ERROR = "#b91c1c"


class ConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("FMP Image Converter")
        self.root.geometry("680x500")
        self.root.resizable(False, False)
        self.root.configure(background=BACKGROUND)

        self.source_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status = tk.StringVar(value="Choose an image to begin.")

        self.configure_styles()
        self.build_interface()
        self.center_window()
        self.root.bind("<Return>", lambda _event: self.convert())

    def configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("App.TFrame", background=BACKGROUND)
        style.configure("Card.TFrame", background=CARD)
        style.configure(
            "Title.TLabel",
            background=BACKGROUND,
            foreground=TEXT,
            font=("Helvetica", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=BACKGROUND,
            foreground=MUTED,
            font=("Helvetica", 11),
        )
        style.configure(
            "Field.TLabel",
            background=CARD,
            foreground=TEXT,
            font=("Helvetica", 11, "bold"),
        )
        style.configure(
            "Hint.TLabel",
            background=CARD,
            foreground=MUTED,
            font=("Helvetica", 9),
        )
        style.configure(
            "Path.TEntry",
            padding=10,
            fieldbackground="#f8fafc",
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
        )
        style.map("Path.TEntry", bordercolor=[("focus", PRIMARY)])
        style.configure(
            "Secondary.TButton",
            padding=(14, 10),
            background="#e8eef8",
            foreground=TEXT,
            borderwidth=0,
            font=("Helvetica", 10, "bold"),
        )
        style.map("Secondary.TButton", background=[("active", "#dce6f5")])
        style.configure(
            "Primary.TButton",
            padding=(18, 12),
            background=PRIMARY,
            foreground="white",
            borderwidth=0,
            font=("Helvetica", 11, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", PRIMARY_DARK), ("pressed", PRIMARY_DARK)],
        )
        style.configure(
            "Status.TLabel",
            background=BACKGROUND,
            foreground=MUTED,
            font=("Helvetica", 10),
        )
        style.configure("Success.Status.TLabel", foreground=SUCCESS)
        style.configure("Error.Status.TLabel", foreground=ERROR)

    def build_interface(self) -> None:
        page = ttk.Frame(self.root, style="App.TFrame", padding=(40, 30))
        page.pack(fill="both", expand=True)

        header = ttk.Frame(page, style="App.TFrame")
        header.pack(fill="x", pady=(0, 22))

        logo = tk.Label(
            header,
            text="FMP",
            background=PRIMARY,
            foreground="white",
            font=("Helvetica", 14, "bold"),
            padx=14,
            pady=12,
        )
        logo.pack(side="left", padx=(0, 14))

        heading = ttk.Frame(header, style="App.TFrame")
        heading.pack(side="left")
        ttk.Label(
            heading,
            text="Convert images to PNG",
            style="Title.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            heading,
            text="JPEG, WebP, SVG, BMP, GIF, and TIFF supported",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        card_border = tk.Frame(
            page,
            background=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0,
        )
        card_border.pack(fill="x")

        card = ttk.Frame(card_border, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text="Input image", style="Field.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Entry(
            card,
            textvariable=self.source_path,
            style="Path.TEntry",
        ).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(7, 5))
        ttk.Button(
            card,
            text="Browse",
            command=self.choose_source,
            style="Secondary.TButton",
        ).grid(row=1, column=1, sticky="ew", pady=(7, 5))
        ttk.Label(
            card,
            text="Choose the image you want to convert.",
            style="Hint.TLabel",
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ttk.Label(card, text="Output location", style="Field.TLabel").grid(
            row=3, column=0, columnspan=2, sticky="w"
        )
        ttk.Entry(
            card,
            textvariable=self.output_path,
            style="Path.TEntry",
        ).grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=(7, 5))
        ttk.Button(
            card,
            text="Save as",
            command=self.choose_output,
            style="Secondary.TButton",
        ).grid(row=4, column=1, sticky="ew", pady=(7, 5))
        ttk.Label(
            card,
            text="Defaults to your Downloads folder.",
            style="Hint.TLabel",
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 22))

        ttk.Button(
            card,
            text="Convert to PNG",
            command=self.convert,
            style="Primary.TButton",
        ).grid(row=6, column=0, columnspan=2, sticky="ew")

        self.status_label = ttk.Label(
            page,
            textvariable=self.status,
            style="Status.TLabel",
            anchor="center",
        )
        self.status_label.pack(fill="x", pady=(18, 0))

    def center_window(self) -> None:
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_status(self, message: str, status_type: str = "normal") -> None:
        styles = {
            "normal": "Status.TLabel",
            "success": "Success.Status.TLabel",
            "error": "Error.Status.TLabel",
        }
        self.status.set(message)
        self.status_label.configure(style=styles[status_type])

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
            self.set_status("Ready to convert.")

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
            self.set_status("Choose an image before converting.", "error")
            messagebox.showwarning("Missing image", "Choose an image to convert.")
            return

        self.set_status("Converting image...")
        self.root.update_idletasks()

        try:
            output = convert_to_png(source, destination)
        except Exception as error:
            self.set_status("Conversion failed. Check the error message.", "error")
            messagebox.showerror("Conversion failed", str(error))
            return

        self.output_path.set(str(output))
        self.set_status(f"Saved successfully to {output}", "success")
        messagebox.showinfo("Conversion complete", f"Saved PNG to:\n{output}")


def main() -> None:
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
