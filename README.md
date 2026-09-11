# Signup & Dashboard App

A small desktop application built with **Python and Tkinter** that lets a user sign up with a Username, Email, and Password, validates their input, securely hashes the password, and displays all registered users in a live dashboard table with the ability to delete entries.

No external libraries, no database, no internet connection required — everything runs from a single Python file using only the standard library.

---

## 🎥 Demo

[Demo Video](https://youtu.be/KMHYh2i21FI)

---

## ✨ Features Implemented

- **Signup form** with three fields: Username, Email, Password
- **Input validation**
  - Username cannot be empty
  - Email must match a valid email pattern (checked with regex)
  - Password must be at least 6 characters long
- **Password hashing** — passwords are hashed with SHA-256 before being stored; the raw password is never saved anywhere
- **Persistent storage** — user records are saved to a local `users_store.json` file, so data survives closing and reopening the app (this is the desktop equivalent of a browser's `localStorage`)
- **Dashboard table** — every registered user is displayed in a table with Username, Email, and hashed Password columns
- **Delete function** — select any row in the table and remove that user, with a confirmation prompt before deleting

## 🌟 Additional Features Added

Beyond the base requirements, this version also includes:

- **Custom color theme** — a consistent indigo/white color palette applied across the whole app
- **Hover-effect buttons** — the Signup and Delete buttons visually react when you hover over them
- **Striped table rows** — alternating row colors for easier reading
- **Scrollable window** — the entire UI is wrapped in a scrollable canvas, so nothing gets cut off even on smaller screens, and it responds to mouse-wheel scrolling on Windows, Mac, and Linux
- **Auto-sizing window** — the window automatically sizes itself to fit its content (capped to the screen size) and centers itself on launch
- **Confirmation dialogs** — success and warning popups guide the user through signup and deletion
- **Card-based layout** — the form and dashboard are each wrapped in a clean, bordered "card" panel, similar to modern web UI design

## 🛠️ How to Run

**Requirements:** Python 3.7+ (Tkinter ships with most standard Python installs)

```bash
# Clone the repository
git clone https://github.com/<your-username>/signup-dashboard-app.git
cd signup-dashboard-app

# Run the app
python signup_app.py
```

> **Linux users:** if you get a `No module named 'tkinter'` error, install it first:
> ```bash
> sudo apt install python3-tk
> ```

On first run, a `users_store.json` file will be created automatically in the same folder — this is where your signed-up users are saved. It's excluded from version control via `.gitignore` since it's user-generated data, not source code.

## 📁 Project Structure

```
signup-dashboard-app/
├── signup_app.py       # the entire application (single file)
├── README.md           # this file
└── .gitignore          # excludes generated data & cache files
```

## 🧠 Concepts Covered

Building this project touches on a range of core programming and software design concepts:

- **GUI programming with Tkinter** — windows, frames, labels, entries, buttons, and the `Treeview` table widget
- **Event-driven programming** — the app doesn't run top-to-bottom; it sits idle and reacts to button clicks and other events via `mainloop()`
- **Layout managers** — using `pack()` and `grid()` together, and understanding how widget packing order affects what's visible on screen
- **Object-oriented design** — the whole app is structured as a class (`SignupApp`), with a custom subclassed widget (`HoverButton`) for reusable behavior
- **Input validation** — writing clear, rule-based checks and giving the user specific feedback when something's wrong
- **Regular expressions** — using `re` to validate email format
- **One-way hashing** — using `hashlib` (SHA-256) to store passwords securely, and understanding why hashing (not encryption) is the right tool for passwords, since it can't be reversed
- **File I/O & JSON** — reading and writing structured data to disk so it persists between runs
- **Styling `ttk` widgets** — using `ttk.Style` to theme widgets (like the table and scrollbar) that don't support plain `tk` color options
- **Building a scrollable container** — Tkinter has no built-in scrollable frame, so this project implements the common `Canvas` + `Scrollbar` + embedded `Frame` pattern from scratch, including handling different scroll-wheel events across operating systems

## 📄 License

Feel free to use this project for learning purposes.
