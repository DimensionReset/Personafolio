###########################
# DimensionReset | helper.py

# helper functions to be used in main.py
# everything lengthy in here so ts anti-bloat
############################

# === LIBRARIES ===
import random
from js import document, window
from pyodide.ffi import create_proxy

# === CONFIG ===
persona_users = [
    # Persona 1
    "Boy With",
    "Naoya Toudou",
    "Maki Sonomura",
    "Masao Inaba",
    "Kei Nanjo",
    "Yukino Mayuzumi",
    "Hidehiko Uesugi",
    "Eriko Kirishima",
    "Reiji Kido",
    "Yuka Ayase",

    # Persona 2
    "Tatsuya Suou",
    "Lisa Silverman",
    "Eikichi Mishina",
    "Jun Kurosu",
    "Maya Amano",
    "Katsuya Suou",
    "Baofu Baofu",
    "Ulala Serizawa",
    "Tatsuya Sudou",
    "Anna Yoshizaka",

    # Persona 3
    "Makoto Yuki",
    "Yukari Takeba",
    "Junpei Iori",
    "Mitsuru Kirijo",
    "Akihiko Sanada",
    "Fuuka Yamagishi",
    "Aigis Aigis",
    "Anti-Shadow Weapon",
    "Ken Amada",
    "Shinjiro Aragaki",
    "Koromaru Dog",
    "Metis Metis",
    "Ryoji Mochizuki",

    # Persona 4
    "Yu Narukami",
    "Yosuke Hanamura",
    "Chie Satonaka",
    "Yukiko Amagi",
    "Kanji Tatsumi",
    "Rise Kujikawa",
    "Naoto Shirogane",
    "Teddie Teddie",
    "Teddie Bear",
    "Tohru Adachi",
    "Marie Marie",

    # Persona 5
    "Ren Amamiya",
    "Ryuji Sakamoto",
    "Ann Takamaki",
    "Yusuke Kitagawa",
    "Makoto Niijima",
    "Futaba Sakura",
    "Haru Okumura",
    "Goro Akechi",
    "Sumire Yoshizawa",
    "Morgana Morgana",
    "Morgana Cat",
    "Morgana Chud",
    "Zenkichi Hasegawa",
    "Sophia Sophia",
    "Erina Erina"
]

BASE_UNIT_WIDTH = 100

# === GLOBALS ===

# Cursor SVG Container
svg_ns = "http://www.w3.org/2000/svg"
svg_container = document.createElement("div")
svg_container.id = "global-cursor-container"
svg_container.classList.add("hidden")
document.body.appendChild(svg_container)

# === HELPER FUNCTIONS ===

# Helper that removes visibility from club output when called
def club_close(event):
    container = document.getElementById("clubOutputContainer")
    playSound("switchToggleSFX")

    container.classList.add("invisible")

# Helper that changes club output content to the input string
def club_output(text):
    container = document.getElementById("clubOutputContainer")
    output = document.getElementById("clubOutput")

    container.classList.remove("invisible")
    output.textContent = str(text)

# Helper that plays sounds that can stack at a certain volume
def playSound(name, vol=None):
    snd = document.getElementById(name)
    if not snd:
        return

    snd_clone = snd.cloneNode(True)
    if vol:
        snd_clone.volume = vol

    def on_ended(event):
        snd_clone.remove()
        ended_proxy.destroy()

    ended_proxy = create_proxy(on_ended)
    snd_clone.addEventListener("ended", ended_proxy)

    snd_clone.play()

# Helper to create template triangle SVGs (used for selection cursors)
def create_base_svg(poly_id, fill_color, extra_class="", y_offset=0, x_offset=0):
    svg = document.createElementNS(svg_ns, "svg")
    svg.setAttribute("width", "400")
    svg.setAttribute("height", "200")
    svg.setAttribute("viewBox", "0 0 400 200")
    svg.setAttribute("class", f"overflow-visible fixed mix-blend-plus-lighter cursor-triangle-svg {extra_class}")

    poly = document.createElementNS(svg_ns, "polygon")
    poly.setAttribute("id", poly_id)
    poly.setAttribute("points", f"{BASE_UNIT_WIDTH + x_offset},{-20 + y_offset} {BASE_UNIT_WIDTH + x_offset},{60 + y_offset} 0,{105 - y_offset}")
    poly.setAttribute("fill", fill_color)

    svg.appendChild(poly)
    svg_container.appendChild(svg)

    return svg

# Helper to hide all scenes and load the options menu
def load_options():
    options_menu = document.getElementById("optionsMenu")
    all_scenes = document.querySelectorAll('div#sceneContainer div[id$="Menu"]')

    for scene in all_scenes:
        scene.classList.add("hidden")

    if options_menu:
        options_menu.classList.remove("animate-circle-wipe")
        options_menu.offsetHeight
        options_menu.classList.remove("hidden")
        options_menu.classList.add("animate-circle-wipe")
        svg_container.classList.remove("hidden")

# Helper to update cursor pos after event and option select
def update_cursor_position(event=None):
    current_selected_span = document.querySelector("#optionsList li span.text-black")
    if not current_selected_span:
        return

    rect = current_selected_span.getBoundingClientRect()
    text_width = rect.width
    scale_x = text_width / BASE_UNIT_WIDTH

    is_resize = event is not None

    for svg in [svg_front, svg_red, svg_back]:
        if is_resize:
            svg.style.transition = "none"
        else:
            svg.style.transition = "transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), top 0.3s cubic-bezier(0.25, 1, 0.5, 1), left 0.3s cubic-bezier(0.25, 1, 0.5, 1)"

        svg.style.top = f"{rect.top + 3}px"
        svg.style.left = f"{rect.left}px"
        svg.style.transform = f"scaleX({scale_x})"

# === SET UPS ===

# for cursor polygons
y_rand = random.uniform(-3, 7)
svg_front = create_base_svg("triangleFront", "rgb(255, 0, 0)", x_offset=2.5, y_offset=y_rand, extra_class="animate-heartbeat") # matches back half
svg_red = create_base_svg("triangleRed", "rgb(255, 0, 0)", extra_class="z-1") # makes text red
svg_back = create_base_svg("triangleBack", "rgb(255, 255, 255)", extra_class="-z-1") # matches front half