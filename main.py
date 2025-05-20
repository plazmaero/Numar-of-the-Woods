import pygame, math, random, json#, cpuinfo
from sys import exit
from pygame.locals import *
from timers import Timer
from map import *

RESOLUTION = WIDTH, HEIGHT = 350, 350
FPS = 30

print("Initializing Pygame...")
#print("CPU:", cpuinfo.get_cpu_info()['brand_raw'])

saves = {
  "save1": {"Suns": 0, "World": "hub1", "Page": -1},
  "save2": {"Suns": 0, "World": "hub1", "Page": -1},
}

#out_ = open("Saves/memory_card/savefile.txt", "w"); json.dump(saves, out_); out_.close()
try: in_ = open("Saves/memory_card/savefile.txt", "r"); saves = json.load(in_); print("JSON serializer", "Enabling ReadableBuffer"); print("SAVES FOUND!", open("Saves/memory_card/savefile.txt", "r"))
except: print("No memory card inserted - if you want to keep saves, install the card in the itch.io page.")

pygame.init()
pygame.joystick.init()
pygame.mixer.init(44100, -16, 1, 2048)
display = pygame.display.set_mode(RESOLUTION, flags = pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Numar of the Woods')
pygame.display.set_icon(pygame.image.load('Assets/sun.png').convert_alpha())
clock = pygame.time.Clock()
screen = pygame.surface.Surface(RESOLUTION)

jump_sfx = pygame.mixer.Sound("Sounds/sfx/jump.wav")
land_sfx = pygame.mixer.Sound("Sounds/sfx/land.wav")
hurt_sfx = pygame.mixer.Sound("Sounds/sfx/hurt.wav")
coin_sfx = pygame.mixer.Sound("Sounds/sfx/coin.wav")
firefly_sfx = pygame.mixer.Sound("Sounds/sfx/firefly.wav")
fly_sfx = pygame.mixer.Sound("Sounds/sfx/fly.wav")
copter_sfx = pygame.mixer.Sound("Sounds/sfx/copter.wav")
cry_sfx = pygame.mixer.Sound("Sounds/sfx/cry.wav")
fall_sfx = pygame.mixer.Sound("Sounds/sfx/fall.wav")
target_sfx = pygame.mixer.Sound("Sounds/sfx/target.wav")
click_sfx = pygame.mixer.Sound("Sounds/sfx/click.wav")
magic_sfx = pygame.mixer.Sound("Sounds/sfx/magic.wav")
nox_flash_sfx = pygame.mixer.Sound("Sounds/sfx/nox flash.wav")
nox_fire_sfx = pygame.mixer.Sound("Sounds/sfx/nox fire.wav")
swing_sfx = pygame.mixer.Sound("Sounds/sfx/swing.wav")
frost_breath_sfx = pygame.mixer.Sound("Sounds/sfx/frost breath.wav")
tornado_sfx = pygame.mixer.Sound("Sounds/sfx/tornado.wav")
crash_sfx = pygame.mixer.Sound("Sounds/sfx/crash.wav")
stance_sfx = pygame.mixer.Sound("Sounds/sfx/stance.wav")
dash_sfx = pygame.mixer.Sound("Sounds/sfx/dash.wav")
blip_sfx = pygame.mixer.Sound("Sounds/sfx/blip.wav")
hp_it_sfx = pygame.mixer.Sound("Sounds/sfx/hp it.wav")

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

retrofontbig = pygame.font.Font('Fonts/retroville.ttf', 27)
retrofontbig2 = pygame.font.Font('Fonts/retroville.ttf', 23)
retrofont = pygame.font.Font('Fonts/retroville.ttf', 20)
retrofontmedium = pygame.font.Font('Fonts/retroville.ttf', 15)
retrofontsmall = pygame.font.Font('Fonts/retroville.ttf', 14)

sun = pygame.image.load('Assets/sun.png').convert_alpha()

logo = pygame.image.load('Assets/logo.png').convert_alpha()
logo_wtm = pygame.image.load('Assets/logo white tm.png').convert_alpha()

mountains = pygame.image.load('Assets/mountains.png').convert_alpha()
humid_sky = pygame.image.load('Assets/humid sky.png').convert_alpha()
poles1 = pygame.image.load(f"Assets/background 1.png").convert_alpha()
poles2 = pygame.image.load(f"Assets/background 2.png").convert_alpha()

moon = pygame.image.load('Assets/moon.png').convert_alpha()
stars1 = pygame.image.load(f"Assets/stars 1.png").convert_alpha()
stars2 = pygame.image.load(f"Assets/stars 2.png").convert_alpha()
gtsbg = pygame.image.load(f"Assets/gather the suns background.png").convert_alpha()

buildings1 = pygame.image.load(f"Assets/buildings 1.png").convert_alpha()
buildings2 = pygame.image.load(f"Assets/buildings 2.png").convert_alpha()
buildings3 = pygame.image.load(f"Assets/buildings 3.png").convert_alpha()

spotlight1 = pygame.image.load(f"Assets/spotlight left.png").convert_alpha()
spotlight2 = pygame.image.load(f"Assets/spotlight right.png").convert_alpha()

overlay = pygame.image.load(f"Assets/overlay.png").convert_alpha()
magic_bg = pygame.image.load(f"Assets/magic bg.png").convert_alpha()

stone_mountains = pygame.image.load('Assets/stone mountains.png').convert_alpha()
sky = pygame.image.load('Assets/sky.png').convert_alpha()
clouds1 = pygame.image.load(f"Assets/clouds 1.png").convert_alpha()
clouds2 = pygame.image.load(f"Assets/clouds 2.png").convert_alpha()
clouds3 = pygame.image.load(f"Assets/clouds 3.png").convert_alpha()
fog = pygame.image.load('Assets/fog.png').convert_alpha()

sunset = pygame.image.load('Assets/sunset.png').convert_alpha()
taiga_mountains = pygame.image.load('Assets/taiga mountain.png').convert_alpha()
taiga_forest1 = pygame.image.load('Assets/taiga forest 1.png').convert_alpha()
taiga_forest2 = pygame.image.load('Assets/taiga forest 2.png').convert_alpha()

night_sky = pygame.image.load('Assets/night sky.png').convert_alpha()

you_fell_text = retrofont.render("YOU FELL...", False, "White")
congratulations_text = retrofont.render("CONGRATULATIONS!!!", False, "White")
push_start_text = retrofont.render("Push START", False, "Yellow")
credits_text = retrofontmedium.render("     - Nox\n\n     - Hootin-Kabloo\n\n     - Hoot-Hoot\n\n     - Glacigon\n\n     - Kyo\n\n     - Kiki\n\n     - Pal\n\n     - Numar\n   Cast\n\n\n\nNumar of the Woods\nA game by Kaan, Tunari", False, "Blue")
tyfp_text = retrofont.render("Thank you for playing!", False, "White")
tbc_text = retrofontsmall.render("Push START Button", False, "White")

def maxint(int, max):
  if int > max: return max
  else: return int

def minint(int, min):
  if int < min: return min
  else: return int

def betweenint(int, min, max, only_for_max=False, only_for_min=False):
  if int: determined_int = 0
  else: determined_int = -1
  while (not ((int >= min or only_for_min) and (int <= max or only_for_max))) and determined_int != int:
    determined_int = int
    if int > max and not only_for_max: int = max - (int - min)
    if int < min and not only_for_min: int = max + (int - min)
  return int


game_over_controller_delay = Timer()
freeze_time = 60

collectibles = {
  "sun": {"type": "sun", "message": "5 +", "sound": coin_sfx, "colors": ["White", "Yellow"], "value": 5, "lives": 0},
  "firefly": {"type": "firefly", "message": "5 + HP", "sound": firefly_sfx, "colors": ["Yellow", "Green", "Cyan"], "value": 0, "lives": 5},
}

monsters = {
  "ampul": {"type": "ampul", "speed": 3, "lives": 1, "grant": 1, "bigger": False},
  "utanpul": {"type": "utanpul", "speed": 2, "lives": 1, "grant": 2, "bigger": False},
  "hapshu right": {"type": "hapshu right", "speed": 1, "lives": 1, "grant": 1, "bigger": False},
  "hapshu left": {"type": "hapshu left", "speed": 1, "lives": 1, "grant": 1, "bigger": False},
  "hapshu up": {"type": "hapshu up", "speed": 1, "lives": 1, "grant": 2, "bigger": False},
  
  "hoot-hoot": {"type": "hoot-hoot", "speed": 3, "lives": 10, "grant": 10, "bigger": True}, #Fun fact, he used to be called Varbay Owl

  "mechampul": {"type": "mechampul", "speed": 1, "lives": 2, "grant": 2, "bigger": False},
  "canfish right": {"type": "canfish right", "speed": 1, "lives": 5, "grant": 3, "bigger": True},
  "canfish left": {"type": "canfish left", "speed": 1, "lives": 5, "grant": 3, "bigger": True},
  "uçampul": {"type": "uçampul", "speed": 1.5, "lives": 1, "grant": 1, "bigger": False},
  
  "lambda": {"type": "lambda", "speed": 0, "lives": 10, "grant": 10, "bigger": True},
  
  "rüyampul": {"type": "rüyampul", "speed": 1.75, "lives": 1, "grant": 1, "bigger": False},
  "wonderfly": {"type": "wonderfly", "speed": 0, "lives": 2, "grant": 2, "bigger": True},
  "wonderfly oscillator": {"type": "wonderfly oscillator", "speed": 0, "lives": 2, "grant": 2, "bigger": True},
  "ruki": {"type": "ruki", "speed": 2, "lives": 1, "grant": 1, "bigger": False},
  
  "nox": {"type": "nox", "speed": 5, "lives": 15, "grant": 10, "bigger": True},

  "donanpul": {"type": "donanpul", "speed": 2, "lives": 2, "grant": 2, "bigger": False},
  "kiskus": {"type": "kiskus", "speed": 3, "lives": 2, "grant": 1, "bigger": False},
  "kartop": {"type": "kartop", "speed": 1, "lives": 3, "grant": 2, "bigger": True},
  
  "glacigon": {"type": "glacigon", "speed": 8, "lives": 15, "grant": 10, "bigger": True},

  "göktop": {"type": "göktop", "speed": 1, "lives": 3, "grant": 2, "bigger": True},
  "hapshu fire": {"type": "hapshu fire", "speed": 1, "lives": 1, "grant": 2, "bigger": False},
  "yaltop": {"type": "yaltop", "speed": 1, "lives": 3, "grant": 2, "bigger": True},
  
  "hootin-kabloo": {"type": "hootin-kabloo", "speed": 7, "lives": 20, "grant": 10, "bigger": True},
  
  "pal": {"type": "pal", "speed": 0, "lives": 1, "grant": 0, "bigger": False},
}

languages = {
  "TR": {" 1. Draw the Numar ": " 1. Numarı çiz " ," 2. Then, draw the sun ": " 2. Sonra, güneşi çiz "," 3. Finally, get the sun! ": " 3. Sonunda, güneşi al! ",},
  "EN": {" 1. Draw the Numar ": " 1. Draw the Numar " ," 2. Then, draw the sun ": " 2. Then, draw the sun "," 3. Finally, get the sun! ": " 3. Finally, get the sun! ",}
}

text_pages = ["   ", "  Numar walked away from the forest\ninto the city. ", " Firefly Pal: \"Hey Numar!||||| I have\na request for you... ", " I have a friend\nleft in Industry Blitz. ", " Could you save him?\", ||||||||||Pal asked...||||||||||\n\"His name is Kyo\" ", " \"Sure, I will give you a hand.\n||||||||||When you see a firefly on your way,\n|||||know that it is from me! |||||It grants\nyou health points.\" ", "   ", " Hoot-Hoot was crying alone.|||||||||\nHoot-Hoot: ||| \"Mom...|||||| Mom...||||||\nsomeone got me...\"||||||||||||\n???: |||\"Who did this to you!?\" ", " Hoot-Hoot:||| \"A monster!|||\nA blue gray monster!|||\nIt was Numar!\" ", " ???: |||\"Numar... ||||||Numar... |||||\nRest assured.\n||||||I'll remember this name.\" ",
              "   ", "  Pal: \"I got the key of the\nlock to your cage\"\n||||||||||\"Lambda had it in store for\nhimself.\" ", " PAL UNLOCKS THE CAGE ", " Kyo: \"Thank you guys! Now I\nam free!\".\n||||||||||\"I will tell my little brother Kiki\nabout you two\" ", "\"O||h||| n|||o|||.|||.|||.|||\"\n\"There is a magician monster\nright above the clouds.\n||||||||||He took Kiki away...!\" ", "   ",
              "   ", "  Nox: \"NOOOOOOOO!!!\" ", " \" ...P|||L|||E|||A|||S|||E||| S|||P|||A|||R|||E||| M|||E|||!\nI| a|m| b|e|g|g|i|n|g| y|o|u|!|\nI| w|o|n't| d|o| i|t| a|g|a|i|n|!|!\" ", " ... ", " \"Oh,||||| I know! |||||I will |||||.|||.|||.||| uhh.|||.|||.||| set Kiki\nfree! |||||The little brother of Kyo!\" ", " ... ", " \"But on one conditio- ||||||||||I mean...\n||||||||||I really need your help!|||||\nSomewhere close from here is\nan ave who took all my goods.\" ", " Nox: \"If you took me down\nthen there is no one who I know\nyou cannot beat!\n||||||||||You can do it,||||| please!!\" ", "   ",
              "   ", "  Kyo: \"Kiki~!\"\n||||||||||\"KIKIII~!!\"\n||||||||||\"Are you around here??\" ", " \"Huh? Who was that just now?\" ", " \nKyo: \"Kiki! You're back!\" ", " Nox: \"HAHAHAHA! I FOOLED YOU\nWITH MY ACTING! ||||||||||Numar, you idiot!\n||||||||||I'll have you know\nI have never been taken down!!!\" ", " \"I let Kiki go so don't ya\ncome after me again, GOT IT!?\"\n||||||||||||||||||||\"Now I am off, byeee loseeer~!!\" ", " \nNumar was left all on her own. ",
              "   ", "  Pal:||| \"oh...|||||||||| Numar,|||||||||||| where are you?\" ", "   ", "   ", "   ", "   ", "   ", " \"Numaaaar!\" ", "\"NUMAAAAAAR!!\" ", "\n ???: |||||||||||| \"Did |||||| I |||||| just |||||| hear |||||||||||||||||| NUMAR!?\" ", " ???: ||| \"That ||||| MONSTER ||||| who hurt\nmy child Hoot-Hoot?!||||||||| \nI will bring her to book!||||||||| \nAnd I will keep you |||a hostage.\" ", "   ",
              "   ", "  Pal:||| \"Numar you're here!\nHootin-Kabloo kept me as a\nhostage, you saved me!\" ", " \"I was out looking for Kiki.\"\n\"Seems he's safe with Kyo now.\" ", " Hoot-Hoot:||||||||| \"Mom!|||||| Mom!|||\n|||||||||         They got away!\" ", " Hootin-Kabloo: |||\"It's okay,||||||     \nthere'll definitely be a next time\" ", " Nox: ||||||\"Did I really get help.|||.|||.|||\"\n||||||||||||||||||\".|||.|||.|||from||| someone||||||||| who||||||\noverpowered|||||| me!?\" ", "   ", " \"You |||petty||| Numar!|||||||||||| the game\nhasn't even begun!!||||||||| I'll show you\nwhen we're facing off again.\"\n||||||||||||\"HAHAHAHAHAAA!!!\" ", "   "]

language = "EN"

class Main:
  def __init__(self):
    print("Starting Game...")
    print("By Tunari! No rights reserved")
    pygame.mixer.music.load("Sounds/tracks/Green Youth.mp3")
    #pygame.mixer.music.load("Sounds/tracks/Numar and Pal.mp3")
    pygame.mixer.music.play(1, 0.0)
    #pygame.mixer.music.set_volume(0)
    self.selected_save = ""
    self.saving_works = True
    self.scrollx = 0
    self.lock_scroll = False
    self.tiles = []
    self.actors = []
    self.collectibles = []
    self.projectiles = []
    self.player = Player(self)
    self.gamestate = 0
    self.timer = Timer()
    self.timer.tally = -logo.get_height()
    self.opening_timer = Timer()
    self.text_timer = Timer()
    self.slide_timer = Timer()
    self.full_dialogue = " "
    self.dialogue = " "
    self.selected_item_y = 0
    self.flash_timer = Timer()
    self.congratulations_text_flash_timer = Timer()
    self.start = False
    self.set_flash = False
    self.set_long_flash = False
    self.available_to_flash = False
    self.transport_timer = Timer()
    self.map = []
    self.track = ""
    self.hp_it = 0
    self.hp_it_timer = Timer()
    self.shakex = 0
    self.waterfall_bg_timer = Timer()
    self.kyo_panic_timer = Timer()
    self.kyo_cage_swing_timer = Timer()
    self.snow_timer = Timer()
    self.snow_timer2 = Timer()
    self.snowflakes1 = []
    self.snowflakes2 = []
    self.cs_timer = Timer()
    self.immobilize = False
    self.stop_motion = False
    self.boss_complete = False
    self.bonus_complete = False
    self.page = -1
    self.grabbed_sun_in_hub = False
    self.scrolly = 0
    self.twinkle_timer = Timer()
    self.shooting_star_timer = Timer()
    self.black_screen_timer = Timer()
    #pygame.mixer.music.load("Sounds/tracks/Numar and Pal.mp3"); pygame.mixer.music.play(-1, 0.0); self.gamestate = 3; self.page = 44; self.selected_save = "save1"
    #self.load_map("level1"); self.player.rect = pygame.Rect((2500, 75), (16, 16)); self.player.movement = [0, 0]; self.player.transport_to_level = []; self.transport_timer.reset(); self.scrollx = 2000
  
  def update(self):
    if self.gamestate == 0: self.menu()
    if self.gamestate == 1 and self.map != "outro": self.gameplay()
    if self.gamestate == 2: self.level(self.player.transport_to_level)
    if self.gamestate == 3: self.scroll_pages()
    if self.gamestate == 4: self.cutscene("numar fall", 83)
    if self.gamestate == 5: self.resetting_black_screen()
    if self.set_flash: self.flash(screen)
    if self.set_long_flash: self.long_flash(screen)
    if self.gamestate == 1 and self.map == "outro": self.gameplay()
    run()

  def menu(self):
    screen.blit(logo, ((WIDTH / 2) - (logo.get_width() / 2), self.timer.tally))
    self.selected_save = ""; self.scrollx = 0; self.scrolly = 0
    if self.opening_timer.tally >= 50:
      self.available_to_flash = True
      screen.blit(retrofontsmall.render(f"By Tunari! No rights reserved", False, "Black"), (5, HEIGHT - 16))
      for index, item in enumerate([("Enter Save 1", "save1"), ("Enter Save 2", "save2")]):
        if index == self.selected_item_y:
          text = retrofont.render(f"> {item[0]} <", False, "Black")
          screen.blit(text, ((WIDTH / 2) - (text.get_width() / 2), 250 + (index * 40)))
          self.selected_save = item[1]; self.player = Player(self, self.player.suns)
        else:
          text = retrofontmedium.render(item[0], False, "Black")
          screen.blit(text, ((WIDTH / 2) - (text.get_width() / 2), 250 + (index * 40)))

    screen.blit(pygame.image.load(f"Assets/cutscene/opening/{self.opening_timer.count(5 - int(self.opening_timer.tally > 27) * 2, 55, 1)}.png"), ((minint(self.opening_timer.tally, 27) - 27) * 10, -30))
    if self.opening_timer.time == 1:
      if self.opening_timer.tally == 1: self.full_dialogue = languages[language][" 1. Draw the Numar "]; self.text_timer.reset(); self.dialogue = ""
      if self.opening_timer.tally == 11: self.full_dialogue = languages[language][" 2. Then, draw the sun "]; self.text_timer.reset(); self.dialogue = ""
      if self.opening_timer.tally == 24: self.full_dialogue = languages[language][" 3. Finally, get the sun! "]; self.text_timer.reset(); self.dialogue = ""
      if self.opening_timer.tally == 43: self.full_dialogue = " "; self.text_timer.reset(); self.dialogue = ""
    self.dialogue += self.full_dialogue[self.text_timer.count(1, len(self.full_dialogue) - 1, 0)]
    screen.blit(retrofont.render(self.dialogue, False, "Black"), ((WIDTH / 2) - (retrofont.render(self.full_dialogue, False, "Black").get_width() / 2), 100))
    if self.timer.tally > 70: self.timer.time = -self.timer.time / 1.4; self.timer.tally += self.timer.time
    if self.timer.tally < 71 and self.opening_timer.tally >= 41: self.timer.time += 0.7; self.timer.tally += self.timer.time
    if (not pygame.mixer.music.get_busy()) and (not self.player.finished): pygame.mixer.music.load("Sounds/tracks/Green Youth 2.mp3"); pygame.mixer.music.play(-1, 0.0)

    self.controls()

  def gameplay(self):
    main.available_to_flash = False
    if levels[self.map]["track"] == "Sunny Day" and float(self.map[5:]) < 17:
      screen.blit(humid_sky, (0, 0)); #screen.fill((50, 200, 230)); pygame.draw.rect(screen, (0, 100, 200), ((0, HEIGHT / 4), (WIDTH, HEIGHT / 4))); pygame.draw.rect(screen, (0, 75, 175), ((0, HEIGHT / 2.5), (WIDTH, HEIGHT / 2.5)))
      for x in range(15): screen.blit(mountains, ((x * WIDTH) - (self.scrollx / 4), 0)); screen.blit(eval(f"poles{betweenint(x, 1, 2)}"), ((x * WIDTH) - (self.scrollx / 2), 0))
    elif levels[self.map]["track"] == "Night-Night" and float(self.map[5:]) < 17:
      screen.fill((0, 10, 40))
      for hue in range(12): pygame.draw.rect(screen, (0, 0, abs(0 - (hue * (255 / 18)))), ((0, (hue * 24)), (WIDTH, HEIGHT)))
      screen.blit(stars1, (0, 0)); screen.blit(moon, (75, 0))
    elif levels[self.map]["track"] == "Gather the Suns (Bonus Stage Remix)":
      screen.blit(gtsbg, (0, 0))
      if self.bonus_complete and not self.immobilize: self.immobilize = True; pygame.mixer.music.load("Sounds/tracks/Spark Spark Spark.mp3"); pygame.mixer.music.play(1, 0.0)
      else: screen.blit(retrofontmedium.render("Gather the Suns", False, "White"), (90, 2))
    elif self.map == "hub1": screen.blit(humid_sky, (0, 0)); screen.blit(pygame.image.load(f"Assets/waterfall{self.waterfall_bg_timer.keep_count(2, 3, 1)}.png").convert_alpha(), (0, 0)); self.hp_it = 0; self.player.wealth = 0; self.lock_scroll, self.boss_complete, self.bonus_complete = False, False, False; #pygame.draw.rect(screen, (0, 125, 200), ((0, HEIGHT / 4), (WIDTH, HEIGHT / 4))); pygame.draw.rect(screen, (0, 100, 175), ((0, HEIGHT / 2.5), (WIDTH, HEIGHT / 2.5))), ((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))
    if levels[self.map]["track"] == "Industry Blitz":
      screen.fill((25, 0, 50)); pygame.draw.rect(screen, (35, 0, 70), ((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))); pygame.draw.rect(screen, (50, 0, 100), ((0, HEIGHT / 1.66), (WIDTH, HEIGHT / 1.66))); 
      for x in range(15): screen.blit(eval(f"buildings{betweenint(x, 1, 3)}"), (x * WIDTH, 100)); screen.blit(eval(f"spotlight{betweenint(x, 1, 2)}"), (((x * (WIDTH * 4)) + WIDTH) - (self.scrollx / 2), 0)); screen.blit(eval(f"buildings{betweenint(x, 1, 3)}"), ((x * WIDTH) - (self.scrollx / 2), 0))
    if levels[self.map]["track"] == "Lushy Assence":
      screen.blit(magic_bg, (0, 0))
      for x in range(15): screen.blit(overlay, ((x * (WIDTH * 2)) - (self.scrollx), 0))
    if levels[self.map]["track"] == "Dry Snow":
      screen.blit(sky, (0, 0))
      if self.map == "level16.1": screen.blit(fog, (0, 0))
      for x in range(15): screen.blit(clouds1, ((x * WIDTH) - (self.scrollx / 6), 0)); screen.blit(clouds2, ((x * WIDTH) - (self.scrollx / 4), 0)); screen.blit(clouds3, ((x * WIDTH) - (self.scrollx / 2), 0))
    elif self.map == "hub2": screen.fill((25, 0, 50)); pygame.draw.rect(screen, (35, 0, 70), ((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))); pygame.draw.rect(screen, (50, 0, 100), ((0, HEIGHT / 1.66), (WIDTH, HEIGHT / 1.66))); screen.blit(buildings1, (0, 0)); self.hp_it = 0; self.player.wealth = 0; self.lock_scroll, self.boss_complete, self.bonus_complete = False, False, False
    elif self.map == "hub3": screen.blit(magic_bg, (0, 0)); self.hp_it = 0; self.player.wealth = 0; self.lock_scroll, self.boss_complete, self.bonus_complete = False, False, False
    elif self.map == "hub4": screen.blit(sky, (0, 0)); screen.blit(stone_mountains, (0, 0)); self.hp_it = 0; self.player.wealth = 0; self.lock_scroll, self.boss_complete, self.bonus_complete = False, False, False
    elif self.map == "hub5": screen.blit(sunset, (0, 0)); self.hp_it = 0; self.player.wealth = 0; self.lock_scroll, self.boss_complete, self.bonus_complete = False, False, False
    if "level" in self.map and float(self.map[5:]) >= 17 and (levels[self.map]["track"] == "Sunny Day" or levels[self.map]["track"] == "Night-Night"):
      if levels[self.map]["track"] == "Sunny Day": screen.blit(sky, (0, 0))
      if levels[self.map]["track"] == "Night-Night":
        screen.fill((0, 10, 40))
        for hue in range(12): pygame.draw.rect(screen, (0, 0, abs(0 - (hue * (255 / 18)))), ((0, (hue * 24)), (WIDTH, HEIGHT)))
        screen.blit(stars1, (0, 0)); screen.blit(moon, (75, 0))
      screen.blit(taiga_mountains, (75 - (self.scrollx / 100), 0))
      for x in range(15): screen.blit(taiga_forest2, ((x * WIDTH) - (self.scrollx / 4), 0)); screen.blit(taiga_forest1, ((x * WIDTH) - (self.scrollx / 2), 0))

    if self.map == "hub4" or levels[self.map]["track"] == "Dry Snow":
      if self.snow_timer2.timer(1): self.snowflakes2.append(SnowflakeFar())
      for snow in self.snowflakes2:
        snow.update()
        if snow.rect.x < 0: self.snowflakes2.remove(snow); del snow
        elif snow.rect.y > HEIGHT: self.snowflakes2.remove(snow); del snow
    
    if self.map == "outro":
      screen.blit(night_sky, (0, -650 - self.scrolly)); screen.blit(credits_text, (20, (-650 + HEIGHT) - self.scrolly)); self.scrollx = 0
      screen.blit(pygame.image.load(f"Assets/twinkle star{self.twinkle_timer.keep_count(FPS / 4, 5, 1)}.png").convert_alpha(), (0, -650 - self.scrolly))
      if pygame.mixer.music.get_pos() > 26000 and self.shooting_star_timer.tally < 9: screen.blit(pygame.image.load(f"Assets/shooting star{self.shooting_star_timer.count(2, 9, 1)}.png").convert_alpha(), (0, -650 - self.scrolly))
      if pygame.mixer.music.get_pos() > 27250:
        flash = abs(self.flash_timer.count(1, 90, 1) * 3.75)
        screen.fill((maxint(flash, 255), maxint(flash, 255), maxint(flash, 255)), special_flags=pygame.BLEND_RGBA_SUB)
      screen.blit(logo_wtm, ((WIDTH / 2) - (logo.get_width() / 2), (-650 + ((HEIGHT / 2) - (logo.get_height() / 2))) - self.scrolly))
      if pygame.mixer.music.get_pos() > 3550 and self.scrolly > -650: self.scrolly -= 1
      if not pygame.mixer.music.get_busy():
        screen.blit(retrofontsmall.render(f"You gathered {self.player.suns} suns in total!", False, "Yellow"), (5, HEIGHT - 16)); screen.blit(tyfp_text, ((WIDTH / 2) - (tyfp_text.get_width() / 2), 265)); screen.blit(tbc_text, ((WIDTH / 2) - (tbc_text.get_width() / 2), 305))
        if k_start: self.black_screen_timer.reset(); saves[self.selected_save]["World"] = "hub1"; saves[self.selected_save]["Suns"] = 0; saves[self.selected_save]["Page"] = -1; self.gamestate = 5

    if self.map == "level8.1": screen.blit(pygame.image.load(f"Assets/kyo in cage{self.kyo_panic_timer.keep_count(2, 3, 1)}.png").convert_alpha(), ((WIDTH - main.scrollx) + 75 + self.kyo_cage_swing_timer.oscillate(FPS / 1.5, 4, 1), 0))
    for tile in [tile for tile in self.tiles if (tile.rect.x - main.scrollx < WIDTH and tile.rect.x - main.scrollx > -40 or tile.speed != 0)]: tile.update()
    for collectible in self.collectibles:
      collectible.update()
      if "hub" in self.map and self.grabbed_sun_in_hub and collectible.type == "sun": self.collectibles.remove(collectible)
    for actor in self.actors:
      actor.update()
      #print(actor.rect.y, actor.rect.x)
      if actor.delete: self.actors.remove(actor)
    for proj in self.projectiles:
      if proj.alive: proj.update()
      else: self.projectiles.remove(proj)
      if (not proj.friendly) and proj.rect.colliderect(self.player.rect) and not self.boss_complete and not proj.hit:
        self.player.lives -= 1; proj.hit = True; main.player.protection_timer.reset(); main.player.protection_timer.tally = 0; main.stop_motion, main.immobilize = True, True; pygame.mixer.music.set_volume(0.3); hurt_sfx.play(); main.shakex = 3
        if isinstance(proj, FrostBreath) and self.player.state != "frozen": self.player.state = "frozen"; self.player.x_vel -= 6; self.player.a_hits = 6
      if (not proj.friendly) and isinstance(proj, Fire) and not proj.rect.colliderect(self.player.rect): proj.hit = False
    if self.player.protection_timer.tally <= 7: screen.fill((200, 200, 200), special_flags=pygame.BLEND_RGBA_SUB)
    self.player.update()
    
    if (not pygame.mixer.music.get_busy()) and (not self.player.finished) and "hub" in self.map: pygame.mixer.music.load("Sounds/tracks/Green Youth 2.mp3"); pygame.mixer.music.play(-1, 0.0)
    if (pygame.mixer.music.get_pos() > 1850 or self.player.dance_timer.tally > 40) and self.player.state == "dance":
      if self.player.wealth > 0: self.player.wealth -= 1; self.player.suns += 1; blip_sfx.play()
      elif self.player.lives - self.hp_it > 0 and self.hp_it_timer.timer(FPS / 6.5): self.hp_it += 1; self.player.suns += 5; hp_it_sfx.play()
    
    if self.map == "hub4":
      if self.snow_timer.timer(2): self.snowflakes.append(Snowflake())
      for snow in self.snowflakes:
        snow.update()
        if snow.rect.x < 0: self.snowflakes.remove(snow); del snow
        elif snow.rect.y > HEIGHT: self.snowflakes.remove(snow); del snow
    
    if self.map != "outro": self.draw_ui(); self.scrolly = 0

    for tile in self.tiles:
      if tile.id == "1w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 100", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 100: self.tiles.remove(tile)
      if tile.id == "2w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 200", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 200: self.tiles.remove(tile)
      if tile.id == "3w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 300", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 300: self.tiles.remove(tile)
        
      if tile.id == "4w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 500", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 500: self.tiles.remove(tile)
      if tile.id == "5w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 600", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 600: self.tiles.remove(tile)
      if tile.id == "6w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 700", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 700: self.tiles.remove(tile)

      if tile.id == "7w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 900", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 900: self.tiles.remove(tile)
      if tile.id == "8w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1000", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1000: self.tiles.remove(tile)
      if tile.id == "9w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1100", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1100: self.tiles.remove(tile)

      if tile.id == "!w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1300", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1300: self.tiles.remove(tile)
      if tile.id == "@w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1400", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1400: self.tiles.remove(tile)
      if tile.id == "#w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1500", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1500: self.tiles.remove(tile)

      if tile.id == "$w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1700", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1700: self.tiles.remove(tile)
      if tile.id == "%w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1800", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1800: self.tiles.remove(tile)
      if tile.id == "^w":
        screen.blit(sun, ((tile.rect.x - self.scrollx) + 75, 10)); screen.blit(pygame.transform.rotate(retrofont.render(f"{self.player.suns} / 1900", False, "White"), -90), ((tile.rect.x - self.scrollx) + 72, 35))
        if self.player.suns >= 1900: self.tiles.remove(tile)

  def level(self, level):
    for x in range(2):
      for y in range(2): screen.blit(pygame.image.load(f"Assets/sun bg {self.map[-1:]}.png").convert_alpha(), ((0 - (x * (HEIGHT - 96)) + self.transport_timer.tally, 0 - (y * (HEIGHT - 96)) + self.transport_timer.tally)))
    self.transport_timer.count(1, 7.2 * FPS, 0)
    if self.transport_timer.tally == 1: pygame.mixer.music.load("Sounds/tracks/The Twinkle Rhythm.mp3"); pygame.mixer.music.play(1, 0.0); self.set_flash = False; self.available_to_flash = False
    screen.blit(retrofontbig.render(levels[level]["name"], False, "White"), (10, 75))
    if self.transport_timer.tally >= 2.7 * FPS: screen.blit(retrofontsmall.render(levels[level]["desc"], False, "White"), (5, 125))
    if self.transport_timer.tally >= 7.2 * FPS:
      screen.blit(retrofont.render("Push START", False, "Yellow"), (100, 275))
      if k_start:
        self.set_flash = True; self.available_to_flash = True
        if self.start: self.gamestate = 1; self.load_map(level); self.player.rect = pygame.Rect((50, 150), (10, 16)); self.player.movement = [0, 0]; self.player.transport_to_level = []; self.transport_timer.reset(); self.scrollx = 100; self.immobilize = False; self.player.state = "idle"; self.player.frame = 1; self.player.energy = 24.0 #50, 100
    
  def draw_ui(self):
    pygame.draw.rect(screen, (255, 125, 0), ((0, 0), (80, HEIGHT)))
    pygame.draw.rect(screen, (240, 230, 0), ((0, 0), (80, HEIGHT)), 2)
    screen.blit(retrofontmedium.render("Lives:", False, (240, 230, 125)), (5, 15))
    for live in range(self.player.lives):
      pygame.draw.rect(screen, (240, 230, 125), ((7, 40 + live * 10), (20, 8)), border_radius = 2)
    for live in range(self.hp_it):
      pygame.draw.rect(screen, (150, 100, 205), ((7, 40 + live * 10), (20, 8)), border_radius = 2)
    screen.blit(retrofontmedium.render("Weary:", False, (240, 230, 125)), (5, 155))
    for energy in range(round(self.player.energy)):
      pygame.draw.rect(screen, (240, 230, 125), ((4 + energy * 3, 180), (2, 20)), border_radius = 2)
    screen.blit(retrofontsmall.render("SCORE", False, (240, 230, 125)), (5, 235))
    wealth_text = retrofontbig.render(str(self.player.wealth), False, (240, 230, 125))
    screen.blit(wealth_text, (42 - wealth_text.get_width() / 2, 250))
    screen.blit(retrofontsmall.render("SUNS", False, (240, 230, 125)), (5, 295))
    wealth_text = retrofontbig2.render(str(self.player.suns), False, (240, 230, 125))
    screen.blit(wealth_text, (42 - wealth_text.get_width() / 2, 312))

    if levels[self.map]["track"] == "Gather the Suns (Bonus Stage Remix)" and self.bonus_complete:
      if self.congratulations_text_flash_timer.wait(FPS / 15) or (pygame.mixer.music.get_pos() > 1000 or not pygame.mixer.music.get_busy()): screen.blit(congratulations_text, ((WIDTH / 2) - (congratulations_text.get_width() / 2), 50))
      screen.blit(push_start_text, ((WIDTH / 2) - (push_start_text.get_width() / 2), 85)); self.player.movement[0] = 0; self.player.finished = True
      if k_start: self.dialogue = ""; self.full_dialogue = ""; self.page += 1; self.full_dialogue = text_pages[self.page]; self.gamestate = 3; pygame.mixer.music.load(f"Sounds/tracks/Numar and Pal.mp3"); pygame.mixer.music.play(-1, 0.0); self.player.finished = False
  
  def controls(self):
    global k_a
    if k_up: self.selected_item_y -= 1; click_sfx.play()
    if k_down: self.selected_item_y += 1; click_sfx.play()
    if self.selected_item_y >= 2: self.selected_item_y = 0
    if self.selected_item_y == -1: self.selected_item_y = 1

    if self.gamestate == 0 and k_start and self.opening_timer.tally >= 50:
      if self.track == "Gather the Suns (Bonus Stage Remix)" and self.bonus_complete:
        self.set_flash = True
        if self.start: self.gamestate = 3
      else:
        self.set_flash = True
        if self.start: self.gamestate = 1; self.load_map(saves[self.selected_save]["World"]); self.player.suns = saves[self.selected_save]["Suns"]; self.page = saves[self.selected_save]["Page"]

  def flash(self, screen=screen):
    global k_start
    flash = abs(self.flash_timer.oscillate(1, 10, 1) * 30)
    screen.fill((maxint(flash, 255), maxint(flash, 255), maxint(flash, 255)), special_flags=pygame.BLEND_RGBA_SUB)
    if flash < 10:
      k_start = False
      if self.start: self.set_flash, self.start = False, False
    if flash >= 300: self.start = True

  def long_flash(self, screen=screen):
    global k_start
    flash = abs(self.flash_timer.oscillate(1, 60, 1) * 5)
    screen.fill((maxint(flash, 255), maxint(flash, 255), maxint(flash, 255)), special_flags=pygame.BLEND_RGBA_SUB)
    if flash < 10:
      k_start = False
      if self.start: self.set_long_flash, self.start = False, False
    if flash >= 300: self.start = True

  def load_map(self, map):
    self.tiles.clear()
    self.actors.clear()
    self.collectibles.clear()
    self.projectiles.clear()
    self.scrolly = 0
    for minimapx, minimap in enumerate(levels[map]["layout"]):
      for y, mapx in enumerate(minimap):
        for x, tile in enumerate(mapx):
          if tiles[tile]["entity"] != "-": self.actors.append(Monster(monsters[tiles[tile]["entity"]], x + (minimapx * 22), y))
          if tiles[tile]["collectible"] != "-": self.collectibles.append(Collectible(collectibles[tiles[tile]["collectible"]]["type"], x + (minimapx * 22), y))
          if tile != "  ":
            try: floor = map[y - 1][x] == "  " and map[y - 2][x] == "  "
            except: floor = False
            self.tiles.append(Tile(tiles[tile]["name"], x + (minimapx * 22), y, floor, tiles[tile]["transport to level"], tiles[tile]["solid"], tiles[tile]["flat"], tiles[tile]["move_x"], tiles[tile]["move_y"], tile == " b" or tile == "zb", tile == " m" or tile == "cm" or tile == "zm", id=tile))

    track = levels[map]["track"]
    if levels[map]["mode"] != "cutscene":
      if track != None and not "." in map and not "hub" in map: pygame.mixer.music.load(f"Sounds/tracks/{track}.mp3"); pygame.mixer.music.play(-1, 0.0); self.scrollx = 150
    else: pygame.mixer.music.load(f"Sounds/tracks/{track}.mp3"); pygame.mixer.music.play(1, 0.0)

    self.snow_timer = Timer()
    self.snowflakes = []
    self.footholds = [tile for tile in self.tiles if tile.floor]
    self.map = map
    self.track = track
    self.immobilize = False

  def scroll_pages(self):
    if self.page == 50: self.page = 51; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.5)
    if self.page == 38: self.page = 39; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.2)
    if self.page == 37: self.page = 38; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.2)
    if self.page == 36: self.page = 37; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.2)
    if self.page == 35: self.page = 36; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.2)
    if self.page == 34: self.page = 35; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.8)
    if self.page == 32: self.page = 33; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.5)
    if self.page == 16: self.page = 17; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.4)
    if self.page == 25: self.page = 26; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.4)
    if self.page == 6: self.page = 7; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.5)
    if self.page == 10:
      self.set_long_flash = True
      if self.start: self.gamestate = 1; self.next_world("hub2"); saves[self.selected_save]["World"] = self.map; self.dialogue = ""; self.full_dialogue = ""
    elif self.page == 15:
      self.set_long_flash = True
      if self.start: self.gamestate = 1; self.next_world("hub3"); saves[self.selected_save]["World"] = self.map; self.dialogue = ""; self.full_dialogue = ""
    elif self.page == 24:
      self.set_long_flash = True
      if self.start: self.gamestate = 1; self.next_world("hub4"); saves[self.selected_save]["World"] = self.map; self.dialogue = ""; self.full_dialogue = ""
    elif self.page == 43:
      self.set_flash = True
      if self.start: self.gamestate = 4; pygame.mixer.music.stop(); self.dialogue = ""; self.full_dialogue = ""
    elif self.page == 52:
      self.set_long_flash = True; pygame.mixer.music.stop()
      if self.start: self.gamestate = 1; self.load_map("outro"); saves[self.selected_save]["World"] = self.map; self.dialogue = ""; self.full_dialogue = ""
    else:
      if (k_start or k_a) and not self.start and len(self.dialogue) >= len(self.full_dialogue): self.page += 1; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""
      letter = self.full_dialogue[self.text_timer.count(1, len(self.full_dialogue) - 1, 0)]
      if letter != "|": self.dialogue += letter
    try: screen.blit(pygame.image.load(f"Assets/slide/page{self.page}.png").convert_alpha(), (0, 0))
    except:
      try: screen.blit(pygame.image.load(f"Assets/slide/page{self.page}_{self.slide_timer.nonstopcount(3, 1)}.png").convert_alpha(), (0, 0))
      except:
        try: self.slide_timer.reset(); screen.blit(pygame.image.load(f"Assets/slide/page{self.page}_{self.slide_timer.nonstopcount(3, 1)}.png").convert_alpha(), (0, 0))
        except: pass
    screen.blit(retrofontsmall.render(self.dialogue, False, "White"), ((WIDTH / 2) - (retrofontsmall.render(self.full_dialogue.replace("|", ""), False, "White").get_width() / 2), 5))
    if self.page == 44: self.page = 45; self.full_dialogue = text_pages[self.page]; self.text_timer.reset(); self.dialogue = ""; clock.tick(FPS / 1.8)

  def cutscene(self, scene, frames):
    screen.blit(pygame.image.load(f"Assets/cutscene/{scene}/{self.cs_timer.count(3, frames, 1)}.png").convert_alpha(), (0, 0))
    
    if self.cs_timer.tally == frames:
      self.set_flash = True
      if self.start: self.gamestate = 1; self.next_world("hub5"); saves[self.selected_save]["World"] = self.map

    if self.cs_timer.tally == 40 and self.cs_timer.time == 1 and self.gamestate == 4: fly_sfx.play()
    if self.cs_timer.tally == 45 and self.cs_timer.time == 1 and self.gamestate == 4: fall_sfx.play()
    if self.cs_timer.tally == 59 and self.cs_timer.time == 1 and self.gamestate == 4: crash_sfx.play()

  def next_world(self, world): self.gamestate = 1; self.load_map(world); self.player.rect = pygame.Rect((50, 150), (10, 16)); self.player.movement = [0, 0]; self.player.transport_to_level = []; self.transport_timer.reset(); self.scrollx = 10; pygame.mixer.music.load(f"Sounds/tracks/Green Youth 2.mp3"); pygame.mixer.music.play(-1, 0.0)
  
  def resetting_black_screen(self):
    screen.fill("Black")
    if self.black_screen_timer.timer(FPS): self.__init__()

  def save_game(self):
    try:
      in_ = open("Saves/memory_card/savefile.txt", "r")
      if self.gamestate != 3:
        saves[self.selected_save]["Suns"] = self.player.suns
        if "hub" in self.map: saves[self.selected_save]["World"] = self.map
        saves[self.selected_save]["Page"] = self.page
      try:
        with open("Saves/memory_card/savefile.txt", "w") as out_: json.dump(saves, out_); return 0
      except FileNotFoundError: print("Save file not found."); return 1
      except EOFError: print("Save file is empty or invalid."); return 1
      except Exception as e: print("An error occurred in saving:", str(e)); return 1
    except KeyError: pass
  
  def quit(self): self.save_game(); pygame.quit(); exit()


