#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 BAL MASQUÉ
Floutage de visages
"""

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
import webbrowser
import ctypes
import sys


def enable_high_dpi():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass


class Style:
    """Styles centralisés"""
    
    # Couleurs vives
    BG = '#0f0f1a'
    BG_PANEL = '#1a1a2e'
    ACCENT = '#ff2d55'
    ACCENT_HOVER = '#ff5c7c'
    SECONDARY = '#00e5a0'
    SECONDARY_HOVER = '#4dffc3'
    HIGHLIGHT = '#ffe600'
    PURPLE = '#a855f7'
    PURPLE_HOVER = '#c084fc'
    ORANGE = '#ff9500'
    CYAN = '#00d4ff'
    PINK = '#ff6bcb'
    TEXT = '#ffffff'
    TEXT_DIM = '#b8b8d0'
    TEXT_MUTED = '#7878a0'
    CANVAS_BG = '#08080f'
    LINK = '#5cb8ff'
    WHITE = '#ffffff'
    BLACK = '#000000'
    
    FONT = None
    FONT_MONO = None
    
    @classmethod
    def init(cls, root):
        available = list(tkfont.families())
        
        for f in ['Inter', 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial']:
            if f in available:
                cls.FONT = f
                break
        cls.FONT = cls.FONT or 'TkDefaultFont'
        
        for f in ['JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco']:
            if f in available:
                cls.FONT_MONO = f
                break
        cls.FONT_MONO = cls.FONT_MONO or 'monospace'
    
    @classmethod
    def apply(cls, widget, style_name, **overrides):
        styles = {
            'body': {'font': (cls.FONT, 11), 'bg': cls.BG, 'fg': cls.TEXT},
            'small': {'font': (cls.FONT, 10), 'bg': cls.BG, 'fg': cls.TEXT_MUTED},
            'section_title': {'font': (cls.FONT, 9, 'bold'), 'bg': cls.BG_PANEL, 'fg': cls.CYAN},
            'link': {'font': (cls.FONT, 10, 'underline'), 'bg': cls.BG, 'fg': cls.LINK, 'cursor': 'hand2'},
            'btn_primary': {
                'font': (cls.FONT, 10, 'bold'),
                'bg': cls.SECONDARY, 'fg': cls.BLACK,
                'activebackground': cls.SECONDARY_HOVER,
                'activeforeground': cls.BLACK,
                'relief': 'flat', 'cursor': 'hand2'
            },
            'btn_accent': {
                'font': (cls.FONT, 10),
                'bg': cls.ACCENT, 'fg': cls.WHITE,
                'activebackground': cls.ACCENT_HOVER,
                'activeforeground': cls.WHITE,
                'relief': 'flat', 'cursor': 'hand2'
            },
            'btn_secondary': {
                'font': (cls.FONT, 10),
                'bg': cls.PURPLE, 'fg': cls.WHITE,
                'activebackground': cls.PURPLE_HOVER,
                'activeforeground': cls.WHITE,
                'relief': 'flat', 'cursor': 'hand2'
            },
            'btn_save': {
                'font': (cls.FONT, 10),
                'bg': cls.ORANGE, 'fg': cls.BLACK,
                'activebackground': cls.HIGHLIGHT,
                'activeforeground': cls.BLACK,
                'relief': 'flat', 'cursor': 'hand2'
            },
            'radio': {
                'font': (cls.FONT, 10),
                'bg': cls.BG_PANEL, 'fg': cls.TEXT,
                'selectcolor': cls.PURPLE,
                'activebackground': cls.BG_PANEL,
                'activeforeground': cls.PINK,
                'highlightthickness': 0
            }
        }
        
        config = styles.get(style_name, {}).copy()
        config.update(overrides)
        widget.configure(**config)


class BalMasque:
    
    LOGO_PATH = "logo.png"
    
    def __init__(self):
        enable_high_dpi()
        
        self.logo_images = {}
        
        if not self.show_disclaimer():
            return
        
        self.root = tk.Tk()
        self.root.title("Bal Masqué")
        self.root.geometry("1300x850")
        self.root.configure(bg=Style.BG)
        self.root.minsize(1000, 700)
        
        Style.init(self.root)
        self.center_window(self.root, 1300, 850)
        
        self.image = None
        self.original = None
        self.filepath = None
        self.tk_image = None
        self.display_ratio = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        self.cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.manual_zones = []
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.temp_rect_id = None
        
        self.build_ui()
        self.root.mainloop()
    
    def center_window(self, win, w, h):
        win.update_idletasks()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
    
    def load_logo(self, height):
        key = f"logo_{height}"
        if key in self.logo_images:
            return self.logo_images[key]
        
        try:
            logo_path = Path(self.LOGO_PATH)
            if not logo_path.exists():
                return None
            
            img = Image.open(logo_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            supersample = 4
            target_h = height * supersample
            orig_w, orig_h = img.size
            ratio = target_h / orig_h
            target_w = int(orig_w * ratio)
            
            img_large = img.resize((target_w, target_h), Image.LANCZOS)
            img_final = img_large.resize((target_w // supersample, height), Image.LANCZOS)
            
            tk_img = ImageTk.PhotoImage(img_final)
            self.logo_images[key] = tk_img
            return tk_img
            
        except Exception as e:
            print(f"Logo error: {e}")
            return None
    
    def show_disclaimer(self):
        enable_high_dpi()
        
        win = tk.Tk()
        win.title("Bal Masqué")
        win.configure(bg=Style.BG)
        
        Style.init(win)
        self.center_window(win, 550, 580)
        
        accepted = [False]
        
        def accept():
            accepted[0] = True
            win.quit()
            win.destroy()
        
        def on_close():
            win.quit()
            win.destroy()
        
        win.protocol("WM_DELETE_WINDOW", on_close)
        
        canvas = tk.Canvas(win, bg=Style.BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        main = tk.Frame(canvas, bg=Style.BG)
        canvas.create_window((0, 0), window=main, anchor='nw')
        
        content = tk.Frame(main, bg=Style.BG)
        content.pack(expand=True, fill='both', padx=45, pady=35)
        
        # Logo plus grand
        logo = self.load_logo(90)
        if logo:
            lbl = tk.Label(content, image=logo, bg=Style.BG)
            lbl.image = logo
            lbl.pack(pady=(0, 10))
        else:
            lbl = tk.Label(content, text="🎭 Bal Masqué", font=(Style.FONT, 22, 'bold'), bg=Style.BG, fg=Style.ACCENT)
            lbl.pack(pady=(0, 10))
        
        sub = tk.Label(content, text="Floutage de visages • Hors-ligne", font=(Style.FONT, 11), bg=Style.BG, fg=Style.CYAN)
        sub.pack(pady=(0, 25))
        
        # Métaphore avec fond coloré
        metaphor_frame = tk.Frame(content, bg=Style.PURPLE, padx=3, pady=3)
        metaphor_frame.pack(fill='x', pady=(0, 25))
        
        metaphor_inner = tk.Frame(metaphor_frame, bg=Style.BG_PANEL, padx=20, pady=18)
        metaphor_inner.pack(fill='x')
        
        metaphor_text = """Au bal masqué, chacun·e choisit ce qu'iel révèle.

