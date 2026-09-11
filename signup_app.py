"""
Signup Form with Validation and Dashboard
------------------------------------------
A small desktop application built with Tkinter that:
  - Takes Username, Email, Password on a signup form
  - Validates the inputs
  - Hashes the password before storing (SHA-256)
  - Persists users to a local JSON file (acts as "localStorage" for a
    desktop app, since browser localStorage doesn't exist outside a browser)
  - Shows all stored users in a styled dashboard table
  - Lets you delete a user entry from the dashboard

Run with:  python signup_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
import os
import hashlib

# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_store.json")

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def load_users():
    """Load the list of user dicts from the JSON storage file."""
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_users(users):
    """Persist the list of user dicts to the JSON storage file."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def hash_password(raw_password: str) -> str:
    """Return a SHA-256 hex digest of the given password."""
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Color palette / theme constants
# ---------------------------------------------------------------------------

COLOR_BG = "#eef1f8"          # app background
COLOR_CARD = "#ffffff"        # card / panel background
COLOR_HEADER = "#4338ca"      # deep indigo header bar
COLOR_HEADER_TEXT = "#ffffff"
COLOR_PRIMARY = "#4f46e5"     # signup button
COLOR_PRIMARY_HOVER = "#4338ca"
COLOR_DANGER = "#ef4444"      # delete button
COLOR_DANGER_HOVER = "#dc2626"
COLOR_TEXT = "#1f2937"
COLOR_MUTED = "#6b7280"
COLOR_ERROR = "#dc2626"
COLOR_BORDER = "#e5e7eb"
COLOR_ROW_EVEN = "#ffffff"
COLOR_ROW_ODD = "#f3f4f6"
COLOR_SELECT = "#c7d2fe"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SECTION = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_ENTRY = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")


