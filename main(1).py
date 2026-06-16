import pygame
import sys
import math
import random
import textwrap
pygame.init()
W, H = 1100, 780
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Blood Scion: Sloan's life")
clock = pygame.time.Clock()
DARK_BG      = (60, 12, 10)
PANEL_BG     = (50, 20, 16)
PANEL_BORDER = (105, 45, 25)
TILE_A       = (50, 26, 18)
TILE_B       = (60, 34, 22)
LADDER_TILE  = (40, 55, 38)
SNAKE_TILE   = (80, 20, 15)
LADDER_COL   = (60, 180, 100)
SNAKE_COL    = (250, 70, 40)
GOLD         = (250, 160, 50)
GOLD_LIGHT   = (250, 200, 100)
CREAM        = (254, 220, 195)
MUTED        = (160, 115, 90)
WHITE        = (255, 255, 255)
P1_COL       = (216, 90, 48)   
P2_COL       = (29, 158, 117)  
GLOW_FIRE    = (255, 120, 30, 60)
GLOW_TEAL    = (40, 200, 140, 60)
def try_font(names, size, bold=False):
    for name in names:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except:
            pass
    return pygame.font.SysFont("serif", size, bold=bold)
font_title  = try_font(["Georgia", "Times New Roman", "serif"], 32, bold=True)
font_big    = try_font(["Georgia", "Times New Roman", "serif"], 22, bold=True)
font_med    = try_font(["Georgia", "Times New Roman", "serif"], 16)
font_small  = try_font(["Georgia", "Times New Roman", "serif"], 13)
font_tiny   = try_font(["Georgia", "Times New Roman", "serif"], 11)
font_num    = try_font(["Georgia", "Times New Roman", "serif"], 10)
font_die    = try_font(["Georgia", "Times New Roman", "serif"], 36, bold=True)
font_event_title = try_font(["Georgia", "Times New Roman", "serif"], 15, bold=True)
font_event_body  = try_font(["Georgia", "Times New Roman", "serif"], 13)
BOARD_X, BOARD_Y = 30, 60
BOARD_SIZE       = 640
TILE_S           = BOARD_SIZE // 10   
EVENTS = EVENTS = {
    4:  {"type":"ladder","to":4,"title":"Looking for Mama",
         "body":"Sloan goes through the graveyard in search for her Mama, who disapeared when she was young.","move":"+0"},
    9:  {"type":"snake", "to":5, "title":"The Nightwalker's Warning",
         "body":"Sloan gets captured by a Nightwalker, and uses her Ase to protect herself. As he burns, the Nightwalker warns her: 'You're a Scion. You'll die for this.' Sloane's secret is no longer safe — she must flee before the Lucis come for her.","move":"-4"},
    17: {"type":"ladder","to":22,"title":"Baba's Protection",
         "body":"Sloane reaches home and Baba is there to help her. He helps her recover and brews her tea to keep her safe. The tea helps her hide her true identity and survive.","move":"+5"},
    19: {"type":"snake", "to":14, "title":"Nicolai is Dead",
         "body":"Baba tells Sloane that Nicolai, her friend has been executed by the Lucis. He was drafted to the army, and hoped to escape.","move":"-5"},
     20: {"type":"snake", "to":11, "title":"Drafted on Her Birthday",
         "body":"On her fifteenth birthday, the Lucis hand over her draft letter. She is forced to join their army of child soldiers. Her and Teo's relationship is destroyed.","move":"-9"},
    28: {"type":"ladder","to":37,"title":"A Plan Takes Shape",
         "body":"Sloane boards the airship to Fort Regulus. She will not just fight to survive — she will infiltrate the Lucis and destroy them from inside. Her mission begins now. Sloan's goal is to find out what happened to Mama.","move":"+9 "},
    35: {"type":"snake", "to":25,"title":"Teo is a Scion",
         "body":"The Lucis find Teo escaping. She must execute him to prove loyalty to the force. She discovers that he is a Yoruba too.","move":"-10"},
    40: {"type":"ladder","to":42,"title":"Malachi Knows",
         "body":"Malachi confronts Sloane on the airship. He knows she is a Scion. Her fire killed his parents. But instead of reporting her, he decides to take revenge. She survives another day.","move":"+2"},
    47: {"type":"snake", "to":34,"title":"Strangled at the Barracks",
         "body":"Malachi grabs Sloane by the throat, screaming at her to say his parents' names. He reaches for his knife. Only Faas's return saves her life. She cannot sleep that night, thinking of Baba and Luna.","move":"-13"},
    51: {"type":"snake", "to":36,"title":"Fight to the death at Fort Regulus",
         "body":"The recruits must find their weakest link and kill them. Faas greets the recruits and congratulates them on their kills. Queen Olympia addresses the child soldiers. Sloane realises the full horror of what she has entered.","move":"-15"},
    53: {"type":"ladder","to":62,"title":"Dane's Jacket",
         "body":"Punished with weapons cleaning during mess — no food — Sloane finds Dane has accidentally left part of his uniform. She slips it on and sneaks toward the forbidden Archives Hall. She moves one step closer to finding the truth","move":"+9"},

    57: {"type":"ladder","to":70,"title":"Izara's Secret",
         "body":"Izara confesses to Sloane: her twin sister is also a Scion. A bond of trust forms between them. For the first time at Fort Regulus, Sloane is not completely alone.","move":"+13"},
    58: {"type":"ladder","to":70,"title":"Sloane Saves Izara",
         "body":"Sloane hears screams from the bathhouse. A guard has cornered Izara. Sloane unleashes her àse and turns the guard to dust and ash. Izara now knows Sloane's secret — but chooses silence.","move":"+12"},
    60: {"type":"snake", "to":45,"title":"Her punishment Her",
         "body":" Sloan protects her own people, but gets discovered in the process. Faas plans to execute her, but Dane protects her and sentences her to a beating and no food.   ","move":"-15"},
    62: {"type":"snake", "to":48,"title":"Phase One: The Trail",
         "body":"Sloane must survive the deadly fitness trial in the Irunmole forest — kill or be killed. She's becoming the monster she hates the most.","move":"-3"},
    67: {"type":"snake", "to":54,"title":"The Forest's Illusions",
         "body":"The trial forest twists Sloane's mind — she sees her mother calling her into a river. She almost follows. Before she can reach her, the vision shatters. The forest wants her dead.","move":"-12"},
    68: {"type":"ladder","to":79,"title":"Malachi Falls",
         "body":"Malachi finds Sloane in the forest and attacks. Sloane drives her knife into his neck. Sloan has killed Malachi","move":"-25"},
    72: {"type":"ladder","to":88,"title":"Dane's True Identity",
         "body":"On the cliffs, Dane reveals the truth: he is Omari Wells, a member of the Blades — the Scion rebel group. He promises Sloane a path to meet the resistance.","move":"+20"},
    75: {"type":"snake", "to":61,"title":"Izara Is Dying",
         "body":"Back at the barracks after Phase One, Izara drops a devastating truth: she has an incurable blood disease. She survived the trail — but she is running out of time.","move":"-14"},
    80: {"type":"ladder","to":90,"title":"Caspian Is a Blade",
         "body":"Omari reveals that Lieutenant Caspian is second-in-command of the Blades. Sloane is shocked and unable to know who to trust. In the end, she promises to help Caspian reach Ile-Orisha and find the Shadow Rebels.","move":"+10"},
    83: {"type":"snake", "to":69,"title":"Kill Amiyah",
         "body":"Faas gives Sloane and Amiyah each two bullets and forces them to fight to the death. Amiyah tells Sloane they have no choice. Sloane wins — and weeps over Amiyah's body.","move":"-20"},
    89: {"type":"snake", "to":65,"title":"Kill The Royal bloodlines",
         "body":"Sloan goes to visit Royal bloodlines, with plans to kill them all.","move":"+2"},
    95: {"type":"snake", "to":65,"title":"The royal bloodlines are dead",
         "body":"Sloan kills all of them, and reunites with Dane.","move":"+2"},
}
PLAYERS = [
    {"name":"Player 1",  "col":P1_COL, "glow":GLOW_FIRE, "pos":1, "symbol":"🔥"},
    {"name":"Player 2",  "col":P2_COL, "glow":GLOW_TEAL,  "pos":1, "symbol":"🌿"},
]
def sq_to_xy(sq):
    """Return pixel centre of a board square (1-100)."""
    idx  = sq - 1
    row  = idx // 10
    col  = idx % 10
    if row % 2 == 0:
        actual_col = col
    else:
        actual_col = 9 - col
    display_row = 9 - row
    cx = BOARD_X + actual_col * TILE_S + TILE_S // 2
    cy = BOARD_Y + display_row * TILE_S + TILE_S // 2
    return cx, cy
