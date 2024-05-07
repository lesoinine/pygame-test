import pygame
from random import randint, choice, shuffle, seed
seed(666)

def arvo_xy(esine:str):
        """ arpoo sijainteja (x,y) esteille sen mukaan missä niitä saa esiintyä
        """
        #vain nurmikolle asettuvat x-koordinaatit:
        nurtsi = [i for i in range(0,170)] + [i for i in range(455,520)]
        shuffle(nurtsi)
        shuffle(nurtsi)

        if esine =="talo":                   
            return randint(0,590), randint(-5000,-100)
        if esine=="life":                     
            return randint(100,500), randint(-500,-200)
        if esine =="pensas":                
            return choice(nurtsi), randint(-6000,-100)
        if esine =="siitepoly":                 
            return choice(nurtsi), randint(-500,-200)

class KuvaOlio:
    '''id: "pahis", "oma_hahmo","siitepoly", "life", "este"'''
    def __init__(self, png:str, id:str):
        self.id = id
        self.vas = pygame.image.load(png).convert_alpha()
        self.oik = pygame.transform.flip(self.vas, True, False)
        self.rect = self.vas.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.mask_vas = pygame.mask.from_surface(self.vas)
        self.mask_oik = pygame.mask.from_surface(self.oik)
        if id =="pahis":
            self.rect.x, self.rect.y = 320, -86
            self.irti = False
        if id == "life":
            self.rect.x, self.rect.y = 320, -350
        if id == "oma_hahmo":
            self.rect.x, self.rect.y = 320, 350
            self.auts = False
            self.lifebar = 200
        if id == "siitepoly":
            self.rect.x, self.rect.y = 500, -200
            
    def __str__(self):
        return f"{self.id}:{self.height} x {self.width}px, blit at x:{self.rect.x},{self.rect.y}"

class Palikat:
    def __init__(self):
        self.pahis = KuvaOlio("kuvat/myrkky.png", "pahis")
        self.oma_hahmo = KuvaOlio("kuvat/oma_hahmo3.png", "oma_hahmo")
        self.siitepoly = KuvaOlio("kuvat/siitepoly.png", "siitepoly")
        self.life = KuvaOlio("kuvat/mesi.png", "life")
        self.talo = KuvaOlio("kuvat/kerrostalo.png", "este")
        self.pensas = KuvaOlio("kuvat/lintupuska.png", "este")
        self.talot = [self.tee_esteet("talo") for i in range(15)]
        self.pensaat = [self.tee_esteet("pensas") for i in range(15)]
        self.apu = self.apurit()

    def tee_esteet(self, este:str):
        """ este: 'talo' tai 'pensas' 
        Palauttaa suorakulmiomääritelmän taloille ja pensaille"""
        if este =="talo":
            arvot = arvo_xy("talo")
            este = self.talo.rect.copy()
            este.x = arvot[0]
            este.y =arvot[1]
        if este=="pensas":
            arvot = arvo_xy("pensas")
            este = self.pensas.rect.copy()
            este.x = arvot[0]
            este.y = arvot[1]
        return este
        
    def apurit(self):
        apurit={
        "siitepolypss" : 0,
        "vauhti": 1,
        "seis" : False,
        "seconds": 0,
        }
        return apurit