import json
import subprocess
from pathlib import Path

CLI_PATH = r"C:\Program Files\ArtCraft\FigCraft\figcraft-cli.exe"
OUT_ROOT = Path(r"d:\APLIKASI\Project Ane\tuntungid")
OUT_FILE = OUT_ROOT / "tuntungid.figcraft"
DESIGN_DIR = OUT_ROOT / "design"
PREVIEW_DIR = DESIGN_DIR / "previews"
SPEC_JSON = DESIGN_DIR / "figcraft_spec.json"

DESIGN_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)


def rect(name, x, y, w, h, fill="#FFFFFF", radius=0, stroke=None, stroke_width=1):
    node = {
        "type": "rectangle",
        "name": name,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "fill": fill,
    }
    if radius > 0:
        node["cornerRadius"] = radius
    if stroke:
        node["stroke"] = stroke
        node["strokeWidth"] = stroke_width
    return node


def ellipse(name, x, y, w, h, fill="#187941", stroke=None, stroke_width=1):
    node = {
        "type": "ellipse",
        "name": name,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "fill": fill,
    }
    if stroke:
        node["stroke"] = stroke
        node["strokeWidth"] = stroke_width
    return node


def txt(name, x, y, w, h, content, size=14, weight="Regular", color="#0E3A2F", family="Plus Jakarta Sans"):
    return {
        "type": "text",
        "name": name,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "text": content,
        "fontSize": size,
        "fontFamily": family,
        "fontStyle": weight,
        "fill": color,
    }


def frame(name, x, y, w, h, fill="#FFFFFF", radius=0, stroke=None, stroke_width=1, children=None):
    node = {
        "type": "frame",
        "name": name,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "fill": fill,
        "children": children or [],
    }
    if radius > 0:
        node["cornerRadius"] = radius
    if stroke:
        node["stroke"] = stroke
        node["strokeWidth"] = stroke_width
    return node


def floating_tile(name, x, y, size, badge_text, bg="#FFFFFF", accent="#187941", text_color="#0E3A2F"):
    return frame(
        name,
        x,
        y,
        size,
        size,
        fill=bg,
        radius=16,
        stroke="#DCE8E2",
        stroke_width=1,
        children=[
            rect(f"{name}_shadow_hint", 4, size - 6, size - 8, 4, fill="#E3EFE9", radius=2),
            rect(f"{name}_inner", 12, 12, size - 24, size - 24, fill=accent, radius=10),
            txt(f"{name}_lbl", 14, int(size / 2) - 10, size - 28, 22, badge_text, size=12, weight="Bold", color=text_color),
        ],
    )