def sq_num_at(display_row, display_col):
    """Board square number at a given display grid position."""
    data_row = 9 - display_row
    if data_row % 2 == 0:
        col = display_col
    else:
        col = 9 - display_col
    return data_row * 10 + col + 1
def draw_text_wrapped(surface, text, font, colour, rect, line_spacing=4):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= rect.width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break
        surf = font.render(line, True, colour)
        surface.blit(surf, (rect.left, y))
        y += font.get_height() + line_spacing
def draw_glow_circle(surface, centre, radius, colour_rgba, steps=4):
    glow_surf = pygame.Surface((radius*2+20, radius*2+20), pygame.SRCALPHA)
    for i in range(steps, 0, -1):
        r = radius + i * 4
        alpha = colour_rgba[3] // steps * i
        pygame.draw.circle(glow_surf, (*colour_rgba[:3], alpha),
                           (radius+10, radius+10), r)
    surface.blit(glow_surf, (centre[0]-radius-10, centre[1]-radius-10))
def draw_rounded_rect(surface, rect, colour, radius=8, border=0, border_colour=None):
    pygame.draw.rect(surface, colour, rect, border_radius=radius)
    if border and border_colour:
        pygame.draw.rect(surface, border_colour, rect, border, border_radius=radius)
def lerp(a, b, t):
    return a + (b - a) * t