class Player:
  def __init__(self, main, suns=0):
    self.main = main
    self.rect = pygame.Rect((50, 200), (10, 16))
    self.movement = [0, 0]
    self.speed = 3
    self.timer = Timer()
    self.flipped = False
    self.state = "idle"
    self.frame = 1
    self.deceive_x = 0
    self.y_vel = 0
    self.jumping_vel = 0
    self.airtimer = 0
    self.on_ice = False
    self.x_vel = 0
    self.terminal_x_vel = 5
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.enemy_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    #self.image = pygame.transform.flip(pygame.image.load(f"Assets/numar/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False)
    self.protection_timer = Timer()

    self.wealth = 0
    self.suns = suns
    self.lives = 10
    self.energy = 24.0
    self.magic_applied = False
    self.numbers = []
    self.dead_animation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, -10, -15, -20, -23, -20, -13, -7, -2, 2, 8, 15, 19, 28, 40, 55, 70, 90, 110, 125, 150, 175, 200, 230, 260, 300, 350, 400]
    self.alive = True
    self.dead_animation_timer = Timer()
    self.finished = False
    self.dance_timer = Timer()
    self.dance_animation = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    self.waiting_timer = Timer()
    self.waiting2_timer = Timer()
    self.waiting_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1]
    self.transport_to_level = []
    self.flash_timer = Timer()
    self.a_hits = 6
    self.fall_sound_played = False

  def update(self):
    global k_start
    #pygame.draw.rect(screen, "Red", self.rect, 2)
    if main.map == "outro": self.state, self.frame = "stargaze", 1; main.immobilize = True; self.rect.x, self.rect.y = 80, 256

    try: self.image = pygame.transform.flip(pygame.image.load(f"Assets/numar/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False)
    except: self.frame = 1
    if self.protection_timer.tally >= FPS - 1 or self.flash_timer.wait(FPS / 8): screen.blit(self.image, (self.deceive_x + (73 if main.map != "outro" else 0), (self.rect.y - main.scrolly) + self.dead_animation[self.dead_animation_timer.tally]))

    self.deceive_x = round(self.rect.x - main.scrollx)
    if self.rect.y < -8: self.rect.y = -8

    colliding_tiles = []
    for tile in main.tiles:
      if self.rect.colliderect(tile.rect):
        colliding_tiles.append(tile.type)
        if tile.transport_to_level != None: self.transport_to_level = tile.transport_to_level

    if "door1" in colliding_tiles:
      main.set_flash = True; main.available_to_flash = True; k_start = True
      if main.start: self.gamestate = 1; main.load_map(self.transport_to_level); self.movement = [0, 0]; self.transport_to_level = []; main.transport_timer.reset()

    try: end_point = (((len(levels[main.map]["layout"]) * 22) + 3) * 16)
    except: end_point = WIDTH

    if not main.lock_scroll:
      if main.scrollx < end_point - WIDTH:
        if self.deceive_x > 205 and self.on_ice: main.scrollx += 1
        if self.deceive_x > 195 and self.on_ice: main.scrollx += 2
        if self.deceive_x > 185: main.scrollx += 3
        elif self.deceive_x > 175: main.scrollx += 1
      if main.scrollx > 0:
        if self.deceive_x < 120 and self.on_ice: main.scrollx -= 1
        if self.deceive_x < 130 and self.on_ice: main.scrollx -= 2
        if self.deceive_x < 140: main.scrollx -= 3
        elif self.deceive_x < 150: main.scrollx -= 1

    if self.x_vel < -self.terminal_x_vel: self.x_vel += 1
    if self.x_vel > self.terminal_x_vel: self.x_vel -= 1

    if self.alive:
      if self.on_ice and (self.collision["bottom"] or not k_a): self.movement[0] = self.x_vel
      if not k_a and not (self.state == "shot" or self.magic_applied):
        self.y_vel += 2
        if self.y_vel > 10: self.y_vel = 10
        self.movement[1] = self.y_vel
        if self.collision["bottom"]: self.y_vel, self.airtimer = 0, 0
        elif self.collision['top']: self.y_vel, self.airtimer = 0, 10
        else: self.airtimer += 2
        if self.on_ice:
          if self.collision["right"] or self.collision["left"]: self.x_vel = 0
          if self.x_vel < 1 and self.x_vel > -1 and not self.collision["bottom"]: self.movement[0] = self.on_ice = False

      if not main.boss_complete: self.rect, self.enemy_collision = self.get_hit(self.rect, self.movement, main.actors)
      self.rect, self.collision = self.move(self.rect, self.movement, main.tiles)
      self.pickup(self.rect, main.collectibles)
      #self.pickup(self.rect, [tile for tile in main.tiles if tile.coin])
      if self.lives <= 0: self.alive = False; 
    else:
      pygame.mixer_music.stop()
      self.dead_animation_timer.count(1, len(self.dead_animation) - 1, 0)
      self.state, self.frame = "defeat", 1
      if self.dead_animation_timer.tally == 25: cry_sfx.play()

    for number in self.numbers:
      if number.alive: number.update()
      else: self.numbers.remove(number)

    if self.rect.y > WIDTH and not "hub" in main.map:
      if not self.fall_sound_played and self.state != "defeat": fall_sfx.play(); self.fall_sound_played = True
      self.state, self.frame = "defeat", 1; self.y_vel = 4; self.movement[0] = 0; self.x_vel = 0
      screen.blit(you_fell_text, ((WIDTH / 2) - (you_fell_text.get_width() / 2) + 35, maxint(self.rect.y - HEIGHT, HEIGHT / 2) - 20))

    if self.state != "defeat" and not self.finished: self.controls()
    elif self.finished and not main.bonus_complete:
      self.movement = [0, 0]; self.x_vel = 0
      self.dance_timer.count(1, FPS, 0)
      if self.dance_timer.tally >= FPS - 1 and self.collision["bottom"]:
        if self.state != "dance": pygame.mixer_music.load("Sounds/tracks/Cherry Berry.mp3"); pygame.mixer_music.play(1, 0.0); self.timer.reset()
        self.state = "dance"; self.protection_timer.count(1, FPS, 0)
        self.frame = self.dance_animation[self.timer.keep_count(1, len(self.dance_animation) - 1, 0)]
        if self.lives - main.hp_it <= 0 and not pygame.mixer_music.get_busy(): main.set_flash = True; main.available_to_flash = True; k_start = True
        if main.start: self.state, self.frame = "jump", 1; self.timer.reset(); main.boss_complete = False; self.gamestate = 1; main.load_map(levels[main.map]["win"]); self.rect = pygame.Rect((50, 160), (10, 16)); self.movement = [0, 0]; self.transport_to_level = []; main.transport_timer.reset(); main.scrollx = 25; pygame.mixer.music.load(f"Sounds/tracks/{levels[main.map]['track']}.mp3"); pygame.mixer.music.play(-1, 0.0); self.alive = True; self.lives = 10; self.dead_animation_timer.reset(); main.actors.clear(); self.finished = False; self.dance_timer.reset(); self.timer.reset(); main.hp_it_timer.reset(); main.lock_scroll, main.immobilize, main.boss_complete, main.bonus_complete, main.hp_it = False, False, False, False, 0; self.fall_sound_played = False
  
    if (self.transport_to_level != None and self.rect.y > HEIGHT * 1.5) or (self.dead_animation_timer.tally >= len(self.dead_animation) - 1):
      main.set_flash = True; main.available_to_flash = True; k_start = True
      if main.start:
        if "hub" in main.map: main.gamestate = 2
        else: self.state, self.frame = "jump", 1; self.timer.reset(); self.gamestate = 1; main.load_map(levels[main.map]["return"]); self.rect = pygame.Rect((50, 130), (10, 16)); self.movement = [0, 0]; self.transport_to_level = []; main.transport_timer.reset(); main.scrollx = 25; pygame.mixer.music.load(f"Sounds/tracks/{levels[main.map]['track']}.mp3"); pygame.mixer.music.play(-1, 0.0); self.alive, main.bonus_complete, self.lives = True, False, 10; self.dead_animation_timer.reset(); main.actors.clear(); main.lock_scroll, main.immobilize, main.boss_complete, main.bonus_complete, main.hp_it = False, False, False, False, 0; self.fall_sound_played = False
    
    if self.waiting_timer.tally > FPS * 3:
      self.state = "waiting"
      self.frame = self.waiting_animation[maxint(self.waiting2_timer.keep_count(1, 100, 0), len(self.waiting_animation) - 1)]

    if self.lives > 10: self.lives = 10

    if main.map == "outro": self.state, self.frame = "stargaze", 1; main.immobilize = True; self.rect.x, self.rect.y = 80, 256

  def controls(self):
    global k_a, k_down
    if not main.immobilize:
      if self.state != "frozen" or self.a_hits == 0:
        if (self.transport_to_level == [] or not "hub" in main.map) and not self.magic_applied:
          self.waiting_timer.count(1, FPS * 4, 1)
          if self.state != "dizzy":
            if k_right:
              if self.collision["bottom"]: self.x_vel += 0.25
              if self.energy < 24 and self.state != "fly": self.energy += 0.3
              self.movement[0] = self.speed; self.waiting_timer.reset(); k_down = False
              if self.state != "fly": self.state = "walk"; self.flipped = False
              if self.state == "walk": self.frame = self.timer.keep_count(2, 3, 1)
              if not self.collision["bottom"] and not self.state == "fly": self.state = "jump"; self.frame = 1
            elif k_left:
              if self.collision["bottom"]: self.x_vel -= 0.25
              if self.energy < 24 and self.state != "fly": self.energy += 0.3
              self.movement[0] = -self.speed; self.waiting_timer.reset(); k_down = False
              if self.state != "fly": self.state = "walk"; self.flipped = True
              if self.state == "walk": self.frame = self.timer.keep_count(2, 3, 1)
              if not self.collision["bottom"] and not self.state == "fly": self.state = "jump"; self.frame = 1
            else:
              self.movement[0] = 0
              if self.state != "fly":
                self.frame = 1
                if self.collision['bottom']: self.state = "idle"
                else: self.state = "jump"
                if self.energy < 24: self.energy += 0.4
              if self.state == "idle": self.frame = self.timer.keep_count(FPS, 3, 1); self.timer.reset()
            if k_up and not (self.collision["bottom"] and self.collision["top"]):
              self.waiting_timer.reset()
              if self.y_vel == 0 and self.collision['bottom'] and self.state != "fly": jump_sfx.play(); self.state = "jump"
              if self.state == "jump": self.timer.reset(); self.frame = 1; self.jumping_vel = -10
              if self.airtimer < 10: self.y_vel = self.jumping_vel
            else:
              if k_up: self.rect.y -= 5
              if k_down: self.rect.y += 5
            if k_a and self.rect.y > -32 and self.rect.y < WIDTH and self.energy > 0 and self.state != "defeat" and not self.collision["bottom"]:
              self.x_vel = 0; self.state = "fly"; self.frame = self.timer.keep_count(1, 3, 1); self.movement[1] = -2; self.speed = 1.5; self.y_vel = 0; self.waiting_timer.reset()
              if self.frame == 2: copter_sfx.play(); self.energy -= 0.9
            else:
              if self.energy <= 0: self.state = "dizzy"; self.timer.reset(); self.frame = 1; k_a = False
              self.speed = 3
              if self.state == "fly": self.state = "jump"; self.frame = 1; self.timer.reset()
          else:
            self.frame = 1; self.movement = [0, 0]; self.waiting_timer.reset(); k_a = False
            if self.energy < 24 and self.state != "fly": self.energy += 0.285
            if self.timer.timer(FPS * 2.75): self.state = "idle"; self.timer.reset()
        elif self.transport_to_level != []: self.movement = [0, 0]
      else:
        if k_a:
          self.a_hits -= 1; k_a = False; self.rect.y -= 2; self.movement[0] = -2; swing_sfx.play()
          if self.a_hits == 0: self.x_vel = 0
    elif not "hub" in main.map: self.movement = [0, 0]
    else: self.movement[0] = 0

  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]

    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if tile.transport_to_level == None:
        if tile.solid and not tile.flat:
          if movement[0] > 0:
            rect.right = tile.rect.left
            collision_type['right'] = True
          elif movement[0] < 0 and not tile.flat:
            rect.left = tile.rect.right
            collision_type['left'] = True
      elif "hub" in main.map: pygame.mixer.music.load("Sounds/tracks/E N G U L F.mp3"); pygame.mixer.music.play(1, 0.0); main.available_to_flash = True; self.transport_to_level = tile.transport_to_level; main.immobilize = True

    if self.state == "swivel": self.frame = self.timer.keep_count(2, 3, 1)
    if not main.lock_scroll: ss = 7
    else: ss = 0
    if self.magic_applied and self.state == "swivel": movement[1] = -7
    if (rect.y < 50 or (k_a and not main.immobilize)) and self.magic_applied and self.state == "swivel": self.magic_applied = False; self.y_vel = 0; self.frame = 1
    if self.magic_applied and self.state == "shot" and not self.flipped: self.movement[0] = 7; main.scrollx += ss; self.y_vel = 0; self.movement[1] = 0
    if self.magic_applied and self.state == "shot" and self.flipped: self.movement[0] = -7; main.scrollx += -ss; self.y_vel = 0; self.movement[1] = 0
    if collision_type["right"] and self.magic_applied and self.state == "shot" and not self.flipped: self.magic_applied = False; self.y_vel = 0
    if collision_type["left"] and self.magic_applied and self.state == "shot" and self.flipped: self.magic_applied = False; self.y_vel = 0
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)

    stand_on_flat = True
    for tile in hit_list:
      if tile.solid and not tile.flat: stand_on_flat = False
    for tile in hit_list:
      if tile.transport_to_level == None:
        if tile.solid:
          if movement[1] > 0 and not (k_down and self.state != "dizzy" and tile.flat and stand_on_flat and not self.finished):
            #if self.y_vel != 0: land_sfx.play()
            rect.bottom = tile.rect.top
            collision_type['bottom'] = True
            tile.stood_on = True
            if tile.move_x: self.rect.x += tile.speed
            if tile.move_y: self.rect.y += tile.speed
            if not self.finished:
              if tile.type == "magic block scope": self.magic_applied = True; self.state = "swivel"; self.timer.reset(); self.frame = 1; magic_sfx.play()
              if tile.type == "magic block shoot left": self.magic_applied = True; self.state = "shot"; self.timer.reset(); self.frame = 1; self.flipped = True; magic_sfx.play()
              if tile.type == "magic block shoot right": self.magic_applied = True; self.state = "shot"; self.timer.reset(); self.frame = 1; self.flipped = False; magic_sfx.play()
              if tile.type == "ice":
                if not self.on_ice: self.x_vel = self.movement[0]
                self.on_ice = True
              else: self.on_ice = False; self.x_vel = 0
          elif movement[1] < 0 and not tile.flat:
            rect.top = tile.rect.bottom
            collision_type['top'] = True
          elif k_down and self.collision["bottom"] and tile.flat and self.movement[0] == 0 and not main.immobilize: self.movement[1] = 0; self.rect.y += 8; self.waiting_timer.reset()
      elif "hub" in main.map: pygame.mixer.music.load("Sounds/tracks/E N G U L F.mp3"); pygame.mixer.music.play(1, 0.0); main.available_to_flash = True; self.transport_to_level = tile.transport_to_level; main.immobilize = True
      if (tile.type == "finish" or main.boss_complete) and self.collision["bottom"]:
        if not self.finished: pygame.mixer_music.stop(); self.dance_timer.reset()
        self.finished = True; self.movement = [0, 0]
      if levels[main.map]["mode"] == "sun" and self.wealth >= 50: main.bonus_complete = True
        
    return rect, collision_type
  
  def pickup(self, rect, tiles):
    hit_list = collision_test(rect, tiles)

    for coin in hit_list:
      main.collectibles.remove(coin); collectibles[coin.type]["sound"].play()
      self.numbers.append(Number(collectibles[coin.type]["message"], self.rect.x, self.rect.y, collectibles[coin.type]["colors"]))
      if "hub" in main.map: self.suns += coin.value; main.grabbed_sun_in_hub = True
      else: self.wealth += coin.value
      self.lives += coin.lives
      
  def get_hit(self, rect, movement, dangers):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}

    hit_list = [enemy for enemy in collision_test(rect, dangers) if enemy.alive]

    self.protection_timer.count(1, FPS, 0)
    if round(self.protection_timer.tally) == 7: main.stop_motion, main.immobilize = False, False; pygame.mixer.music.set_volume(1); main.shakex = 0
    elif self.protection_timer.tally <= 7: main.shakex *= -1

    for enemy in hit_list:
      if (self.rect.y > enemy.rect.y and self.protection_timer.tally >= FPS - 1) and enemy.type != "lambda":
        if not self.magic_applied:
          if self.rect.x < enemy.rect.x and self.state != "fly" and self.state != "shot": self.lives -= 1; self.protection_timer.reset(); collision_type['right'] = True; enemy.direction = "right"; hurt_sfx.play(); self.y_vel = 5; self.rect.y -= 5
          elif self.rect.x > enemy.rect.x and self.state != "fly" and self.state != "shot": self.lives -= 1; self.protection_timer.reset(); collision_type['left'] = True; enemy.direction = "left"; hurt_sfx.play(); self.y_vel = 5; self.rect.y -= 5
        else:
          if enemy.type != "nox": enemy.alive = False; enemy.lives = 0; self.wealth += enemy.grant; self.numbers.append(Number(f"{enemy.grant} +", enemy.rect.x, enemy.rect.y))
          else: enemy.lives -= 1; self.y_vel = 5; self.rect.y -= 5; self.magic_applied = False; self.y_vel = 0; self.frame = 1

    hit_list = [enemy for enemy in collision_test(rect, dangers) if enemy.alive]

    for enemy in hit_list:
      if movement[1] > 0 and not collision_type["left"] and not collision_type["right"] and rect.bottom >= enemy.rect.top:
        if (self.rect.y < enemy.rect.y or self.state == "fly" or self.state == "shot") and not enemy.cannot_be_attacked:
          if self.y_vel != 0: land_sfx.play()
          rect.bottom = enemy.rect.top
          if movement[1] > 0 and self.state != "fly": self.state == "jump"; self.frame = 1; self.y_vel = -15
          collision_type['bottom'] = True
          enemy.lives -= 1
          if enemy.lives <= 0: self.wealth += enemy.grant; self.numbers.append(Number(f"{enemy.grant} +", enemy.rect.x, enemy.rect.y))
        elif self.protection_timer.tally >= FPS - 1 and self.state != "fly" and self.state != "shot" and enemy.type != "lambda": self.lives -= 1; self.protection_timer.reset(); self.protection_timer.tally = 0; main.stop_motion, main.immobilize = True, True; pygame.mixer.music.set_volume(0.3); hurt_sfx.play(); main.shakex = 5
      elif (self.state == "fly" or self.state == "shot") and enemy.rect.width < 20:
        enemy.lives -= 0.5
        if enemy.lives <= 0.5: self.wealth += enemy.grant; self.numbers.append(Number(f"{enemy.grant} +", enemy.rect.x, enemy.rect.y))
      elif movement[1] < 0:
        #rect.top = enemy.rect.bottom
        collision_type['top'] = True
    return rect, collision_type
    

