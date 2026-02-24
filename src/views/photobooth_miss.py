"""
Photobooth Miss – Bouton Python (Tkinter)
Lancer : python photobooth_miss.py
"""
import tkinter as tk
import math
import random
import time


# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#0a0008"
GOLD        = "#d4af37"
GOLD_LIGHT  = "#f5d47a"
GOLD_DARK   = "#9a7b10"
ROSE        = "#c0507a"
WHITE_WARM  = "#fff8e7"
BTN_BG      = "#110010"
BTN_RIM     = "#d4af37"

W, H = 520, 480
CX, CY = W // 2, H // 2      # centre du bouton
R      = 68                   # rayon du bouton


# ── Utilitaires ──────────────────────────────────────────────────────────────
def lerp_color(c1, c2, t):
    """Interpolation linéaire entre deux couleurs hex."""
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# ── App principale ────────────────────────────────────────────────────────────
class PhotoboothApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("✦ Photobooth Miss ✦")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=W, height=H,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()

        # ── État ──
        self.angle_ring1   = 0.0
        self.angle_ring2   = 0.0
        self.crown_offset  = 0.0
        self.sparkles: list[dict] = []
        self.particles: list[dict] = []
        self.flash_alpha   = 0.0
        self.flash_rect    = None
        self.hovered       = False
        self.btn_scale     = 1.0
        self.btn_scale_target = 1.0
        self.photo_count   = 0

        # ── Dessin ──
        self._draw_background()
        self._build_static_labels()
        self._build_button_layers()
        self._bind_events()
        self._tick()

    # ── Fond radial simulé avec des cercles ──────────────────────────────────
    def _draw_background(self):
        for i in range(30, 0, -1):
            alpha = i / 30
            r_val = int(10 + 20 * alpha * 0.5)
            g_val = int(2 + 5 * alpha * 0.2)
            b_val = int(10 + 15 * alpha * 0.3)
            color = f"#{r_val:02x}{g_val:02x}{b_val:02x}"
            size = i * 18
            self.canvas.create_oval(CX - size, CY - size,
                                    CX + size, CY + size,
                                    fill=color, outline="")

    # ── Labels statiques ─────────────────────────────────────────────────────
    def _build_static_labels(self):
        # Titre haut
        self.canvas.create_text(CX, 28, text="✦  PHOTOBOOTH  ✦",
                                font=("Georgia", 11, "italic"),
                                fill=GOLD_DARK)
        # Sous-titre
        self.canvas.create_text(CX, H - 38,
                                text="Votre moment de gloire vous attend…",
                                font=("Georgia", 10, "italic"),
                                fill="#7a5c20")
        # Diamants décoratifs bas
        for dx in (-18, 0, 18):
            size = 5 if dx != 0 else 7
            self.canvas.create_polygon(
                CX + dx, H - 18 - size,
                CX + dx + size, H - 18,
                CX + dx, H - 18 + size,
                CX + dx - size, H - 18,
                fill=GOLD_DARK, outline=""
            )

    # ── Couches du bouton (recréées à chaque frame si besoin) ────────────────
    def _build_button_layers(self):
        # Flash overlay (invisible au départ)
        self.flash_rect = self.canvas.create_rectangle(
            0, 0, W, H, fill=WHITE_WARM, outline="", state="hidden"
        )

        # Anneau 2 (pointillé externe) – simulé par tirets
        self.ring2_items = self._create_dashed_circle(CX, CY, R + 32, 40,
                                                      GOLD_DARK, dash_ratio=0.4)
        # Anneau 1
        self.ring1_id = self.canvas.create_oval(
            CX - R - 18, CY - R - 18,
            CX + R + 18, CY + R + 18,
            outline=GOLD, width=1
        )
        # Gemmes sur l'anneau 1 (✦)
        self.gem1 = self.canvas.create_text(0, 0, text="✦", fill=GOLD,
                                            font=("Arial", 8))
        self.gem2 = self.canvas.create_text(0, 0, text="✦", fill=GOLD,
                                            font=("Arial", 8))

        # Corps du bouton (cercle rempli)
        self.btn_body = self._create_gradient_circle(CX, CY, R)

        # Reflet interne
        self.btn_shine = self.canvas.create_oval(
            CX - R * 0.55, CY - R * 0.65,
            CX + R * 0.1,  CY + R * 0.05,
            fill="#ffffff", outline="", stipple="gray25"
        )

        # Icône appareil photo
        self._draw_camera(CX, CY - 8)

        # Texte "Capture"
        self.canvas.create_text(CX, CY + R * 0.55,
                                text="C A P T U R E",
                                font=("Georgia", 7, "italic"),
                                fill=GOLD_DARK)

        # Couronne (sera repositionnée chaque frame)
        self.crown_id = self.canvas.create_text(
            CX, CY - R - 52,
            text="👑",
            font=("Arial", 26),
        )

        # Compteur photo
        self.counter_id = self.canvas.create_text(
            W - 20, 20,
            text="📸 0",
            font=("Georgia", 10),
            fill=GOLD_DARK,
            anchor="ne"
        )

    def _create_gradient_circle(self, cx, cy, r):
        """Cercle avec gradient simulé par couches."""
        ids = []
        steps = 20
        for i in range(steps, -1, -1):
            t = i / steps
            ri = int(r * t)
            # couleur du centre vers bord
            if t < 0.3:
                col = lerp_color("#3a1a2e", "#1a0018", t / 0.3)
            else:
                col = lerp_color("#1a0018", "#0a0008", (t - 0.3) / 0.7)
            ids.append(self.canvas.create_oval(
                cx - ri, cy - ri, cx + ri, cy + ri,
                fill=col, outline=""
            ))
        # Bord doré
        self.btn_border = self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="", outline=GOLD, width=2
        )
        return ids

    def _create_dashed_circle(self, cx, cy, r, segments, color, dash_ratio=0.5):
        items = []
        for i in range(segments):
            a1 = 2 * math.pi * i / segments
            a2 = 2 * math.pi * (i + dash_ratio) / segments
            steps = 6
            coords = []
            for j in range(steps + 1):
                a = a1 + (a2 - a1) * j / steps
                coords += [cx + r * math.cos(a), cy + r * math.sin(a)]
            if len(coords) >= 4:
                items.append(self.canvas.create_line(*coords,
                                                     fill=color, width=1))
        return items

    def _draw_camera(self, cx, cy):
        s = 1.0  # scale
        # Corps
        bw, bh = int(40 * s), int(30 * s)
        br = 6
        self.canvas.create_arc(cx - bw//2, cy - bh//2,
                               cx - bw//2 + br*2, cy - bh//2 + br*2,
                               start=90, extent=90, style="chord",
                               fill=GOLD, outline=GOLD)
        self.canvas.create_arc(cx + bw//2 - br*2, cy - bh//2,
                               cx + bw//2, cy - bh//2 + br*2,
                               start=0, extent=90, style="chord",
                               fill=GOLD, outline=GOLD)
        self.canvas.create_rectangle(cx - bw//2, cy - bh//2 + br,
                                     cx + bw//2, cy + bh//2,
                                     fill=GOLD, outline=GOLD)
        self.canvas.create_rectangle(cx - bw//2 + br, cy - bh//2,
                                     cx + bw//2 - br, cy + bh//2,
                                     fill=GOLD, outline=GOLD)
        # Bosse objectif (haut)
        bumpw = int(14 * s)
        self.canvas.create_rectangle(cx - bumpw//2, cy - bh//2 - int(8*s),
                                     cx + bumpw//2, cy - bh//2,
                                     fill=GOLD, outline=GOLD)
        # Objectif (cercle extérieur)
        lr = int(13 * s)
        self.canvas.create_oval(cx - lr, cy - lr//2 + 2,
                                cx + lr, cy + lr - lr//2 + 2,
                                fill=BTN_BG, outline=GOLD, width=2)
        # Objectif (cercle intérieur)
        lr2 = int(8 * s)
        self.canvas.create_oval(cx - lr2, cy - lr2//2 + 2,
                                cx + lr2, cy + lr2 - lr2//2 + 2,
                                fill="#1a1030", outline=GOLD_DARK, width=1)
        # Flash dot
        self.canvas.create_oval(cx + bw//2 - 8, cy - bh//2 + 2,
                                cx + bw//2 - 2, cy - bh//2 + 8,
                                fill=GOLD_LIGHT, outline="")

    # ── Événements ───────────────────────────────────────────────────────────
    def _bind_events(self):
        self.canvas.bind("<Motion>",     self._on_mouse_move)
        self.canvas.bind("<Button-1>",   self._on_click)
        self.canvas.bind("<Leave>",      lambda e: self._set_hover(False))

    def _on_mouse_move(self, event):
        dist = math.hypot(event.x - CX, event.y - CY)
        self._set_hover(dist <= R + 5)

    def _set_hover(self, val):
        if val != self.hovered:
            self.hovered = val
            self.btn_scale_target = 1.08 if val else 1.0
            self.root.config(cursor="hand2" if val else "")

    def _on_click(self, event):
        dist = math.hypot(event.x - CX, event.y - CY)
        if dist > R + 5:
            return
        self.photo_count += 1
        self.canvas.itemconfig(self.counter_id,
                               text=f"📸 {self.photo_count}")
        # Flash
        self._trigger_flash()
        # Explosion de particules
        self._spawn_particles(CX, CY, 24)

    def _trigger_flash(self):
        self.flash_alpha = 1.0
        self.canvas.itemconfig(self.flash_rect, state="normal")

    def _spawn_particles(self, cx, cy, count):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.5, 6.5)
            colors = [GOLD, GOLD_LIGHT, WHITE_WARM, ROSE, "#ffffff"]
            size = random.uniform(2, 6)
            self.particles.append({
                "x": cx, "y": cy,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": 1.0,
                "decay": random.uniform(0.025, 0.06),
                "color": random.choice(colors),
                "size": size,
                "id": None,
                "shape": random.choice(["circle", "diamond"]),
            })

    # ── Boucle d'animation ───────────────────────────────────────────────────
    def _tick(self):
        now = time.time()

        # Rotation anneaux
        self.angle_ring1 += 0.6
        self.angle_ring2 -= 0.3

        # Flottement couronne
        self.crown_offset = math.sin(now * 1.8) * 7
        self.canvas.coords(self.crown_id, CX, CY - R - 52 + self.crown_offset)

        # Scale smooth du bouton
        diff = self.btn_scale_target - self.btn_scale
        self.btn_scale += diff * 0.12
        self._update_button_scale()

        # Gems sur l'anneau 1
        ring1_r = R + 18
        a1 = math.radians(self.angle_ring1)
        a2 = math.radians(self.angle_ring1 + 180)
        self.canvas.coords(self.gem1,
                           CX + ring1_r * math.cos(a1),
                           CY + ring1_r * math.sin(a1))
        self.canvas.coords(self.gem2,
                           CX + ring1_r * math.cos(a2),
                           CY + ring1_r * math.sin(a2))

        # Rotation anneau 2 (tirets) – déplacer par rotation
        ring2_r = R + 32
        offset2 = math.radians(self.angle_ring2)
        for i, item in enumerate(self.ring2_items):
            try:
                self.canvas.itemconfig(item, fill=GOLD_DARK)
            except Exception:
                pass

        # Paillettes ambiantes
        if random.random() < 0.25:
            self._spawn_sparkle()
        self._update_sparkles()

        # Particules
        self._update_particles()

        # Flash fade
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 0.08)
            if self.flash_alpha <= 0:
                self.canvas.itemconfig(self.flash_rect, state="hidden")
            else:
                # simuler transparence via grisé
                v = int(255 * self.flash_alpha)
                col = f"#{v:02x}{min(v, 248):02x}{min(v, 230):02x}"
                self.canvas.itemconfig(self.flash_rect, fill=col)

        self.root.after(16, self._tick)   # ~60 fps

    def _update_button_scale(self):
        sc = self.btn_scale
        try:
            self.canvas.coords(self.btn_border,
                               CX - R * sc, CY - R * sc,
                               CX + R * sc, CY + R * sc)
            col = lerp_color(GOLD, GOLD_LIGHT, (sc - 1.0) / 0.08) if sc > 1.0 else GOLD
            self.canvas.itemconfig(self.btn_border, outline=col,
                                   width=2 if sc <= 1.0 else 3)
        except Exception:
            pass

    def _spawn_sparkle(self):
        x = random.randint(30, W - 30)
        y = random.randint(H // 3, H - 40)
        size = random.uniform(1, 3)
        self.sparkles.append({
            "x": x, "y": y,
            "vy": -random.uniform(0.4, 1.2),
            "life": 1.0,
            "decay": random.uniform(0.018, 0.04),
            "size": size,
            "id": self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=GOLD_LIGHT, outline=""
            )
        })

    def _update_sparkles(self):
        alive = []
        for sp in self.sparkles:
            sp["y"] += sp["vy"]
            sp["life"] -= sp["decay"]
            if sp["life"] <= 0:
                self.canvas.delete(sp["id"])
            else:
                size = sp["size"] * sp["life"]
                self.canvas.coords(sp["id"],
                                   sp["x"] - size, sp["y"] - size,
                                   sp["x"] + size, sp["y"] + size)
                alive.append(sp)
        self.sparkles = alive

    def _update_particles(self):
        alive = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15   # gravité légère
            p["life"] -= p["decay"]
            if p["id"] is not None:
                self.canvas.delete(p["id"])
            if p["life"] <= 0:
                continue
            size = p["size"] * p["life"]
            if p["shape"] == "circle":
                p["id"] = self.canvas.create_oval(
                    p["x"] - size, p["y"] - size,
                    p["x"] + size, p["y"] + size,
                    fill=p["color"], outline=""
                )
            else:
                s = size
                p["id"] = self.canvas.create_polygon(
                    p["x"],     p["y"] - s,
                    p["x"] + s, p["y"],
                    p["x"],     p["y"] + s,
                    p["x"] - s, p["y"],
                    fill=p["color"], outline=""
                )
            alive.append(p)
        self.particles = alive


# ── Point d'entrée ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoboothApp(root)
    root.mainloop()