def build_landing_desktop():
    children = []

    # Top Navigation (ChronoTask style, clean links, specific CTAs per R-15)
    children.extend([
        rect("Navbar_Bg", 0, 0, 1440, 80, fill="#FFFFFF"),
        ellipse("Logo_Dot_TL", 56, 26, 12, 12, fill="#187941"),
        ellipse("Logo_Dot_TR", 72, 26, 12, 12, fill="#0E3A2F"),
        ellipse("Logo_Dot_BL", 56, 42, 12, 12, fill="#0E3A2F"),
        ellipse("Logo_Dot_BR", 72, 42, 12, 12, fill="#F4B41A"),
        txt("Brand_Name", 96, 26, 160, 28, "Tuntung.id", size=20, weight="Bold", color="#0E3A2F"),
        txt("Nav_Solusi", 500, 30, 80, 22, "Layanan", size=14, weight="Medium", color="#355E52"),
        txt("Nav_Duo", 600, 30, 115, 22, "The Power Duo", size=14, weight="Medium", color="#355E52"),
        txt("Nav_Metode", 735, 30, 115, 22, "5 Tahap Kerja", size=14, weight="Medium", color="#355E52"),
        txt("Nav_Paket", 870, 30, 120, 22, "Brief & 5 T&C", size=14, weight="Medium", color="#355E52"),
        txt("Nav_SignIn", 1110, 30, 130, 22, "Buka Workspace", size=14, weight="SemiBold", color="#0E3A2F"),
        rect("Nav_CTA_Box", 1252, 20, 144, 40, fill="#FFFFFF", radius=20, stroke="#C7DDD3", stroke_width=1),
        txt("Nav_CTA_Txt", 1272, 31, 110, 20, "Audit 30 Menit", size=13, weight="SemiBold", color="#0E3A2F"),
    ])

    # =========================================================================
    # SECTION 1: HERO CONTAINER (ChronoTask Centered Hero + 4 Corner Widgets)
    # =========================================================================
    hero_children = [
        rect("Hero_Grid_Line_H1", 40, 140, 1280, 1, fill="#E7F1EC"),
        rect("Hero_Grid_Line_H2", 40, 520, 1280, 1, fill="#E7F1EC"),
        # Center Floating App Icon Tile (84x84)
        frame(
            "Center_Brand_Tile",
            638,
            150,
            84,
            84,
            fill="#FFFFFF",
            radius=22,
            stroke="#DAE8E1",
            stroke_width=1,
            children=[
                ellipse("Tile_Dot_1", 20, 20, 18, 18, fill="#22A45D"),
                ellipse("Tile_Dot_2", 46, 20, 18, 18, fill="#0E3A2F"),
                ellipse("Tile_Dot_3", 20, 46, 18, 18, fill="#0E3A2F"),
                ellipse("Tile_Dot_4", 46, 46, 18, 18, fill="#F4B41A"),
            ],
        ),
        # Main 2-line Headline (<= 2 lines per R-06 / lint rules)
        txt(
            "Hero_H1_Line1",
            330,
            254,
            720,
            58,
            "Rancang, bangun, dan pantau",
            size=44,
            weight="Bold",
            color="#0E3A2F",
        ),
        txt(
            "Hero_H1_Line2",
            355,
            312,
            680,
            58,
            "aplikasi bisnis di satu tempat",
            size=44,
            weight="Bold",
            color="#8AA399",
        ),
        txt(
            "Hero_Subtitle",
            270,
            386,
            820,
            28,
            "Mitra 2 programmer (The Power Duo) untuk membangun aplikasi web kustom, micro-app, dan otomasi bisnis.",
            size=14,
            weight="Regular",
            color="#355E52",
        ),
        # Center Primary CTA Button (Specific label per R-15)
        rect("Hero_Primary_CTA", 538, 456, 284, 52, fill="#187941", radius=14),
        txt(
            "Hero_Primary_CTA_Txt",
            562,
            473,
            240,
            22,
            "Jadwalkan Audit Gratis 30 Menit",
            size=14,
            weight="Bold",
            color="#FFFFFF",
        ),
        # TOP-LEFT WIDGET: Yellow Sticky Note + Checkmark Tile
        frame(
            "Hero_Sticky_Note",
            44,
            42,
            244,
            210,
            fill="#FFF29C",
            radius=12,
            stroke="#E8D876",
            stroke_width=1,
            children=[
                ellipse("Sticky_Pin", 114, 10, 14, 14, fill="#D93829"),
                txt(
                    "Sticky_Copy",
                    20,
                    36,
                    204,
                    114,
                    "Ceritakan alur kerja yang masih manual. Kami rancang UI/UX, bangun aplikasi web, dan integrasikan sistemnya hingga tuntas.",
                    size=12,
                    weight="Medium",
                    color="#2D3A24",
                ),
                txt("Sticky_Tag", 20, 162, 200, 20, "Gawi Manuntung, Supaya Untung", size=11, weight="Bold", color="#5C6B32"),
            ],
        ),
        floating_tile("Hero_Check_Tile", 92, 206, 74, "Tuntas", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
        # TOP-RIGHT WIDGET: Free 30-Min Audit Card + Clock Tile
        frame(
            "Hero_Reminders_Card",
            1040,
            46,
            284,
            234,
            fill="#FFFFFF",
            radius=20,
            stroke="#DCE8E2",
            stroke_width=1,
            children=[
                txt("Rem_Title", 20, 18, 220, 24, "Sesi Audit & Konsultasi", size=15, weight="Bold", color="#0E3A2F"),
                txt("Rem_Sub", 20, 42, 240, 18, "Tahap 1 Metode Kerja (Gratis)", size=12, weight="Regular", color="#587A6E"),
                rect("Rem_Inner", 16, 70, 252, 144, fill="#F5FAF7", radius=14, stroke="#E1EDE7", stroke_width=1),
                txt("Rem_Item_Title", 28, 84, 224, 20, "Bedah Masalah & Roadmap App", size=13, weight="Bold", color="#0E3A2F"),
                txt("Rem_Item_Desc", 28, 106, 224, 20, "Langsung bersama The Power Duo", size=12, weight="Regular", color="#355E52"),
                rect("Rem_Time_Pill", 28, 138, 164, 28, fill="#E3F5EC", radius=8),
                txt("Rem_Time_Txt", 40, 145, 144, 18, "Sesi 30 Menit Terfokus", size=11, weight="Bold", color="#187941"),
                txt("Rem_Platform", 28, 178, 220, 18, "Output: 6 Poin Client Brief", size=11, weight="Medium", color="#587A6E"),
            ],
        ),
        floating_tile("Hero_Clock_Tile", 992, 92, 68, "30m", bg="#FFFFFF", accent="#0E3A2F", text_color="#F4B41A"),
        # BOTTOM-LEFT WIDGET: Honest Domain Solutions & 5-Stage Progress (No fake client names per R-17)
        frame(
            "Hero_Tasks_Card",
            44,
            404,
            336,
            208,
            fill="#FFFFFF",
            radius=20,
            stroke="#DCE8E2",
            stroke_width=1,
            children=[
                txt("Tasks_Header", 22, 18, 280, 24, "Solusi Aplikasi yang Kami Bangun", size=15, weight="Bold", color="#0E3A2F"),
                # Row 1
                rect("Task1_Badge", 22, 56, 22, 22, fill="#F4B41A", radius=6),
                txt("Task1_Num", 28, 59, 14, 16, "1", size=11, weight="Bold", color="#0E3A2F"),
                txt("Task1_Name", 52, 57, 260, 20, "Aplikasi Kasir, Stok & Gudang UMKM", size=12, weight="SemiBold", color="#0E3A2F"),
                txt("Task1_Date", 22, 86, 110, 16, "Tahap 1 s/d 5", size=11, weight="Regular", color="#587A6E"),
                rect("Task1_Bar_Bg", 132, 90, 130, 8, fill="#E6F0EC", radius=4),
                rect("Task1_Bar_Fg", 132, 90, 104, 8, fill="#187941", radius=4),
                txt("Task1_Pct", 272, 85, 50, 16, "Custom", size=11, weight="Bold", color="#0E3A2F"),
                # Row 2
                rect("Task2_Badge", 22, 126, 22, 22, fill="#187941", radius=6),
                txt("Task2_Num", 28, 129, 14, 16, "2", size=11, weight="Bold", color="#FFFFFF"),
                txt("Task2_Name", 52, 127, 260, 20, "Rekap Medis, Jurnal Sekolah & Kantor", size=12, weight="SemiBold", color="#0E3A2F"),
                txt("Task2_Date", 22, 156, 110, 16, "Garansi 30 Hari", size=11, weight="Regular", color="#587A6E"),
                rect("Task2_Bar_Bg", 132, 160, 130, 8, fill="#E6F0EC", radius=4),
                rect("Task2_Bar_Fg", 132, 160, 130, 8, fill="#22A45D", radius=4),
                txt("Task2_Pct", 272, 155, 50, 16, "Tuntas", size=11, weight="Bold", color="#187941"),
            ],
        ),
        # BOTTOM-RIGHT WIDGET: Multi-Stack Architecture (Web App, Database/API, Automation)
        frame(
            "Hero_Integrations_Mini",
            988,
            414,
            336,
            198,
            fill="#FFFFFF",
            radius=20,
            stroke="#DCE8E2",
            stroke_width=1,
            children=[
                txt("Int_Mini_Title", 24, 20, 288, 22, "Teknologi & Integrasi Fleksibel", size=15, weight="Bold", color="#0E3A2F"),
                txt("Int_Mini_Sub", 24, 42, 288, 18, "Web Kustom, Database SQL, API, WA, & Cloud", size=12, weight="Regular", color="#587A6E"),
                floating_tile("Mini_Tile_Web", 24, 76, 86, "Web App", bg="#F7FBF9", accent="#187941", text_color="#FFFFFF"),
                floating_tile("Mini_Tile_DB", 125, 76, 86, "SQL / API", bg="#F7FBF9", accent="#0E3A2F", text_color="#F4B41A"),
                floating_tile("Mini_Tile_WA", 226, 76, 86, "Otomasi", bg="#F7FBF9", accent="#22A45D", text_color="#FFFFFF"),
            ],
        ),
    ]

    children.append(
        frame(
            "Hero_Rounded_Canvas",
            40,
            92,
            1360,
            636,
            fill="#F6FAF8",
            radius=28,
            stroke="#E2EEE8",
            stroke_width=1,
            children=hero_children,
        )
    )

    # =========================================================================
    # SECTION 2: SOLUTIONS + EMBEDDED DASHBOARD PREVIEW (Image 2 Reference)
    # =========================================================================
    children.extend([
        txt(
            "Sol_Heading",
            420,
            780,
            600,
            84,
            "Tuntaskan kendala operasional terbesar tim Anda",
            size=38,
            weight="Bold",
            color="#0E3A2F",
        ),
        frame(
            "Sol_Col_1",
            180,
            888,
            320,
            110,
            fill="#FFFFFF",
            children=[
                rect("Sol_Icon_1", 0, 0, 28, 28, fill="#E4F3EC", radius=8),
                txt("Sol_T1", 0, 38, 300, 64, "Bangun aplikasi web kustom dan database terpusat yang mengikuti alur kerja nyata usaha Anda.", size=13, weight="Regular", color="#355E52"),
            ],
        ),
        frame(
            "Sol_Col_2",
            560,
            888,
            320,
            110,
            fill="#FFFFFF",
            children=[
                rect("Sol_Icon_2", 0, 0, 28, 28, fill="#FEF5D9", radius=8),
                txt("Sol_T2", 0, 38, 300, 64, "Kunci spesifikasi fitur dan anggaran sejak awal melalui 6 poin Client Brief serta 5 poin T&C.", size=13, weight="Regular", color="#355E52"),
            ],
        ),
        frame(
            "Sol_Col_3",
            940,
            888,
            320,
            110,
            fill="#FFFFFF",
            children=[
                rect("Sol_Icon_3", 0, 0, 28, 28, fill="#E4F3EC", radius=8),
                txt("Sol_T3", 0, 38, 300, 64, "Data operasional 100% milik Anda di akun cloud, server, atau Google Drive Anda sendiri.", size=13, weight="Regular", color="#355E52"),
            ],
        ),
    ])

    # Vibrant Framed Dashboard Preview
    dash_preview_children = [
        frame(
            "Dash_Inner_Window",
            28,
            28,
            1064,
            584,
            fill="#F6F9F7",
            radius=20,
            stroke="#D5E6DD",
            stroke_width=1,
            children=[
                frame(
                    "Preview_Sidebar",
                    0,
                    0,
                    220,
                    584,
                    fill="#FFFFFF",
                    radius=20,
                    children=[
                        ellipse("P_Dot1", 20, 22, 10, 10, fill="#187941"),
                        ellipse("P_Dot2", 34, 22, 10, 10, fill="#F4B41A"),
                        txt("P_Brand", 52, 18, 140, 22, "Tuntung Studio", size=14, weight="Bold", color="#0E3A2F"),
                        rect("P_Create_Btn", 16, 54, 188, 34, fill="#F4FAF7", radius=10, stroke="#CFE2D8", stroke_width=1),
                        txt("P_Create_Txt", 32, 63, 150, 18, "+ Buat Client Brief", size=12, weight="SemiBold", color="#187941"),
                        txt("P_Group_1", 20, 106, 120, 16, "ALUR PROYEK", size=10, weight="Bold", color="#7A9288"),
                        rect("P_Nav_Active", 12, 128, 196, 32, fill="#E8F4EE", radius=8),
                        txt("P_Nav_1", 26, 136, 150, 18, "Ringkasan Proyek", size=12, weight="Bold", color="#0E3A2F"),
                        txt("P_Nav_2", 26, 170, 160, 18, "Client Brief (6 Poin)", size=12, weight="Regular", color="#355E52"),
                        txt("P_Nav_3", 26, 202, 160, 18, "Persetujuan T&C (5)", size=12, weight="Regular", color="#355E52"),
                        txt("P_Nav_4", 26, 234, 160, 18, "Tracker 5 Tahap", size=12, weight="Regular", color="#355E52"),
                        txt("P_Nav_5", 26, 266, 160, 18, "Garansi 30 Hari", size=12, weight="Regular", color="#355E52"),
                        txt("P_Group_2", 20, 316, 150, 16, "TIM THE POWER DUO", size=10, weight="Bold", color="#7A9288"),
                        txt("P_Ws_1", 26, 342, 170, 18, "Solution Architect", size=12, weight="Medium", color="#0E3A2F"),
                        txt("P_Ws_2", 26, 372, 170, 18, "Automation Engineer", size=12, weight="Medium", color="#0E3A2F"),
                        txt("P_Ws_3", 26, 402, 170, 18, "Modul Kasir & Stok", size=12, weight="Regular", color="#355E52"),
                        txt("P_Ws_4", 26, 432, 170, 18, "Modul Rekap Medis", size=12, weight="Regular", color="#355E52"),
                    ],
                ),
                txt("P_Date_Top", 248, 20, 260, 18, "Ruang Kerja Kolaborasi Klien & Programmer", size=12, weight="Medium", color="#587A6E"),
                txt("P_User_Top", 880, 20, 160, 18, "[Akun Klien / Duo]", size=12, weight="SemiBold", color="#0E3A2F"),
                txt("P_Greeting", 248, 52, 580, 36, "Pantau Progres Aplikasi Secara Transparan", size=24, weight="Bold", color="#0E3A2F"),
                rect("P_Custom_Btn", 912, 52, 128, 32, fill="#FFFFFF", radius=10, stroke="#D5E6DD", stroke_width=1),
                txt("P_Custom_Txt", 928, 60, 100, 18, "Unduh Dokumen", size=11, weight="SemiBold", color="#0E3A2F"),
                # Card 1: Checklist
                frame(
                    "P_Card_Checklist",
                    248,
                    102,
                    290,
                    320,
                    fill="#FFFFFF",
                    radius=16,
                    stroke="#E2EEE8",
                    stroke_width=1,
                    children=[
                        txt("PC1_Title", 20, 18, 240, 24, "Checklist Standar Proyek", size=15, weight="Bold", color="#0E3A2F"),
                        txt("PC1_Add", 20, 50, 220, 18, "+ Catat spesifikasi atau kendala", size=11, weight="Medium", color="#187941"),
                        rect("PC1_Chk1", 20, 84, 16, 16, fill="#187941", radius=4),
                        txt("PC1_Item1", 44, 82, 226, 34, "6 Poin Client Brief & Sesi Audit 30 Menit tuntas", size=11, weight="Regular", color="#587A6E"),
                        rect("PC1_Chk2", 20, 130, 16, 16, fill="#187941", radius=4),
                        txt("PC1_Item2", 44, 128, 226, 34, "5 Poin Terms & Conditions disetujui & Scope terkunci", size=11, weight="Regular", color="#587A6E"),
                        rect("PC1_Chk3", 20, 176, 16, 16, fill="#187941", radius=4),
                        txt("PC1_Item3", 44, 174, 226, 34, "Arsitektur UI/UX, Database, & API terhubung", size=11, weight="SemiBold", color="#0E3A2F"),
                        rect("PC1_Chk4", 20, 222, 16, 16, fill="#FFFFFF", radius=4, stroke="#94B3A6", stroke_width=1),
                        txt("PC1_Item4", 44, 220, 226, 34, "Testing & Training penggunaan bersama tim klien", size=11, weight="SemiBold", color="#0E3A2F"),
                        rect("PC1_Chk5", 20, 268, 16, 16, fill="#FFFFFF", radius=4, stroke="#94B3A6", stroke_width=1),
                        txt("PC1_Item5", 44, 266, 226, 34, "Serah terima penuh 100% & Garansi 30 Hari", size=11, weight="Regular", color="#355E52"),
                    ],
                ),
                # Card 2: Warranty Timer
                frame(
                    "P_Card_Tracker",
                    554,
                    102,
                    224,
                    206,
                    fill="#FFFFFF",
                    radius=16,
                    stroke="#E2EEE8",
                    stroke_width=1,
                    children=[
                        txt("PC2_Title", 20, 18, 180, 20, "Garansi Pasca-Rilis", size=13, weight="Bold", color="#0E3A2F"),
                        txt("PC2_Timer", 24, 78, 180, 44, "30 Hari", size=34, weight="Bold", color="#0E3A2F"),
                        txt("PC2_Unit", 24, 122, 180, 18, "Perbaikan Bug Teknis Rp 0", size=11, weight="Regular", color="#587A6E"),
                        ellipse("PC2_Btn1", 74, 152, 34, 34, fill="#E8F4EE"),
                        ellipse("PC2_Btn2", 118, 152, 34, 34, fill="#187941"),
                    ],
                ),
                # Card 3: Structural Completeness (Honest ratios from brief: 6/6, 5/5, 5/5)
                frame(
                    "P_Card_Activity",
                    794,
                    102,
                    246,
                    206,
                    fill="#FFFFFF",
                    radius=16,
                    stroke="#E2EEE8",
                    stroke_width=1,
                    children=[
                        txt("PC3_Title", 18, 18, 130, 20, "Parameter Proyek", size=13, weight="Bold", color="#0E3A2F"),
                        txt("PC3_Badge", 160, 18, 70, 18, "Terstruktur", size=10, weight="Bold", color="#187941"),
                        txt("PC3_M1_Lbl", 18, 52, 100, 14, "Poin Client Brief", size=10, weight="Regular", color="#587A6E"),
                        txt("PC3_M1_Val", 18, 68, 80, 22, "6/6", size=15, weight="Bold", color="#0E3A2F"),
                        txt("PC3_M2_Lbl", 18, 98, 100, 14, "Komitmen T&C", size=10, weight="Regular", color="#587A6E"),
                        txt("PC3_M2_Val", 18, 114, 80, 22, "5/5", size=15, weight="Bold", color="#187941"),
                        txt("PC3_M3_Lbl", 18, 144, 100, 14, "Tahap Metode Kerja", size=10, weight="Regular", color="#587A6E"),
                        txt("PC3_M3_Val", 18, 160, 80, 22, "5 Tahap", size=14, weight="Bold", color="#D99B00"),
                        ellipse("PC3_Ring_Outer", 124, 62, 104, 104, fill="#FFFFFF", stroke="#187941", stroke_width=8),
                        ellipse("PC3_Ring_Mid", 138, 76, 76, 76, fill="#FFFFFF", stroke="#22A45D", stroke_width=8),
                        ellipse("PC3_Ring_Inner", 152, 90, 48, 48, fill="#FFFFFF", stroke="#F4B41A", stroke_width=8),
                    ],
                ),
                # Card 4: Data Ownership
                frame(
                    "P_Card_Reminder",
                    248,
                    436,
                    290,
                    126,
                    fill="#FFFFFF",
                    radius=16,
                    stroke="#E2EEE8",
                    stroke_width=1,
                    children=[
                        txt("PC4_Title", 20, 16, 220, 20, "Hak Kekayaan Intelektual & Data", size=13, weight="Bold", color="#0E3A2F"),
                        rect("PC4_Box", 16, 44, 258, 66, fill="#F4FAF7", radius=10),
                        txt("PC4_Txt1", 28, 54, 234, 18, "100% Milik Klien di Akun Sendiri", size=12, weight="Bold", color="#187941"),
                        txt("PC4_Txt2", 28, 76, 234, 20, "Tersimpan di Cloud, Server, atau Drive Klien.", size=11, weight="Regular", color="#355E52"),
                    ],
                ),
                # Card 5: 5-Stage Method
                frame(
                    "P_Card_Stages",
                    554,
                    324,
                    486,
                    238,
                    fill="#FFFFFF",
                    radius=16,
                    stroke="#E2EEE8",
                    stroke_width=1,
                    children=[
                        txt("PC5_Title", 20, 18, 280, 22, "Alur 5 Tahap Metode Kerja", size=14, weight="Bold", color="#0E3A2F"),
                        txt("PC5_Tab1", 20, 46, 95, 18, "Tahap Proyek", size=11, weight="Bold", color="#187941"),
                        txt("PC5_Tab2", 125, 46, 115, 18, "Scope Baseline", size=11, weight="Regular", color="#587A6E"),
                        txt("PC5_Tab3", 250, 46, 120, 18, "Simulasi Add-on", size=11, weight="Regular", color="#587A6E"),
                        txt("Stg1_Name", 20, 80, 230, 18, "1. Konsultasi & Diagnosa (Gratis)", size=11, weight="Medium", color="#0E3A2F"),
                        rect("Stg1_Bg", 260, 84, 140, 8, fill="#E6F0EC", radius=4),
                        rect("Stg1_Fg", 260, 84, 140, 8, fill="#187941", radius=4),
                        txt("Stg1_Pct", 412, 80, 56, 18, "Tahap 1", size=11, weight="Bold", color="#187941"),
                        txt("Stg2_Name", 20, 114, 230, 18, "2. Perancangan Prototype (MVP)", size=11, weight="Medium", color="#0E3A2F"),
                        rect("Stg2_Bg", 260, 118, 140, 8, fill="#E6F0EC", radius=4),
                        rect("Stg2_Fg", 260, 118, 140, 8, fill="#187941", radius=4),
                        txt("Stg2_Pct", 412, 114, 56, 18, "Tahap 2", size=11, weight="Bold", color="#187941"),
                        txt("Stg3_Name", 20, 148, 230, 18, "3. Eksekusi & Development App", size=11, weight="Bold", color="#0E3A2F"),
                        rect("Stg3_Bg", 260, 152, 140, 8, fill="#E6F0EC", radius=4),
                        rect("Stg3_Fg", 260, 152, 100, 8, fill="#F4B41A", radius=4),
                        txt("Stg3_Pct", 412, 148, 56, 18, "Tahap 3", size=11, weight="Bold", color="#0E3A2F"),
                        txt("Stg4_Name", 20, 182, 230, 18, "4-5. Testing, Training & Garansi", size=11, weight="Regular", color="#587A6E"),
                        rect("Stg4_Bg", 260, 186, 140, 8, fill="#E6F0EC", radius=4),
                        rect("Stg4_Fg", 260, 186, 40, 8, fill="#22A45D", radius=4),
                        txt("Stg4_Pct", 412, 182, 56, 18, "Tahap 4-5", size=11, weight="Regular", color="#587A6E"),
                    ],
                ),
            ],
        )
    ]

    children.append(
        frame(
            "Solutions_Dashboard_Frame",
            160,
            1020,
            1120,
            612,
            fill="#22A45D",
            radius=28,
            children=dash_preview_children,
        )
    )
    children.append(floating_tile("Dash_Left_Badge_30", 120, 1340, 72, "30H", bg="#FFFFFF", accent="#0E3A2F", text_color="#F4B41A"))
    children.append(floating_tile("Dash_Right_Badge_OK", 1248, 1180, 72, "Duo", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"))

    # =========================================================================
    # SECTION 3: BENTO GRID FEATURES (2x2 Asymmetric Grid)
    # =========================================================================
    bento_children = [
        txt(
            "Bento_Heading",
            250,
            44,
            860,
            48,
            "Semua proses pembuatan aplikasi di satu tempat",
            size=32,
            weight="Bold",
            color="#0E3A2F",
        ),
        txt(
            "Bento_Sub",
            360,
            98,
            680,
            24,
            "Dari bedah masalah operasional, desain UI/UX, koding aplikasi, hingga garansi pasca-rilis.",
            size=14,
            weight="Regular",
            color="#355E52",
        ),
        # Card 1 (Top-Left): Dikerjakan Langsung oleh 2 Programmer (The Power Duo)
        frame(
            "Bento_Card_1",
            60,
            152,
            596,
            360,
            fill="#FFFFFF",
            radius=24,
            stroke="#E2EEE8",
            stroke_width=1,
            children=[
                frame(
                    "B1_Mock",
                    48,
                    32,
                    500,
                    190,
                    fill="#F6FAF8",
                    radius=16,
                    stroke="#DCE8E2",
                    stroke_width=1,
                    children=[
                        txt("B1_M_Title", 24, 18, 320, 20, "Tim Inti Kami: The Power Duo (2 Programmer)", size=13, weight="Bold", color="#0E3A2F"),
                        rect("B1_Role1", 24, 52, 452, 54, fill="#FFFFFF", radius=10, stroke="#E2EEE8", stroke_width=1),
                        ellipse("B1_Av1", 38, 63, 32, 32, fill="#187941"),
                        txt("B1_R1_Name", 82, 59, 320, 20, "Solution Architect & Conceptor", size=13, weight="Bold", color="#0E3A2F"),
                        txt("B1_R1_Desc", 82, 79, 380, 18, "Audit alur kerja, perancangan UI/UX, & konsultasi solusi teknis bisnis", size=11, weight="Regular", color="#355E52"),
                        rect("B1_Role2", 24, 118, 452, 54, fill="#FFFFFF", radius=10, stroke="#E2EEE8", stroke_width=1),
                        ellipse("B1_Av2", 38, 129, 32, 32, fill="#0E3A2F"),
                        txt("B1_R2_Name", 82, 125, 320, 20, "Automation & App Engineer", size=13, weight="Bold", color="#0E3A2F"),
                        txt("B1_R2_Desc", 82, 145, 380, 18, "Eksekusi koding aplikasi web, integrasi API, & pemeliharaan sistem", size=11, weight="Regular", color="#355E52"),
                    ],
                ),
                txt("B1_Title", 90, 248, 420, 28, "Ditangani Langsung oleh The Power Duo", size=17, weight="Bold", color="#0E3A2F"),
                txt(
                    "B1_Desc",
                    80,
                    282,
                    440,
                    48,
                    "Anda berkomunikasi langsung dengan arsitek solusi dan engineer pembuat aplikasi tanpa perantara berlapis.",
                    size=13,
                    weight="Regular",
                    color="#355E52",
                ),
            ],
        ),
        # Card 2 (Top-Right): 6 Poin Client Brief & Sesi Audit 30 Menit (No fake % per R-18)
        frame(
            "Bento_Card_2",
            684,
            152,
            616,
            360,
            fill="#FFFFFF",
            radius=24,
            stroke="#E2EEE8",
            stroke_width=1,
            children=[
                frame(
                    "B2_Bars",
                    32,
                    32,
                    160,
                    190,
                    fill="#F6FAF8",
                    radius=16,
                    children=[
                        txt("B2_B_Lbl", 16, 16, 130, 18, "Tahap Pengembangan", size=11, weight="Bold", color="#0E3A2F"),
                        rect("Bar_Before", 28, 86, 28, 80, fill="#CFE2D8", radius=6),
                        rect("Bar_After", 72, 62, 28, 104, fill="#187941", radius=6),
                        rect("Bar_Save", 116, 44, 28, 122, fill="#F4B41A", radius=6),
                    ],
                ),
                frame(
                    "B2_Sched",
                    208,
                    32,
                    212,
                    190,
                    fill="#F6FAF8",
                    radius=16,
                    children=[
                        txt("B2_S_Title", 16, 16, 180, 18, "6 Poin Client Brief", size=12, weight="Bold", color="#0E3A2F"),
                        rect("B2_Slot1", 14, 46, 184, 38, fill="#FFFFFF", radius=8),
                        txt("B2_Slot1_T", 24, 56, 164, 18, "1-2. Profil & Problem Goal", size=11, weight="Medium", color="#0E3A2F"),
                        rect("B2_Slot2", 14, 92, 184, 38, fill="#FFFFFF", radius=8),
                        txt("B2_Slot2_T", 24, 102, 164, 18, "3-4. Alur & Spesifikasi Fitur", size=11, weight="Medium", color="#0E3A2F"),
                        rect("B2_Slot3", 14, 138, 184, 38, fill="#E3F5EC", radius=8),
                        txt("B2_Slot3_T", 24, 148, 164, 18, "5-6. Bahan Awal & Anggaran", size=11, weight="Bold", color="#187941"),
                    ],
                ),
                frame(
                    "B2_Ring_Box",
                    436,
                    32,
                    148,
                    190,
                    fill="#F6FAF8",
                    radius=16,
                    children=[
                        txt("B2_R_Title", 20, 16, 110, 18, "Audit Awal", size=12, weight="Bold", color="#0E3A2F"),
                        ellipse("B2_Ring", 28, 56, 92, 92, fill="#FFFFFF", stroke="#F4B41A", stroke_width=10),
                        txt("B2_R_Pct", 44, 90, 64, 24, "30m", size=18, weight="Bold", color="#0E3A2F"),
                    ],
                ),
                txt("B2_Title", 150, 248, 320, 28, "Diagnosa Tepat Sejak Hari Pertama", size=18, weight="Bold", color="#0E3A2F"),
                txt(
                    "B2_Desc",
                    90,
                    282,
                    440,
                    48,
                    "Sesi konsultasi gratis 30 menit dan 6 poin Client Brief memastikan solusi aplikasi menjawab kebutuhan inti bisnis Anda.",
                    size=13,
                    weight="Regular",
                    color="#355E52",
                ),
            ],
        ),
        # Card 3 (Bottom-Left): Pelacakan 5 Tahap & Scope Guard
        frame(
            "Bento_Card_3",
            60,
            540,
            780,
            330,
            fill="#FFFFFF",
            radius=24,
            stroke="#E2EEE8",
            stroke_width=1,
            children=[
                floating_tile("B3_Badge", 32, 28, 54, "5T", bg="#FEF5D9", accent="#F4B41A", text_color="#0E3A2F"),
                txt("B3_Title", 32, 120, 240, 56, "5 Poin T&C & Scope Transparan", size=20, weight="Bold", color="#0E3A2F"),
                txt(
                    "B3_Desc",
                    32,
                    186,
                    240,
                    88,
                    "Pengerjaan mengacu pada kesepakatan awal. Penambahan fitur di luar scope dihitung jelas sebagai add-on.",
                    size=13,
                    weight="Regular",
                    color="#355E52",
                ),
                frame(
                    "B3_Timeline_Mock",
                    300,
                    28,
                    452,
                    274,
                    fill="#F6FAF8",
                    radius=16,
                    stroke="#DCE8E2",
                    stroke_width=1,
                    children=[
                        txt("B3_TL_H", 20, 16, 260, 20, "Timeline 5 Tahap & Pemisahan Scope", size=13, weight="Bold", color="#0E3A2F"),
                        rect("B3_Pill_1", 20, 52, 190, 32, fill="#187941", radius=8),
                        txt("B3_Pill_1_T", 32, 60, 170, 18, "Tahap 1-2: Diagnosa & MVP", size=11, weight="Bold", color="#FFFFFF"),
                        rect("B3_Pill_2", 160, 96, 236, 32, fill="#F4B41A", radius=8),
                        txt("B3_Pill_2_T", 174, 104, 212, 18, "Tahap 3: Koding Web & API", size=11, weight="Bold", color="#0E3A2F"),
                        rect("B3_Kanban_1", 20, 146, 200, 108, fill="#FFFFFF", radius=12, stroke="#E2EEE8", stroke_width=1),
                        txt("B3_K1_T", 34, 160, 172, 18, "Scope Baseline (Terkunci)", size=11, weight="Bold", color="#187941"),
                        txt("B3_K1_B", 34, 184, 172, 52, "Fitur utama sesuai Client Brief awal, termasuk garansi bug 30 hari.", size=11, weight="Regular", color="#355E52"),
                        rect("B3_Kanban_2", 234, 146, 198, 108, fill="#FFFFFF", radius=12, stroke="#E2EEE8", stroke_width=1),
                        txt("B3_K2_T", 248, 160, 172, 18, "Mekanisme Add-on", size=11, weight="Bold", color="#D99B00"),
                        txt("B3_K2_B", 248, 184, 172, 52, "Permintaan fitur baru di luar kesepakatan dihitung dengan estimasi ulang.", size=11, weight="Regular", color="#355E52"),
                    ],
                ),
            ],
        ),
        # Card 4 (Bottom-Right): Multi-Sector Custom Apps
        frame(
            "Bento_Card_4",
            868,
            540,
            432,
            330,
            fill="#F9FBFA",
            radius=24,
            stroke="#CFE2D8",
            stroke_width=1,
            children=[
                frame(
                    "B4_Widget_Highlight",
                    126,
                    36,
                    180,
                    118,
                    fill="#F4B41A",
                    radius=20,
                    children=[
                        txt("B4_W_Sub", 20, 18, 140, 18, "Garansi Pasca-Rilis", size=12, weight="Bold", color="#0E3A2F"),
                        txt("B4_W_Time", 20, 46, 140, 34, "30 Hari", size=24, weight="Bold", color="#0E3A2F"),
                        txt("B4_W_Foot", 20, 86, 140, 16, "Bebas Bug & Pendampingan", size=10, weight="SemiBold", color="#0E3A2F"),
                    ],
                ),
                txt("B4_Title", 86, 182, 260, 52, "Solusi Lintas Sektor Bisnis", size=20, weight="Bold", color="#0E3A2F"),
                txt(
                    "B4_Desc",
                    56,
                    244,
                    320,
                    56,
                    "Siap mendukung UMKM, Instansi Pendidikan, Fasilitas Kesehatan, dan Perkantoran.",
                    size=13,
                    weight="Regular",
                    color="#355E52",
                ),
            ],
        ),
    ]

    children.append(
        frame(
            "Bento_Section_Container",
            40,
            1684,
            1360,
            916,
            fill="#F3F7F5",
            radius=32,
            children=bento_children,
        )
    )

    # =========================================================================
    # SECTION 4: TECH & INTEGRATIONS + 3 SERVICE PLANS + FOOTER
    # =========================================================================
    children.extend([
        txt(
            "Int_Section_Heading",
            370,
            2648,
            700,
            84,
            "Terhubung dengan teknologi dan platform yang Anda gunakan",
            size=34,
            weight="Bold",
            color="#0E3A2F",
        ),
        floating_tile("Int_1_Web", 150, 2756, 116, "Web App", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
        floating_tile("Int_2_SQL", 316, 2756, 116, "SQL / DB", bg="#FFFFFF", accent="#0E3A2F", text_color="#F4B41A"),
        floating_tile("Int_3_API", 482, 2756, 116, "REST API", bg="#FFFFFF", accent="#22A45D", text_color="#FFFFFF"),
        floating_tile("Int_4_WA", 648, 2756, 116, "WhatsApp", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
        floating_tile("Int_5_PDF", 814, 2756, 116, "Dokumen PDF", bg="#FFFFFF", accent="#F4B41A", text_color="#0E3A2F"),
        floating_tile("Int_6_Cloud", 980, 2756, 116, "Cloud / VPS", bg="#FFFFFF", accent="#0E3A2F", text_color="#FFFFFF"),
        floating_tile("Int_7_GWS", 1146, 2756, 116, "Workspace", bg="#FFFFFF", accent="#22A45D", text_color="#FFFFFF"),
    ])

    children.extend([
        txt(
            "Pricing_Heading",
            280,
            2904,
            880,
            48,
            "Tiga layanan utama untuk kerja yang lebih tuntas",
            size=32,
            weight="Bold",
            color="#0E3A2F",
        ),
        # Left Card: Sesi Audit & Konsultasi Gratis (30 Menit)
        frame(
            "Plan_Card_1_Audit",
            150,
            3008,
            344,
            460,
            fill="#F7FAF8",
            radius=24,
            stroke="#DCE8E2",
            stroke_width=1,
            children=[
                txt("P1_Name", 32, 32, 280, 24, "Sesi Audit & Konsultasi", size=18, weight="Bold", color="#0E3A2F"),
                txt("P1_Sub", 32, 58, 280, 18, "Tahap awal membedah kendala operasional.", size=12, weight="Regular", color="#587A6E"),
                txt("P1_Price", 32, 100, 200, 44, "Gratis", size=36, weight="Bold", color="#0E3A2F"),
                txt("P1_Unit", 150, 114, 120, 22, "/ 30 Menit", size=15, weight="Medium", color="#587A6E"),
                rect("P1_CTA", 32, 166, 280, 44, fill="#187941", radius=12),
                txt("P1_CTA_T", 74, 179, 200, 20, "Booking Sesi Audit 30m", size=13, weight="Bold", color="#FFFFFF"),
                txt("P1_F1", 32, 236, 280, 20, "v  Bedah masalah operasional saat ini", size=12, weight="Regular", color="#0E3A2F"),
                txt("P1_F2", 32, 268, 280, 20, "v  Penyusunan roadmap digitalisasi", size=12, weight="Regular", color="#0E3A2F"),
                txt("P1_F3", 32, 300, 280, 20, "v  Pemetaan 6 poin Client Brief", size=12, weight="Regular", color="#0E3A2F"),
                txt("P1_F4", 32, 332, 280, 20, "v  Rekomendasi arsitektur aplikasi & DB", size=12, weight="Regular", color="#0E3A2F"),
                txt("P1_F5", 32, 364, 280, 20, "v  Konsultasi bersama Solution Architect", size=12, weight="Regular", color="#0E3A2F"),
            ],
        ),
        # Center Highlighted Card: Custom Micro-App & Otomasi
        frame(
            "Plan_Card_2_Custom",
            524,
            2984,
            392,
            496,
            fill="#187941",
            radius=28,
            children=[
                txt("P2_Name", 36, 36, 320, 26, "Custom Micro-App & Otomasi", size=20, weight="Bold", color="#FFFFFF"),
                txt("P2_Sub", 36, 64, 320, 18, "Pengembangan aplikasi kustom sesuai proses kerja.", size=12, weight="Regular", color="#D9F2E4"),
                txt("P2_Price", 36, 108, 240, 44, "Custom", size=36, weight="Bold", color="#FFFFFF"),
                txt("P2_Unit", 190, 122, 150, 22, "/ sesuai scope", size=14, weight="Medium", color="#D9F2E4"),
                txt("P2_Tag", 36, 156, 280, 18, "Mengacu Kesepakatan Client Brief", size=12, weight="SemiBold", color="#F4B41A"),
                rect("P2_CTA", 36, 186, 320, 48, fill="#FFFFFF", radius=12),
                txt("P2_CTA_T", 88, 201, 220, 20, "Mulai Isi Client Brief", size=14, weight="Bold", color="#0E3A2F"),
                txt("P2_F1", 36, 258, 320, 20, "v  Aplikasi Kasir/Stok, Rekap Medis, Jurnal", size=13, weight="Medium", color="#FFFFFF"),
                txt("P2_F2", 36, 290, 320, 20, "v  Otomasi Dokumen, API, & WhatsApp", size=13, weight="Medium", color="#FFFFFF"),
                txt("P2_F3", 36, 322, 320, 20, "v  100% Data Milik Klien di Akun Sendiri", size=13, weight="Medium", color="#FFFFFF"),
                txt("P2_F4", 36, 354, 320, 20, "v  Perancangan Prototype MVP & Training", size=13, weight="Medium", color="#FFFFFF"),
                txt("P2_F5", 36, 386, 320, 20, "v  Termasuk Garansi Pasca-Rilis 30 Hari", size=13, weight="Medium", color="#FFFFFF"),
                txt("P2_F6", 36, 418, 320, 20, "v  5 Poin T&C & Scope Baseline Transparan", size=13, weight="Medium", color="#F4B41A"),
            ],
        ),
        floating_tile("Plan_Lightning_Badge", 862, 2954, 72, "INTI", bg="#FFFFFF", accent="#F4B41A", text_color="#0E3A2F"),
        # Right Card: Onboarding & Maintenance
        frame(
            "Plan_Card_3_Maintenance",
            946,
            3008,
            344,
            460,
            fill="#F7FAF8",
            radius=24,
            stroke="#DCE8E2",
            stroke_width=1,
            children=[
                txt("P3_Name", 32, 32, 280, 24, "Onboarding & Maintenance", size=18, weight="Bold", color="#0E3A2F"),
                txt("P3_Sub", 32, 58, 280, 18, "Pendampingan penuh & pemeliharaan sistem.", size=12, weight="Regular", color="#587A6E"),
                txt("P3_Price", 32, 100, 200, 44, "30 Hari", size=36, weight="Bold", color="#0E3A2F"),
                txt("P3_Unit", 175, 114, 140, 22, "+ Opsi Retainer", size=14, weight="Medium", color="#187941"),
                rect("P3_CTA", 32, 166, 280, 44, fill="#0E3A2F", radius=12),
                txt("P3_CTA_T", 74, 179, 200, 20, "Lihat Ketentuan Garansi", size=13, weight="Bold", color="#FFFFFF"),
                txt("P3_F1", 32, 236, 280, 20, "v  Garansi 30 hari perbaikan bug Rp 0", size=12, weight="Regular", color="#0E3A2F"),
                txt("P3_F2", 32, 268, 280, 20, "v  Pendampingan penuh tim operasional", size=12, weight="Regular", color="#0E3A2F"),
                txt("P3_F3", 32, 300, 280, 20, "v  Penyesuaian fitur baru via skema Add-on", size=12, weight="Regular", color="#0E3A2F"),
                txt("P3_F4", 32, 332, 280, 20, "v  Opsi retainer pemeliharaan berkala", size=12, weight="Regular", color="#0E3A2F"),
                txt("P3_F5", 32, 364, 280, 20, "v  Dukungan langsung Automation Engineer", size=12, weight="Regular", color="#0E3A2F"),
            ],
        ),
        # Footer Container with Floating Tiles (No decorative arrows per R-08)
        frame(
            "Footer_Rounded_Canvas",
            40,
            3540,
            1360,
            460,
            fill="#F3F7F5",
            radius=28,
            stroke="#E2EEE8",
            stroke_width=1,
            children=[
                ellipse("F_Dot1", 60, 46, 10, 10, fill="#187941"),
                ellipse("F_Dot2", 74, 46, 10, 10, fill="#0E3A2F"),
                ellipse("F_Dot3", 60, 60, 10, 10, fill="#0E3A2F"),
                ellipse("F_Dot4", 74, 60, 10, 10, fill="#F4B41A"),
                txt("F_Brand", 94, 44, 160, 24, "Tuntung.id", size=18, weight="Bold", color="#0E3A2F"),
                txt("F_Headline_1", 60, 92, 540, 44, "Gawi Manuntung,", size=34, weight="Bold", color="#0E3A2F"),
                txt("F_Headline_2", 60, 138, 540, 44, "Supaya Untung", size=34, weight="Bold", color="#187941"),
                txt("F_Col1_1", 860, 60, 190, 20, "Tentang Tuntung.id", size=13, weight="Medium", color="#355E52"),
                txt("F_Col1_2", 860, 90, 190, 20, "Tim The Power Duo", size=13, weight="Medium", color="#355E52"),
                txt("F_Col1_3", 860, 120, 190, 20, "6 Poin Client Brief", size=13, weight="Medium", color="#355E52"),
                txt("F_Col1_4", 860, 150, 190, 20, "5 Poin Terms & Conditions", size=13, weight="Medium", color="#355E52"),
                txt("F_Col2_1", 1090, 60, 210, 20, "Audit Gratis 30 Menit", size=13, weight="Medium", color="#355E52"),
                txt("F_Col2_2", 1090, 90, 210, 20, "Custom Micro-App & Web App", size=13, weight="Medium", color="#355E52"),
                txt("F_Col2_3", 1090, 120, 210, 20, "Integrasi API & WhatsApp", size=13, weight="Medium", color="#355E52"),
                txt("F_Col2_4", 1090, 150, 210, 20, "Garansi Pasca-Rilis 30 Hari", size=13, weight="Medium", color="#355E52"),
                floating_tile("FT_1", 88, 256, 78, "Brief", bg="#FFFFFF", accent="#0E3A2F", text_color="#FFFFFF"),
                floating_tile("FT_2", 244, 314, 78, "UI/UX", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
                floating_tile("FT_3", 386, 224, 78, "30H", bg="#FFFFFF", accent="#F4B41A", text_color="#0E3A2F"),
                floating_tile("FT_4", 538, 296, 78, "30m", bg="#FFFFFF", accent="#0E3A2F", text_color="#F4B41A"),
                floating_tile("FT_5", 694, 232, 78, "Web", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
                floating_tile("FT_6", 846, 316, 78, "API", bg="#FFFFFF", accent="#22A45D", text_color="#FFFFFF"),
                floating_tile("FT_7", 1004, 228, 78, "T&C", bg="#FFFFFF", accent="#187941", text_color="#FFFFFF"),
                floating_tile("FT_8", 1168, 294, 78, "Untung", bg="#FFFFFF", accent="#F4B41A", text_color="#0E3A2F"),
                txt("F_Copy", 60, 418, 480, 18, "Tuntung.id · Solusi Digital untuk Kerja yang Lebih Tuntas", size=12, weight="Regular", color="#587A6E"),
                txt("F_Right", 1060, 418, 260, 18, "100% Kepemilikan Data Milik Klien", size=12, weight="SemiBold", color="#187941"),
            ],
        ),
    ])

    return frame(
        "01a_Landing_Page_ChronoTask_Style_1440",
        0,
        0,
        1440,
        4060,
        fill="#FFFFFF",
        children=children,
    )


def build_dashboard_workspace():
    return frame(
        "02_Dashboard_Workspace_ChronoTask_Style_1440",
        0,
        0,
        1440,
        1024,
        fill="#F4F8F6",
        children=[
            # Left Sidebar (260px, white, clean)
            frame(
                "App_Sidebar",
                0,
                0,
                260,
                1024,
                fill="#FFFFFF",
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    ellipse("App_Dot1", 28, 28, 12, 12, fill="#187941"),
                    ellipse("App_Dot2", 44, 28, 12, 12, fill="#0E3A2F"),
                    ellipse("App_Dot3", 28, 44, 12, 12, fill="#0E3A2F"),
                    ellipse("App_Dot4", 44, 44, 12, 12, fill="#F4B41A"),
                    txt("App_Brand", 68, 28, 160, 28, "Tuntung.id", size=18, weight="Bold", color="#0E3A2F"),
                    rect("App_Create_Btn", 20, 76, 220, 42, fill="#F4FAF7", radius=12, stroke="#C7DDD3", stroke_width=1),
                    txt("App_Create_Txt", 44, 88, 176, 20, "+ Buat Client Brief Baru", size=13, weight="Bold", color="#187941"),
                    txt("App_Menu_Hdr", 24, 142, 140, 18, "ALUR KERJA UTAMA", size=11, weight="Bold", color="#7A9288"),
                    rect("App_Nav_1_Bg", 16, 168, 228, 40, fill="#E6F4EC", radius=10),
                    txt("App_Nav_1", 32, 179, 180, 20, "Workspace Proyek", size=13, weight="Bold", color="#0E3A2F"),
                    txt("App_Nav_2", 32, 224, 170, 20, "Client Brief (6 Poin)", size=13, weight="Medium", color="#355E52"),
                    txt("App_Nav_2_Cnt", 214, 224, 24, 20, "6", size=12, weight="Bold", color="#187941"),
                    txt("App_Nav_3", 32, 264, 170, 20, "Terms & Conditions", size=13, weight="Medium", color="#355E52"),
                    txt("App_Nav_3_Cnt", 214, 264, 24, 20, "5", size=12, weight="Bold", color="#187941"),
                    txt("App_Nav_4", 32, 304, 170, 20, "Tracker 5 Tahap", size=13, weight="Medium", color="#355E52"),
                    txt("App_Nav_5", 32, 344, 170, 20, "Garansi 30H & Handover", size=13, weight="Medium", color="#355E52"),
                    txt("App_Ws_Hdr", 24, 410, 190, 18, "KATEGORI SISTEM & TIM", size=11, weight="Bold", color="#7A9288"),
                    rect("Ws_Badge_1", 24, 442, 12, 12, fill="#187941", radius=3),
                    txt("Ws_Item_1", 46, 439, 190, 20, "Sistem Kasir & Stok UMKM", size=12, weight="Bold", color="#0E3A2F"),
                    rect("Ws_Badge_2", 24, 478, 12, 12, fill="#22A45D", radius=3),
                    txt("Ws_Item_2", 46, 475, 190, 20, "Aplikasi Rekap Medis Faskes", size=12, weight="Medium", color="#355E52"),
                    rect("Ws_Badge_3", 24, 514, 12, 12, fill="#F4B41A", radius=3),
                    txt("Ws_Item_3", 46, 511, 190, 20, "Jurnal & Presensi Pendidikan", size=12, weight="Medium", color="#355E52"),
                    rect("Ws_Badge_4", 24, 550, 12, 12, fill="#0E3A2F", radius=3),
                    txt("Ws_Item_4", 46, 547, 190, 20, "Otomasi Dokumen Kantor", size=12, weight="Medium", color="#355E52"),
                    frame(
                        "Sidebar_Role_Box",
                        16,
                        910,
                        228,
                        92,
                        fill="#0E3A2F",
                        radius=16,
                        children=[
                            txt("SR_Lbl", 16, 14, 196, 16, "PERAN AKTIF (THE POWER DUO)", size=10, weight="Bold", color="#F4B41A"),
                            txt("SR_Name", 16, 36, 196, 20, "Solution Architect", size=14, weight="Bold", color="#FFFFFF"),
                            txt("SR_Sub", 16, 58, 196, 18, "Beralih ke Automation Engineer", size=11, weight="Regular", color="#BFDCD0"),
                        ],
                    ),
                ],
            ),
            txt("Top_Date_Chip", 296, 28, 340, 22, "Portal Kolaborasi Klien & Tim The Power Duo", size=13, weight="Medium", color="#587A6E"),
            txt("Top_Profile_Name", 1180, 28, 220, 22, "Mode: Solution Architect", size=13, weight="SemiBold", color="#0E3A2F"),
            txt("Dash_Greeting_H1", 296, 68, 720, 44, "Ruang Kendali Proyek & Scope Aplikasi", size=32, weight="Bold", color="#0E3A2F"),
            rect("Dash_Action_Btn", 1188, 68, 216, 42, fill="#187941", radius=12),
            txt("Dash_Action_Txt", 1212, 80, 176, 20, "Ekspor Dokumen Proyek", size=13, weight="Bold", color="#FFFFFF"),
            # CARD 1 (Left Tall): Checklist 6 Poin Brief & Kepemilikan Data
            frame(
                "Dash_Card_Checklist",
                296,
                132,
                380,
                530,
                fill="#FFFFFF",
                radius=22,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("DC1_Title", 28, 26, 300, 26, "Checklist Brief & Kepemilikan Data", size=17, weight="Bold", color="#0E3A2F"),
                    rect("DC1_Add_Box", 28, 64, 324, 38, fill="#F6FAF8", radius=10, stroke="#DCE8E2", stroke_width=1),
                    txt("DC1_Add_Txt", 44, 74, 280, 18, "+ Catat temuan audit atau fitur baru", size=12, weight="SemiBold", color="#187941"),
                    rect("DC1_C1", 28, 122, 18, 18, fill="#187941", radius=5),
                    txt("DC1_T1", 58, 120, 290, 38, "Poin 1-3 Brief: Profil Usaha, Problem & QoL Goal, serta Alur Kerja Saat Ini", size=12, weight="Regular", color="#587A6E"),
                    rect("DC1_C2", 28, 178, 18, 18, fill="#187941", radius=5),
                    txt("DC1_T2", 58, 176, 290, 38, "Poin 4-6 Brief: Spesifikasi Fitur, Data Awal, serta Target Timeline & Anggaran", size=12, weight="Regular", color="#587A6E"),
                    rect("DC1_C3", 28, 234, 18, 18, fill="#187941", radius=5),
                    txt("DC1_T3", 58, 232, 290, 38, "5 Poin Terms & Conditions disetujui dan Scope Baseline terkunci", size=12, weight="SemiBold", color="#0E3A2F"),
                    rect("DC1_C4", 28, 290, 18, 18, fill="#187941", radius=5),
                    txt("DC1_T4", 58, 288, 290, 38, "Database, Server/Cloud, atau Google Drive 100% di akun milik klien", size=12, weight="SemiBold", color="#0E3A2F"),
                    rect("DC1_C5", 28, 346, 18, 18, fill="#FFFFFF", radius=5, stroke="#8AA399", stroke_width=1),
                    txt("DC1_T5", 58, 344, 290, 38, "Tahap 4: Testing & Training bersama pengguna operasional", size=12, weight="Bold", color="#0E3A2F"),
                    rect("DC1_C6", 28, 402, 18, 18, fill="#FFFFFF", radius=5, stroke="#8AA399", stroke_width=1),
                    txt("DC1_T6", 58, 400, 290, 38, "Tahap 5: Serah Terima penuh & aktivasi Garansi 30 Hari", size=12, weight="Regular", color="#355E52"),
                    rect("DC1_Foot", 28, 462, 324, 44, fill="#E8F4EE", radius=12),
                    txt("DC1_Foot_T", 44, 475, 292, 20, "Status Scope: TERKUNCI SESUAI CLIENT BRIEF", size=11, weight="Bold", color="#187941"),
                ],
            ),
            # CARD 2 (Top Center): Warranty & Support Card
            frame(
                "Dash_Card_Timer",
                700,
                132,
                336,
                292,
                fill="#FFFFFF",
                radius=22,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("DC2_Title", 28, 26, 260, 24, "Garansi & Dukungan (Poin 4 T&C)", size=16, weight="Bold", color="#0E3A2F"),
                    txt("DC2_Sub", 28, 52, 280, 18, "Perbaikan bug atau kendala teknis pasca-rilis", size=12, weight="Regular", color="#587A6E"),
                    txt("DC2_Big_Num", 42, 108, 260, 56, "30 Hari", size=42, weight="Bold", color="#0E3A2F"),
                    txt("DC2_Unit_Row", 42, 168, 260, 20, "Garansi Penuh Pasca-Rilis (Rp 0)", size=12, weight="Medium", color="#187941"),
                    rect("DC2_Btn_Bug", 28, 216, 134, 44, fill="#F4FAF7", radius=12, stroke="#C7DDD3", stroke_width=1),
                    txt("DC2_Btn_Bug_T", 46, 229, 104, 18, "Lapor Bug (Rp 0)", size=12, weight="Bold", color="#187941"),
                    rect("DC2_Btn_Add", 174, 216, 134, 44, fill="#187941", radius=12),
                    txt("DC2_Btn_Add_T", 192, 229, 104, 18, "+ Hitung Add-on", size=12, weight="Bold", color="#FFFFFF"),
                ],
            ),
            # CARD 3 (Top Right): Scope & Structural Ring Card
            frame(
                "Dash_Card_Activity",
                1060,
                132,
                344,
                292,
                fill="#FFFFFF",
                radius=22,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("DC3_Title", 28, 26, 180, 24, "Kepatuhan Alur Kerja", size=16, weight="Bold", color="#0E3A2F"),
                    txt("DC3_Pill", 236, 26, 82, 20, "Transparan", size=11, weight="Bold", color="#187941"),
                    txt("DC3_L1", 28, 72, 140, 16, "Dokumen Client Brief", size=11, weight="Regular", color="#587A6E"),
                    txt("DC3_V1", 28, 92, 140, 24, "6 / 6 Poin", size=16, weight="Bold", color="#0E3A2F"),
                    txt("DC3_L2", 28, 132, 140, 16, "Persetujuan T&C", size=11, weight="Regular", color="#587A6E"),
                    txt("DC3_V2", 28, 152, 140, 24, "5 / 5 Poin", size=16, weight="Bold", color="#187941"),
                    txt("DC3_L3", 28, 192, 140, 16, "Kepemilikan Data", size=11, weight="Regular", color="#587A6E"),
                    txt("DC3_V3", 28, 212, 140, 24, "100% Klien", size=16, weight="Bold", color="#D99B00"),
                    ellipse("DC3_Ring_1", 188, 86, 128, 128, fill="#FFFFFF", stroke="#187941", stroke_width=10),
                    ellipse("DC3_Ring_2", 206, 104, 92, 92, fill="#FFFFFF", stroke="#22A45D", stroke_width=10),
                    ellipse("DC3_Ring_3", 224, 122, 56, 56, fill="#FFFFFF", stroke="#F4B41A", stroke_width=10),
                ],
            ),
            # CARD 4 (Bottom Left): Sesi Audit & Kolaborasi The Power Duo
            frame(
                "Dash_Card_Reminder",
                296,
                686,
                380,
                302,
                fill="#FFFFFF",
                radius=22,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("DC4_Title", 28, 24, 300, 24, "Kolaborasi Langsung The Power Duo", size=16, weight="Bold", color="#0E3A2F"),
                    rect("DC4_Box", 24, 62, 332, 214, fill="#F6FAF8", radius=16, stroke="#DCE8E2", stroke_width=1),
                    txt("DC4_Ev_Name", 44, 84, 290, 24, "Sesi Audit & Review Prototype MVP", size=15, weight="Bold", color="#0E3A2F"),
                    txt("DC4_Ev_Time", 44, 114, 290, 20, "Durasi 30 Menit · Bedah Alur & Arsitektur", size=12, weight="SemiBold", color="#187941"),
                    txt("DC4_Ev_Desc", 44, 146, 290, 44, "Didampingi Solution Architect & Conceptor serta Automation & App Engineer.", size=12, weight="Regular", color="#355E52"),
                    rect("DC4_Ev_Btn", 44, 210, 292, 42, fill="#0E3A2F", radius=10),
                    txt("DC4_Ev_Btn_T", 78, 222, 224, 18, "Kelola Repository & Server Klien", size=12, weight="Bold", color="#FFFFFF"),
                ],
            ),
            # CARD 5 (Bottom Right Wide): 5-Stage Method Progress
            frame(
                "Dash_Card_Stages",
                700,
                448,
                704,
                540,
                fill="#FFFFFF",
                radius=22,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("DC5_Title", 28, 26, 380, 26, "Metode Kerja 5 Tahap & Deliverable", size=18, weight="Bold", color="#0E3A2F"),
                    rect("DC5_Adv_Btn", 488, 22, 188, 36, fill="#187941", radius=10),
                    txt("DC5_Adv_Txt", 508, 31, 152, 18, "Lanjutkan Tahap Proyek", size=12, weight="Bold", color="#FFFFFF"),
                    txt("DC5_Tab_1", 28, 70, 140, 20, "5 Tahap Metode Kerja", size=12, weight="Bold", color="#187941"),
                    txt("DC5_Tab_2", 188, 70, 150, 20, "5 Poin T&C (Terkunci)", size=12, weight="Medium", color="#587A6E"),
                    txt("DC5_Tab_3", 358, 70, 160, 20, "Kalkulator Add-on", size=12, weight="Medium", color="#587A6E"),
                    # Row 1
                    rect("R1_Box", 28, 110, 648, 72, fill="#F6FAF8", radius=14),
                    rect("R1_Badge", 44, 126, 36, 36, fill="#187941", radius=10),
                    txt("R1_Num", 58, 135, 16, 18, "1", size=13, weight="Bold", color="#FFFFFF"),
                    txt("R1_Name", 96, 124, 370, 20, "Konsultasi & Diagnosa (Gratis 30 Menit)", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R1_Deliv", 96, 146, 370, 18, "Bedah masalah operasional & penyusunan roadmap aplikasi.", size=12, weight="Regular", color="#355E52"),
                    rect("R1_Bar", 480, 142, 112, 8, fill="#187941", radius=4),
                    txt("R1_Pct", 600, 136, 68, 20, "Selesai", size=12, weight="Bold", color="#187941"),
                    # Row 2
                    rect("R2_Box", 28, 196, 648, 72, fill="#F6FAF8", radius=14),
                    rect("R2_Badge", 44, 212, 36, 36, fill="#187941", radius=10),
                    txt("R2_Num", 58, 221, 16, 18, "2", size=13, weight="Bold", color="#FFFFFF"),
                    txt("R2_Name", 96, 210, 370, 20, "Perancangan Prototype (MVP) & Kunci Scope", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R2_Deliv", 96, 232, 370, 18, "Desain UI/UX, skema database, & persetujuan 5 poin T&C.", size=12, weight="Regular", color="#355E52"),
                    rect("R2_Bar", 480, 228, 112, 8, fill="#187941", radius=4),
                    txt("R2_Pct", 600, 222, 68, 20, "Selesai", size=12, weight="Bold", color="#187941"),
                    # Row 3
                    rect("R3_Box", 28, 282, 648, 72, fill="#FEF9E7", radius=14, stroke="#F4B41A", stroke_width=1),
                    rect("R3_Badge", 44, 298, 36, 36, fill="#F4B41A", radius=10),
                    txt("R3_Num", 58, 307, 16, 18, "3", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R3_Name", 96, 296, 370, 20, "Eksekusi & Development (Full-Stack & Otomasi)", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R3_Deliv", 96, 318, 370, 18, "Koding aplikasi web, integrasi API, database, & notifikasi WA.", size=12, weight="Regular", color="#355E52"),
                    rect("R3_Bar_Bg", 480, 314, 112, 8, fill="#E6F0EC", radius=4),
                    rect("R3_Bar_Fg", 480, 314, 78, 8, fill="#F4B41A", radius=4),
                    txt("R3_Pct", 600, 308, 68, 20, "Aktif", size=12, weight="Bold", color="#0E3A2F"),
                    # Row 4
                    rect("R4_Box", 28, 368, 648, 72, fill="#F6FAF8", radius=14),
                    rect("R4_Badge", 44, 384, 36, 36, fill="#DCE8E2", radius=10),
                    txt("R4_Num", 58, 393, 16, 18, "4", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R4_Name", 96, 382, 370, 20, "Testing & Training Staf Operasional", size=13, weight="SemiBold", color="#355E52"),
                    txt("R4_Deliv", 96, 404, 370, 18, "Uji coba sistem menyeluruh & pelatihan tim pengguna.", size=12, weight="Regular", color="#587A6E"),
                    rect("R4_Bar_Bg", 480, 400, 112, 8, fill="#E6F0EC", radius=4),
                    txt("R4_Pct", 600, 394, 68, 20, "Tahap 4", size=11, weight="Medium", color="#587A6E"),
                    # Row 5
                    rect("R5_Box", 28, 454, 648, 64, fill="#F6FAF8", radius=14),
                    rect("R5_Badge", 44, 466, 36, 36, fill="#DCE8E2", radius=10),
                    txt("R5_Num", 58, 475, 16, 18, "5", size=13, weight="Bold", color="#0E3A2F"),
                    txt("R5_Name", 96, 466, 370, 20, "Serah Terima 100% Data Klien & Garansi 30 Hari", size=13, weight="SemiBold", color="#355E52"),
                    txt("R5_Deliv", 96, 488, 370, 18, "Penyerahan akses penuh sistem & jaminan perbaikan bug 30 hari.", size=12, weight="Regular", color="#587A6E"),
                    txt("R5_Pct", 600, 476, 68, 20, "Tahap 5", size=11, weight="Medium", color="#587A6E"),
                ],
            ),
        ],
    )


def build_brief_and_tc_screen():
    return frame(
        "03_Client_Brief_and_TC_ChronoTask_Style_1440",
        0,
        0,
        1440,
        1024,
        fill="#F4F8F6",
        children=[
            txt("Brief_Page_Title", 60, 36, 680, 40, "Formulir 6 Poin Client Brief & 5 Poin T&C", size=30, weight="Bold", color="#0E3A2F"),
            txt("Brief_Page_Sub", 60, 80, 820, 22, "Standar transparansi Tuntung.id agar pengembangan aplikasi tepat sasaran, terukur, dan berdampak nyata.", size=14, weight="Regular", color="#355E52"),
            # Left Column: 6 Poin Client Brief Interactive Card
            frame(
                "Brief_Wizard_Card",
                60,
                124,
                640,
                840,
                fill="#FFFFFF",
                radius=24,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("BW_Header", 32, 28, 420, 28, "Overview 6 Poin Client Brief", size=20, weight="Bold", color="#0E3A2F"),
                    rect("BW_Slot_Pill", 456, 26, 152, 32, fill="#E8F4EE", radius=16),
                    txt("BW_Slot_Txt", 472, 34, 124, 18, "Audit Gratis 30m", size=11, weight="Bold", color="#187941"),
                    rect("BP_1", 32, 78, 576, 102, fill="#F6FAF8", radius=16, stroke="#187941", stroke_width=1),
                    txt("BP_1_T", 52, 92, 520, 22, "1. Profil & Identitas Bisnis", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_1_D", 52, 118, 536, 44, "Ceritakan sedikit tentang usaha atau lembaga Anda (UMKM, Pendidikan, Fasilitas Kesehatan, atau Perkantoran).", size=12, weight="Regular", color="#355E52"),
                    rect("BP_2", 32, 194, 576, 102, fill="#F6FAF8", radius=16),
                    txt("BP_2_T", 52, 208, 520, 22, "2. Problem & Quality of Life Goal", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_2_D", 52, 234, 536, 44, "Apa kendala utama yang ingin diselesaikan dan hasil akhir efisiensi kerja yang diharapkan?", size=12, weight="Regular", color="#355E52"),
                    rect("BP_3", 32, 310, 576, 102, fill="#F6FAF8", radius=16),
                    txt("BP_3_T", 52, 324, 520, 22, "3. Alur Kerja Saat Ini", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_3_D", 52, 350, 536, 44, "Bagaimana urutan alur kerja Anda saat ini, dan di bagian mana letak kendala utamanya?", size=12, weight="Regular", color="#355E52"),
                    rect("BP_4", 32, 426, 576, 102, fill="#F6FAF8", radius=16),
                    txt("BP_4_T", 52, 440, 520, 22, "4. Spesifikasi & Fitur yang Diinginkan", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_4_D", 52, 466, 536, 44, "Fitur apa saja yang dibutuhkan dalam aplikasi web, sistem internal, integrasi API, atau otomasi?", size=12, weight="Regular", color="#355E52"),
                    rect("BP_5", 32, 542, 576, 92, fill="#F6FAF8", radius=16),
                    txt("BP_5_T", 52, 556, 520, 22, "5. Data & Bahan Awal", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_5_D", 52, 582, 536, 36, "Apakah sudah tersedia data awal, format dokumen, atau sistem lama yang bisa digunakan?", size=12, weight="Regular", color="#355E52"),
                    rect("BP_6", 32, 648, 576, 92, fill="#F6FAF8", radius=16),
                    txt("BP_6_T", 52, 662, 520, 22, "6. Timeline & Anggaran", size=15, weight="Bold", color="#0E3A2F"),
                    txt("BP_6_D", 52, 688, 536, 36, "Kapan target implementasi aplikasi dan perkiraan anggaran yang disiapkan?", size=12, weight="Regular", color="#355E52"),
                    rect("BW_Submit_Btn", 32, 764, 576, 52, fill="#187941", radius=14),
                    txt("BW_Submit_Txt", 168, 780, 320, 22, "Simpan Client Brief & Kunci Jadwal Audit", size=14, weight="Bold", color="#FFFFFF"),
                ],
            ),
            # Right Column: 5 Poin Terms & Conditions Interactive Card
            frame(
                "TC_Agreement_Card",
                740,
                124,
                640,
                840,
                fill="#FFFFFF",
                radius=24,
                stroke="#E2EEE8",
                stroke_width=1,
                children=[
                    txt("TC_Header", 32, 28, 440, 28, "Overview 5 Poin Terms & Conditions", size=20, weight="Bold", color="#0E3A2F"),
                    rect("TC_Status_Pill", 464, 26, 144, 32, fill="#FEF5D9", radius=16),
                    txt("TC_Status_Txt", 482, 34, 112, 18, "Komitmen Kerja", size=11, weight="Bold", color="#0E3A2F"),
                    rect("TC_1", 32, 78, 576, 114, fill="#F6FAF8", radius=16),
                    rect("TC_1_Chk", 52, 96, 20, 20, fill="#187941", radius=6),
                    txt("TC_1_T", 84, 94, 490, 22, "1. Ruang Lingkup Layanan", size=15, weight="Bold", color="#0E3A2F"),
                    txt("TC_1_D", 84, 120, 500, 56, "Pengerjaan aplikasi dan otomasi didasarkan pada dokumen Client Brief dan kesepakatan fitur awal. Perubahan di luar kesepakatan dihitung sebagai add-on.", size=12, weight="Regular", color="#355E52"),
                    rect("TC_2", 32, 208, 576, 114, fill="#F6FAF8", radius=16),
                    rect("TC_2_Chk", 52, 226, 20, 20, fill="#187941", radius=6),
                    txt("TC_2_T", 84, 224, 490, 22, "2. Hak Kekayaan Intelektual & Kepemilikan Data", size=15, weight="Bold", color="#0E3A2F"),
                    txt("TC_2_D", 84, 250, 500, 56, "Seluruh data operasional Anda adalah milik Anda sepenuhnya dan tersimpan aman di akun cloud, server, atau Google Drive milik Anda.", size=12, weight="Regular", color="#355E52"),
                    rect("TC_3", 32, 338, 576, 114, fill="#F6FAF8", radius=16),
                    rect("TC_3_Chk", 52, 356, 20, 20, fill="#187941", radius=6),
                    txt("TC_3_T", 84, 354, 490, 22, "3. Biaya, Pembayaran & Penjadwalan", size=15, weight="Bold", color="#0E3A2F"),
                    txt("TC_3_D", 84, 380, 500, 56, "Biaya layanan mengacu pada kesepakatan awal. Pembayaran dilakukan sesuai skema yang disepakati, dan pengerjaan dimulai setelah pembayaran tahap awal.", size=12, weight="Regular", color="#355E52"),
                    rect("TC_4", 32, 468, 576, 114, fill="#F6FAF8", radius=16),
                    rect("TC_4_Chk", 52, 486, 20, 20, fill="#187941", radius=6),
                    txt("TC_4_T", 84, 484, 490, 22, "4. Garansi & Dukungan Pasca-Rilis 30 Hari", size=15, weight="Bold", color="#0E3A2F"),
                    txt("TC_4_D", 84, 510, 500, 56, "Garansi pasca-rilis selama 30 hari untuk perbaikan bug atau kendala teknis tanpa biaya tambahan, serta pendampingan sesuai paket layanan.", size=12, weight="Regular", color="#355E52"),
                    rect("TC_5", 32, 598, 576, 114, fill="#F6FAF8", radius=16),
                    rect("TC_5_Chk", 52, 616, 20, 20, fill="#187941", radius=6),
                    txt("TC_5_T", 84, 614, 490, 22, "5. Perubahan & Pembatalan", size=15, weight="Bold", color="#0E3A2F"),
                    txt("TC_5_D", 84, 640, 500, 56, "Perubahan fitur dapat diajukan dengan estimasi ulang. Pembatalan proyek mengikuti ketentuan yang berlaku berdasarkan progres pengerjaan.", size=12, weight="Regular", color="#355E52"),
                    rect("TC_Sign_Btn", 32, 764, 576, 52, fill="#0E3A2F", radius=14),
                    txt("TC_Sign_Txt", 150, 780, 350, 22, "Setujui 5 Poin T&C & Kunci Ruang Lingkup Awal", size=14, weight="Bold", color="#FFFFFF"),
                ],
            ),
        ],
    )


def flatten_node_to_commands(node, ox=0, oy=0, commands=None, is_root_frame=False):
    if commands is None:
        commands = []

    abs_x = ox + node.get("x", 0)
    abs_y = oy + node.get("y", 0)
    w = node.get("width", 100)
    h = node.get("height", 40)
    ntype = node["type"]

    props = {}
    if "fill" in node and node["fill"]:
        props["fill"] = node["fill"]
    if "cornerRadius" in node:
        props["cornerRadius"] = node["cornerRadius"]
    if "stroke" in node and node["stroke"]:
        props["stroke"] = node["stroke"]
        props["strokeWeight"] = node.get("strokeWidth", 1)

    if ntype == "text":
        props["fontFamily"] = node.get("fontFamily", "Plus Jakarta Sans")
        props["fontStyle"] = node.get("fontStyle", "Regular")
        props["fontSize"] = node.get("fontSize", 14)
        props["textAutoResize"] = "height"
        commands.append({
            "command": "node.create",
            "params": {
                "type": "text",
                "name": node["name"],
                "x": abs_x,
                "y": abs_y,
                "width": w,
                "height": h,
                "text": node.get("text", ""),
                "props": props,
                "select": False,
            },
        })
    elif ntype == "frame":
        layer_type = "frame" if is_root_frame else "rectangle"
        commands.append({
            "command": "node.create",
            "params": {
                "type": layer_type,
                "name": node["name"],
                "x": abs_x,
                "y": abs_y,
                "width": w,
                "height": h,
                "props": props,
                "select": False,
            },
        })
        for child in node.get("children", []):
            flatten_node_to_commands(child, abs_x, abs_y, commands, is_root_frame=False)
    else:
        commands.append({
            "command": "node.create",
            "params": {
                "type": ntype,
                "name": node["name"],
                "x": abs_x,
                "y": abs_y,
                "width": w,
                "height": h,
                "props": props,
                "select": False,
            },
        })

    return commands


def main():
    pages = [
        ("01 Landing Page (ChronoTask Style)", build_landing_desktop()),
        ("02 Dashboard Workspace (ChronoTask Style)", build_dashboard_workspace()),
        ("03 Client Brief & T&C (ChronoTask Style)", build_brief_and_tc_screen()),
    ]

    commands = []
    for idx, (page_name, root_frame) in enumerate(pages):
        if idx == 0:
            commands.append({"command": "page.rename", "params": {"name": page_name}})
        else:
            commands.append({"command": "page.add", "params": {"name": page_name}})
        commands.append({"command": "page.setBackground", "params": {"color": "#E6ECE9"}})
        flatten_node_to_commands(root_frame, 0, 0, commands, is_root_frame=True)

    SPEC_JSON.write_text(json.dumps(commands, indent=2, ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [CLI_PATH, "run", str(SPEC_JSON), "--out", str(OUT_FILE)],
        check=True,
    )
    subprocess.run(
        [CLI_PATH, "run", str(SPEC_JSON), "--out", str(DESIGN_DIR / "tuntungid-ui.figcraft")],
        check=True,
    )

    renders = [
        ("01 Landing Page (ChronoTask Style)", "02a_landing_desktop.png"),
        ("02 Dashboard Workspace (ChronoTask Style)", "04a_internal_workspace.png"),
        ("03 Client Brief & T&C (ChronoTask Style)", "03a_client_brief_wizard.png"),
    ]
    for page_name, filename in renders:
        out_png = PREVIEW_DIR / filename
        subprocess.run(
            [
                CLI_PATH,
                "render",
                str(OUT_FILE),
                "--page",
                page_name,
                "--out",
                str(out_png),
                "--scale",
                "1",
            ],
            check=True,
        )
    print("FigCraft ChronoTask-style UI (Multi-Stack & AGENTS.md compliant) generated and rendered successfully.")


if __name__ == "__main__":
    main()
