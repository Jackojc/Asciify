import pygame
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


class asciify():
    def __init__(self, width, height, font, margin=0, fontsize=16, bgcolor=(0, 0, 0), color=(255, 255, 255), offsets=(0, 0, 0, 0), aa=True):
        self.OffsetX, self.OffsetY, self.CellOffsetX, self.CellOffsetY = offsets
        self.Alias = aa
        self.Images = {}

        pygame.init()
        if ".ttf" not in font:
            font = font+".ttf"
        self.Font = pygame.font.Font(font, fontsize)
        chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789£$€%&_+-=@~#<>?")
        maxcharw = 0
        maxcharh = 0
        for char in chars:
            xt, yt = self.Font.size(char)
            if xt > maxcharw:
                maxcharw = xt
            if yt > maxcharh:
                maxcharh = yt

        cellx, celly = maxcharw+self.CellOffsetX, maxcharh+self.CellOffsetY
        self.CellsWidth = width
        self.CellsHeight = height

        self.Width = width * cellx
        self.Height = height * celly

        self.Margin = margin
        self.Skip = 0

        self.DefColor = color
        self.DefBgColor = bgcolor

        self.CellX = cellx
        self.CellY = celly

        self.Clock = pygame.time.Clock()
        self.Screen = pygame.display.set_mode((self.Width, self.Height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.Foreground = pygame.Surface(self.Screen.get_size(), pygame.SRCALPHA, 32)
        self.Foreground = self.Foreground.convert_alpha()
        self.Background = pygame.Surface(self.Screen.get_size())

    def setCell(self, x, y, string=None, color=None):
        if color is None:
            color = self.DefColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        if string is None:
            pygame.draw.rect(self.Background, color, (posX, posY, self.CellX, self.CellY))
        else:
            string = string[0]
            string = self.Font.render(string, self.Alias, color)
            self.Foreground.blit(string, (posX+self.OffsetX, posY+self.OffsetY))

    def setStringBlock(self, x, y, string=None, color=None, bgcolor=None):
        if color is None:
            color = self.DefColor
        if bgcolor is None:
            bgcolor = self.DefBgColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        pygame.draw.rect(self.Background, bgcolor, (posX, posY, self.CellX, self.CellY))
        string = string[0]
        string = self.Font.render(string, self.Alias, color)
        self.Foreground.blit(string, (posX+self.OffsetX, posY+self.OffsetY))

    def setString(self, x, y, string, color=None):
        if color is None:
            color = self.DefColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        string = string[0]
        string = self.Font.render(string, self.Alias, color)
        self.Foreground.blit(string, (posX+self.OffsetX, posY+self.OffsetY))

    def setBlock(self, x, y, color=None):
        if color is None:
            color = self.DefBgColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        pygame.draw.rect(self.Foreground, color, (posX, posY, self.CellX, self.CellY))

    def setBg(self, x, y, color=None):
        if color is None:
            color = self.DefBgColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        pygame.draw.rect(self.Background, color, (posX, posY, self.CellX, self.CellY))

    def loadImg(self, path):
        image = self.Images.get(path)
        if image is None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            self.Images[path] = image
        return image

    def setImg(self, x, y, path, bg=0):
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        if not bg:
            self.Foreground.blit(self.Images[path], (posX, posY))
        else:
            self.Background.blit(self.Images[path], (posX, posY))

    def textFixed(self, x, y, string, color=None, shadow=1, shadowcolor=(20, 20, 20), shadowdist=2):
        if color is None:
            color = self.DefColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        if shadow:
            text = self.Font.render(string, self.Alias, shadowcolor)
            self.Foreground.blit(text, (posX+self.OffsetX, posY+self.OffsetY+shadowdist))
        text = self.Font.render(string, self.Alias, color)
        self.Foreground.blit(text, (posX+self.OffsetX, posY+self.OffsetY))

    def text(self, x, y, string, center=(0, 0), padchars=("", ""), transbg=True, color=None, vertical=False, shadow=1, shadowcolor=(20, 20, 20)):
        if color is None:
            color = self.DefColor
        string = str(padchars[0]) + str(string) + str(padchars[1])
        if center[1]:
            if vertical:
                y = x + round(((self.CellsHeight/2) - (len(string)/2)))
            else:
                y = y + round((self.CellsHeight/2))
        else:
            y = y
        if center[0]:
            if vertical:
                x = y + round((self.CellsWidth/2))
            else:
                x = x + round(((self.CellsWidth/2) - (len(string)/2)))
        else:
            x = x
        for num, char in enumerate(string):
            if transbg:
                if not vertical:
                    if shadow:
                        self.setStringBlock(x+num, y+0.07, char, color=shadowcolor)
                    self.setString(x+num, y, char, color=color)
                else:
                    if shadow:
                        self.setStringBlock(x+num, y+0.07, char, color=shadowcolor)
                    self.setString(x, y+num, char, color=color)
            else:
                if not vertical:
                    if shadow:
                        self.setStringBlock(x+num,  y+0.07, char, color=shadowcolor, bgcolor=self.DefBgColor)
                    self.setStringBlock(x+num, y, char, color=color, bgcolor=self.DefBgColor)
                else:
                    if shadow:
                        self.setStringBlock(x, y+num+0.07, char, color=shadowcolor)
                    self.setStringBlock(x, y+num, char, color=color)

    def textSimple(self, x, y, string, color=None):
        if color is None:
            color = self.DefColor
        for num, char in enumerate(string):
            self.setString(x+num, y, char, color=color)

    def box(self, x, y, w, h, filled=1, color=None, bg=0):
        if color is None:
            color = self.DefColor
        posX = (self.CellX * x) + (self.Margin * 2)
        posY = (self.CellY * y) + (self.Margin * 2)
        posW = (self.CellX * w) + (self.Margin * 2)
        posH = (self.CellY * h) + (self.Margin * 2)

        if filled:
            if bg:
                pygame.draw.rect(self.Background, color, (posX, posY, posW, posH))
            else:
                pygame.draw.rect(self.Foreground, color, (posX, posY, posW, posH))
        else:
            if bg:
                pygame.draw.rect(self.Background, color, (posX, posY, posW, self.CellY))
                pygame.draw.rect(self.Background, color, (posX, posY, self.CellX, posH))
                pygame.draw.rect(self.Background, color, (posX, posH+posY, posW+self.CellX, self.CellY))
                pygame.draw.rect(self.Background, color, (posW+posX, posY, self.CellX, posH))
            else:
                pygame.draw.rect(self.Foreground, color, (posX, posY, posW, self.CellY))
                pygame.draw.rect(self.Foreground, color, (posX, posY, self.CellX, posH))
                pygame.draw.rect(self.Foreground, color, (posX, posH+posY, posW+self.CellX, self.CellY))
                pygame.draw.rect(self.Foreground, color, (posW+posX, posY, self.CellX, posH))

    def boxoutline(self, x, y, w, h, color=None, outline=None, bg=0):
        self.box(x, y, w, h, color=color, bg=bg)
        self.box(x, y, w-1, h-1, color=outline, filled=0, bg=bg)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkexit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()

    def clear(self):
        self.Background.fill(self.DefBgColor)
        self.Foreground.fill(0)

    def tick(self, fps):
        if not fps <= 0:
            self.Clock.tick(fps)

    def getfps(self):
        return self.Clock.get_fps()

    def blit(self):
        self.Screen.blit(self.Background, (0, 0))
        self.Screen.blit(self.Foreground, (0, 0))

    def listkeys(self):
        return pygame.key.get_pressed()

    def update(self, fps, clear=True, skip=0, update=True):
        if skip == 0:
            self.Skip = 0
        else:
            self.Skip += 1
        if self.Skip == skip:
            if update:
                self.blit()
            pygame.display.update()
            self.Skip = 0
            if fps > 0:
                self.tick(fps)
            if clear:
                self.clear()
        else:
            pygame.display.update()
            if fps > 0:
                self.tick(fps)
            if clear:
                self.clear()

