import threading
from main import research
import customtkinter as ctk
from tkinter import messagebox

# ============================================================
# assistGPT - CustomTkinter UI prototype
# Based on the draw.io design supplied by the user.
# This version focuses on the UI only; AI/API logic comes later.
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AssistGPT(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("assistGPT")
        self.geometry("1200x720")
        self.minsize(900, 600)

        # ---------- Colors ----------
        self.bg = "#0b0f14"
        self.sidebar_bg = "#101720"
        self.panel_bg = "#111820"
        self.input_bg = "#151b22"
        self.border = "#303841"
        self.text = "#f3f6f8"
        self.muted = "#8f9aa5"
        self.blue = "#168cff"
        self.blue_hover = "#0b75dc"
        self.purple = "#8b72e8"
        self.green = "#14b8a6"

        self.configure(fg_color=self.bg)

        # Main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    # ========================================================
    # SIDEBAR
    # ========================================================
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color=self.sidebar_bg
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo / app name
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(20, 22))

        logo = ctk.CTkLabel(
            brand,
            text="◉",
            width=38,
            height=38,
            corner_radius=9,
            fg_color="#12a99b",
            text_color="#071014",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo.pack(side="left")

        name = ctk.CTkLabel(
            brand,
            text="assistGPT",
            text_color=self.text,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name.pack(side="left", padx=10)

        # New chat
        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="＋  NEW",
            height=42,
            corner_radius=9,
            fg_color=self.purple,
            hover_color="#735bd1",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.new_chat
        )
        self.new_chat_btn.pack(fill="x", padx=18, pady=(0, 18))

        # Chat label
        ctk.CTkLabel(
            self.sidebar,
            text="CHAT",
            anchor="w",
            text_color=self.muted,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(fill="x", padx=20, pady=(0, 8))

        # Chat history
        self.chat_list = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            scrollbar_button_color="#29333d",
            scrollbar_button_hover_color="#3b4854"
        )
        self.chat_list.pack(fill="both", expand=True, padx=10)

        for title in ["Welcome chat", "Python project", "AI Assistant", "My project"]:
            self.add_chat_item(title)

        # Bottom user profile
        profile = ctk.CTkFrame(
            self.sidebar,
            height=70,
            corner_radius=0,
            fg_color="#0c1219"
        )
        profile.pack(fill="x", side="bottom")

        avatar = ctk.CTkLabel(
            profile,
            text="👤",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#26313c",
            font=ctk.CTkFont(size=18)
        )
        avatar.pack(side="left", padx=(15, 10), pady=14)

        ctk.CTkLabel(
            profile,
            text="Admin",
            text_color=self.text,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            profile,
            text="⚙",
            width=35,
            height=35,
            fg_color="transparent",
            hover_color="#202a34",
            text_color=self.muted,
            font=ctk.CTkFont(size=18),
            command=self.show_settings
        ).pack(side="right", padx=10)

    def add_chat_item(self, title):
        button = ctk.CTkButton(
            self.chat_list,
            text="  💬  " + title,
            anchor="w",
            height=40,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#1d2731",
            text_color="#d9e0e6",
            font=ctk.CTkFont(size=13),
            command=lambda t=title: self.select_chat(t)
        )
        button.pack(fill="x", pady=2)

    # ========================================================
    # MAIN AREA
    # ========================================================
    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.bg
        )
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(
            self.main,
            height=70,
            corner_radius=0,
            fg_color="#0d131a",
            border_width=1,
            border_color=self.border
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=24, pady=12)

        bot_avatar = ctk.CTkLabel(
            title_frame,
            text="✦",
            width=42,
            height=42,
            corner_radius=21,
            fg_color="#146fe8",
            text_color="white",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        bot_avatar.pack(side="left")

        titles = ctk.CTkFrame(title_frame, fg_color="transparent")
        titles.pack(side="left", padx=12)

        ctk.CTkLabel(
            titles,
            text="assistGPT",
            text_color=self.text,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            titles,
            text="AI Assistant",
            text_color=self.muted,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="⋮",
            width=42,
            height=42,
            fg_color="transparent",
            hover_color="#1b252e",
            text_color=self.muted,
            font=ctk.CTkFont(size=24),
            command=self.show_menu
        ).pack(side="right", padx=15)

        ctk.CTkLabel(
            header,
            text="⚙  Admin",
            text_color="#b7c0c8",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="right", padx=5)

        # Chat area
        self.chat_area = ctk.CTkScrollableFrame(
            self.main,
            fg_color=self.bg,
            corner_radius=0
        )
        self.chat_area.grid(row=1, column=0, sticky="nsew", padx=18, pady=10)

        # Welcome message
        self.add_bot_message(
            "Hello! I'm assistGPT. How can I help you today?"
        )

        # Input section
        self.create_input_area()

    # ========================================================
    # CHAT MESSAGES
    # ========================================================
    def add_bot_message(self, text):
        row = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        row.pack(fill="x", pady=10, padx=8)                

        avatar = ctk.CTkLabel(
            row,
            text="✦",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#146fe8",
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        avatar.pack(side="left", anchor="n")

        bubble = ctk.CTkLabel(
            row,
            text=text,
            justify="left",
            anchor="w",
            wraplength=650,
            corner_radius=12,
            fg_color="#171f28",
            text_color="#e8edf1",
            padx=16,
            pady=12,
            font=ctk.CTkFont(size=14)
        )
        bubble.pack(side="left", padx=10)
        return bubble                   

    def add_user_message(self, text):
        row = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        row.pack(fill="x", pady=10, padx=8)

        bubble = ctk.CTkLabel(
            row,
            text=text,
            justify="left",
            anchor="e",
            wraplength=650,
            corner_radius=12,
            fg_color="#1677ed",
            text_color="white",
            padx=16,
            pady=12,
            font=ctk.CTkFont(size=14)
        )
        bubble.pack(side="right", padx=(10, 0))

        avatar = ctk.CTkLabel(
            row,
            text="●",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#26313c",
            text_color="#cbd5df",
            font=ctk.CTkFont(size=17)
        )
        avatar.pack(side="right", anchor="n")

    # ========================================================
    # INPUT BAR
    # ========================================================
    def create_input_area(self):
        container = ctk.CTkFrame(
            self.main,
            height=95,
            corner_radius=0,
            fg_color=self.bg
        )
        container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        container.grid_columnconfigure(0, weight=1)

        input_frame = ctk.CTkFrame(
            container,
            height=66,
            corner_radius=14,
            fg_color=self.input_bg,
            border_width=1,
            border_color="#6b727a"
        )
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="ask anything",
            height=58,
            border_width=0,
            fg_color="transparent",
            text_color=self.text,
            placeholder_text_color="#7e8994",
            font=ctk.CTkFont(size=14)
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(14, 5))
        self.entry.bind("<Return>", self.send_message)

        # Think
        ctk.CTkButton(
            input_frame,
            text="🧠 Think",
            width=90,
            height=45,
            fg_color="transparent",
            hover_color="#222b34",
            text_color="#f0f3f5",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.think_mode
        ).grid(row=0, column=1, padx=2)

        # Mic
        ctk.CTkButton(
            input_frame,
            text="🎙",
            width=45,
            height=45,
            fg_color="transparent",
            hover_color="#222b34",
            text_color="#24a5ff",
            font=ctk.CTkFont(size=19),
            command=self.microphone
        ).grid(row=0, column=2, padx=2)

        # Voice
        ctk.CTkButton(
            input_frame,
            text="〽",
            width=45,
            height=45,
            fg_color="transparent",
            hover_color="#222b34",
            text_color="#ff7200",
            font=ctk.CTkFont(size=22),
            command=self.voice_mode
        ).grid(row=0, column=3, padx=(2, 8))

    # ========================================================
    # ACTIONS
    # ========================================================
    def send_message(self, event=None):
        text = self.entry.get().strip()

        if not text:
            return

        self.add_user_message(text)
        self.entry.delete(0, "end")


        bubble = self.add_bot_message("Thinking...")
        bubble.is_thinking = True
        self.animate_thinking(bubble)
        threading.Thread(target=self.run_backend, args=(text, bubble), daemon=True).start()
        threading.Thread(target=self.run_backend, args=(text, bubble), daemon=True).start()
            
    def animate_thinking(self, bubble, step=0):
        if not bubble.is_thinking:
            return
        bubble.configure(text="Thinking" + "." * (step % 3 + 1))
        self.after(400, lambda: self.animate_thinking(bubble, step + 1))
    def run_backend(self, query, bubble):
           try:
               result = research(query)
               answer = result.summary
           except Exception as e:
               answer = f"Error: {e}"
           self.after(0, lambda:self.show_answer(bubble,answer))
    def show_answer(self, bubble, answer):
        bubble.is_thinking = False
        bubble.configure(text=answer)
    def new_chat(self):
        for widget in self.chat_area.winfo_children():
            widget.destroy()
        self.add_bot_message("New conversation started. How can I help you?")

    def select_chat(self, title):
        for widget in self.chat_area.winfo_children():
            widget.destroy()
        self.add_bot_message(f"You opened: {title}")

    def think_mode(self):
        messagebox.showinfo("Think", "Think mode is ready to be connected to your AI model.")

    def microphone(self):
        messagebox.showinfo("Microphone", "Microphone functionality will be connected later.")

    def voice_mode(self):
        messagebox.showinfo("Voice", "Voice mode will be connected later.")

    def show_settings(self):
        messagebox.showinfo("Settings", "Settings panel will be added here.")

    def show_menu(self):
        messagebox.showinfo("Menu", "More options will be added here.")


if __name__ == "__main__":
    app = AssistGPT()
    app.mainloop()
