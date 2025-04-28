import subprocess
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from colorama import init
from datetime import datetime
import sys
from GamesFinder import Steam, EpicGames
import random
import ping3
import socket
from statistics import stdev
import csv

# Initialize colorama
init(convert=True, autoreset=True)

class QoSManagerApp:
    def __init__(self, root):
        self.root = root
        self.program_path = os.getcwd()
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.game_dscp_values = {}
        # Configure the main window
        self.root.title("ApkalessShell QoS Manager")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.configure(bg="#1e1e1e")
        
        # Initialize status_var first to avoid reference errors
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Set default DSCP value
        self.default_dscp = tk.IntVar(value=46)
        
        # Set application icon
        try:
            icon_path = os.path.join(self.program_path, "icon.png")
            if os.path.exists(icon_path):
                self.icon = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(False, self.icon)
        except Exception as e:
            print(f"Error loading icon: {str(e)}")
        
        # Create a custom style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure the colors for the dark theme
        self.configure_styles()
        
        # Create the main frame for content
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status bar at the bottom - create this before any other UI elements that might use it
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#252525",
            fg="#00b4d8",
            font=("Consolas", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create header
        self.create_header()
        
        # Create the main content area with tabs
        self.create_tabs()
        
        # Center the window on the screen
        self.center_window()
        
        # Store DSCP values for each game
        self.load_dscp_settings()

    def configure_styles(self):
        """Configure the styles for ttk widgets"""
        # Define colors
        bg_color = "#1e1e1e"
        fg_color = "#ffffff"
        accent_color = "#00b4d8"
        accent_hover = "#0096c7"
        button_bg = "#252525"
        
        # Configure style for ttk.Button
        self.style.configure(
            "TButton",
            background=button_bg,
            foreground=fg_color,
            borderwidth=0,
            focusthickness=3,
            focuscolor=accent_color,
            padding=(10, 5),
            font=("Segoe UI", 10)
        )
        self.style.map(
            "TButton",
            background=[("active", accent_color)],
            foreground=[("active", "#ffffff")]
        )
        
        # Configure style for ttk.Label
        self.style.configure(
            "TLabel",
            background=bg_color,
            foreground=fg_color,
            font=("Segoe UI", 10)
        )
        
        # Configure style for ttk.Entry
        self.style.configure(
            "TEntry",
            fieldbackground="#252525",
            foreground=fg_color,
            borderwidth=1,
            padding=5
        )
        
        # Configure style for ttk.Frame
        self.style.configure(
            "TFrame",
            background=bg_color
        )
        
        # Configure style for ttk.Notebook
        self.style.configure(
            "TNotebook",
            background=bg_color,
            borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab",
            background=button_bg,
            foreground=fg_color,
            padding=(10, 5),
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", accent_color)],
            foreground=[("selected", "#ffffff")],
            expand=[("selected", [1, 1, 1, 0])]
        )
        
        # Configure style for ttk.Treeview
        self.style.configure(
            "Treeview",
            background="#252525",
            foreground=fg_color,
            rowheight=25,
            fieldbackground="#252525",
            borderwidth=0,
            font=("Segoe UI", 9)
        )
        self.style.map(
            "Treeview",
            background=[("selected", accent_color)],
            foreground=[("selected", "#ffffff")]
        )
        
        # Configure style for ttk.Scrollbar
        self.style.configure(
            "Vertical.TScrollbar",
            background=button_bg,
            arrowcolor=fg_color,
            borderwidth=0,
            troughcolor=bg_color
        )
        self.style.map(
            "Vertical.TScrollbar",
            background=[("active", accent_color)]
        )
        
        # Configure style for ttk.Progressbar
        self.style.configure(
            "TProgressbar",
            background=accent_color,
            troughcolor="#252525",
            borderwidth=0
        )
        
        # Add new styles for performance monitoring
        self.style.configure(
            "Accent.TButton",
            background="#00b4d8",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )
        
        self.style.configure(
            "Stop.TButton",
            background="#ff5252",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )
        
        self.style.map(
            "Accent.TButton",
            background=[("active", "#0096c7")],
            foreground=[("active", "#ffffff")]
        )
        
        self.style.map(
            "Stop.TButton",
            background=[("active", "#ff1744")],
            foreground=[("active", "#ffffff")]
        )

    def create_header(self):
        """Create the header section of the application"""
        header_frame = tk.Frame(self.main_frame, bg="#252525", height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Logo and title
        title_label = tk.Label(
            header_frame,
            text="ApkalessShell QoS Manager",
            font=("Segoe UI", 16, "bold"),
            bg="#252525",
            fg="#00b4d8"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # User info
        user_info = tk.Label(
            header_frame,
            text=f"Welcome, {os.getlogin()}",
            font=("Segoe UI", 10),
            bg="#252525",
            fg="#ffffff"
        )
        user_info.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Links
        links_frame = tk.Frame(header_frame, bg="#252525")
        links_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        github_link = tk.Label(
            links_frame,
            text="GitHub: github.com/apkaless",
            font=("Segoe UI", 8),
            bg="#252525",
            fg="#aaaaaa",
            cursor="hand2"
        )
        github_link.pack(side=tk.TOP)
        github_link.bind("<Button-1>", lambda e: self.open_url("https://github.com/apkaless"))
        
        instagram_link = tk.Label(
            links_frame,
            text="Instagram: Apkaless",
            font=("Segoe UI", 8),
            bg="#252525",
            fg="#aaaaaa",
            cursor="hand2"
        )
        instagram_link.pack(side=tk.TOP)
        instagram_link.bind("<Button-1>", lambda e: self.open_url("https://instagram.com/Apkaless"))

    def create_tabs(self):
        """Create the tabbed interface for the application"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Dashboard tab
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.create_dashboard()
        
        # Game List tab
        self.games_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.games_tab, text="Game List")
        self.create_game_list()
        
        # Add Game tab
        self.add_game_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_game_tab, text="Add Game")
        self.create_add_game()
        
        # Remove Game tab
        self.remove_game_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.remove_game_tab, text="Remove Game")
        self.create_remove_game()
        
        # DSCP Settings tab
        self.dscp_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dscp_tab, text="DSCP Settings")
        self.create_dscp_settings()
        
        # Performance tab (NEW)
        self.performance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.performance_tab, text="Performance")
        self.create_performance_tab()
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        self.create_settings()

    def create_dashboard(self):
        """Create the dashboard tab content"""
        # Main container with some padding
        container = ttk.Frame(self.dashboard_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = ttk.Frame(container)
        welcome_frame.pack(fill="x", pady=(0, 20))
        
        welcome_label = tk.Label(
            welcome_frame,
            text="QoS Game Manager Dashboard",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        welcome_label.pack(anchor="w")
        
        description = tk.Label(
            welcome_frame,
            text="Prioritize your gaming traffic and reduce latency with Windows QoS policies.",
            font=("Segoe UI", 10),
            bg="#1e1e1e",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        description.pack(anchor="w", pady=(5, 0))
        
        # Stats and quick actions
        stats_frame = tk.Frame(container, bg="#1e1e1e")
        stats_frame.pack(fill="both", expand=True)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        # Left side - Stats
        stats_left = tk.Frame(stats_frame, bg="#252525", padx=20, pady=20)
        stats_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        stats_title = tk.Label(
            stats_left,
            text="Statistics",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        stats_title.pack(anchor="w", pady=(0, 10))
        
        self.games_count_var = tk.StringVar(value="0")
        
        games_count_frame = tk.Frame(stats_left, bg="#252525")
        games_count_frame.pack(fill="x", pady=5)
        
        games_count_label = tk.Label(
            games_count_frame,
            text="Games in QoS:",
            font=("Segoe UI", 10),
            bg="#252525",
            fg="#aaaaaa"
        )
        games_count_label.pack(side=tk.LEFT)
        
        games_count_value = tk.Label(
            games_count_frame,
            textvariable=self.games_count_var,
            font=("Segoe UI", 10, "bold"),
            bg="#252525",
            fg="#00b4d8"
        )
        games_count_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Default DSCP display
        default_dscp_frame = tk.Frame(stats_left, bg="#252525")
        default_dscp_frame.pack(fill="x", pady=5)
        
        default_dscp_label = tk.Label(
            default_dscp_frame,
            text="Default DSCP Value:",
            font=("Segoe UI", 10),
            bg="#252525",
            fg="#aaaaaa"
        )
        default_dscp_label.pack(side=tk.LEFT)
        
        default_dscp_value = tk.Label(
            default_dscp_frame,
            textvariable=self.default_dscp,
            font=("Segoe UI", 10, "bold"),
            bg="#252525",
            fg="#00b4d8"
        )
        default_dscp_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Refresh button for stats
        refresh_stats_btn = ttk.Button(
            stats_left,
            text="Refresh Stats",
            command=self.refresh_stats
        )
        refresh_stats_btn.pack(anchor="w", pady=(10, 0))
        
        # Right side - Quick Actions
        actions_right = tk.Frame(stats_frame, bg="#252525", padx=20, pady=20)
        actions_right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        actions_title = tk.Label(
            actions_right,
            text="Quick Actions",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        actions_title.pack(anchor="w", pady=(0, 10))
        
        # Quick action buttons
        auto_detect_btn = ttk.Button(
            actions_right,
            text="Auto Detect and Add Games",
            command=self.auto_detect_games
        )
        auto_detect_btn.pack(fill="x", pady=5)
        
        view_games_btn = ttk.Button(
            actions_right,
            text="View All Games",
            command=lambda: self.notebook.select(self.games_tab)
        )
        view_games_btn.pack(fill="x", pady=5)
        
        add_game_btn = ttk.Button(
            actions_right,
            text="Add New Game",
            command=lambda: self.notebook.select(self.add_game_tab)
        )
        add_game_btn.pack(fill="x", pady=5)
        
        dscp_settings_btn = ttk.Button(
            actions_right,
            text="DSCP Settings",
            command=lambda: self.notebook.select(self.dscp_tab)
        )
        dscp_settings_btn.pack(fill="x", pady=5)
        
        remove_all_btn = ttk.Button(
            actions_right,
            text="Remove All Games",
            command=self.remove_all_games
        )
        remove_all_btn.pack(fill="x", pady=5)
        
        # Bottom section - Log
        log_frame = tk.Frame(container, bg="#1e1e1e", pady=20)
        log_frame.pack(fill="x")
        
        log_title = tk.Label(
            log_frame,
            text="Activity Log",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        log_title.pack(anchor="w", pady=(0, 10))
        
        log_container = tk.Frame(log_frame, bg="#252525", padx=2, pady=2)
        log_container.pack(fill="x")
        
        self.log_text = tk.Text(
            log_container,
            height=8,
            bg="#252525",
            fg="#aaaaaa",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        log_scrollbar = ttk.Scrollbar(
            log_container,
            orient="vertical",
            command=self.log_text.yview
        )
        log_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Add initial log entry
        self.add_log("Application started successfully.")
        
        # Initial refresh of stats - moved after log_text creation
        try:
            self.refresh_stats()
        except Exception as e:
            self.add_log(f"Error refreshing stats: {str(e)}", error=True)

    def create_game_list(self):
        """Create the game list tab content"""
        container = ttk.Frame(self.games_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Games in QoS Policy List",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            header_frame,
            text="Refresh List",
            command=self.refresh_game_list
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Create treeview for games list
        tree_frame = tk.Frame(container, bg="#252525", padx=2, pady=2)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("name", "path", "dscp")
        self.games_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Define headings
        self.games_tree.heading("name", text="Game Name")
        self.games_tree.heading("path", text="Path")
        self.games_tree.heading("dscp", text="DSCP Value")
        
        # Define columns properties
        self.games_tree.column("name", width=200, minwidth=150)
        self.games_tree.column("path", width=400, minwidth=200)
        self.games_tree.column("dscp", width=100, minwidth=80)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.games_tree.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.games_tree.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill="x")
        
        self.games_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.games_tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Add double-click binding for editing
        self.games_tree.bind("<Double-1>", self.edit_game_dscp)
        
        # Action buttons
        actions_frame = ttk.Frame(container)
        actions_frame.pack(fill="x", pady=(20, 0))
        
        remove_selected_btn = ttk.Button(
            actions_frame,
            text="Remove Selected Game",
            command=self.remove_selected_game
        )
        remove_selected_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        edit_dscp_btn = ttk.Button(
            actions_frame,
            text="Edit DSCP Value",
            command=lambda: self.edit_game_dscp(None)
        )
        edit_dscp_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_all_btn = ttk.Button(
            actions_frame,
            text="Remove All Games",
            command=self.remove_all_games
        )
        remove_all_btn.pack(side=tk.LEFT)
        
        # Initial population of the game list
        self.refresh_game_list()

    def create_add_game(self):
        """Create the add game tab content"""
        container = ttk.Frame(self.add_game_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        title_label = tk.Label(
            container,
            text="Add New Game to QoS Policy",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Form for adding a game
        form_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        form_frame.pack(fill="x")
        
        # Game name input
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ttk.Label(
            name_frame,
            text="Game Name:",
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        self.game_name_var = tk.StringVar()
        game_name_entry = ttk.Entry(
            name_frame,
            textvariable=self.game_name_var,
            width=50
        )
        game_name_entry.pack(fill="x")
        
        # Game path input
        path_frame = ttk.Frame(form_frame)
        path_frame.pack(fill="x", pady=(0, 15))
        
        path_label = ttk.Label(
            path_frame,
            text="Game Executable Path:",
        )
        path_label.pack(anchor="w", pady=(0, 5))
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x")
        
        self.game_path_var = tk.StringVar()
        game_path_entry = ttk.Entry(
            path_input_frame,
            textvariable=self.game_path_var,
            width=50
        )
        game_path_entry.pack(side=tk.LEFT, fill="x", expand=True)
        
        browse_btn = ttk.Button(
            path_input_frame,
            text="Browse...",
            command=self.browse_file
        )
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # DSCP Value input
        dscp_frame = ttk.Frame(form_frame)
        dscp_frame.pack(fill="x", pady=(0, 15))
        
        dscp_label = ttk.Label(
            dscp_frame,
            text="DSCP Value (0-63):",
        )
        dscp_label.pack(anchor="w", pady=(0, 5))
        
        self.game_dscp_var = tk.StringVar(value="46")
        dscp_entry = ttk.Entry(
            dscp_frame,
            textvariable=self.game_dscp_var,
            width=10
        )
        dscp_entry.pack(anchor="w")
        
        dscp_info = ttk.Label(
            dscp_frame,
            text="Common values: 46 (Expedited Forwarding), 32 (Class Selector 4), 24 (Class Selector 3)",
            foreground="#aaaaaa",
            font=("Segoe UI", 8)
        )
        dscp_info.pack(anchor="w", pady=(5, 0))
        
        # Add button
        add_btn = ttk.Button(
            form_frame,
            text="Add Game to QoS",
            command=self.add_game
        )
        add_btn.pack(anchor="w", pady=(10, 0))
        
        # Auto-detect section
        auto_frame = tk.Frame(container, bg="#252525", padx=20, pady=20, highlightbackground="#323232", highlightthickness=1)
        auto_frame.pack(fill="x", pady=(20, 0))
        
        auto_title = tk.Label(
            auto_frame,
            text="Auto-Detect Games",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        auto_title.pack(anchor="w", pady=(0, 10))
        
        auto_description = tk.Label(
            auto_frame,
            text="Automatically scan and add games from Steam and Epic Games libraries.",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        auto_description.pack(anchor="w", pady=(0, 10))
        
        auto_detect_btn = ttk.Button(
            auto_frame,
            text="Auto-Detect and Add Games",
            command=self.auto_detect_games
        )
        auto_detect_btn.pack(anchor="w")

    def create_remove_game(self):
        """Create the remove game tab content"""
        container = ttk.Frame(self.remove_game_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        title_label = tk.Label(
            container,
            text="Remove Game from QoS Policy",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Form for removing a game
        form_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        form_frame.pack(fill="x")
        
        # Game selection
        select_frame = ttk.Frame(form_frame)
        select_frame.pack(fill="x", pady=(0, 15))
        
        select_label = ttk.Label(
            select_frame,
            text="Select Game:",
        )
        select_label.pack(anchor="w", pady=(0, 5))
        
        self.remove_game_var = tk.StringVar()
        self.remove_game_combo = ttk.Combobox(
            select_frame,
            textvariable=self.remove_game_var,
            state="readonly",
            width=50
        )
        self.remove_game_combo.pack(fill="x")
        
        # Game details display
        self.game_details_frame = tk.Frame(form_frame, bg="#252525")
        self.game_details_frame.pack(fill="x", pady=(10, 15))
        
        # Path display
        path_label = tk.Label(
            self.game_details_frame,
            text="Path:",
            bg="#252525",
            fg="#aaaaaa",
            anchor="w"
        )
        path_label.pack(anchor="w")
        
        self.selected_game_path = tk.StringVar()
        path_value = tk.Label(
            self.game_details_frame,
            textvariable=self.selected_game_path,
            bg="#252525",
            fg="#ffffff",
            anchor="w",
            wraplength=500
        )
        path_value.pack(anchor="w", padx=(20, 0), pady=(0, 5))
        
        # DSCP display
        dscp_label = tk.Label(
            self.game_details_frame,
            text="DSCP Value:",
            bg="#252525",
            fg="#aaaaaa",
            anchor="w"
        )
        dscp_label.pack(anchor="w")
        
        self.selected_game_dscp = tk.StringVar()
        dscp_value = tk.Label(
            self.game_details_frame,
            textvariable=self.selected_game_dscp,
            bg="#252525",
            fg="#ffffff",
            anchor="w"
        )
        dscp_value.pack(anchor="w", padx=(20, 0))
        
        # Add combobox selection event
        self.remove_game_combo.bind("<<ComboboxSelected>>", self.update_game_details)
        
        # Remove button
        remove_btn = ttk.Button(
            form_frame,
            text="Remove Game from QoS",
            command=self.remove_selected_from_combo
        )
        remove_btn.pack(side=tk.LEFT, padx=(0, 10), pady=(10, 0))
        
        # Refresh combobox
        refresh_btn = ttk.Button(
            form_frame,
            text="Refresh Game List",
            command=self.refresh_remove_combo
        )
        refresh_btn.pack(side=tk.LEFT, pady=(10, 0))
        
        # Remove all section
        remove_all_frame = tk.Frame(container, bg="#252525", padx=20, pady=20, highlightbackground="#323232", highlightthickness=1)
        remove_all_frame.pack(fill="x", pady=(20, 0))
        
        remove_all_title = tk.Label(
            remove_all_frame,
            text="Remove All Games",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        remove_all_title.pack(anchor="w", pady=(0, 10))
        
        remove_all_description = tk.Label(
            remove_all_frame,
            text="Remove all games from the QoS policy list at once.",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        remove_all_description.pack(anchor="w", pady=(0, 10))
        
        remove_all_btn = ttk.Button(
            remove_all_frame,
            text="Remove All Games",
            command=self.remove_all_games
        )
        remove_all_btn.pack(anchor="w")
        
        # Initial population of the combobox
        self.refresh_remove_combo()
        
    def create_dscp_settings(self):
        """Create the DSCP settings tab content"""
        container = ttk.Frame(self.dscp_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        title_label = tk.Label(
            container,
            text="DSCP Settings",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Default DSCP setting
        default_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        default_frame.pack(fill="x", pady=(0, 20))
        
        default_title = tk.Label(
            default_frame,
            text="Default DSCP Value",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        default_title.pack(anchor="w", pady=(0, 10))
        
        default_desc = tk.Label(
            default_frame,
            text="This value will be used for new games added to QoS unless specified otherwise.",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        default_desc.pack(anchor="w", pady=(0, 10))
        
        dscp_input_frame = ttk.Frame(default_frame)
        dscp_input_frame.pack(fill="x", pady=(0, 10))
        
        dscp_input_label = ttk.Label(
            dscp_input_frame,
            text="Default DSCP Value (0-63):"
        )
        dscp_input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        dscp_entry = ttk.Entry(
            dscp_input_frame,
            textvariable=self.default_dscp,
            width=8
        )
        dscp_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        save_default_btn = ttk.Button(
            dscp_input_frame,
            text="Save Default",
            command=self.save_default_dscp
        )
        save_default_btn.pack(side=tk.LEFT)
        
        # DSCP Value information
        info_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        info_frame.pack(fill="x")
        
        info_title = tk.Label(
            info_frame,
            text="DSCP Value Information",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        info_title.pack(anchor="w", pady=(0, 10))
        
        # Create info table
        info_table_frame = tk.Frame(info_frame, bg="#252525")
        info_table_frame.pack(fill="x", pady=(0, 10))
        
        # Headers
        headers = ["DSCP Value", "Name", "Description", "Typical Use"]
        for col, header in enumerate(headers):
            header_label = tk.Label(
                info_table_frame,
                text=header,
                font=("Segoe UI", 9, "bold"),
                bg="#252525",
                fg="#00b4d8",
                padx=5,
                pady=2
            )
            header_label.grid(row=0, column=col, sticky="w", padx=(5, 10))
        
        # DSCP values information
        dscp_info = [
            {"value": "46", "name": "Expedited Forwarding (EF)", "desc": "Low loss, low latency traffic", "use": "VoIP, gaming, video calls"},
            {"value": "40", "name": "Class Selector 5 (CS5)", "desc": "Critical applications", "use": "Video streaming, interactive gaming"},
            {"value": "32", "name": "Class Selector 4 (CS4)", "desc": "Flash override", "use": "Real-time interactive applications"},
            {"value": "24", "name": "Class Selector 3 (CS3)", "desc": "Flash traffic", "use": "Call signaling"},
            {"value": "16", "name": "Class Selector 2 (CS2)", "desc": "Immediate traffic", "use": "Network management"},
            {"value": "8", "name": "Class Selector 1 (CS1)", "desc": "Priority traffic", "use": "Bulk data transfer"},
            {"value": "0", "name": "Default", "desc": "Best effort delivery", "use": "Standard internet traffic"}
        ]
        
        for row, info in enumerate(dscp_info, 1):
            bg_color = "#303030" if row % 2 == 0 else "#252525"
            
            for col, key in enumerate(["value", "name", "desc", "use"]):
                cell_label = tk.Label(
                    info_table_frame,
                    text=info[key],
                    font=("Segoe UI", 9),
                    bg=bg_color,
                    fg="#ffffff" if col == 0 else "#aaaaaa",
                    padx=5,
                    pady=2,
                    anchor="w"
                )
                cell_label.grid(row=row, column=col, sticky="w", padx=(5, 10))
        
        # Bulk update section
        bulk_frame = tk.Frame(container, bg="#252525", padx=20, pady=20, highlightbackground="#323232", highlightthickness=1)
        bulk_frame.pack(fill="x", pady=(20, 0))
        
        bulk_title = tk.Label(
            bulk_frame,
            text="Bulk Update DSCP Values",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        bulk_title.pack(anchor="w", pady=(0, 10))
        
        bulk_desc = tk.Label(
            bulk_frame,
            text="Update DSCP values for all existing games at once.",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        bulk_desc.pack(anchor="w", pady=(0, 10))
        
        bulk_input_frame = ttk.Frame(bulk_frame)
        bulk_input_frame.pack(fill="x", pady=(0, 10))
        
        self.bulk_dscp_var = tk.StringVar(value="46")
        
        bulk_input_label = ttk.Label(
            bulk_input_frame,
            text="New DSCP Value for All Games (0-63):"
        )
        bulk_input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        bulk_entry = ttk.Entry(
            bulk_input_frame,
            textvariable=self.bulk_dscp_var,
            width=8
        )
        bulk_entry.pack(side=tk.LEFT, padx=(0, 10))
        
    def create_performance_tab(self):
        """Create the performance monitoring tab"""
        container = ttk.Frame(self.performance_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        title_label = tk.Label(
            container,
            text="Performance Optimization",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Create notebook for different views
        self.performance_notebook = ttk.Notebook(container)
        self.performance_notebook.pack(fill="both", expand=True)
        
        # Current Performance tab
        current_frame = ttk.Frame(self.performance_notebook)
        self.performance_notebook.add(current_frame, text="Current Performance")
        self._create_current_performance_frame(current_frame)
        
        # Historical Data tab
        historical_frame = ttk.Frame(self.performance_notebook)
        self.performance_notebook.add(historical_frame, text="Historical Data")
        self._create_historical_performance_frame(historical_frame)
        
        # Advanced Diagnostics tab
        diagnostics_frame = ttk.Frame(self.performance_notebook)
        self.performance_notebook.add(diagnostics_frame, text="Advanced Diagnostics")
        self._create_diagnostics_frame(diagnostics_frame)
        
        # Performance Optimization tab
        optimization_frame = ttk.Frame(self.performance_notebook)
        self.performance_notebook.add(optimization_frame, text="Optimization")
        self._create_optimization_frame(optimization_frame)
        
        # Initialize monitoring variables
        self.monitoring_active = False
        self.monitoring_thread = None
        self.performance_history = []
        self.max_history_points = 100  # Store last 100 measurements
        self.optimization_active = False
        self.optimization_thread = None

    def _create_current_performance_frame(self, parent):
        """Create the current performance monitoring frame"""
        # Performance metrics frame
        metrics_frame = tk.Frame(parent, bg="#252525", padx=20, pady=20)
        metrics_frame.pack(fill="x", pady=(0, 20))
        
        metrics_title = tk.Label(
            metrics_frame,
            text="Current Network Performance",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        metrics_title.pack(anchor="w", pady=(0, 10))
        
        # Create metrics grid
        metrics_grid = tk.Frame(metrics_frame, bg="#252525")
        metrics_grid.pack(fill="x")
        
        # Latency
        latency_frame = tk.Frame(metrics_grid, bg="#252525")
        latency_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        latency_label = tk.Label(
            latency_frame,
            text="Latency:",
            bg="#252525",
            fg="#aaaaaa"
        )
        latency_label.pack(anchor="w")
        
        self.latency_var = tk.StringVar(value="-- ms")
        latency_value = tk.Label(
            latency_frame,
            textvariable=self.latency_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10, "bold")
        )
        latency_value.pack(anchor="w")
        
        # Add tooltip for latency
        self._create_tooltip(latency_frame, "Network latency (ping time) in milliseconds. Lower is better.")
        
        # Packet Loss
        loss_frame = tk.Frame(metrics_grid, bg="#252525")
        loss_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        loss_label = tk.Label(
            loss_frame,
            text="Packet Loss:",
            bg="#252525",
            fg="#aaaaaa"
        )
        loss_label.pack(anchor="w")
        
        self.loss_var = tk.StringVar(value="-- %")
        loss_value = tk.Label(
            loss_frame,
            textvariable=self.loss_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10, "bold")
        )
        loss_value.pack(anchor="w")
        
        # Add tooltip for packet loss
        self._create_tooltip(loss_frame, "Percentage of packets lost during transmission. Should be close to 0%.")
        
        # Jitter
        jitter_frame = tk.Frame(metrics_grid, bg="#252525")
        jitter_frame.pack(side=tk.LEFT)
        
        jitter_label = tk.Label(
            jitter_frame,
            text="Jitter:",
            bg="#252525",
            fg="#aaaaaa"
        )
        jitter_label.pack(anchor="w")
        
        self.jitter_var = tk.StringVar(value="-- ms")
        jitter_value = tk.Label(
            jitter_frame,
            textvariable=self.jitter_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10, "bold")
        )
        jitter_value.pack(anchor="w")
        
        # Add tooltip for jitter
        self._create_tooltip(jitter_frame, "Variation in latency. Lower values mean more stable connection.")
        
        # Performance impact indicator with color coding
        impact_frame = tk.Frame(parent, bg="#252525", padx=20, pady=20)
        impact_frame.pack(fill="x", pady=(0, 20))
        
        impact_title = tk.Label(
            impact_frame,
            text="QoS Impact",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        impact_title.pack(anchor="w", pady=(0, 10))
        
        self.impact_var = tk.StringVar(value="No impact data available")
        self.impact_label = tk.Label(
            impact_frame,
            textvariable=self.impact_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10)
        )
        self.impact_label.pack(anchor="w")
        
        # Add tooltip for impact
        self._create_tooltip(impact_frame, "Current impact of network conditions on gaming performance.")
        
        # DSCP Recommendations with visual feedback
        recommendations_frame = tk.Frame(parent, bg="#252525", padx=20, pady=20)
        recommendations_frame.pack(fill="x")
        
        recommendations_title = tk.Label(
            recommendations_frame,
            text="DSCP Recommendations",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        recommendations_title.pack(anchor="w", pady=(0, 10))
        
        self.recommendations_var = tk.StringVar(value="No recommendations available")
        recommendations_value = tk.Label(
            recommendations_frame,
            textvariable=self.recommendations_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10),
            wraplength=600,
            justify=tk.LEFT
        )
        recommendations_value.pack(anchor="w")
        
        # Start monitoring button
        monitor_btn = ttk.Button(
            parent,
            text="Start Performance Monitoring",
            command=self.start_performance_monitoring
        )
        monitor_btn.pack(pady=(20, 0))

    def _create_historical_performance_frame(self, parent):
        """Create the historical performance data frame"""
        # Create canvas and scrollbar for the graph
        canvas_frame = tk.Frame(parent, bg="#1e1e1e")
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.history_canvas = tk.Canvas(
            canvas_frame,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.history_canvas.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.history_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.history_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame inside canvas for the graph
        self.graph_frame = tk.Frame(
            self.history_canvas,
            bg="#1e1e1e"
        )
        self.history_canvas.create_window(
            (0, 0),
            window=self.graph_frame,
            anchor="nw"
        )
        
        # Bind canvas to frame size
        self.graph_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(
                scrollregion=self.history_canvas.bbox("all")
            )
        )
        
        # Add export button
        export_btn = ttk.Button(
            parent,
            text="Export Performance Data",
            command=self.export_performance_data
        )
        export_btn.pack(pady=(0, 20))

    def _update_performance_history(self, latency, loss, jitter):
        """Update the performance history and redraw the graph"""
        try:
            # Add new data point
            timestamp = datetime.now()
            self.performance_history.append({
                'timestamp': timestamp,
                'latency': latency,
                'loss': loss,
                'jitter': jitter
            })
            
            # Keep only the last max_history_points
            if len(self.performance_history) > self.max_history_points:
                self.performance_history = self.performance_history[-self.max_history_points:]
            
            # Redraw the graph
            self._draw_performance_graph()
            
        except Exception as e:
            self.add_log(f"Error updating performance history: {str(e)}", error=True)

    def _draw_performance_graph(self):
        """Draw the performance history graph"""
        try:
            # Clear previous graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if not self.performance_history:
                return
            
            # Calculate graph dimensions
            width = 800
            height = 400
            padding = 50
            
            # Create graph canvas
            graph_canvas = tk.Canvas(
                self.graph_frame,
                width=width,
                height=height,
                bg="#1e1e1e",
                highlightthickness=0
            )
            graph_canvas.pack(pady=20)
            
            # Draw axes
            graph_canvas.create_line(padding, height - padding, width - padding, height - padding, fill="#ffffff")  # X-axis
            graph_canvas.create_line(padding, padding, padding, height - padding, fill="#ffffff")  # Y-axis
            
            # Find min and max latency values for scaling
            latencies = [data['latency'] for data in self.performance_history]
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            # Ensure we have a valid range for scaling
            if min_latency == max_latency:
                # If all values are the same, create a small range around the value
                min_latency = max(0, min_latency - 10)
                max_latency = min_latency + 20
            
            # Draw grid lines and labels
            for i in range(0, 101, 20):
                y = height - padding - (i * (height - 2 * padding) / 100)
                graph_canvas.create_line(padding, y, width - padding, y, fill="#333333", dash=(2, 2))
                # Calculate actual latency value for the label
                latency_value = min_latency + (i / 100) * (max_latency - min_latency)
                graph_canvas.create_text(padding - 10, y, text=f"{latency_value:.1f}ms", fill="#ffffff", anchor="e")
            
            # Plot data points
            x_step = (width - 2 * padding) / max(1, len(self.performance_history) - 1)
            points = []
            
            for i, data in enumerate(self.performance_history):
                x = padding + (i * x_step)
                # Scale the latency value to fit the graph
                scaled_latency = ((data['latency'] - min_latency) / (max_latency - min_latency)) * (height - 2 * padding)
                y = height - padding - scaled_latency
                points.append((x, y))
                
                # Draw timestamp labels (every 10th point or at least 2 points)
                if i % max(1, len(self.performance_history) // 10) == 0:
                    time_str = data['timestamp'].strftime("%H:%M:%S")
                    graph_canvas.create_text(x, height - padding + 20, text=time_str, fill="#ffffff", angle=45)
            
            # Draw lines between points
            if len(points) > 1:
                graph_canvas.create_line(points, fill="#00b4d8", width=2)
            
            # Add legend
            legend_frame = tk.Frame(self.graph_frame, bg="#1e1e1e")
            legend_frame.pack(pady=(0, 20))
            
            legend_label = tk.Label(
                legend_frame,
                text="Latency (ms) over time",
                font=("Segoe UI", 10),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            legend_label.pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            self.add_log(f"Error drawing performance graph: {str(e)}", error=True)

    def export_performance_data(self):
        """Export performance data to CSV file"""
        try:
            if not self.performance_history:
                messagebox.showinfo("No Data", "No performance data available to export.")
                return
            
            # Get save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Performance Data"
            )
            
            if not file_path:
                return
            
            # Write data to CSV
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Latency (ms)', 'Packet Loss (%)', 'Jitter (ms)'])
                for data in self.performance_history:
                    writer.writerow([
                        data['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                        data['latency'],
                        data['loss'],
                        data['jitter']
                    ])
            
            self.add_log(f"Performance data exported to {file_path}")
            messagebox.showinfo("Success", "Performance data exported successfully.")
            
        except Exception as e:
            self.add_log(f"Error exporting performance data: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to export performance data: {str(e)}")

    def _monitor_performance(self):
        """Monitor network performance and update UI"""
        import ping3
        import socket
        import time
        from statistics import stdev
        
        # Common game servers to test against
        TEST_SERVERS = [
            "google.com",  # For general latency
            "8.8.8.8",    # Google DNS
            "1.1.1.1",    # Cloudflare DNS
            "valve.net",  # Steam servers
            "epicgames.com"  # Epic Games servers
        ]
        
        while self.monitoring_active:
            try:
                # Test latency and packet loss
                latencies = []
                lost_packets = 0
                total_packets = len(TEST_SERVERS)
                
                for server in TEST_SERVERS:
                    try:
                        # Set timeout to 2 seconds
                        latency = ping3.ping(server, timeout=2)
                        if latency is not None:
                            latencies.append(latency * 1000)  # Convert to milliseconds
                        else:
                            lost_packets += 1
                    except Exception:
                        lost_packets += 1
                
                # Calculate metrics
                if latencies:
                    avg_latency = sum(latencies) / len(latencies)
                    packet_loss = (lost_packets / total_packets) * 100
                    
                    # Calculate jitter (standard deviation of latency)
                    if len(latencies) > 1:
                        jitter = stdev(latencies)
                    else:
                        jitter = 0
                    
                    # Update UI with real values
                    self.root.after(0, lambda: self.latency_var.set(f"{avg_latency:.1f} ms"))
                    self.root.after(0, lambda: self.loss_var.set(f"{packet_loss:.1f} %"))
                    self.root.after(0, lambda: self.jitter_var.set(f"{jitter:.1f} ms"))
                    
                    # Update impact and recommendations
                    self._update_performance_impact(avg_latency, packet_loss, jitter)
                    
                    # Update performance history
                    self._update_performance_history(avg_latency, packet_loss, jitter)
                else:
                    # If all packets were lost
                    self.root.after(0, lambda: self.latency_var.set("-- ms"))
                    self.root.after(0, lambda: self.loss_var.set("100 %"))
                    self.root.after(0, lambda: self.jitter_var.set("-- ms"))
                    self.root.after(0, lambda: self.impact_var.set("Network connection failed"))
                    self.root.after(0, lambda: self.recommendations_var.set(
                        "Check your internet connection\nTry using a wired connection if possible"
                    ))
                
                # Sleep for 3 seconds before next update
                time.sleep(3)
                
            except Exception as e:
                self.add_log(f"Error in performance monitoring: {str(e)}", error=True)
                time.sleep(3)

    def start_performance_monitoring(self):
        """Start or stop performance monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitor_performance)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            self.add_log("Started performance monitoring")
        else:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=1)
            self.add_log("Stopped performance monitoring")

    def _update_performance_impact(self, latency, loss, jitter):
        """Update performance impact and recommendations based on metrics"""
        try:
            # Determine impact level
            if latency > 100 or loss > 1 or jitter > 15:
                impact = "High impact - Network conditions may affect gaming performance"
            elif latency > 50 or loss > 0.5 or jitter > 10:
                impact = "Moderate impact - Some performance degradation possible"
            else:
                impact = "Low impact - Good network conditions for gaming"
            
            # Generate recommendations
            recommendations = []
            
            if latency > 100:
                recommendations.append("Consider using a lower DSCP value (e.g., 46) to prioritize gaming traffic")
            if loss > 1:
                recommendations.append("Check your network connection and consider using a wired connection")
            if jitter > 15:
                recommendations.append("Try using a DSCP value of 32 to reduce jitter")
            
            if not recommendations:
                recommendations.append("Current DSCP settings are optimal for your network conditions")
            
            # Update UI
            self.root.after(0, lambda: self.impact_var.set(impact))
            self.root.after(0, lambda: self.recommendations_var.set("\n".join(recommendations)))
            
        except Exception as e:
            self.add_log(f"Error updating performance impact: {str(e)}", error=True)

    def create_settings(self):
        """Create the settings tab content"""
        container = ttk.Frame(self.settings_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        title_label = tk.Label(
            container,
            text="Settings",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Settings sections
        about_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        about_frame.pack(fill="x", pady=(0, 20))
        
        about_title = tk.Label(
            about_frame,
            text="About",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        about_title.pack(anchor="w", pady=(0, 10))
        
        about_text = tk.Label(
            about_frame,
            text="ApkalessShell QoS Manager helps you prioritize gaming traffic by setting up Windows QoS policies. This reduces latency and improves your gaming experience.",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT,
            wraplength=600
        )
        about_text.pack(anchor="w")
        
        version_text = tk.Label(
            about_frame,
            text="Version: 2.1.0",
            bg="#252525",
            fg="#aaaaaa",
            justify=tk.LEFT
        )
        version_text.pack(anchor="w", pady=(10, 0))
        
        # Advanced settings
        advanced_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
        advanced_frame.pack(fill="x")
        
        advanced_title = tk.Label(
            advanced_frame,
            text="Advanced",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        advanced_title.pack(anchor="w", pady=(0, 10))
        
        # View logs button
        view_logs_btn = ttk.Button(
            advanced_frame,
            text="View Error Logs",
            command=self.view_error_logs
        )
        view_logs_btn.pack(anchor="w", pady=(0, 10))
        
        # Clear logs button
        clear_logs_btn = ttk.Button(
            advanced_frame,
            text="Clear Error Logs",
            command=self.clear_error_logs
        )
        clear_logs_btn.pack(anchor="w")
        
    def open_url(self, url):
        """Open a URL in the default browser"""
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            self.add_log(f"Error opening URL: {str(e)}", error=True)

    def add_log(self, message, error=False):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "ERROR" if error else "INFO"
        color = "#ff5252" if error else "#00b4d8"
        
        # Check if log_text exists before trying to use it
        if not hasattr(self, 'log_text'):
            print(f"[{timestamp}] {prefix}: {message}")  # Fallback to console
            return
        
        self.log_text.config(state=tk.NORMAL)
        
        # Apply tag for the timestamp
        self.log_text.tag_configure("timestamp", foreground="#aaaaaa")
        self.log_text.tag_configure("prefix", foreground=color)
        self.log_text.tag_configure("message", foreground="#ffffff")
        
        # Insert the log entry
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{prefix}: ", "prefix")
        self.log_text.insert(tk.END, f"{message}\n", "message")
        
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Update status bar
        if hasattr(self, 'status_var'):
            self.status_var.set(message)
        
        # If error, also write to error log
        if error:
            with open("Errors.txt", "a") as errors:
                errors.write(f"[{timestamp}] {message}\n")

    def refresh_stats(self):
        """Refresh the statistics on the dashboard"""
        try:
            policies = self.get_qos_policy_details()
            count = len(policies)
            self.games_count_var.set(str(count))
            # Only log if log_text exists
            if hasattr(self, 'log_text'):
                self.add_log(f"Statistics refreshed. Found {count} games in QoS list.")
        except Exception as e:
            # Only log if log_text exists
            if hasattr(self, 'log_text'):
                self.add_log(f"Error refreshing stats: {str(e)}", error=True)
            else:
                print(f"Error refreshing stats: {str(e)}")  # Fallback to console
    def _auto_detect_games_thread(self):
        """Thread function to auto-detect and add games"""
        try:
            self.status_var.set("Detecting games...")
            self.add_log("Starting auto-detection of games...")
            
            # Progress dialog
            self.root.after(0, self._show_progress_dialog, "Auto-detecting games", "Scanning for Steam and Epic Games...", 0)
            
            # Find Epic Games
            self.root.after(0, lambda: self._update_progress("Scanning for Epic Games...", 10))
            epic = EpicGames()
            epic_found = epic.find_epic()
            
            added_count = 0
            dscp_value = int(self.default_dscp.get())
            
            if epic_found:
                self.root.after(0, lambda: self._update_progress("Processing Epic Games...", 30))
                epic_games = epic.get_epic_games()
                self.add_log(f"Found {len(epic_games)} Epic games.")
                
                for i, (game, path) in enumerate(epic_games):
                    progress = 30 + (i / len(epic_games) * 30)
                    self.root.after(0, lambda p=progress, g=game: self._update_progress(f"Adding Epic game: {g}", int(p)))
                    
                    game_name = game.strip('.exe')
                    if os.path.exists(path):
                        result = self.set_new_qos_policy_with_dscp(game_name, path, dscp_value, silent=True)
                        if result:
                            # Store DSCP value
                            self.game_dscp_values[game_name] = dscp_value
                            added_count += 1
                            self.add_log(f"Added Epic game: {game_name}")
            else:
                self.add_log("No Epic Games installation found.", error=False)
            
            # Find Steam Games
            self.root.after(0, lambda: self._update_progress("Scanning for Steam Games...", 60))
            steam_instance = Steam()
            steam_path = steam_instance.find_steam()
            
            if steam_path:
                self.root.after(0, lambda: self._update_progress("Processing Steam Games...", 70))
                steam_games = steam_instance.get_steam_games(steam_path)
                self.add_log(f"Found {len(steam_games)} Steam games.")
                
                for i, (game, path) in enumerate(steam_games):
                    progress = 70 + (i / len(steam_games) * 20)
                    self.root.after(0, lambda p=progress, g=game: self._update_progress(f"Adding Steam game: {g}", int(p)))
                    
                    game_name = game.strip('.exe')
                    if os.path.exists(path):
                        result = self.set_new_qos_policy_with_dscp(game_name, path, dscp_value, silent=True)
                        if result:
                            # Store DSCP value
                            self.game_dscp_values[game_name] = dscp_value
                            added_count += 1
                            self.add_log(f"Added Steam game: {game_name}")
            else:
                self.add_log("No Steam installation found.", error=False)
            
            # Save DSCP settings
            if added_count > 0:
                self.save_dscp_settings()
                
            # Close progress dialog
            self.root.after(0, self._close_progress_dialog)
            
            # Refresh the stats and game list
            self.root.after(0, self.refresh_stats)
            self.root.after(0, self.refresh_game_list)
            self.root.after(0, self.refresh_remove_combo)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("Auto-Detection Complete", 
                                            f"Auto-detection complete.\nAdded {added_count} games to QoS."))
            
            self.add_log(f"Auto-detection complete. Added {added_count} games to QoS.")
        except Exception as e:
            self.add_log(f"Error in auto-detection: {str(e)}", error=True)
            self.root.after(0, self._close_progress_dialog)
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error in auto-detection: {str(e)}"))
        
        self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def _show_progress_dialog(self, title, message, initial_value=0):
        """Show a progress dialog"""
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title(title)
        self.progress_window.geometry("400x150")
        self.progress_window.resizable(False, False)
        self.progress_window.configure(bg="#1e1e1e")
        self.progress_window.transient(self.root)
        self.progress_window.grab_set()
        
        # Center the progress window
        self.progress_window.update_idletasks()
        width = self.progress_window.winfo_width()
        height = self.progress_window.winfo_height()
        x = (self.root.winfo_x() + (self.root.winfo_width() // 2)) - (width // 2)
        y = (self.root.winfo_y() + (self.root.winfo_height() // 2)) - (height // 2)
        self.progress_window.geometry(f"+{x}+{y}")
        
        # Progress message
        self.progress_message = tk.StringVar(value=message)
        message_label = tk.Label(
            self.progress_window,
            textvariable=self.progress_message,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Segoe UI", 10)
        )
        message_label.pack(pady=(20, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_window,
            orient="horizontal",
            length=350,
            mode="determinate",
            value=initial_value
        )
        self.progress_bar.pack(pady=10)
        
        # Prevent closing the window
        self.progress_window.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def _update_progress(self, message, value):
        """Update the progress dialog"""
        if hasattr(self, 'progress_message'):
            self.progress_message.set(message)
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = value
    
    def _close_progress_dialog(self):
        """Close the progress dialog"""
        if hasattr(self, 'progress_window') and self.progress_window:
            self.progress_window.grab_release()
            self.progress_window.destroy()
            delattr(self, 'progress_window')
    
    def view_error_logs(self):
        """View the error logs"""
        try:
            if os.path.exists("Errors.txt"):
                # Create a new window to show logs
                log_window = tk.Toplevel(self.root)
                log_window.title("Error Logs")
                log_window.geometry("600x400")
                log_window.configure(bg="#1e1e1e")
                log_window.transient(self.root)
                
                # Text widget to display logs
                log_frame = tk.Frame(log_window, bg="#252525", padx=2, pady=2)
                log_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                log_text = tk.Text(
                    log_frame,
                    bg="#252525",
                    fg="#ff5252",
                    font=("Consolas", 9),
                    wrap=tk.WORD
                )
                log_text.pack(side=tk.LEFT, fill="both", expand=True)
                
                log_scrollbar = ttk.Scrollbar(
                    log_frame,
                    orient="vertical",
                    command=log_text.yview
                )
                log_scrollbar.pack(side=tk.RIGHT, fill="y")
                log_text.config(yscrollcommand=log_scrollbar.set)
                
                # Read and display logs
                with open("Errors.txt", "r") as f:
                    log_content = f.read()
                    log_text.insert(tk.END, log_content if log_content else "No errors found.")
                    log_text.config(state=tk.DISABLED)
                
                # Close button
                close_btn = ttk.Button(
                    log_window,
                    text="Close",
                    command=log_window.destroy
                )
                close_btn.pack(pady=10)
                
                # Center the window
                log_window.update_idletasks()
                width = log_window.winfo_width()
                height = log_window.winfo_height()
                x = (self.root.winfo_x() + (self.root.winfo_width() // 2)) - (width // 2)
                y = (self.root.winfo_y() + (self.root.winfo_height() // 2)) - (height // 2)
                log_window.geometry(f"+{x}+{y}")
            else:
                messagebox.showinfo("No Logs", "No error logs found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error viewing logs: {str(e)}")
    
    def clear_error_logs(self):
        """Clear the error logs"""
        try:
            if os.path.exists("Errors.txt"):
                if messagebox.askyesno("Confirm", "Are you sure you want to clear all error logs?"):
                    open("Errors.txt", "w").close()
                    self.add_log("Error logs cleared.")
                    messagebox.showinfo("Success", "Error logs have been cleared.")
            else:
                messagebox.showinfo("No Logs", "No error logs found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing logs: {str(e)}")
            self.add_log(f"Error clearing logs: {str(e)}", error=True)
    
    def get_powershell_path(self):
        """Get the path to PowerShell executable"""
        try:
            syspath = "c:/Windows/System32/WindowsPowerShell"
            current_dir = os.getcwd()
            os.chdir(syspath)
            dirs = os.listdir()
            for dir in dirs:
                sub_dirs = os.listdir(dir)
                if "powershell.exe" in sub_dirs:
                    os.chdir(current_dir)
                    return syspath + "/" + dir + "/powershell.exe"
            
            os.chdir(current_dir)
            return None
        except Exception as e:
            self.add_log(f"Error getting PowerShell path: {str(e)}", error=True)
            return None
    
    def path_validator(self, path):
        """Validate if the path is an executable file"""
        try:
            file_name = os.path.basename(path)
            return file_name.lower().endswith('.exe')
        except Exception as e:
            self.add_log(f"Error validating path: {str(e)}", error=True)
            return False
    
    def set_new_qos_policy(self, name, app_path, silent=False):
        """Set a new QoS policy for a game (using default DSCP value)"""
        dscp_value = int(self.default_dscp.get())
        return self.set_new_qos_policy_with_dscp(name, app_path, dscp_value, silent)
    
    def set_new_qos_policy_with_dscp(self, name, app_path, dscp_value, silent=False):
        """Set a new QoS policy for a game with a specific DSCP value"""
        try:
            # Format the path correctly for PowerShell
            new_app_path = app_path.replace('/', '\\')
            
            # Create the PowerShell command with DSCP value
            command = f'Remove-NetQosPolicy -Name "{name}" -Confirm:$false -ErrorAction SilentlyContinue; New-NetQosPolicy -Name "{name}" -AppPathNameMatchCondition "{new_app_path}" -IPProtocol Both -DSCPAction {dscp_value}'
            
            # Execute the command directly using PowerShell.exe
            process = subprocess.run(
                ["powershell.exe", "-Command", command],
                capture_output=True,
                text=True
            )
            
            if not silent:
                self.add_log(f"PowerShell output: {process.stdout}")
                if process.stderr:
                    self.add_log(f"PowerShell error: {process.stderr}", error=True)
            
            # Verify the policy was created
            verify_cmd = f'Get-NetQosPolicy -Name "{name}" | Format-List'
            verify_process = subprocess.run(
                ["powershell.exe", "-Command", verify_cmd],
                capture_output=True,
                text=True
            )
            
            if name in verify_process.stdout:
                if not silent:
                    self.add_log(f"Successfully added game: {name} with DSCP value: {dscp_value}")
                return True
            else:
                if not silent:
                    self.add_log(f"Failed to add game to QoS list. Verification failed.", error=True)
                return False
        except Exception as e:
            if not silent:
                self.add_log(f"Error setting QoS policy: {str(e)}", error=True)
            return False
    
    def remove_qos_policy(self, name, silent=False):
        """Remove a QoS policy for a game"""
        try:
            psp = self.get_powershell_path()
            if not psp:
                self.add_log("PowerShell not found.", error=True)
                return False
            
            # Create the PowerShell command
            script = f"{psp} Remove-NetQosPolicy -Name '{name}' -Confirm:$false"
            
            # Execute the command
            res = subprocess.call(script, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            # Check if the command was successful
            if res == 0:
                if not silent:
                    self.add_log(f"Game '{name}' removed from the QoS list.")
                return True
            else:
                if not silent:
                    self.add_log(f"Failed to remove '{name}' from QoS list.", error=True)
                return False
        except Exception as e:
            if not silent:
                self.add_log(f"Error removing QoS policy: {str(e)}", error=True)
            with open("Errors.txt", "a") as errors:
                errors.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error removing QoS policy for {name}: {str(e)}\n")
            return False
    
    def get_qos_policy(self, silent=False):
        """Get all QoS policy names"""
        try:
            policy_names = []
            psp = self.get_powershell_path()
            if not psp:
                self.add_log("PowerShell not found.", error=True)
                return policy_names
            
            # Create the PowerShell command
            script = f"{psp} Get-NetQosPolicy | Select-Object -ExpandProperty Name"
            
            # Execute the command
            res = subprocess.run(script, capture_output=True, text=True, shell=True)
            
            # Process the output - split by lines and clean up
            policy_names = [name.strip() for name in res.stdout.split('\n') if name.strip()]
            
            return policy_names
        except Exception as e:
            if not silent:
                self.add_log(f"Error getting QoS policies: {str(e)}", error=True)
            with open("Errors.txt", "a") as errors:
                errors.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error getting QoS policies: {str(e)}\n")
            return []
    
    def get_qos_policy_details(self):
        """Get QoS policies with their details"""
        try:
            policy_details = []
            
            # Direct PowerShell command for listing QoS policies
            process = subprocess.run(
                ["powershell.exe", "-Command", "Get-NetQosPolicy | Format-Table Name, AppPathNameMatchCondition -AutoSize | Out-String -Width 4096"],
                capture_output=True,
                text=True
            )
            
            # Debug output
            self.add_log(f"Raw PowerShell output: {process.stdout}")
            
            # Process each line
            lines = process.stdout.strip().split('\n')
            if len(lines) > 2:  # Skip header lines
                for line in lines[2:]:  # Skip the first two lines (headers)
                    if line.strip():
                        parts = line.strip().split(None, 1)  # Split by whitespace, but only on first occurrence
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            path = parts[1].strip()
                            policy_details.append((name, path))
                            self.add_log(f"Found policy: {name} -> {path}")
            
            return policy_details
        except Exception as e:
            self.add_log(f"Error getting QoS policy details: {str(e)}", error=True)
            return []

    def refresh_game_list(self):
        """Refresh the games list in the treeview"""
        try:
            # Clear existing items
            for item in self.games_tree.get_children():
                self.games_tree.delete(item)
            
            # Get QoS policies
            policy_output = self.get_qos_policy_details()
            
            # Debug output
            self.add_log(f"Found {len(policy_output)} policies to display")
            
            # Process and add to treeview
            for name, path in policy_output:
                if name.strip():
                    # Get DSCP value for this game (or use default)
                    dscp_value = self.game_dscp_values.get(name, self.default_dscp.get())
                    
                    # Insert into treeview
                    item_id = self.games_tree.insert("", "end", values=(name, path, dscp_value))
                    self.add_log(f"Added to treeview: {name} (ID: {item_id})")
            
            self.add_log("Game list refreshed successfully.")
        except Exception as e:
            self.add_log(f"Error refreshing game list: {str(e)}", error=True)
            
    def edit_game_dscp(self, event):
        """Edit DSCP value for selected game"""
        try:
            # Get selected item
            selected = self.games_tree.selection()
            if not selected:
                if event is not None:  # Only show error if triggered by event (not button)
                    messagebox.showerror("Error", "Please select a game to edit.")
                return
            
            game_info = self.games_tree.item(selected, "values")
            game_name = game_info[0]
            current_dscp = game_info[2]
            
            # Create a dialog to edit DSCP value
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Edit DSCP Value - {game_name}")
            edit_window.geometry("400x200")
            edit_window.configure(bg="#1e1e1e")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            # Center the window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (self.root.winfo_x() + (self.root.winfo_width() // 2)) - (width // 2)
            y = (self.root.winfo_y() + (self.root.winfo_height() // 2)) - (height // 2)
            edit_window.geometry(f"+{x}+{y}")
            
            # Create form
            container = tk.Frame(edit_window, bg="#1e1e1e", padx=20, pady=20)
            container.pack(fill="both", expand=True)
            
            title_label = tk.Label(
                container,
                text=f"Edit DSCP Value for {game_name}",
                font=("Segoe UI", 12, "bold"),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            title_label.pack(pady=(0, 20))
            
            form_frame = tk.Frame(container, bg="#252525", padx=20, pady=20)
            form_frame.pack(fill="x")
            
            dscp_label = tk.Label(
                form_frame,
                text="DSCP Value (0-63):",
                bg="#252525",
                fg="#ffffff"
            )
            dscp_label.pack(anchor="w", pady=(0, 5))
            
            new_dscp_var = tk.StringVar(value=current_dscp)
            dscp_entry = ttk.Entry(
                form_frame,
                textvariable=new_dscp_var,
                width=10
            )
            dscp_entry.pack(anchor="w")
            
            info_label = tk.Label(
                form_frame,
                text="Common values: 46 (EF), 32 (CS4), 24 (CS3)",
                bg="#252525",
                fg="#aaaaaa",
                font=("Segoe UI", 8)
            )
            info_label.pack(anchor="w", pady=(5, 0))
            
            # Buttons
            buttons_frame = tk.Frame(container, bg="#1e1e1e", pady=10)
            buttons_frame.pack(fill="x")
            
            cancel_btn = ttk.Button(
                buttons_frame,
                text="Cancel",
                command=edit_window.destroy
            )
            cancel_btn.pack(side=tk.RIGHT, padx=5)
            
            def save_dscp():
                try:
                    dscp_value = int(new_dscp_var.get())
                    if 0 <= dscp_value <= 63:
                        # Update in tree
                        self.games_tree.item(selected, values=(game_name, game_info[1], dscp_value))
                        
                        # Update in memory
                        self.game_dscp_values[game_name] = dscp_value
                        
                        # Save settings
                        self.save_dscp_settings()
                        
                        # Update actual QoS policy
                        threading.Thread(target=self._update_game_dscp_thread, 
                                         args=(game_name, game_info[1], dscp_value)).start()
                        
                        edit_window.destroy()
                    else:
                        messagebox.showerror("Error", "DSCP value must be between 0 and 63.")
                except ValueError:
                    messagebox.showerror("Error", "DSCP value must be a number between 0 and 63.")
            
            save_btn = ttk.Button(
                buttons_frame,
                text="Save",
                command=save_dscp
            )
            save_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            self.add_log(f"Error editing DSCP value: {str(e)}", error=True)
    
    
    def save_default_dscp(self):
        """Save the default DSCP value"""
        try:
            dscp_value = int(self.default_dscp.get())
            if 0 <= dscp_value <= 63:
                self.game_dscp_values["DEFAULT"] = dscp_value
                self.save_dscp_settings()
                messagebox.showinfo("Success", f"Default DSCP value set to {dscp_value}.")
            else:
                messagebox.showerror("Error", "DSCP value must be between 0 and 63.")
        except ValueError:
            messagebox.showerror("Error", "DSCP value must be a number between 0 and 63.")

    # Make sure this method is also properly defined
    def save_dscp_settings(self):
        """Save DSCP settings to file"""
        try:
            with open("dscp_settings.txt", "w") as f:
                f.write(f"DEFAULT={self.default_dscp.get()}\n")
                for name, dscp in self.game_dscp_values.items():
                    if name != "DEFAULT":
                        f.write(f"{name}={dscp}\n")
            
            self.add_log("DSCP settings saved successfully.")
        except Exception as e:
            self.add_log(f"Error saving DSCP settings: {str(e)}", error=True)



    def load_dscp_settings(self):
        """Load DSCP settings from file"""
        try:
            if os.path.exists("dscp_settings.txt"):
                with open("dscp_settings.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip():
                            parts = line.strip().split('=')
                            if len(parts) == 2:
                                name, dscp = parts
                                try:
                                    self.game_dscp_values[name] = int(dscp)
                                except ValueError:
                                    pass
                    
                    # Set default DSCP value if exists
                    if "DEFAULT" in self.game_dscp_values:
                        self.default_dscp.set(self.game_dscp_values["DEFAULT"])
                
                self.add_log("DSCP settings loaded successfully.")
        except Exception as e:
            self.add_log(f"Error loading DSCP settings: {str(e)}", error=True)
            
    def _update_game_dscp_thread(self, game_name, game_path, dscp_value):
        """Thread function to update DSCP value for a game"""
        try:
            self.status_var.set(f"Updating DSCP value for {game_name}...")
            
            # Remove existing policy first
            self.remove_qos_policy(game_name, silent=True)
            
            # Add back with new DSCP value
            self.set_new_qos_policy_with_dscp(game_name, game_path, dscp_value, silent=True)
            
            self.add_log(f"Updated DSCP value for {game_name} to {dscp_value}.")
            self.root.after(0, lambda: self.status_var.set("Ready"))
        except Exception as e:
            self.add_log(f"Error updating DSCP value: {str(e)}", error=True)
            self.root.after(0, lambda: self.status_var.set("Ready"))
            
    def refresh_remove_combo(self):
        """Refresh the combobox in the remove game tab"""
        try:
            policy_details = self.get_qos_policy_details()
            policy_names = [name for name, _ in policy_details if name.strip()]
            
            self.remove_game_combo['values'] = policy_names
            if policy_names:
                self.remove_game_combo.current(0)
                # Update details for the first game
                self.update_game_details(None)
            else:
                # Clear details if no games
                self.selected_game_path.set("")
                self.selected_game_dscp.set("")
            
            self.add_log("Remove game list refreshed.")
        except Exception as e:
            self.add_log(f"Error refreshing remove game list: {str(e)}", error=True)
    
    def update_game_details(self, event):
        """Update game details when a game is selected in the combobox"""
        try:
            selected_game = self.remove_game_var.get()
            if not selected_game:
                return
            
            # Find the game details
            policy_details = self.get_qos_policy_details()
            for name, path in policy_details:
                if name == selected_game:
                    self.selected_game_path.set(path)
                    
                    # Get DSCP value for this game
                    dscp_value = self.game_dscp_values.get(name, self.default_dscp.get())
                    self.selected_game_dscp.set(dscp_value)
                    break
        except Exception as e:
            self.add_log(f"Error updating game details: {str(e)}", error=True)
    
    def browse_file(self):
        """Open file browser to select game executable"""
        file_path = filedialog.askopenfilename(
            title='Select Game Executable',
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.game_path_var.set(file_path)
            self.add_log(f"Selected file: {file_path}")
            
            # Auto-set game name from filename if name field is empty
            if not self.game_name_var.get():
                file_name = os.path.basename(file_path)
                game_name = os.path.splitext(file_name)[0]
                self.game_name_var.set(game_name)
    
    def add_game(self):
        """Add a game to the QoS policy"""
        game_name = self.game_name_var.get().strip()
        game_path = self.game_path_var.get().strip()
        
        if not game_name or not game_path:
            messagebox.showerror("Error", "Please provide both game name and path.")
            self.add_log("Failed to add game: Missing name or path.", error=True)
            return
        
        if not self.path_validator(game_path):
            messagebox.showerror("Error", "Please select a valid executable file (.exe).")
            self.add_log("Failed to add game: Invalid file type.", error=True)
            return
        
        # Try to get DSCP value
        try:
            dscp_value = int(self.game_dscp_var.get())
            if not 0 <= dscp_value <= 63:
                messagebox.showerror("Error", "DSCP value must be between 0 and 63.")
                return
        except ValueError:
            messagebox.showerror("Error", "DSCP value must be a number between 0 and 63.")
            return
        
        # Run in a separate thread to avoid UI freezing
        threading.Thread(target=self._add_game_thread, args=(game_name, game_path, dscp_value)).start()
    
    def remove_selected_game(self):
        """Remove the selected game from the treeview"""
        selected = self.games_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a game to remove.")
            return
        
        game_info = self.games_tree.item(selected, "values")
        game_name = game_info[0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{game_name}' from QoS?"):
            threading.Thread(target=self._remove_game_thread, args=(game_name,)).start()
    
    def remove_selected_from_combo(self):
        """Remove the selected game from the combobox"""
        game_name = self.remove_game_var.get()
        
        if not game_name:
            messagebox.showerror("Error", "Please select a game to remove.")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{game_name}' from QoS?"):
            threading.Thread(target=self._remove_game_thread, args=(game_name,)).start()
    
    def _remove_game_thread(self, game_name):
        """Thread function to remove a game from QoS policy"""
        try:
            self.status_var.set(f"Removing game {game_name}...")
            
            self.remove_qos_policy(game_name)
            
            # Remove from DSCP settings if exists
            if game_name in self.game_dscp_values:
                del self.game_dscp_values[game_name]
                self.save_dscp_settings()
            
            self.add_log(f"Removed game: {game_name}")
            
            # Refresh the stats and game list
            self.root.after(0, self.refresh_stats)
            self.root.after(0, self.refresh_game_list)
            self.root.after(0, self.refresh_remove_combo)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Game '{game_name}' has been removed from QoS."))
        except Exception as e:
            self.add_log(f"Error removing game: {str(e)}", error=True)
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error removing game: {str(e)}"))
        
        self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def remove_all_games(self):
        """Remove all games from QoS policy"""
        if not messagebox.askyesno("Confirm", "Are you sure you want to remove ALL games from QoS?\nThis action cannot be undone."):
            return
        
        threading.Thread(target=self._remove_all_games_thread).start()
    
    def _remove_all_games_thread(self):
        """Thread function to remove all games from QoS policy"""
        try:
            self.status_var.set("Removing all games...")
            
            policies = self.get_qos_policy_details()
            for name, _ in policies:
                if name.strip():
                    self.remove_qos_policy(name, silent=True)
            
            # Clear DSCP settings except for DEFAULT
            default_value = self.game_dscp_values.get("DEFAULT", 46)
            self.game_dscp_values.clear()
            self.game_dscp_values["DEFAULT"] = default_value
            self.save_dscp_settings()
            
            self.add_log("All games have been removed from QoS.")
            
            # Refresh the stats and game list
            self.root.after(0, self.refresh_stats)
            self.root.after(0, self.refresh_game_list)
            self.root.after(0, self.refresh_remove_combo)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("Success", "All games have been removed from QoS."))
        except Exception as e:
            self.add_log(f"Error removing all games: {str(e)}", error=True)
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error removing all games: {str(e)}"))
        
        self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def auto_detect_games(self):
        """Auto-detect and add games from Steam and Epic Games"""
        if messagebox.askyesno("Confirm", "This will scan your system for Steam and Epic Games and add them to QoS.\nContinue?"):
            threading.Thread(target=self._auto_detect_games_thread).start()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_diagnostics_frame(self, parent):
        """Create the advanced diagnostics frame"""
        # Create notebook for different diagnostic sections
        self.diagnostics_notebook = ttk.Notebook(parent)
        self.diagnostics_notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Network Path Analysis tab
        path_frame = ttk.Frame(self.diagnostics_notebook)
        self.diagnostics_notebook.add(path_frame, text="Network Path")
        
        # Server selection
        server_frame = tk.Frame(path_frame, bg="#252525", padx=20, pady=20)
        server_frame.pack(fill="x", pady=(0, 20))
        
        server_label = tk.Label(
            server_frame,
            text="Test Server:",
            bg="#252525",
            fg="#ffffff"
        )
        server_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.server_var = tk.StringVar(value="google.com")
        server_entry = ttk.Entry(
            server_frame,
            textvariable=self.server_var,
            width=30
        )
        server_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        trace_btn = ttk.Button(
            server_frame,
            text="Trace Route",
            command=self.trace_route
        )
        trace_btn.pack(side=tk.LEFT)
        
        # Path results with hop-by-hop analysis
        self.path_text = tk.Text(
            path_frame,
            height=15,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.path_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Network Interfaces tab
        interface_frame = ttk.Frame(self.diagnostics_notebook)
        self.diagnostics_notebook.add(interface_frame, text="Network Interfaces")
        
        # Interface details with statistics
        self.interface_text = tk.Text(
            interface_frame,
            height=15,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.interface_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bandwidth Testing tab
        bandwidth_frame = ttk.Frame(self.diagnostics_notebook)
        self.diagnostics_notebook.add(bandwidth_frame, text="Bandwidth Test")
        
        # Bandwidth test controls
        bandwidth_controls = tk.Frame(bandwidth_frame, bg="#252525", padx=20, pady=20)
        bandwidth_controls.pack(fill="x")
        
        self.bandwidth_status = tk.StringVar(value="Ready to test")
        status_label = tk.Label(
            bandwidth_controls,
            textvariable=self.bandwidth_status,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10)
        )
        status_label.pack(side=tk.LEFT)
        
        test_btn = ttk.Button(
            bandwidth_controls,
            text="Start Bandwidth Test",
            command=self.start_bandwidth_test
        )
        test_btn.pack(side=tk.RIGHT)
        
        # Bandwidth results
        self.bandwidth_text = tk.Text(
            bandwidth_frame,
            height=10,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.bandwidth_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Connection Quality tab
        quality_frame = ttk.Frame(self.diagnostics_notebook)
        self.diagnostics_notebook.add(quality_frame, text="Connection Quality")
        
        # Quality metrics
        quality_metrics = tk.Frame(quality_frame, bg="#252525", padx=20, pady=20)
        quality_metrics.pack(fill="x")
        
        # Bufferbloat test
        bufferbloat_frame = tk.Frame(quality_metrics, bg="#252525")
        bufferbloat_frame.pack(fill="x", pady=(0, 10))
        
        bufferbloat_label = tk.Label(
            bufferbloat_frame,
            text="Bufferbloat Test:",
            bg="#252525",
            fg="#ffffff"
        )
        bufferbloat_label.pack(side=tk.LEFT)
        
        self.bufferbloat_var = tk.StringVar(value="Not tested")
        bufferbloat_value = tk.Label(
            bufferbloat_frame,
            textvariable=self.bufferbloat_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10, "bold")
        )
        bufferbloat_value.pack(side=tk.LEFT, padx=(10, 0))
        
        test_bufferbloat_btn = ttk.Button(
            bufferbloat_frame,
            text="Test Bufferbloat",
            command=self.test_bufferbloat
        )
        test_bufferbloat_btn.pack(side=tk.RIGHT)
        
        # Connection stability
        stability_frame = tk.Frame(quality_metrics, bg="#252525")
        stability_frame.pack(fill="x", pady=(0, 10))
        
        stability_label = tk.Label(
            stability_frame,
            text="Connection Stability:",
            bg="#252525",
            fg="#ffffff"
        )
        stability_label.pack(side=tk.LEFT)
        
        self.stability_var = tk.StringVar(value="Not tested")
        stability_value = tk.Label(
            stability_frame,
            textvariable=self.stability_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10, "bold")
        )
        stability_value.pack(side=tk.LEFT, padx=(10, 0))
        
        test_stability_btn = ttk.Button(
            stability_frame,
            text="Test Stability",
            command=self.test_connection_stability
        )
        test_stability_btn.pack(side=tk.RIGHT)
        
        # Quality recommendations
        self.quality_recommendations = tk.Text(
            quality_frame,
            height=8,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Segoe UI", 9),
            wrap=tk.WORD
        )
        self.quality_recommendations.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initial refresh
        self.refresh_diagnostics()

    def start_bandwidth_test(self):
        """Start bandwidth testing"""
        try:
            self.bandwidth_status.set("Testing bandwidth...")
            self.bandwidth_text.delete(1.0, tk.END)
            self.bandwidth_text.insert(tk.END, "Starting bandwidth test...\n")
            
            # Run bandwidth test in a separate thread
            threading.Thread(target=self._bandwidth_test_thread).start()
            
        except Exception as e:
            self.add_log(f"Error starting bandwidth test: {str(e)}", error=True)
            self.bandwidth_status.set("Test failed")

    def _bandwidth_test_thread(self):
        """Thread function to perform bandwidth testing"""
        try:
            import speedtest
            
            # Initialize speedtest
            st = speedtest.Speedtest()
            
            # Get best server
            self.root.after(0, lambda: self.bandwidth_text.insert(tk.END, "Finding best server...\n"))
            st.get_best_server()
            
            # Test download speed
            self.root.after(0, lambda: self.bandwidth_text.insert(tk.END, "Testing download speed...\n"))
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            # Test upload speed
            self.root.after(0, lambda: self.bandwidth_text.insert(tk.END, "Testing upload speed...\n"))
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            # Display results
            self.root.after(0, lambda: self.bandwidth_text.insert(tk.END, 
                f"\nResults:\n"
                f"Download Speed: {download_speed:.2f} Mbps\n"
                f"Upload Speed: {upload_speed:.2f} Mbps\n"
                f"Ping: {st.results.ping:.2f} ms\n"
                f"Server: {st.results.server['sponsor']} ({st.results.server['name']})\n"
            ))
            
            self.root.after(0, lambda: self.bandwidth_status.set("Test complete"))
            
        except Exception as e:
            self.root.after(0, lambda: self.bandwidth_text.insert(tk.END, f"Error: {str(e)}\n"))
            self.root.after(0, lambda: self.bandwidth_status.set("Test failed"))
            self.add_log(f"Error in bandwidth test: {str(e)}", error=True)

    def test_bufferbloat(self):
        """Test for bufferbloat"""
        try:
            self.bufferbloat_var.set("Testing...")
            
            # Run bufferbloat test in a separate thread
            threading.Thread(target=self._bufferbloat_test_thread).start()
            
        except Exception as e:
            self.add_log(f"Error starting bufferbloat test: {str(e)}", error=True)
            self.bufferbloat_var.set("Test failed")

    def _bufferbloat_test_thread(self):
        """Thread function to test for bufferbloat"""
        try:
            import subprocess
            
            # Use ping to test for bufferbloat
            process = subprocess.Popen(
                ["ping", "-n", "10", "8.8.8.8"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            latencies = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if "time=" in line:
                    try:
                        latency = float(line.split("time=")[1].split("ms")[0])
                        latencies.append(latency)
                    except:
                        pass
            
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                max_latency = max(latencies)
                bufferbloat = max_latency - avg_latency
                
                if bufferbloat > 100:
                    result = "High bufferbloat detected"
                elif bufferbloat > 50:
                    result = "Moderate bufferbloat detected"
                else:
                    result = "Low bufferbloat"
                
                self.root.after(0, lambda: self.bufferbloat_var.set(f"{result} ({bufferbloat:.1f}ms)"))
                
                # Update recommendations
                self._update_quality_recommendations()
            else:
                self.root.after(0, lambda: self.bufferbloat_var.set("Test failed"))
                
        except Exception as e:
            self.root.after(0, lambda: self.bufferbloat_var.set("Test failed"))
            self.add_log(f"Error in bufferbloat test: {str(e)}", error=True)

    def test_connection_stability(self):
        """Test connection stability"""
        try:
            self.stability_var.set("Testing...")
            
            # Run stability test in a separate thread
            threading.Thread(target=self._stability_test_thread).start()
            
        except Exception as e:
            self.add_log(f"Error starting stability test: {str(e)}", error=True)
            self.stability_var.set("Test failed")

    def _stability_test_thread(self):
        """Thread function to test connection stability"""
        try:
            import subprocess
            import statistics
            
            # Test connection stability using ping
            process = subprocess.Popen(
                ["ping", "-n", "20", "8.8.8.8"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            latencies = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if "time=" in line:
                    try:
                        latency = float(line.split("time=")[1].split("ms")[0])
                        latencies.append(latency)
                    except:
                        pass
            
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                jitter = statistics.stdev(latencies)
                
                if jitter > 20:
                    result = "Unstable connection"
                elif jitter > 10:
                    result = "Moderately stable"
                else:
                    result = "Stable connection"
                
                self.root.after(0, lambda: self.stability_var.set(
                    f"{result} (Jitter: {jitter:.1f}ms)"
                ))
                
                # Update recommendations
                self._update_quality_recommendations()
            else:
                self.root.after(0, lambda: self.stability_var.set("Test failed"))
                
        except Exception as e:
            self.root.after(0, lambda: self.stability_var.set("Test failed"))
            self.add_log(f"Error in stability test: {str(e)}", error=True)

    def _update_quality_recommendations(self):
        """Update quality recommendations based on test results"""
        try:
            recommendations = []
            
            # Bufferbloat recommendations
            bufferbloat = self.bufferbloat_var.get()
            if "High bufferbloat" in bufferbloat:
                recommendations.append("• Enable QoS on your router to reduce bufferbloat")
                recommendations.append("• Consider using a gaming router with SQM (Smart Queue Management)")
            elif "Moderate bufferbloat" in bufferbloat:
                recommendations.append("• Monitor bufferbloat during gaming sessions")
                recommendations.append("• Consider enabling QoS if issues persist")
            
            # Stability recommendations
            stability = self.stability_var.get()
            if "Unstable" in stability:
                recommendations.append("• Check for network congestion or interference")
                recommendations.append("• Consider using a wired connection instead of WiFi")
                recommendations.append("• Update network drivers and firmware")
            elif "Moderately stable" in stability:
                recommendations.append("• Monitor connection stability during gaming")
                recommendations.append("• Consider optimizing network settings")
            
            # Update recommendations text
            self.quality_recommendations.delete(1.0, tk.END)
            if recommendations:
                self.quality_recommendations.insert(tk.END, "Recommendations:\n\n")
                for rec in recommendations:
                    self.quality_recommendations.insert(tk.END, f"{rec}\n")
            else:
                self.quality_recommendations.insert(tk.END, "No specific recommendations at this time.")
            
        except Exception as e:
            self.add_log(f"Error updating quality recommendations: {str(e)}", error=True)

    def _create_optimization_frame(self, parent):
        """Create the performance optimization frame"""
        # Auto-optimization section
        auto_frame = tk.Frame(parent, bg="#252525", padx=20, pady=20)
        auto_frame.pack(fill="x", pady=(0, 20))
        
        auto_title = tk.Label(
            auto_frame,
            text="Automatic Optimization",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        auto_title.pack(anchor="w", pady=(0, 10))
        
        auto_desc = tk.Label(
            auto_frame,
            text="Automatically adjust DSCP values based on network conditions",
            bg="#252525",
            fg="#aaaaaa",
            wraplength=600,
            justify=tk.LEFT
        )
        auto_desc.pack(anchor="w", pady=(0, 10))
        
        # Optimization controls
        controls_frame = tk.Frame(auto_frame, bg="#252525")
        controls_frame.pack(fill="x", pady=(0, 10))
        
        self.auto_optimize_var = tk.BooleanVar(value=False)
        auto_check = ttk.Checkbutton(
            controls_frame,
            text="Enable Auto-Optimization",
            variable=self.auto_optimize_var,
            command=self.toggle_auto_optimization
        )
        auto_check.pack(side=tk.LEFT, padx=(0, 10))
        
        # Optimization status
        self.optimization_status_var = tk.StringVar(value="Auto-optimization is disabled")
        status_label = tk.Label(
            controls_frame,
            textvariable=self.optimization_status_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 9)
        )
        status_label.pack(side=tk.LEFT)
        
        # Optimization recommendations
        rec_frame = tk.Frame(parent, bg="#252525", padx=20, pady=20)
        rec_frame.pack(fill="x")
        
        rec_title = tk.Label(
            rec_frame,
            text="Optimization Recommendations",
            font=("Segoe UI", 12, "bold"),
            bg="#252525",
            fg="#ffffff"
        )
        rec_title.pack(anchor="w", pady=(0, 10))
        
        self.optimization_rec_var = tk.StringVar(value="No recommendations available")
        rec_label = tk.Label(
            rec_frame,
            textvariable=self.optimization_rec_var,
            bg="#252525",
            fg="#00b4d8",
            font=("Segoe UI", 10),
            wraplength=600,
            justify=tk.LEFT
        )
        rec_label.pack(anchor="w")

    def trace_route(self):
        """Perform a traceroute to the specified server"""
        try:
            server = self.server_var.get().strip()
            if not server:
                messagebox.showerror("Error", "Please enter a server address")
                return
            
            self.path_text.delete(1.0, tk.END)
            self.path_text.insert(tk.END, f"Tracing route to {server}...\n")
            
            # Run traceroute in a separate thread
            threading.Thread(target=self._trace_route_thread, args=(server,)).start()
            
        except Exception as e:
            self.add_log(f"Error starting traceroute: {str(e)}", error=True)

    def _trace_route_thread(self, server):
        """Thread function to perform traceroute"""
        try:
            import subprocess
            
            # Use tracert command for Windows
            process = subprocess.Popen(
                ["tracert", server],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    self.root.after(0, lambda l=line: self.path_text.insert(tk.END, l))
            
            self.root.after(0, lambda: self.path_text.insert(tk.END, "\nTrace complete.\n"))
            
        except Exception as e:
            self.root.after(0, lambda: self.path_text.insert(tk.END, f"Error: {str(e)}\n"))
            self.add_log(f"Error in traceroute: {str(e)}", error=True)

    def refresh_diagnostics(self):
        """Refresh network interface information"""
        try:
            import subprocess
            import re
            
            self.interface_text.delete(1.0, tk.END)
            
            # Get network interface information
            process = subprocess.Popen(
                ["ipconfig", "/all"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, _ = process.communicate()
            
            # Parse and display relevant information
            self.interface_text.insert(tk.END, "Network Interfaces:\n\n")
            
            # Find all network adapters
            adapters = re.split(r'\n(?=\w)', output)
            for adapter in adapters:
                if "Ethernet" in adapter or "Wi-Fi" in adapter:
                    self.interface_text.insert(tk.END, adapter + "\n\n")
            
        except Exception as e:
            self.interface_text.insert(tk.END, f"Error: {str(e)}\n")
            self.add_log(f"Error refreshing diagnostics: {str(e)}", error=True)

    def toggle_auto_optimization(self):
        """Toggle automatic optimization"""
        if self.auto_optimize_var.get():
            self.optimization_active = True
            self.optimization_thread = threading.Thread(target=self._optimization_thread)
            self.optimization_thread.daemon = True
            self.optimization_thread.start()
            self.optimization_status_var.set("Auto-optimization is active")
            self.add_log("Started automatic optimization")
        else:
            self.optimization_active = False
            if self.optimization_thread:
                self.optimization_thread.join(timeout=1)
            self.optimization_status_var.set("Auto-optimization is disabled")
            self.add_log("Stopped automatic optimization")

    def _optimization_thread(self):
        """Thread function for automatic optimization"""
        while self.optimization_active:
            try:
                # Get current performance metrics
                if not self.performance_history:
                    time.sleep(3)
                    continue
                
                latest = self.performance_history[-1]
                latency = latest['latency']
                loss = latest['loss']
                jitter = latest['jitter']
                
                # Generate optimization recommendations
                recommendations = []
                
                if latency > 100:
                    recommendations.append("Consider lowering DSCP values to prioritize gaming traffic")
                if loss > 1:
                    recommendations.append("Check network connection and consider using QoS policies")
                if jitter > 15:
                    recommendations.append("Try using a lower DSCP value to reduce jitter")
                
                if not recommendations:
                    recommendations.append("Current settings are optimal")
                
                # Update UI
                self.root.after(0, lambda r=recommendations: self.optimization_rec_var.set("\n".join(r)))
                
                # Sleep for 5 seconds before next check
                time.sleep(5)
                
            except Exception as e:
                self.add_log(f"Error in optimization thread: {str(e)}", error=True)
                time.sleep(5)

    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # Create tooltip window
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create tooltip label
            label = tk.Label(
                tooltip,
                text=text,
                justify=tk.LEFT,
                background="#ffffe0",
                foreground="#000000",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=5,
                pady=2
            )
            label.pack()
            
            # Remove tooltip when mouse leaves
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind("<Leave>", hide_tooltip)
        
        widget.bind("<Enter>", show_tooltip)

# Main function to run the application
def main():
    # Enable high DPI awareness for better display on high-resolution screens
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    # Create the root window
    root = tk.Tk()
    
    # Apply the dark theme to the application
    root.configure(bg="#1e1e1e")
    
    # Check for admin privileges
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            messagebox.showwarning(
                "Administrator Privileges Required",
                "This application requires administrator privileges to manage QoS policies.\n\n"
                "Please restart the application as administrator."
            )
    except Exception:
        pass
    
    # Initialize the application
    app = QoSManagerApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()