class Particle:
    def __init__(self, x, y, colour):
        self.x  = x + random.randint(-8, 8)
        self.y  = y + random.randint(-8, 8)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-3, -0.5)
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.r = random.randint(2, 5)
        self.col = colour
    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.05
        self.life -= 1
    def draw(self, surface):
        alpha = int(255 * self.life / self.max_life)
        s = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.col, alpha), (self.r, self.r), self.r)
        surface.blit(s, (int(self.x)-self.r, int(self.y)-self.r))
particles = []
def burst(x, y, colour, n=20):
    for _ in range(n):
        particles.append(Particle(x, y, colour))
anim = {
    "active": False,
    "player": 0,
    "steps":  [],
    "step_idx": 0,
    "timer":  0,
    "step_delay": 10,  
    "phase":  "move",  
    "slide_from": 0,
    "slide_to":   0,
    "slide_progress": 0.0,
}

state = {
    "turn":        0,
    "last_roll":   0,
    "event":       {"title":"Roll","body":"This game is about sloans life.","move":""},
    "winner":      None,
    "showing_event": False,
    "event_timer": 0,
}
STARS = [(random.randint(0, W), random.randint(0, H), random.random()) for _ in range(120)]
def draw_orisha_mark(surface, sq, cx, cy):
    ev = EVENTS.get(sq)
    if not ev:
        return
    s = TILE_S // 2 - 4
    if ev["type"] == "ladder":
        pts = [(cx, cy-s), (cx-6, cy+4), (cx-2, cy+2), (cx-2, cy+s),
               (cx+2, cy+s), (cx+2, cy+2), (cx+6, cy+4)]
        pygame.draw.polygon(surface, (*LADDER_COL, 180), pts)
    else:
        pts = [(cx, cy+s), (cx-6, cy-4), (cx-2, cy-2), (cx-2, cy-s),
               (cx+2, cy-s), (cx+2, cy-2), (cx+6, cy-4)]
        pygame.draw.polygon(surface, (*SNAKE_COL, 180), pts)