class Tile:
  def __init__(self, tile, x, y, floor, transport_to_level, solid, flat, move_x, move_y, backer, move_backer, id=""):
    self.size = 16
    self.type = tile
    self.floor = floor
    self.image = self.load_img(tile)
    self.rect = pygame.Rect((x * self.size, (y * self.size) + (int(tile == "puff grass") * 2)), (self.image.get_width(), self.image.get_height() / (int(flat) + 1)))
    self.y = y * self.size
    self.coin = False
    self.timer = Timer()
    self.stood_on = False
    self.falling = False
    self.transport_to_level = transport_to_level
    self.solid = solid
    self.flat = flat
    self.backer = backer
    self.m_backer = move_backer
    self.move_x = move_x
    self.move_y = move_y
    self.speed = 0
    if move_x: self.speed = move_x
    if move_y: self.speed = move_y
    self.id = id

  def update(self):
    #self.rect.x += main.scrolls[0]; self.rect.y += main.scrolls[1]
    screen.blit(self.image, ((self.rect.x - main.scrollx) + (75 if main.map != "outro" else 0), self.rect.y - main.scrolly))

    if self.type == "cloud" and self.stood_on:
      if self.timer.timer(FPS): self.falling = True
      if self.falling:
        self.image = self.load_img("cloud fall")
        if not self.rect.y > HEIGHT + (self.size * 16): self.rect.y += 3
        #if self.rect.y > HEIGHT + self.size: main.tiles.remove(self)
 
    if (self.rect.x < main.scrollx - 15 or self.rect.x > main.scrollx + (WIDTH / 1.25)) and self.type == "cloud": self.rect.y = self.y; self.falling = False; self.stood_on = False; self.image = self.load_img("cloud")

    if "door" in self.type: self.image = pygame.image.load("Assets/tiles/door" + str(self.timer.keep_count(FPS / 8, 3, 1)) + ".png").convert_alpha()
    if "closedor" in self.type: self.image = pygame.image.load("Assets/tiles/closedor" + str(self.timer.keep_count(FPS / 8, 3, 1)) + ".png").convert_alpha()

    if self.move_x or self.move_y and not self.falling:
      self.timer.nonstopcount(1, 0)
      for tile in [tile for tile in main.tiles if self.rect.colliderect(tile.rect) and (tile.m_backer or (tile.timer.tally == 0 and (tile.move_x or tile.move_y)))]:
        self.timer.reset(); self.speed *= -1
        if abs(self.speed) == 1 or abs(self.speed) == 1.0: self.falling = True; self.speed = 0
      if self.stood_on or (self.speed != 1 and self.speed != -1):
        if self.move_x: self.rect.x += self.speed
        if self.move_y: self.rect.y += self.speed

  def load_img(self, tile): return pygame.image.load("Assets/tiles/" + tile + ".png").convert_alpha()