class HoverButton(tk.Button):
    """A tk.Button that lightens/darkens on hover for a livelier feel."""

    def __init__(self, master, bg, hover_bg, fg="white", **kwargs):
        super().__init__(master, bg=bg, fg=fg, activebackground=hover_bg,
                          activeforeground=fg, relief="flat", bd=0,
                          cursor="hand2", font=FONT_BUTTON,
                          highlightthickness=0, **kwargs)
        self._bg = bg
        self._hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self._hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class SignupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signup & Dashboard")
        self.geometry("700x680")
        self.minsize(560, 420)
        self.resizable(True, True)
        self.configure(bg=COLOR_BG)

        self.users = load_users()

        self._configure_styles()

        # Everything lives inside a scrollable canvas so that no widget
        # (especially the user table) ever gets clipped off-screen on
        # smaller windows or lower-resolution displays.
        self._build_scrollable_container()

        self._build_header()
        self._build_signup_section()
        self._build_dashboard_section()
        self._refresh_table()

    def _build_scrollable_container(self):
        canvas = tk.Canvas(self, bg=COLOR_BG, highlightthickness=0)
        vscroll = ttk.Scrollbar(self, orient="vertical",
                                 command=canvas.yview,
                                 style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=vscroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        # self.content is where every widget below actually gets built.
        self.content = tk.Frame(canvas, bg=COLOR_BG)
        window_id = canvas.create_window((0, 0), window=self.content,
                                          anchor="nw")

        def on_content_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            # Make the inner frame track the canvas width so cards stretch
            # to fill the window instead of staying a fixed narrow width.
            canvas.itemconfig(window_id, width=event.width)

        self.content.bind("<Configure>", on_content_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)          # Windows/macOS
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

    # -- Styling --------------------------------------------------------

    def _configure_styles(self):
        style = ttk.Style(self)
        # 'clam' theme is the most reliably customizable across platforms
        style.theme_use("clam")

        style.configure("Treeview",
                         background=COLOR_ROW_EVEN,
                         fieldbackground=COLOR_ROW_EVEN,
                         foreground=COLOR_TEXT,
                         rowheight=30,
                         font=FONT_LABEL,
                         borderwidth=0)
        style.map("Treeview",
                  background=[("selected", COLOR_SELECT)],
                  foreground=[("selected", COLOR_TEXT)])

        style.configure("Treeview.Heading",
                         background=COLOR_HEADER,
                         foreground=COLOR_HEADER_TEXT,
                         font=FONT_SECTION,
                         relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", COLOR_PRIMARY_HOVER)])

        style.configure("Vertical.TScrollbar",
                         background=COLOR_BORDER,
                         troughcolor=COLOR_BG,
                         arrowcolor=COLOR_TEXT,
                         borderwidth=0)

    # -- UI construction --------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self.content, bg=COLOR_HEADER, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="🔐  Signup & Dashboard", bg=COLOR_HEADER,
                 fg=COLOR_HEADER_TEXT, font=FONT_TITLE).pack(
            side="left", padx=20)

        tk.Label(header, text="passwords hashed with SHA-256",
                 bg=COLOR_HEADER, fg="#c7d2fe",
                 font=("Segoe UI", 9, "italic")).pack(side="right", padx=20)

    def _card(self, title):
        """Build a card-style container with a title strip on top."""
        # IMPORTANT: parent must be self.content (the scrollable frame),
        # not self (the root window) — otherwise this card competes for
        # space with the canvas/scrollbar at the root level and gets
        # squeezed to zero size, making it invisible.
        outer = tk.Frame(self.content, bg=COLOR_CARD,
                          highlightbackground=COLOR_BORDER,
                          highlightthickness=1, bd=0)
        title_bar = tk.Frame(outer, bg=COLOR_CARD)
        title_bar.pack(fill="x", padx=18, pady=(14, 0))
        tk.Label(title_bar, text=title, bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_SECTION).pack(anchor="w")
        tk.Frame(outer, bg=COLOR_BORDER, height=1).pack(fill="x", padx=18,
                                                          pady=(8, 0))
        return outer

    def _build_signup_section(self):
        card = self._card("Create an account")
        card.pack(fill="x", padx=18, pady=(16, 8))

        body = tk.Frame(card, bg=COLOR_CARD)
        body.pack(fill="x", padx=18, pady=14)
        body.grid_columnconfigure(1, weight=1)

        entry_style = dict(font=FONT_ENTRY, bg="#f9fafb", fg=COLOR_TEXT,
                            relief="flat", highlightthickness=1,
                            highlightbackground=COLOR_BORDER,
                            highlightcolor=COLOR_PRIMARY, insertbackground=COLOR_TEXT)

        # Username
        tk.Label(body, text="👤 Username", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_LABEL, anchor="w").grid(row=0, column=0, sticky="w",
                                                     pady=(0, 4))
        self.username_var = tk.StringVar()
        tk.Entry(body, textvariable=self.username_var, **entry_style).grid(
            row=1, column=0, columnspan=2, sticky="ew", ipady=6, pady=(0, 12))

        # Email
        tk.Label(body, text="✉ Email", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_LABEL, anchor="w").grid(row=2, column=0, sticky="w",
                                                     pady=(0, 4))
        self.email_var = tk.StringVar()
        tk.Entry(body, textvariable=self.email_var, **entry_style).grid(
            row=3, column=0, columnspan=2, sticky="ew", ipady=6, pady=(0, 12))

        # Password
        tk.Label(body, text="🔒 Password", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_LABEL, anchor="w").grid(row=4, column=0, sticky="w",
                                                     pady=(0, 4))
        self.password_var = tk.StringVar()
        tk.Entry(body, textvariable=self.password_var, show="•",
                  **entry_style).grid(row=5, column=0, columnspan=2,
                                       sticky="ew", ipady=6, pady=(0, 4))

        # Error / status label
        self.status_label = tk.Label(body, text="", fg=COLOR_ERROR,
                                      bg=COLOR_CARD, font=("Segoe UI", 9),
                                      anchor="w", justify="left")
        self.status_label.grid(row=6, column=0, columnspan=2, sticky="w",
                                pady=(2, 10))

        # Signup button
        signup_btn = HoverButton(body, bg=COLOR_PRIMARY,
                                  hover_bg=COLOR_PRIMARY_HOVER,
                                  text="Create Account", command=self.on_signup)
        signup_btn.grid(row=7, column=0, columnspan=2, sticky="ew", ipady=8)

    def _build_dashboard_section(self):
        card = self._card("Registered Users")
        card.pack(fill="both", expand=True, padx=18, pady=(8, 18))

        body = tk.Frame(card, bg=COLOR_CARD)
        body.pack(fill="both", expand=True, padx=18, pady=14)

        # Reserve space for the button at the BOTTOM first, so it always
        # stays visible even if the table above grows to fill the space.
        button_bar = tk.Frame(body, bg=COLOR_CARD)
        button_bar.pack(side="bottom", fill="x", pady=(12, 0))

        delete_btn = HoverButton(button_bar, bg=COLOR_DANGER,
                                  hover_bg=COLOR_DANGER_HOVER,
                                  text="🗑  Delete Selected",
                                  command=self.on_delete)
        delete_btn.pack(ipadx=10, ipady=6)

        # Table + scrollbar container
        table_container = tk.Frame(body, bg=COLOR_CARD)
        table_container.pack(side="top", fill="both", expand=True)

        columns = ("username", "email", "password")
        self.tree = ttk.Treeview(table_container, columns=columns,
                                  show="headings", height=10,
                                  selectmode="browse")
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.heading("password", text="Password (hashed)")
        self.tree.column("username", width=140, anchor="w")
        self.tree.column("email", width=240, anchor="w")
        self.tree.column("password", width=220, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        # Alternating row colors (striped table)
        self.tree.tag_configure("evenrow", background=COLOR_ROW_EVEN)
        self.tree.tag_configure("oddrow", background=COLOR_ROW_ODD)

        scrollbar = ttk.Scrollbar(table_container, orient="vertical",
                                   command=self.tree.yview,
                                   style="Vertical.TScrollbar")
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # -- Behaviour ------------------------------------------------------

    def on_signup(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()

        error = self._validate(username, email, password)
        if error:
            self.status_label.config(text=f"⚠ {error}")
            return

        self.status_label.config(text="")

        new_user = {
            "username": username,
            "email": email,
            "password": hash_password(password),  # never store raw password
        }
        self.users.append(new_user)
        save_users(self.users)

        self._refresh_table()
        self._clear_form()
        messagebox.showinfo("Success", f"User '{username}' signed up successfully!")

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a row to delete.")
            return

        item_id = selected[0]
        index = int(item_id)  # we tag items with their index in self.users
        username = self.users[index]["username"]

        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete user '{username}'?")
        if not confirm:
            return

        del self.users[index]
        save_users(self.users)
        self._refresh_table()

    # -- Helpers ----------------------------------------------------------

    def _validate(self, username, email, password):
        if not username:
            return "Username cannot be empty."
        if not email or not EMAIL_REGEX.match(email):
            return "Please enter a valid email address."
        if not password or len(password) < 6:
            return "Password must be at least 6 characters long."
        return None

    def _clear_form(self):
        self.username_var.set("")
        self.email_var.set("")
        self.password_var.set("")

    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for idx, user in enumerate(self.users):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            # iid = string index into self.users, used later for deletion
            self.tree.insert("", "end", iid=str(idx), values=(
                user["username"], user["email"], user["password"]),
                tags=(tag,))


if __name__ == "__main__":
    app = SignupApp()
    app.mainloop()