def draw_connections():
    for sq, ev in EVENTS.items():
        fx, fy = sq_to_xy(sq)
        tx, ty = sq_to_xy(ev["to"])
        col    = LADDER_COL if ev["type"] == "ladder" else SNAKE_COL
        dx, dy = tx - fx, ty - fy
        length = math.hypot(dx, dy)
        if length == 0:
            continue
        nx, ny = dx/length, dy/length
        dash, gap = 8, 5
        pos = 0
        drawing = True
        while pos < length:
            seg = dash if drawing else gap
            end = min(pos + seg, length)
            if drawing:
                sx1, sy1 = fx + nx*pos,  fy + ny*pos
                sx2, sy2 = fx + nx*end,  fy + ny*end
                pygame.draw.line(screen, (*col, 140), (int(sx1), int(sy1)),
                                 (int(sx2), int(sy2)), 2)
            pos += seg
            drawing = not drawing
        angle = math.atan2(ty-fy, tx-fx)
        al = 10
        ax1 = tx - al * math.cos(angle - 0.4)
        ay1 = ty - al * math.sin(angle - 0.4)
        ax2 = tx - al * math.cos(angle + 0.4)
        ay2 = ty - al * math.sin(angle + 0.4)
        pygame.draw.polygon(screen, col, [(tx,ty),(int(ax1),int(ay1)),(int(ax2),int(ay2))])
def draw_board():
    glow = pygame.Surface((BOARD_SIZE+30, BOARD_SIZE+30), pygame.SRCALPHA)
    pygame.draw.rect(glow, (180, 100, 30, 40), (0, 0, BOARD_SIZE+30, BOARD_SIZE+30), border_radius=12)
    screen.blit(glow, (BOARD_X-15, BOARD_Y-15))
    pygame.draw.rect(screen, PANEL_BORDER, (BOARD_X-2, BOARD_Y-2, BOARD_SIZE+4, BOARD_SIZE+4), 2, border_radius=4)
    for dr in range(10):
        for dc in range(10):
            sq  = sq_num_at(dr, dc)
            x   = BOARD_X + dc * TILE_S
            y   = BOARD_Y + dr * TILE_S
            ev  = EVENTS.get(sq)
            if ev:
                base = LADDER_TILE if ev["type"]=="ladder" else SNAKE_TILE
            else:
                base = TILE_A if (dr + dc) % 2 == 0 else TILE_B
            pygame.draw.rect(screen, base, (x, y, TILE_S, TILE_S))
            pygame.draw.rect(screen, (60, 40, 25), (x, y, TILE_S, TILE_S), 1)
            num_s = font_num.render(str(sq), True, MUTED)
            screen.blit(num_s, (x+3, y+3))
            if ev:
                cx, cy = x + TILE_S//2, y + TILE_S//2
                draw_orisha_mark(screen, sq, cx, cy)
    fx, fy = sq_to_xy(100)
    draw_glow_circle(screen, (fx, fy), 24, (210, 160, 50, 80))
    star = font_big.render("★", True, GOLD)
    screen.blit(star, star.get_rect(center=(fx, fy)))
def draw_players():
    for i, p in enumerate(PLAYERS):
        cx, cy = sq_to_xy(p["pos"])
        offset = -11 if i == 0 else 11
        cx += offset
        draw_glow_circle(screen, (cx, cy), 14, (*p["col"], 80))
        pygame.draw.circle(screen, p["col"], (cx, cy), 13)
        pygame.draw.circle(screen, WHITE,    (cx, cy), 13, 2)
        init = font_small.render(p["name"][0], True, WHITE)
        screen.blit(init, init.get_rect(center=(cx, cy)))