Dans la rue comme au carnaval, le masque protège.
Il permet d'exister sans être fiché, de défiler sans être ciblé.

Vos images restent sur votre machine."""
        
        metaphor = tk.Label(
            metaphor_inner, text=metaphor_text,
            font=(Style.FONT, 11), bg=Style.BG_PANEL, fg=Style.TEXT,
            justify='left', wraplength=420
        )
        metaphor.pack()
        
        # Bouton principal
        btn = tk.Button(
            content, text="Accéder au bal",
            command=accept, padx=25, pady=10,
            font=(Style.FONT, 12, 'bold'),
            bg=Style.SECONDARY, fg=Style.BLACK,
            activebackground=Style.SECONDARY_HOVER,
            activeforeground=Style.BLACK,
            relief='flat', cursor='hand2'
        )
        btn.pack(pady=(0, 25))
        
        # Ressources
        resources_frame = tk.Frame(content, bg=Style.BG)
        resources_frame.pack(fill='x')
        
        expanded = [False]
        resources_content = [None]
        
        def toggle_resources():
            expanded[0] = not expanded[0]
            
            if expanded[0]:
                toggle_btn.config(text="▾ Ressources", fg=Style.PINK)
                rc = tk.Frame(resources_frame, bg=Style.BG)
                rc.pack(fill='x', pady=(10, 0))
                resources_content[0] = rc
                
                resources = [
                    ("La Quadrature du Net", "https://www.laquadrature.net", "Libertés numériques"),
                    ("Technopolice", "https://technopolice.fr", "Surveillance urbaine"),
                    ("Guide Boum", "https://guide.boum.org", "Autodéfense numérique"),
                ]
                
                for name, url, desc in resources:
                    row = tk.Frame(rc, bg=Style.BG)
                    row.pack(fill='x', pady=3)
                    
                    link = tk.Label(row, text=f"★ {name}", font=(Style.FONT, 10, 'underline'), bg=Style.BG, fg=Style.LINK, cursor='hand2')
                    link.pack(side='left')
                    link.bind('<Button-1>', lambda e, u=url: webbrowser.open(u))
                    
                    tk.Label(row, text=f" — {desc}", font=(Style.FONT, 10), bg=Style.BG, fg=Style.TEXT_DIM).pack(side='left')
                
                main.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'))
            else:
                toggle_btn.config(text="▸ Ressources", fg=Style.TEXT_DIM)
                if resources_content[0]:
                    resources_content[0].destroy()
                main.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'))
        
        toggle_btn = tk.Button(
            resources_frame, text="▸ Ressources",
            command=toggle_resources,
            font=(Style.FONT, 10),
            bg=Style.BG, fg=Style.TEXT_DIM,
            activebackground=Style.BG, activeforeground=Style.PINK,
            relief='flat', cursor='hand2', bd=0
        )
        toggle_btn.pack(anchor='w')
        
        tk.Label(
            content,
            text="Fonte Ouvrières — typotheque.genderfluid.space",
            font=(Style.FONT, 9),
            bg=Style.BG, fg=Style.TEXT_MUTED
        ).pack(pady=(20, 0))
        
        main.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        
        canvas.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'))
        
        win.mainloop()
        return accepted[0]
    
    def build_ui(self):
        # Header avec gradient simulé
        header = tk.Frame(self.root, bg=Style.BG_PANEL)
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=Style.BG_PANEL)
        header_content.pack(fill='x', padx=25, pady=12)
        
        logo = self.load_logo(45)
        if logo:
            lbl = tk.Label(header_content, image=logo, bg=Style.BG_PANEL)
            lbl.image = logo
            lbl.pack(side='left')
        else:
            tk.Label(header_content, text="🎭 Bal Masqué", font=(Style.FONT, 16, 'bold'), bg=Style.BG_PANEL, fg=Style.ACCENT).pack(side='left')
        
        btn_open = tk.Button(header_content, text="Ouvrir image", command=self.open_image, padx=15, pady=6)
        Style.apply(btn_open, 'btn_accent')
        btn_open.pack(side='right')
        
        body = tk.Frame(self.root, bg=Style.BG)
        body.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.panel = tk.Frame(body, bg=Style.BG_PANEL, padx=15, pady=15)
        self.panel.pack(side='left', fill='y', padx=(0, 15))
        
        self.build_panel()
        
        canvas_frame = tk.Frame(body, bg=Style.CYAN, padx=2, pady=2)
        canvas_frame.pack(side='left', fill='both', expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg=Style.CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        self.show_welcome()
        
        status = tk.Frame(self.root, bg=Style.BG_PANEL)
        status.pack(fill='x')
        
        self.status = tk.Label(status, text="✦ Prêt", font=(Style.FONT, 10), bg=Style.BG_PANEL, fg=Style.CYAN, padx=20, pady=8)
        self.status.pack(side='left')
    
    def build_panel(self):
        p = self.panel
        pad_x = 5
        
        def section(text):
            lbl = tk.Label(p, text=text, font=(Style.FONT, 9, 'bold'), bg=Style.BG_PANEL, fg=Style.CYAN)
            lbl.pack(anchor='w', padx=pad_x, pady=(18, 8))
        
        # Mode
        section("Mode")
        
        self.mode = tk.StringVar(value='auto')
        
        for txt, val in [("Auto-détection", "auto"), ("Manuel", "manual")]:
            rb = tk.Radiobutton(p, text=txt, variable=self.mode, value=val, command=self.on_mode_change)
            Style.apply(rb, 'radio')
            rb.pack(anchor='w', padx=pad_x, pady=2)
        
        # Effet
        section("Effet")
        
        self.blur_type = tk.StringVar(value='pixel')
        
        for txt, val in [("Pixels", "pixel"), ("Flou", "blur"), ("Noir", "black")]:
            rb = tk.Radiobutton(p, text=txt, variable=self.blur_type, value=val)
            Style.apply(rb, 'radio')
            rb.pack(anchor='w', padx=pad_x, pady=2)
        
        # Intensité
        section("Intensité")
        
        self.intensity = tk.IntVar(value=51)
        
        scale = tk.Scale(
            p, from_=15, to=99, orient='horizontal',
            variable=self.intensity,
            bg=Style.BG_PANEL, fg=Style.TEXT,
            highlightthickness=0, length=160,
            troughcolor=Style.PURPLE,
            activebackground=Style.PINK,
            font=(Style.FONT, 9)
        )
        scale.pack(padx=pad_x, pady=(0, 8))
        
        # Zones
        section("Zones manuelles")
        
        self.zone_label = tk.Label(p, text="Aucune zone", font=(Style.FONT, 10), bg=Style.BG_PANEL, fg=Style.TEXT_DIM)
        self.zone_label.pack(anchor='w', padx=pad_x, pady=(0, 8))
        
        zone_btns = tk.Frame(p, bg=Style.BG_PANEL)
        zone_btns.pack(fill='x', padx=pad_x)
        
        self.btn_undo = tk.Button(zone_btns, text="Annuler", command=self.undo_zone, padx=10, pady=5, state='disabled')
        Style.apply(self.btn_undo, 'btn_secondary')
        self.btn_undo.pack(side='left', padx=(0, 8))
        
        self.btn_clear = tk.Button(zone_btns, text="Effacer", command=self.clear_zones, padx=10, pady=5, state='disabled')
        Style.apply(self.btn_clear, 'btn_secondary')
        self.btn_clear.pack(side='left')
        
        # Actions
        section("Actions")
        
        self.btn_mask = tk.Button(p, text="✦ Masquer", command=self.apply_blur, pady=8, state='disabled')
        Style.apply(self.btn_mask, 'btn_primary')
        self.btn_mask.pack(fill='x', padx=pad_x, pady=(5, 8))
        
        self.btn_reset = tk.Button(p, text="Réinitialiser", command=self.reset_image, pady=6, state='disabled')
        Style.apply(self.btn_reset, 'btn_secondary')
        self.btn_reset.pack(fill='x', padx=pad_x, pady=4)
        
        self.btn_save = tk.Button(p, text="Enregistrer", command=self.save_image, pady=6, state='disabled')
        Style.apply(self.btn_save, 'btn_save')
        self.btn_save.pack(fill='x', padx=pad_x, pady=4)
        
        tk.Frame(p, bg=Style.BG_PANEL, height=20).pack()
    
    def show_welcome(self):
        self.canvas.delete('all')
        self.canvas.update()
        
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 500
        cx, cy = w // 2, h // 2
        
        self.canvas.create_oval(cx - 60, cy - 60, cx + 60, cy + 60, outline=Style.PURPLE, width=3)
        self.canvas.create_text(cx, cy, text="🎭", font=(Style.FONT, 32), fill=Style.TEXT)
        self.canvas.create_text(cx, cy + 85, text="Ouvrir une image pour commencer", font=(Style.FONT, 12), fill=Style.TEXT_DIM)
    
    def on_mode_change(self):
        if self.mode.get() == 'manual':
            self.canvas.config(cursor='crosshair')
            self.status.config(text="✦ Mode manuel : dessiner les zones à masquer")
        else:
            self.canvas.config(cursor='arrow')
            self.status.config(text="✦ Mode auto-détection")
        self.update_display()
    
    def update_zones_ui(self):
        n = len(self.manual_zones)
        self.zone_label.config(text=f"{n} zone{'s' if n > 1 else ''}" if n else "Aucune zone")
        state = 'normal' if n else 'disabled'
        self.btn_undo.config(state=state)
        self.btn_clear.config(state=state)
    
    def enable_buttons(self, on=True):
        state = 'normal' if on else 'disabled'
        self.btn_mask.config(state=state)
        self.btn_reset.config(state=state)
        self.btn_save.config(state=state)
    
    def open_image(self):
        path = filedialog.askopenfilename(
            title="Ouvrir une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tous", "*.*")]
        )
        
        if not path:
            return
        
        try:
            arr = np.fromfile(path, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            
            if img is None:
                pil = Image.open(path).convert('RGB')
                img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
            
            self.original = img
            self.image = img.copy()
            self.filepath = path
            self.manual_zones.clear()
            
            self.update_zones_ui()
            self.enable_buttons(True)
            self.update_display()
            
            h, w = img.shape[:2]
            self.status.config(text=f"✦ {Path(path).name} — {w}×{h}")
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def update_display(self):
        if self.image is None:
            self.show_welcome()
            return
        
        self.canvas.delete('all')
        
        disp = self.image.copy()
        
        for (x, y, w, h) in self.manual_zones:
            cv2.rectangle(disp, (x, y), (x + w, y + h), (255, 107, 203), 2)
        
        rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        
        self.canvas.update()
        cw = max(self.canvas.winfo_width(), 400)
        ch = max(self.canvas.winfo_height(), 300)
        
        iw, ih = pil.size
        self.display_ratio = min(cw / iw, ch / ih, 1.0)
        
        nw = int(iw * self.display_ratio)
        nh = int(ih * self.display_ratio)
        
        pil = pil.resize((nw, nh), Image.LANCZOS)
        
        self.offset_x = (cw - nw) // 2
        self.offset_y = (ch - nh) // 2
        
        self.tk_image = ImageTk.PhotoImage(pil)
        self.canvas.create_image(self.offset_x, self.offset_y, anchor='nw', image=self.tk_image)
    
    def on_press(self, e):
        if self.mode.get() != 'manual' or self.image is None:
            return
        
        self.drawing = True
        self.start_x = e.x
        self.start_y = e.y
        
        self.temp_rect_id = self.canvas.create_rectangle(
            e.x, e.y, e.x, e.y,
            outline=Style.HIGHLIGHT, width=2, dash=(6, 3)
        )
    
    def on_drag(self, e):
        if not self.drawing or not self.temp_rect_id:
            return
        self.canvas.coords(self.temp_rect_id, self.start_x, self.start_y, e.x, e.y)
    
    def on_release(self, e):
        if not self.drawing:
            return
        
        self.drawing = False
        
        if self.temp_rect_id:
            self.canvas.delete(self.temp_rect_id)
            self.temp_rect_id = None
        
        x1, y1 = min(self.start_x, e.x), min(self.start_y, e.y)
        x2, y2 = max(self.start_x, e.x), max(self.start_y, e.y)
        
        if (x2 - x1) < 10 or (y2 - y1) < 10:
            return
        
        ix1 = int((x1 - self.offset_x) / self.display_ratio)
        iy1 = int((y1 - self.offset_y) / self.display_ratio)
        ix2 = int((x2 - self.offset_x) / self.display_ratio)
        iy2 = int((y2 - self.offset_y) / self.display_ratio)
        
        if self.original is not None:
            h, w = self.original.shape[:2]
            ix1, ix2 = max(0, min(ix1, w)), max(0, min(ix2, w))
            iy1, iy2 = max(0, min(iy1, h)), max(0, min(iy2, h))
        
        zone = (ix1, iy1, ix2 - ix1, iy2 - iy1)
        
        if zone[2] > 5 and zone[3] > 5:
            self.manual_zones.append(zone)
            self.update_zones_ui()
            self.update_display()
    
    def undo_zone(self):
        if self.manual_zones:
            self.manual_zones.pop()
            self.update_zones_ui()
            self.update_display()
    
    def clear_zones(self):
        self.manual_zones.clear()
        self.update_zones_ui()
        self.update_display()
    
    def apply_blur(self):
        if self.image is None:
            return
        
        zones = list(self.manual_zones)
        
        if self.mode.get() == 'auto':
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = self.cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            zones.extend(faces)
        
        if not zones:
            messagebox.showinfo("Info", "Aucun visage détecté.\nPassez en mode manuel pour dessiner les zones.")
            return
        
        k = self.intensity.get()
        if k % 2 == 0:
            k += 1
        
        blur_type = self.blur_type.get()
        
        for (x, y, w, h) in zones:
            x, y = max(0, x), max(0, y)
            roi = self.image[y:y+h, x:x+w]
            
            if roi.size == 0:
                continue
            
            if blur_type == 'blur':
                result = cv2.GaussianBlur(roi, (k, k), 0)
            elif blur_type == 'pixel':
                sw = max(1, w // max(5, k // 10))
                sh = max(1, h // max(5, k // 10))
                small = cv2.resize(roi, (sw, sh), interpolation=cv2.INTER_LINEAR)
                result = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
            else:
                result = np.zeros_like(roi)
            
            self.image[y:y+h, x:x+w] = result
        
        self.manual_zones.clear()
        self.update_zones_ui()
        self.update_display()
        
        self.status.config(text=f"✦ {len(zones)} zone{'s' if len(zones) > 1 else ''} masquée{'s' if len(zones) > 1 else ''}")
    
    def reset_image(self):
        if self.original is None:
            return
        
        self.image = self.original.copy()
        self.manual_zones.clear()
        self.update_zones_ui()
        self.update_display()
        self.status.config(text="✦ Image réinitialisée")
    
    def save_image(self):
        if self.image is None:
            return
        
        name = f"masque_{Path(self.filepath).stem}.png" if self.filepath else "masque.png"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=name,
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        
        if not path:
            return
        
        try:
            ext = Path(path).suffix.lower()
            
            if ext in ['.jpg', '.jpeg']:
                _, enc = cv2.imencode('.jpg', self.image, [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                _, enc = cv2.imencode('.png', self.image)
            
            enc.tofile(path)
            self.status.config(text=f"✦ Enregistré : {Path(path).name}")
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    BalMasque()