class Collectible:
  def __init__(self, coin, x, y):
    self.type = coin
    self.image = self.load_img(coin)
    self.rect = pygame.Rect((x * 16, y * 16), (16, 16))
    self.value = collectibles[coin]["value"]
    self.lives = collectibles[coin]["lives"]
    self.timer = Timer()

  def update(self):
    #self.rect.x += main.scrolls[0]; self.rect.y += main.scrolls[1]
    screen.blit(self.image, ((self.rect.x - main.scrollx) + 75, self.rect.y + self.timer.oscillate(2, 3, -3)))

  def load_img(self, coin): return pygame.transform.scale(pygame.image.load("Assets/" + coin + ".png").convert_alpha(), (16, 16))


class Monster:
  def __init__(self, type, x, y):
    self.rect = pygame.Rect((x * 16, y * 16), (16, 16))
    self.movement = [0, 0]
    self.speed = type["speed"]
    self.lives = type["lives"]
    self.timer = Timer()
    self.timer2 = Timer()
    self.timer3 = Timer()
    self.flipped = False
    self.state = "idle"
    self.frame = 1
    self.y_vel = 0
    self.jumping_vel = 0
    self.airtimer = 0
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.type = type["type"]
    self.direction = "left"
    self.go_down = [True, False][random.randrange(0, 2)]
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha()
    self.target_image = pygame.image.load(f"Assets/target.png").convert_alpha()
    self.grant = type["grant"]
    if type["bigger"]: self.rect.width, self.rect.height = 32, 32 / (int("wonderfly" in type) + 1)
    self.alive = True
    self.dead_animation_timer = Timer()
    self.dead_animation = [0, -5, -10, -15, -20, -23, -20, -13, -7, -2, 2, 8, 15, 19, 28, 40, 55, 70, 90, 110, 125, 150, 175, 200, 230, 260, 300, 350, 400]
    self.delete = False
    if "right" in self.type: self.flipped, self.direction = False, "right"
    elif "left" in self.type: self.flipped, self.direction = True, "left"
    if self.type == "wonderfly oscillator": self.direction = "down" #self.direction = ["down", "up"][random.randrange(0, 2)]
    self.switch_state_timer = Timer()
    self.cannot_be_attacked = False
    self.waking_animation_timer = Timer()
    self.dying_animation_timer = Timer()
    self.waking_animation = [1]
    self.go_back = False
    if self.type == "hapshu fire": main.projectiles.append(Fire(self))

    if self.type == "hoot-hoot":
      self.rect.x -= 8; self.dead_animation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -5, -10, -15, -20, -23, -20, -16, -12, -7, -2, 5, 11, 19, 28, 37, 48, 59, 60, 71, 82, 94, 106, 118, 130, 147, 158, 170, 180, 201, 222, 243, 275, 300, 350]
      self.waking_animation_timer = Timer()
      self.waking_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    if self.type == "lambda":
      self.dead_animation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      self.waking_animation_timer = Timer()
      self.waking_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
      self.dying_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
      self.target_rect = pygame.Rect((-16, -16), (16, 16))
      self.state = "wake"
    if self.type == "nox":
      self.dstate = "walk"
      self.dead_animation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -5, -10, -15, -20, -23, -20, -13, -7, -2, 2, 8, 15, 19, 28, 40, 55, 70, 90, 110, 125, 150, 175, 200, 230, 260, 300, 350, 400]
      self.waking_animation_timer = Timer()
      self.waking_animation = [2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6]
      self.last_attack = "B"; self.rect.width, self.rect.height = 64, 64
      self.dying_animation = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    if self.type == "glacigon":
      self.state = "wake"
      self.last_attack = "B"; self.rect.width, self.rect.height = 64, 64
      self.intended_direction = "left"
      self.dead_animation = [-1, -5, -10, -15, -20, -23, -20, -13, -7, -2, 2, 8, 15, 19, 28, 40, 55, 70, 90, 110, 125, 150, 175, 200, 230, 260, 300, 350, 400]
      self.waking_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3]
      self.waking_animation_timer = Timer()
      self.dying_animation = [1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3]
    if self.type == "hootin-kabloo":
      self.state = "wake"
      self.dstate = "idle"
      self.last_attack = "spin"
      self.dead_animation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -5, -10, -15, -20, -23, -20, -13, -7, -2, 2, 8, 15, 19, 28, 40, 55, 70, 90, 110, 125, 150, 175, 200, 230, 260, 300, 350, 400]
      self.waking_animation_timer = Timer()
      self.waking_animation = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 5, 6, 7, 8, 9, 10, 11, 10, 11, 10, 11]
      self.rect.width, self.rect.height = 64, 64
      self.dying_animation = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
      self.rect.x += 15

  def update(self):
    global k_left
    try: self.image = pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{math.floor(self.frame)}.png").convert_alpha(), self.flipped, False)
    except: self.frame = 1
    #pygame.draw.rect(screen, "Red", ((self.rect.x - main.scrollx, self.rect.y), (self.rect.width, self.rect.height)), 2)
    screen.blit(self.image, ((self.rect.x + (73 if main.map != "outro" else 0)) - main.scrollx, (self.rect.y - main.scrolly) + self.dead_animation[self.dead_animation_timer.tally] + (int(round(self.switch_state_timer.tally / 2) % 2 and self.type == "glacigon" and self.state == "attackA") * 2) ))
    
    if self.alive and not main.stop_motion:
      if self.lives < 1: self.alive = False
      if self.rect.x - main.scrollx < WIDTH and self.rect.x - main.scrollx > -30 and self.type != "hoot-hoot" and self.type != "lambda" and self.type != "nox" and self.type != "glacigon" and self.type != "pal" and not "wonderfly" in self.type: self.rect, self.collision = self.move(self.rect, self.movement, main.tiles)
      if "hapshu" in self.type:
        if not "fire" in self.type:
          if self.type == "hapshu left": self.flipped = True; self.direction = "left"
          if self.type == "hapshu right": self.flipped = False; self.direction = "right"
          if self.frame == 3.7: self.frame = 1.0
          if self.frame == 3.3: self.frame = 3.7
          if self.frame == 3.0: self.frame = 3.3; main.projectiles.append(Spitball(self))
          if self.frame == 2.7: self.frame = 3.0
          if self.frame == 2.3: self.frame = 2.7
          if self.frame == 2.0: self.frame = 2.3
          if self.timer.timer(FPS * 1.25): self.frame = 2.0
      elif "canfish" in self.type:
        if self.type == "canfish left": self.flipped = True; self.direction = "left"
        if self.type == "canfish right": self.flipped = False; self.direction = "right"
        if self.frame == 4.7: self.frame = 1.0
        if self.frame == 4.3: self.frame = 4.7
        if self.frame == 4.0: self.frame = 4.3
        if self.frame == 3.7: self.frame = 4.0
        if self.frame == 3.3: self.frame = 3.7
        if self.frame == 3.0: self.frame = 3.3; main.projectiles.append(Canfish(self))
        if self.frame == 2.7: self.frame = 3.0
        if self.frame == 2.3: self.frame = 2.7
        if self.frame == 2.0: self.frame = 2.3
        if self.timer.timer(FPS * 2): self.frame = 2.0

      elif self.type == "hoot-hoot":
        if self.lives < 1: main.boss_complete = True; main.player.state = "idle"; main.player.magic_applied = False
        if main.player.rect.x > 1760:
          if main.scrollx < 1755: main.scrollx += 2; self.cannot_be_attacked = True; pygame.mixer.music.stop(); main.immobilize = True
          else: self.frame = self.waking_animation[self.waking_animation_timer.count(2, len(self.waking_animation) - 1, 0)]
          if self.waking_animation_timer.tally == len(self.waking_animation) - 2: pygame.mixer.music.load("Sounds/tracks/Ave Miles.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False
          elif self.waking_animation_timer.tally >= len(self.waking_animation) - 1:
            screen.blit(retrofontsmall.render("Hoot-Hoot HP", False, "White"), (85, 2))
            for hp in range(round(self.lives)): pygame.draw.rect(screen, "White", ((85 + hp * 5, 20), (4, 10)), border_radius = 3)
            self.switch_state_timer.keep_count(1, FPS * 5, 0)
            if self.switch_state_timer.tally < FPS * 3:
              self.state = "walk"
              if self.rect.y > 60: self.rect.y -= 4
              self.frame = self.timer.keep_count(2, 3, 1)
              if main.player.rect.x > self.rect.x: self.rect.x += 2
              if main.player.rect.x < self.rect.x: self.rect.x -= 2
              self.cannot_be_attacked = True
            else: self.movement[1] = 25; self.move(self.rect, self.movement, main.tiles); self.state, self.frame = "attack", 1; self.cannot_be_attacked = False
          main.lock_scroll = True
        if main.player.rect.x < 1770 and main.scrollx > 1700: k_left = False

      elif self.type == "lambda":
        if self.lives < 1: main.boss_complete = True; main.player.state = "idle"; main.player.magic_applied = False; self.state = "defeat"; self.frame = self.dying_animation[self.dying_animation_timer.count(2, len(self.dying_animation) - 1, 0)]
        if main.player.rect.x > 385:
          if main.scrollx < 380: main.scrollx += 2; self.cannot_be_attacked = True; pygame.mixer.music.stop(); main.immobilize = True
          else: self.frame = self.waking_animation[self.waking_animation_timer.count(2, len(self.waking_animation) - 1, 0)]
          if self.waking_animation_timer.tally == len(self.waking_animation) - 2: pygame.mixer.music.load("Sounds/tracks/Ave Miles.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False
          elif self.waking_animation_timer.tally >= len(self.waking_animation) - 1:
            screen.blit(retrofontsmall.render("Lambda HP", False, "White"), (85, 2))
            for hp in range(round(self.lives)): pygame.draw.rect(screen, "White", ((85 + hp * 5, 20), (4, 10)), border_radius = 3)
            self.switch_state_timer.count(1, FPS * 4, 0)
            if self.timer2.timer(FPS / (1.5 + (int(self.lives < 6) * 1.5))): main.projectiles.append(Strike(self))
            if self.switch_state_timer.tally < FPS / 4 and self.lives != monsters["lambda"]["lives"]: main.shakex = 0; self.state = "defeat"; self.frame = 1
            elif self.switch_state_timer.tally < FPS * 3: self.state = "idle"; self.frame = self.timer.keep_count(2, 3, 1)
            else:
              if self.switch_state_timer.tally == FPS * 3: self.target_rect.x, self.target_rect.y = random.randrange(self.rect.x, (self.rect.x + 144) - 16), random.randrange(self.rect.y, (self.rect.y + 112) - 16)
              screen.blit(self.target_image, ((self.target_rect.x + 73) - main.scrollx, (self.target_rect.y)))
              if self.switch_state_timer.tally < FPS * 3.5: self.state = "hurt"; self.frame = 1
              else: self.state = "idle"; self.frame = self.timer.keep_count(2, 3, 1)
          if self.target_rect.colliderect(main.player.rect) and main.player.state == "fly": self.target_rect.x, self.target_rect.y = -16, -16; self.lives -= 1; self.switch_state_timer.reset(); target_sfx.play(); main.shakex = 5
          main.lock_scroll = True
        if main.player.rect.x < 395 and main.scrollx > 295: k_left = False

      elif self.type == "nox":
        if self.lives < 1: main.boss_complete = True; main.player.state = "idle"; main.player.magic_applied = False
        if main.player.rect.x > 3250:
          if main.scrollx < 3235: main.scrollx += 2; self.cannot_be_attacked = True; pygame.mixer.music.stop(); main.immobilize = True; main.player.x_vel = 0
          else: self.frame = self.waking_animation[self.waking_animation_timer.count(2, len(self.waking_animation) - 1, 0)]
          if self.waking_animation_timer.tally == len(self.waking_animation) - 2: pygame.mixer.music.load("Sounds/tracks/Ave Miles.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False
          elif self.waking_animation_timer.tally >= len(self.waking_animation) - 1:
            screen.blit(retrofontsmall.render("Nox HP", False, "White"), (85, 2))
            for hp in range(round(self.lives)): pygame.draw.rect(screen, "White", ((85 + hp * 5, 20), (4, 10)), border_radius = 3)
            self.switch_state_timer.nonstopcount(1, 0)
            if self.switch_state_timer.tally < FPS * 3:
              if self.dstate == "walk":
                self.state = "walk"
                if self.rect.y > 60: self.rect.y -= 4
                self.frame = self.timer.keep_count(2, 3, 1)
                if (WIDTH / 4) + main.scrollx > self.rect.x: self.rect.x += 4
                if (WIDTH / 4) + main.scrollx < self.rect.x: self.rect.x -= 4
                self.cannot_be_attacked = False
              elif self.dstate == "attackA":
                self.state = "attackA"; self.rect.x += 4; self.frame = self.timer.keep_count(2, 5, 1)
                if self.timer.time == 1 and self.timer.tally == 1: swing_sfx.play()
                self.cannot_be_attacked = False
              elif self.dstate == "attackB":
                self.state = "attackB"; self.frame = self.timer.keep_count(5, 3, 1); angle = math.atan2(self.rect.centery - main.player.rect.centery, self.rect.centerx - main.player.rect.centerx)
                if self.timer.time == 1 and self.timer.tally == 1: main.projectiles.append(NoxFire(self, angle)); nox_fire_sfx.play()
                self.cannot_be_attacked = True
            else:
              if self.state != "teleport": self.frame = 1; self.timer.reset(); self.state = "teleport"; nox_flash_sfx.play()
              self.state = "teleport"; self.frame = self.timer.keep_count(2, 7, 1)
              if self.frame == 6:
                if self.lives > 5: yr = [18, 25]
                if self.lives < 6: yr = [12, 19]
                if self.dstate == "walk" and self.frame != 1 and self.last_attack == "B": self.dstate = "attackA"; self.last_attack = "A"; self.frame = 1; self.timer.reset(); self.rect = pygame.Rect((main.scrollx, random.randrange(yr[0], yr[1]) * 10), (64, 64)); self.switch_state_timer.reset()
                if self.dstate == "walk" and self.frame != 1 and self.last_attack == "A": self.dstate = "attackB"; self.last_attack = "B"; self.frame = 1; self.timer.reset(); self.rect = pygame.Rect((WIDTH / 4 + main.scrollx, 4), (64, 64)); self.switch_state_timer.reset()
                if "attack" in self.dstate and self.frame != 1: self.dstate = "walk"; self.frame = 1; self.timer.reset(); self.rect = pygame.Rect(((WIDTH / 4) + main.scrollx, 60), (64, 64)); self.switch_state_timer.reset()
          main.lock_scroll = True
        if main.player.rect.x < 3260 and main.scrollx > 3190: k_left = False; main.player.rect.x = 3260

      elif self.type == "glacigon":
        if self.lives < 1: main.boss_complete = True; main.player.state = "idle"; main.player.magic_applied = False
        if main.player.rect.x > 7630:
          if main.scrollx < 7618: main.scrollx += 2; self.cannot_be_attacked = True; pygame.mixer.music.stop(); main.immobilize = True; main.player.x_vel = 0
          else: self.frame = self.waking_animation[self.waking_animation_timer.count(2, len(self.waking_animation) - 1, 0)]
          if self.waking_animation_timer.tally == len(self.waking_animation) - 2: pygame.mixer.music.load("Sounds/tracks/Ave Miles.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False; self.state = "idle"
          elif self.waking_animation_timer.tally >= len(self.waking_animation) - 1:
            screen.blit(retrofontsmall.render("Glacigon HP", False, "White"), (85, 2))
            for hp in range(round(self.lives)): pygame.draw.rect(screen, "White", ((85 + hp * 5, 20), (4, 10)), border_radius = 3)
            self.switch_state_timer.nonstopcount(1, 0)
            if self.switch_state_timer.tally < FPS * (3 - int(self.lives < 7)):
              if self.state == "idle":
                if self.rect.y > 150: self.rect.y -= 4
                self.frame = self.timer.keep_count(2, 5, 1)
                self.cannot_be_attacked = False
                if self.intended_direction == "right": self.flipped = True
                if self.intended_direction == "left": self.flipped = False
              if self.state == "walk":
                self.cannot_be_attacked = False
                self.frame = self.timer.keep_count(2, 5, 1)
                if self.intended_direction == "right": self.rect.x += 5
                if self.intended_direction == "left": self.rect.x -= 5
                self.cannot_be_attacked = False
                if self.switch_state_timer.tally >= FPS * 1.5: self.state = "idle"; self.intended_direction = {"left": "right", "right": "left"}[self.intended_direction]
              elif self.state == "attackA":
                self.cannot_be_attacked = True
                self.frame = self.timer.count(2, 2, 1)
                if self.switch_state_timer.time % 5 == 0: frost_breath_sfx.play()
                if self.timer.tally == 1 and self.timer.time == 1: main.projectiles.append(FrostBreath(self))
              elif self.state == "attackB":
                self.cannot_be_attacked = True
                self.frame = self.timer.count(FPS / (3.5 + int(self.lives < 7)), 5, 1)
                if (self.frame == 2 or self.frame == 4) and self.timer.time == 1: main.projectiles.append(Tornado(self)); tornado_sfx.play()
            else:
              for proj in main.projectiles:
                if isinstance(proj, FrostBreath): main.projectiles.remove(proj)
              self.switch_state_timer.reset()
              if self.state == "idle" and self.frame != 1 and self.last_attack == "B": self.state = "attackA"; self.last_attack = "A"; self.frame = 1; self.timer.reset()
              if self.state == "idle" and self.frame != 1 and self.last_attack == "A": self.state = "attackB"; self.last_attack = "B"; self.frame = 1; self.timer.reset()
              if "attack" in self.state and self.frame != 1: self.state = "walk"; self.frame = 1; self.timer.reset()
          main.lock_scroll = True
        if main.player.rect.x < 7640 and main.scrollx > 7570: k_left = False; main.player.x_vel = 0; main.player.rect.x += 1
      
      elif self.type == "hootin-kabloo":
        if self.lives < 1: main.boss_complete = True; main.player.state = "idle"; main.player.magic_applied = False
        if main.player.rect.x > 3900:
          if main.scrollx < 3885: main.scrollx += 3; self.cannot_be_attacked = True; pygame.mixer.music.stop(); main.immobilize = True; main.player.x_vel = 0
          else: self.frame = self.waking_animation[self.waking_animation_timer.count(2, len(self.waking_animation) - 1, 0)]
          if self.waking_animation_timer.tally == len(self.waking_animation) - 2: pygame.mixer.music.load("Sounds/tracks/Ave Miles.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False
          elif self.waking_animation_timer.tally >= len(self.waking_animation) - 1:
            screen.blit(retrofontsmall.render("Hootin-Kabloo HP", False, "White"), (85, 2))
            for hp in range(round(self.lives)): pygame.draw.rect(screen, "White", ((85 + hp * 5, 20), (4, 10)), border_radius = 3)
            if self.state != "spin" and self.state != "dash": self.switch_state_timer.nonstopcount(1, 0)
            if self.switch_state_timer.tally <= FPS * (1.5 - int(self.lives < 12)):
              if self.dstate == "idle":
                self.state = "idle"
                self.frame = self.timer.keep_count(2, 3, 1)
                if not self.flipped:
                  if 4095 >= self.rect.x: self.rect.x += 4
                  if 4095 <= self.rect.x: self.rect.x -= 4
                elif self.flipped:
                  if main.scrollx >= self.rect.x: self.rect.x += 4
                  if main.scrollx <= self.rect.x: self.rect.x -= 4
                self.cannot_be_attacked = False; self.go_back = False
              elif self.dstate == "spin" and self.last_attack == "dash":
                self.state = "spin"; self.movement[1] = random.randrange(-5 - ((monsters["hootin-kabloo"]["lives"] - self.lives) // 2), 6 + ((monsters["hootin-kabloo"]["lives"] - self.lives) // 2)); self.frame = self.timer.keep_count(2, 3, 1)
                if self.timer.time == 1 and self.timer.tally == 1: swing_sfx.play()
                if not self.flipped:
                  if self.rect.x <= main.scrollx: self.go_back = True
                  if self.go_back: self.movement[0] = 4
                  else: self.movement[0] = -4
                elif self.flipped:
                  if self.rect.x >= 4095: self.go_back = True
                  if self.go_back: self.movement[0] = -4
                  else: self.movement[0] = 4
                self.cannot_be_attacked = True
                if (self.rect.x >= 4095 and self.go_back and not self.flipped) or (self.rect.x <= main.scrollx and self.go_back and self.flipped): self.go_back = False; self.dstate = "idle"; self.frame = 1; self.timer.reset(); self.switch_state_timer.reset(); self.movement = [0, 0]; self.last_attack = "spin"
                self.rect, self.collision = self.move(self.rect, self.movement, main.tiles)
              elif self.dstate == "dash" and self.last_attack == "spin":
                self.state = "dash"; self.frame = self.timer.keep_count(2, 3, 1)
                if not self.flipped: self.movement[0] = -10
                elif self.flipped: self.movement[0] = 10
                self.cannot_be_attacked = True
                if self.rect.x < main.scrollx + 23 and not self.flipped: self.flipped = True; self.dstate = "idle"; self.frame = 1; self.timer.reset(); self.switch_state_timer.reset(); self.movement = [0, 0]; self.last_attack = "dash"
                if self.rect.x >= 4095 and self.flipped: self.flipped = False; self.dstate = "idle"; self.frame = 1; self.timer.reset(); self.switch_state_timer.reset(); self.movement = [0, 0]; self.last_attack = "dash"
            else:
              if self.state != "stance": self.frame = 1; self.timer.reset(); self.state = "stance"; stance_sfx.play()
              self.state = "stance"; self.frame = self.timer.keep_count(2, 7, 1); self.movement[1] = 0
              if self.frame == 6 and self.last_attack == "dash": self.frame = 1; self.dstate = "spin"; self.timer.reset(); self.switch_state_timer.reset()
              if self.frame == 6 and self.last_attack == "spin": self.frame = 1; self.dstate = "dash"; self.timer.reset(); self.switch_state_timer.reset(); dash_sfx.play()
          main.lock_scroll = True
        if main.player.rect.x < 3910 and main.scrollx > 3840: k_left = False; main.player.rect.x = 3910

      else:
        if self.direction == "left": self.movement[0] = -2; self.flipped = True
        if self.direction == "right": self.movement[0] = 2; self.flipped = False
        if self.collision['right']: self.direction = "left"
        if self.collision["left"]: self.direction = "right"
        self.frame = self.timer.keep_count(FPS / 8, 3, 1)
    
    elif not self.alive:
      self.dead_animation_timer.count(1, len(self.dead_animation) - 1, 0)
      self.state = "defeat"; self.frame = 1
      if self.lives < 1 and self.type == "lambda" or self.type == "nox" or self.type == "glacigon": self.frame = self.dying_animation[self.dying_animation_timer.count(2, len(self.dying_animation) - 1, 0)]

    if self.dead_animation_timer.tally == 6: fly_sfx.play()
    if self.dead_animation_timer.tally == 1 and (self.type == "kartop" or self.type == "göktop" or self.type == "yaltop"): main.tiles.append(Tile("cart", self.rect.x / 16, (self.rect.y + 20) / 16, False, None, True, False, 0, 0, False, False, ))
    if self.dead_animation_timer.tally == len(self.dead_animation) - 1: self.delete = True

    if self.type != "uçampul" and self.type != "wonderfly" and self.type != "wonderfly oscillator" and self.type != "ruki" and self.type != "kiskus" and self.type != "pal":
      self.y_vel += 2
      if self.y_vel > 10: self.y_vel = 10
      self.movement[1] = self.y_vel
      if self.collision["bottom"]: self.y_vel, self.airtimer = 0, 0
      elif self.collision['top']: self.y_vel, self.airtimer = 0, 10
      else: self.airtimer += 1
    elif self.type == "wonderfly oscillator":
      #if self.direction == "up": self.movement[1] = -1
      #if self.direction == "down": self.movement[1] = 1
      #if self.collision['bottom']: self.direction = "up"
      #if self.collision["top"]: self.direction = "down"
      if self.timer3.timer(FPS): self.go_down = not self.go_down
      if self.go_down: self.rect.y += 1.25
      if not self.go_down: self.rect.y -= 1.25
    if "wonderfly" in self.type and self.state != "defeat":
      if self.timer2.timer(FPS / 2): main.projectiles.append(Glint(self))
  
  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    if self.type != "wonderfly oscillator": rect.x += movement[0]

    hit_list = collision_test(rect, [tile for tile in tiles if tile.solid or tile.backer])
    for tile in hit_list:
      if self.type != "wonderfly oscillator":
        if movement[0] > 0: rect.right = tile.rect.left; collision_type['right'] = True
        elif movement[0] < 0: rect.left = tile.rect.right; collision_type['left'] = True
      else:
        if movement[1] > 0: rect.top = tile.rect.bottom; collision_type['bottom'] = True
        elif movement[1] < 0: rect.bottom = tile.rect.top; collision_type['top'] = True
      
    rect.y += movement[1]
    hit_list = collision_test(rect, [tile for tile in tiles if tile.solid])

    if self.type != "wonderfly oscillator":
      for tile in hit_list:
        if movement[1] > 0:
          rect.bottom = tile.rect.top
          collision_type['bottom'] = True
          if tile.move_x: self.rect.x += tile.speed
          if tile.move_y: self.rect.y += tile.speed
          if tile.type == "ice":
            if not self.flipped: rect.x += 1
            elif self.flipped: rect.x += -1
        elif movement[1] < 0: rect.top = tile.rect.bottom; collision_type['top'] = True
    return rect, collision_type
  

class Spitball:
  def __init__(self, user):
    self.image = pygame.image.load("Assets/spitball.png").convert_alpha()
    self.rect = pygame.Rect((user.rect.x, user.rect.y), (16, 16))
    if not user.flipped: self.speed = -10
    elif user.flipped: self.speed = 10
    if "up" in user.type or "down" in user.type: self.speed = -10; self.vertical = True
    else: self.vertical = False
    self.timer = Timer()
    self.hit = False
    self.friendly = False
    self.alive = True

  def update(self):
    #self.image = pygame.transform.rotate(self.image, 45)
    screen.blit(self.image, ((self.rect.x + 73) - main.scrollx, self.rect.y))
    if not main.stop_motion:
      if not self.vertical: self.rect.x += self.speed
      elif self.vertical: self.rect.y += self.speed; self.speed += 1 
      if self.timer.timer(FPS * 1): self.alive = False

class Canfish:
  def __init__(self, user):
    self.user = user
    self.image = pygame.image.load("Assets/canfish right/canfish1.png").convert_alpha()
    self.flipped = user.flipped
    if not user.flipped: self.speed = 5; self.rect = pygame.Rect((user.rect.x + 26, user.rect.y + 2), (32, 29))
    elif user.flipped: self.speed = 5; self.rect = pygame.Rect((user.rect.x - 26, user.rect.y + 2), (32, 29))
    if "up" in user.type or "down" in user.type: self.speed = -5; self.vertical = True; self.rect = pygame.Rect((user.rect.x, user.rect.y - 26), (32, 32))
    else: self.vertical = False
    self.frame_timer = Timer()
    self.timer = Timer()
    self.state = "canfish"
    self.hit = False
    self.explode = False
    self.friendly = False
    self.alive = True

  def update(self):
    self.image = pygame.image.load(f"Assets/canfish {self.user.direction}/{self.state}{self.frame_timer.keep_count(4, 3 + int(self.explode), 1)}.png").convert_alpha()
    screen.blit(self.image, ((self.rect.x + 73) - main.scrollx, self.rect.y - 3))
    if not main.stop_motion:
      if not self.vertical:
        if not self.flipped: self.rect.x += self.speed
        elif self.flipped: self.rect.x -= self.speed
      elif self.vertical: self.rect.y += self.speed; self.speed += 1
      if self.timer.timer(FPS * 3) and not self.explode: self.explode = True; self.state = "defeat"; self.frame_timer.tally = 1
      for tile in [tile for tile in main.tiles if self.rect.colliderect(tile.rect) and tile.solid and not self.explode and self.timer.time > FPS / 2]: self.explode = True; self.state = "defeat"; self.frame_timer.tally = 1; self.speed = 1
      if self.explode and self.frame_timer.tally == 3: self.alive = False

class Strike:
  def __init__(self, user):
    self.image = pygame.image.load("Assets/strike.png").convert_alpha()
    self.rect = pygame.Rect((random.randrange(user.rect.x - 100, user.rect.x + 100), -16), (16, 16))
    self.speed = 5
    self.timer = Timer()
    self.hit = False
    self.friendly = False
    self.alive = True

  def update(self):
    if self.timer.tally == 1: self.image.fill("Yellow", special_flags=pygame.BLEND_RGB_ADD)
    else: self.image = pygame.image.load("Assets/strike.png").convert_alpha()
    screen.blit(self.image, ((self.rect.x + 73) - main.scrollx, self.rect.y + (self.timer.keep_count(2, 3, 1) * 3)))
    if not main.stop_motion:
      self.rect.y += self.speed
      if self.hit: self.alive = False

class Glint:
  def __init__(self, user):
    self.size = random.randrange(1, 6)
    self.rect = pygame.Rect((random.randrange(user.rect.x, user.rect.x + 32), user.rect.bottom), (self.size, self.size))
    self.color = ["White", "Dark gray", "White", "Gray"]
    self.speed = 2
    self.timer = Timer()
    self.flash_timer = Timer()
    self.hit = False
    self.friendly = self.size < 5
    self.alive = True

  def update(self):
    if self.flash_timer.keep_count(1, 3, 0) != 2: pygame.draw.rect(screen, self.color[self.timer.keep_count(4, len(self.color), 0)], (((self.rect.x + 73) - main.scrollx, self.rect.y), (self.rect.width, self.rect.height)), border_radius=math.floor(self.size / 2))
    if not main.stop_motion:
      self.rect.y += self.speed
      if self.hit or self.rect.y > HEIGHT: self.alive = False

class NoxFire:
  def __init__(self, user, angle):
    self.rect = pygame.Rect((user.rect.x + 24, user.rect.y + 24), (16, 16))
    self.colors = ("Blue", "White", "Red", "Black")
    self.speed = 9
    self.dirx = self.speed * math.cos(angle)
    self.diry = self.speed * math.sin(angle)
    self.timer = Timer()
    self.flash_timer = Timer()
    self.hit = False
    self.friendly = False
    self.alive = True

  def update(self):
    pygame.draw.rect(screen, self.colors[self.flash_timer.keep_count(0, len(self.colors))], (((self.rect.x + 73) - main.scrollx, self.rect.y), (self.rect.width, self.rect.height)), border_radius=8)
    if not main.stop_motion: self.rect.move_ip(-self.dirx, -self.diry)
    if self.timer.timer(FPS * 10): self.alive = False
    if self.hit: self.alive = False

class Snowflake:
  def __init__(self): self.rect = pygame.Rect((random.randrange(75, WIDTH * 2), 0), (4, 4))
  def update(self): pygame.draw.rect(screen, (190, 190, 190), ((self.rect.x, self.rect.y), (5, 5)), border_radius=3); pygame.draw.rect(screen, "Dark gray", ((self.rect.x, self.rect.y), (5, 5)), width=1, border_radius=3); self.rect.x -= 25; self.rect.y += 20

class SnowflakeFar:
  def __init__(self): self.rect = pygame.Rect((random.randrange(75, WIDTH * 2), 0), (2, 2))
  def update(self): pygame.draw.rect(screen, (190, 190, 190), ((self.rect.x, self.rect.y), (3, 3)), border_radius=3); pygame.draw.rect(screen, "Dark gray", ((self.rect.x, self.rect.y), (3, 3)), width=1, border_radius=3); self.rect.x -= 15; self.rect.y += 12
  
class FrostBreath:
  def __init__(self, user):
    self.rect = pygame.Rect((user.rect.x - 48, user.rect.y - 16), (48, 48))
    self.image = pygame.image.load(f"Assets/frost1.png")
    self.timer = Timer()
    self.hit = False
    self.friendly = False
    self.alive = True
    
  def update(self):
    self.image = pygame.image.load(f"Assets/frost{self.timer.keep_count(2, 5, 1)}.png")
    screen.blit(self.image, ((self.rect.x + 65) - main.scrollx, self.rect.y + 16))

class Tornado:
  def __init__(self, user):
    self.rect = pygame.Rect((user.rect.x, user.rect.y), (48, 48))
    self.image = pygame.image.load(f"Assets/tornado1.png")
    self.timer = Timer()
    self.oscil_timer = Timer()
    self.speed = 5
    self.hit = False
    self.friendly = False
    self.alive = True

  def update(self):
    self.image = pygame.transform.scale(pygame.image.load(f"Assets/tornado{self.timer.keep_count(FPS / 18, 3, 1)}.png"), (48, 48))
    screen.blit(self.image, (((self.rect.x + 73) - main.scrollx) + (self.oscil_timer.oscillate(1, 3, -3) * 2), self.rect.y))
    self.rect.y += 1
    self.rect.x += self.speed
    if self.rect.x > WIDTH + main.scrollx: self.alive = False

class Fire:
  def __init__(self, user):
    self.rect = pygame.Rect((user.rect.x, user.rect.y - 48), (16, 48))
    self.image = pygame.image.load(f"Assets/fire1.png").convert_alpha()
    self.timer = Timer()
    self.user = user
    self.hit = False
    self.friendly = False
    self.alive = True

  def update(self):
    self.image = pygame.image.load(f"Assets/fire{self.timer.keep_count(1, 4, 1)}.png").convert_alpha()
    screen.blit(self.image, ((self.rect.x + 73) - main.scrollx, self.rect.y))
    if self.user.state == "defeat": self.alive = False



def collision_test(rect, tiles):
  hit_list = []
  for tile in tiles:
    if rect.colliderect(tile):
      hit_list.append(tile)
      
  return hit_list


class Number:
  def __init__(self, text, x, y, colors=["White"]):
    self.text = text
    self.x = x
    self.y = y
    self.timer = Timer()
    self.flash_timer = Timer()
    self.alive = True
    self.colors = colors

  def update(self):
    screen.blit(retrofontsmall.render(f"{self.text}", True, self.colors[self.flash_timer.keep_count(2, len(self.colors), 0)]), ((self.x - main.scrollx) + 75, self.y))
    if self.timer.timer(FPS * 2): self.alive = False
    


k_right, k_left, k_down, k_up, k_a, k_select, k_start = False, False, False, False, False, False, False

def run():
  global k_down, k_up, k_right, k_left, k_a, k_select, k_start
  k_select = False, False
  if not main.available_to_flash: k_start = False
  if main.gamestate == 0: k_down, k_up, k_right, k_left, k_a = False, False, False, False, False
  for event in pygame.event.get():
    if event.type == pygame.QUIT: main.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN: k_start = True
      if event.key == pygame.K_e or event.key == pygame.K_SPACE: k_a = True
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = True
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = True
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = True
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = True
      if event.key == pygame.K_i: k_select = True
      if event.key == pygame.K_ESCAPE:
        if main.gamestate == 0: main.quit()
        elif "hub" in main.map and main.gamestate == 1 and main.player.transport_to_level == []: main.gamestate = 0
    if event.type == pygame.KEYUP:
      #if event.key == pygame.K_RETURN: k_start = False
      if event.key == pygame.K_SPACE or event.key == pygame.K_e: k_a = False
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = False
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = False
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = False
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = False
      if event.key == pygame.K_i: k_select = False
        
    if event.type == JOYBUTTONDOWN:
      if event.button == 0: k_a = True #□ X
      if event.button == 1: k_up = True #x A
      if event.button == 2 and "hub" in main.map and main.gamestate == 1 and main.player.transport_to_level == []: main.gamestate = 0 #o B
      if event.button == 3: k_a = True #△ Y
      if event.button == 4: pygame.image.save(screen, "screenshot.png") #share
      if event.button == 5: k_start = True #PS
      if event.button == 6:
        if main.gamestate == 0: main.quit()
        elif "hub" in main.map and main.gamestate == 1 and main.player.transport_to_level == []: main.gamestate = 0 #menu
      if event.button == 7: k_select = True #L3
      if event.button == 8: k_select = True #R3
      if event.button == 9: k_start = True #L1 LB
      if event.button == 10: pass #R1 RB
      if event.button == 11: k_a = True #up
      if event.button == 12: k_down = True #down
      if event.button == 13: k_left = True #left
      if event.button == 14: k_right = True #right
      if event.button == 15: pygame.image.save(screen, "screenshot.png") #pad
    axis_values = [0, 0]
    if event.type == JOYAXISMOTION:
      if abs(event.value) > 0.1: axis_values[event.axis] = event.value
      k_a = axis_values[1] < -0.7 and main.gamestate == 1
      k_up = axis_values[1] < -0.7 and main.gamestate != 1
      k_down = axis_values[1] > 0.7
      k_left = axis_values[0] < -0.7
      k_right = axis_values[0] > 0.7
    if event.type == JOYBUTTONUP:
      if event.button == 0: k_a = False #□ X
      if event.button == 1: k_up = False #x A
      if event.button == 2: k_up = False #o B
      if event.button == 3: k_a = False #△ Y
      if event.button == 4: pass #share
      if event.button == 5: k_start = False #PS
      if event.button == 6: k_select = False #menu
      if event.button == 7: k_select = True #L3
      if event.button == 8: k_select = False #R3
      if event.button == 9: k_start = False #L1 LB
      if event.button == 10: pass #R1 RB
      if event.button == 11: k_a = False #up
      if event.button == 12: k_down = False #down
      if event.button == 13: k_left = False #left
      if event.button == 14: k_right = False #right
      if event.button == 15: pass #pad
    if event.type == JOYDEVICEADDED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
    if event.type == JOYDEVICEREMOVED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
  try:
    if pygame.mouse.get_pressed() and (k_down and k_up): pygame.image.save(screen, "screenshot.png")
  except: pass
  clock.tick(FPS)
  display.blit(screen, (main.shakex, 0))
  pygame.display.update()
  screen.fill("Black")
  if main.gamestate == 0: screen.fill((210, 225, 230))
  else: screen.fill((50, 200, 230))
  for x in range(37):
    for y in range(37):
      if main.gamestate == 0: pygame.draw.rect(screen, (160, 165, 175), ((x * 10 + (int(y % 2) * 5), y * 10), (5, 5)), 0, 2)
  #for x in range(37):
  #  pygame.draw.line(screen, (160, 165, 175), (0, x * 10), (WIDTH, x * 10), 1)

main = Main()

while True: main.update()