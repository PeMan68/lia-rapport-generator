"""
Dialog för granskning och selektiv filtrering av kommentarer före PDF-generering
"""

import tkinter as tk
from tkinter import ttk


class CommentFilterDialog:
    """
    Modal dialog som låter läraren granska och selektivt dölja enstaka
    kommentarer innan PDF-rapporterna genereras.

    Användning:
        dialog = CommentFilterDialog(parent, students_data)
        if not dialog.cancelled:
            exclusions = dialog.exclusions
    """

    def __init__(self, parent, students_data):
        self.students_data = students_data
        self._vars = {}
        self._cancelled = True
        self._exclusions = {}

        self._win = tk.Toplevel(parent)
        self._win.title("Granska kommentarer")
        self._win.geometry("760x560")
        self._win.minsize(580, 400)
        self._win.transient(parent)
        self._win.grab_set()

        self._build_ui()
        parent.wait_window(self._win)

    # ── public ──────────────────────────────────────────────────

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    @property
    def exclusions(self) -> dict:
        """
        Dict med kommentarer som ska döljas.
        Format: {student_name: {'assessments': {idx: False}, 'final_comments': False}}
        Endast uteslutna kommentarer ingår i returvärdet.
        """
        return self._exclusions

    # ── UI ──────────────────────────────────────────────────────

    def _build_ui(self):
        top = ttk.Frame(self._win, padding="10 10 10 5")
        top.pack(fill=tk.X)

        ttk.Label(
            top,
            text="Avmarkera kommentarer som INTE ska synas i studentrapporten:",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Separator(self._win, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)

        scroll_area = tk.Frame(self._win)
        scroll_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar måste packas INNAN canvas på Windows
        vsb = ttk.Scrollbar(scroll_area, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas = tk.Canvas(scroll_area, yscrollcommand=vsb.set, highlightthickness=0)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self._canvas.yview)

        # tk.Frame (inte ttk) inuti canvas för bättre Windows-kompatibilitet
        self._inner = tk.Frame(self._canvas)
        self._inner.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._cwin = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._canvas.bind("<Configure>", self._on_canvas_resize)
        self._win.bind("<MouseWheel>", self._on_scroll)

        # Dubbel after_idle: första ideln låter pack-geometri beräknas,
        # andra ideln kör populate när canvas verkligen har sin slutstorlek
        self._win.after_idle(lambda: self._win.after_idle(self._start_populate))

        ttk.Separator(self._win, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)
        bottom = ttk.Frame(self._win, padding="10 8")
        bottom.pack(fill=tk.X)

        self._status = ttk.Label(bottom, text="", foreground="#666")
        self._status.pack(side=tk.LEFT)

        ttk.Button(bottom, text="Avbryt", command=self._on_cancel).pack(
            side=tk.RIGHT, padx=(5, 0)
        )
        ttk.Button(bottom, text="OK", command=self._on_ok).pack(side=tk.RIGHT)

        self._refresh_status()

    def _start_populate(self):
        """Kallas via dubbel after_idle för att canvas ska ha korrekt storlek."""
        w = self._canvas.winfo_width()
        if w <= 1:
            # Canvas ännu inte ritat klart — försök igen om 100ms
            self._win.after(100, self._start_populate)
            return
        self._canvas.itemconfig(self._cwin, width=w)
        self._populate()
        self._win.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._refresh_status()

    def _populate(self):
        for student in self.students_data:
            name = student.get("student_name", "Okänd")
            assessments = student.get("assessments", [])
            final = student.get("final_comments", "").strip()

            self._vars[name] = {"assessments": {}, "final_comments": None}

            section = ttk.LabelFrame(self._inner, text=name, padding="5 3 5 5")
            section.pack(fill=tk.X, padx=5, pady=3)

            # Knappar per student
            btn_row = tk.Frame(section)
            btn_row.pack(anchor=tk.E, pady=(0, 4))
            ttk.Button(
                btn_row, text="Välj alla", width=10,
                command=lambda n=name: self._select_student(n)
            ).pack(side=tk.LEFT, padx=(0, 4))
            ttk.Button(
                btn_row, text="Avmarkera alla", width=13,
                command=lambda n=name: self._deselect_student(n)
            ).pack(side=tk.LEFT)

            has_any = False

            for i, area in enumerate(assessments):
                comment = area.get("comment", "").strip()
                if not comment:
                    continue
                has_any = True
                area_label = area.get('area', area.get('name', f'Område {i+1}'))
                label = f"{area_label}: \"{self._clip(comment)}\""
                var = tk.BooleanVar(value=True)
                var.trace_add("write", lambda *_: self._refresh_status())
                self._vars[name]["assessments"][i] = var
                tk.Checkbutton(
                    section, text=label, variable=var, wraplength=680, anchor=tk.W, justify=tk.LEFT
                ).pack(anchor=tk.W, pady=1, fill=tk.X)

            if final:
                has_any = True
                var = tk.BooleanVar(value=True)
                var.trace_add("write", lambda *_: self._refresh_status())
                self._vars[name]["final_comments"] = var
                tk.Checkbutton(
                    section,
                    text=f"Avslutande: \"{self._clip(final)}\"",
                    variable=var,
                    wraplength=680,
                    anchor=tk.W,
                    justify=tk.LEFT,
                ).pack(anchor=tk.W, pady=1, fill=tk.X)

            if not has_any:
                tk.Label(section, text="(Inga kommentarer)", fg="#999").pack(anchor=tk.W)

    # ── helpers ─────────────────────────────────────────────────

    @staticmethod
    def _clip(text: str, max_len: int = 90) -> str:
        return text if len(text) <= max_len else text[: max_len - 3] + "..."

    def _on_canvas_resize(self, event):
        self._canvas.itemconfig(self._cwin, width=event.width)

    def _on_scroll(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _each_var(self):
        for d in self._vars.values():
            yield from d["assessments"].values()
            if d["final_comments"]:
                yield d["final_comments"]

    def _select_student(self, name: str):
        d = self._vars.get(name, {})
        for v in d.get("assessments", {}).values():
            v.set(True)
        if d.get("final_comments"):
            d["final_comments"].set(True)

    def _deselect_student(self, name: str):
        d = self._vars.get(name, {})
        for v in d.get("assessments", {}).values():
            v.set(False)
        if d.get("final_comments"):
            d["final_comments"].set(False)

    def _refresh_status(self):
        total = sum(1 for _ in self._each_var())
        hidden = sum(1 for v in self._each_var() if not v.get())
        if hidden == 0:
            self._status.config(text=f"Alla {total} kommentarer visas")
        else:
            self._status.config(
                text=f"{hidden} av {total} kommentarer kommer döljas i studentrapporten"
            )

    def _on_ok(self):
        excl = {}
        for name, d in self._vars.items():
            s = {}
            hidden = {idx: False for idx, v in d["assessments"].items() if not v.get()}
            if hidden:
                s["assessments"] = hidden
            if d["final_comments"] and not d["final_comments"].get():
                s["final_comments"] = False
            if s:
                excl[name] = s
        self._exclusions = excl
        self._cancelled = False
        self._win.destroy()

    def _on_cancel(self):
        self._win.destroy()