def draw_slide_piece():
    if not anim["active"] or anim["phase"] != "slide":
        return
    t   = anim["slide_progress"]
    t   = t * t * (3 - 2 * t) 
    fx, fy = sq_to_xy(anim["slide_from"])
    tx, ty = sq_to_xy(anim["slide_to"])
    cx  = int(lerp(fx, tx, t))
    cy  = int(lerp(fy, ty, t))
    pi  = anim["player"]
    p   = PLAYERS[pi]
    offset = -11 if pi == 0 else 11
    cx += offset
    draw_glow_circle(screen, (cx, cy), 18, (*p["col"], 120))
    pygame.draw.circle(screen, p["col"], (cx, cy), 14)
    pygame.draw.circle(screen, WHITE,    (cx, cy), 14, 2)
    init = font_small.render(p["name"][0], True, WHITE)
    screen.blit(init, init.get_rect(center=(cx, cy)))
PNL_X = BOARD_X + BOARD_SIZE + 20
PNL_W = W - PNL_X - 15
PNL_Y = BOARD_Y
def draw_panel():
    t = font_title.render("Blood Scion", True, GOLD)
    screen.blit(t, t.get_rect(centerx=PNL_X + PNL_W//2, y=8))
    sub = font_small.render("Sloans adventure", True, MUTED)
    screen.blit(sub, sub.get_rect(centerx=PNL_X + PNL_W//2, y=42))
    y = PNL_Y
    for i, p in enumerate(PLAYERS):
        card_h = 64
        rect   = pygame.Rect(PNL_X, y, PNL_W, card_h)
        is_turn = state["turn"] == i and not state["winner"]
        bg     = (45, 30, 18) if is_turn else PANEL_BG
        bdr    = p["col"] if is_turn else PANEL_BORDER
        draw_rounded_rect(screen, rect, bg, 8, 2, bdr)
        if is_turn:
            g = pygame.Surface((PNL_W+10, card_h+10), pygame.SRCALPHA)
            pygame.draw.rect(g, (*p["col"], 25), (0,0,PNL_W+10,card_h+10), border_radius=10)
            screen.blit(g, (PNL_X-5, y-5))
        pygame.draw.circle(screen, p["col"], (PNL_X+22, y+card_h//2), 10)
        pygame.draw.circle(screen, WHITE,    (PNL_X+22, y+card_h//2), 10, 2)
        name_s  = font_big.render(p["name"], True, WHITE if is_turn else CREAM)
        screen.blit(name_s, (PNL_X+40, y+8))
        pos_label = font_small.render("Square", True, MUTED)
        pos_val   = font_big.render(str(p["pos"]), True, p["col"])
        screen.blit(pos_label, (PNL_X+40, y+34))
        screen.blit(pos_val,   (PNL_X+90, y+30))

        y += card_h + 8
    y += 6
    dice_rect = pygame.Rect(PNL_X, y, PNL_W, 68)
    draw_rounded_rect(screen, dice_rect, PANEL_BG, 8, 1, PANEL_BORDER)
    if state["last_roll"]:
        d_label = font_small.render("Rolled", True, MUTED)
        screen.blit(d_label, (PNL_X+12, y+8))
        d_val   = font_die.render(str(state["last_roll"]), True, GOLD_LIGHT)
        screen.blit(d_val, (PNL_X+70, y+12))
        pips = ["", "⚀","⚁","⚂","⚃","⚄","⚅"]
        pip_s = pygame.font.SysFont("segoe ui emoji", 36).render(pips[state["last_roll"]], True, GOLD)
        screen.blit(pip_s, (PNL_X+PNL_W-54, y+14))
    else:
        ph = font_med.render("– no roll yet –", True, MUTED)
        screen.blit(ph, ph.get_rect(centerx=PNL_X+PNL_W//2, y=y+22))
    y += 76
    ev_rect = pygame.Rect(PNL_X, y, PNL_W, 200)
    draw_rounded_rect(screen, ev_rect, PANEL_BG, 8, 1, PANEL_BORDER)
    ev = state["event"]
    ev_type = ""
    for sq, data in EVENTS.items():
        if data["title"] == ev["title"]:
            ev_type = data["type"]
            break
    accent = LADDER_COL if ev_type == "ladder" else (SNAKE_COL if ev_type == "snake" else GOLD)
    pygame.draw.rect(screen, accent, (PNL_X, y, 4, 200), border_radius=8)
    title_s = font_event_title.render(ev["title"], True, accent if ev_type else GOLD)
    screen.blit(title_s, (PNL_X+14, y+10))
    if ev.get("move"):
        move_col = LADDER_COL if ev["move"].startswith("+") else SNAKE_COL
        move_s   = font_event_title.render(ev["move"] + " squares", True, move_col)
        screen.blit(move_s, (PNL_X+14, y+30))
        body_y = y + 52
    else:
        body_y = y + 30
    draw_text_wrapped(screen, ev["body"], font_event_body, CREAM,
                      pygame.Rect(PNL_X+14, body_y, PNL_W-28, 200 - (body_y - y) - 10))
    y += 208
    y += 6
    btn_rect = pygame.Rect(PNL_X, y, PNL_W, 52)
    can_roll = not anim["active"] and not state["winner"]
    btn_col  = (70, 45, 20) if can_roll else (38, 28, 18)
    btn_bdr  = GOLD if can_roll else PANEL_BORDER
    draw_rounded_rect(screen, btn_rect, btn_col, 10, 2, btn_bdr)
    if can_roll:
        g2 = pygame.Surface((PNL_W, 52), pygame.SRCALPHA)
        pygame.draw.rect(g2, (210,160,50,18), (0,0,PNL_W,52), border_radius=10)
        screen.blit(g2, (PNL_X, y))
    lbl = "Roll the Dice" if can_roll else ("Game Over" if state["winner"] else "Moving…")
    lbl_col = GOLD_LIGHT if can_roll else MUTED
    lbl_s   = font_big.render(lbl, True, lbl_col)
    screen.blit(lbl_s, lbl_s.get_rect(centerx=PNL_X+PNL_W//2, centery=y+26))
    y += 60
    if not state["winner"]:
        tl = font_med.render(PLAYERS[state["turn"]]["name"] + "'s turn", True, PLAYERS[state["turn"]]["col"])
        screen.blit(tl, tl.get_rect(centerx=PNL_X+PNL_W//2, y=y+4))
    y += 30
    y += 6
    for label, col in [("▲  Ladder — Sloane rises", LADDER_COL), ("▼  Snake — Sloane falls", SNAKE_COL)]:
        ls = font_small.render(label, True, col)
        screen.blit(ls, (PNL_X+10, y))
        y += 20
    if state["winner"]:
        y += 10
        w_rect = pygame.Rect(PNL_X, y, PNL_W, 56)
        draw_rounded_rect(screen, w_rect, (20, 60, 35), 10, 2, LADDER_COL)
        w_txt = font_big.render(state["winner"]["name"] + "Oof", True, LADDER_COL)
        screen.blit(w_txt, w_txt.get_rect(centerx=PNL_X+PNL_W//2, centery=y+28))
        r_txt = font_small.render("Press R to restart", True, MUTED)
        screen.blit(r_txt, r_txt.get_rect(centerx=PNL_X+PNL_W//2, y=y+60))
def draw_background():
    screen.fill(DARK_BG)
    t = pygame.time.get_ticks() / 1000
    for sx, sy, speed in STARS:
        alpha = int(128 + 80 * math.sin(t * speed * 2))
        s = pygame.Surface((2, 2), pygame.SRCALPHA)
        s.fill((235, 220, 180, alpha))
        screen.blit(s, (sx, sy))
def do_roll():
    if anim["active"] or state["winner"]:
        return
    roll = random.randint(1, 6)
    state["last_roll"] = roll
    pi   = state["turn"]
    p    = PLAYERS[pi]
    target = min(p["pos"] + roll, 100)
    steps  = list(range(p["pos"]+1, target+1))
    state["event"] = {"title": f"Rolled a {roll}!",
                      "body":  f"{p['name']} moves {roll} square{'s' if roll>1 else ''} forward…",
                      "move":  ""}
    anim.update({"active":True, "player":pi, "steps":steps,
                 "step_idx":0, "timer":0, "phase":"move",
                 "slide_from":p["pos"], "slide_to":target, "slide_progress":0.0})
def reset_game():
    for p in PLAYERS:
        p["pos"] = 1
    state.update({"turn":0,"last_roll":0,
                  "event":{"title":"Roll to begin","body":"Two Scions race to square 100. Sloane's choices will lift her higher — or drag her back.","move":""},
                  "winner":None,"showing_event":False,"event_timer":0})
    anim["active"] = False
    particles.clear()
def update_anim():
    if not anim["active"]:
        return
    pi = anim["player"]
    p  = PLAYERS[pi]
    if anim["phase"] == "move":
        anim["timer"] += 1
        if anim["timer"] >= anim["step_delay"]:
            anim["timer"] = 0
            if anim["step_idx"] < len(anim["steps"]):
                p["pos"] = anim["steps"][anim["step_idx"]]
                burst(*sq_to_xy(p["pos"]), p["col"], n=6)
                anim["step_idx"] += 1
            else:
                sq = p["pos"]
                if sq == 100:
                    state["winner"] = p
                    state["event"] = {"title": p["name"] + " wins!",
                                      "body":  "Sloan has been captured.!",
                                      "move":  ""}
                    burst(*sq_to_xy(100), GOLD_LIGHT, n=50)
                    anim["active"] = False
                    return
                ev = EVENTS.get(sq)
                if ev:
                    state["event"] = {"title": ev["title"],
                                      "body":  ev["body"],
                                      "move":  ev["move"]}
                    anim["phase"]       = "event_pause"
                    anim["timer"]       = 0
                    anim["slide_from"]  = sq
                    anim["slide_to"]    = ev["to"]
                    anim["slide_progress"] = 0.0
                    burst(*sq_to_xy(sq), LADDER_COL if ev["type"]=="ladder" else SNAKE_COL, n=25)
                else:
                    state["turn"] = (state["turn"] + 1) % 2
                    anim["active"] = False
    elif anim["phase"] == "event_pause":
        anim["timer"] += 1
        if anim["timer"] >= 90:  
            anim["phase"] = "slide"
            anim["slide_progress"] = 0.0
    elif anim["phase"] == "slide":
        anim["slide_progress"] += 0.02
        if anim["slide_progress"] >= 1.0:
            p["pos"] = anim["slide_to"]
            burst(*sq_to_xy(p["pos"]), p["col"], n=15)
            state["turn"] = (state["turn"] + 1) % 2
            anim["active"] = False
btn_rect_global = None
def main():
    global btn_rect_global
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    do_roll()
                elif event.key == pygame.K_r:
                    reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect_global and btn_rect_global.collidepoint(event.pos):
                    if state["winner"]:
                        reset_game()
                    else:
                        do_roll()

        update_anim()
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
        draw_background()
        draw_connections()
        draw_board()
        draw_players()
        if anim["active"] and anim["phase"] == "slide":
            draw_slide_piece()
        for p in particles:
            p.draw(screen)
        draw_panel()
        pi = state["turn"]
        p  = PLAYERS[pi]
        y_offset = PNL_Y
        for i in range(2):
            y_offset += 72
        y_offset += 82   
        y_offset += 214  
        y_offset += 6
        btn_rect_global = pygame.Rect(PNL_X, y_offset, PNL_W, 52)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()