import pygame
from pelielementit import Palikat, arvo_xy, KuvaOlio
from random import randint, seed
seed(666)


class Peli:                       
    nurmi_vihr = (80,150,85)
    pinkki= (220,109,164)
    ruskea = (216,179,101)
    vaal_harmaa = (90,90,90)
    tumma_harmaa = (64,64,64)
    punainen = (197,27,125)
    tumma_ruskea = (116,79,1)
    valkoinen = (245,245,245)
    
    def __init__(self):
        pygame.init()
        self.nimi = "Kimalainen"
        self.naytto = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(self.nimi)
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.suunta = "vasen"
        self.pahis,\
        self.oma_hahmo,\
        self.siitepoly,\
        self.life,\
        self.talot,\
        self.pensaat,\
        self.talo,\
        self.pensas,\
        self.apu = self.pura_palikat()
        self.kesto = 200
        self.koti = pygame.image.load("kuvat/koti.png")
        self.koti_rect = self.koti.get_rect()
        self.nuolet = pygame.image.load("kuvat/nuolinapit.png")
        self.starttaus()
        self.luuppi()

    def starttaus(self):
        aja = True
        self.naytto.blit(pygame.image.load("kuvat/kansikuva.png"), (0,0))
        pygame.display.update()
        while aja:
            napit = pygame.key.get_pressed()
            if napit[pygame.K_RETURN]:
                aja = False
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
        self.aloitus = self.sekunnit()

    def sekunnit(self):
        """ Antaa pygame-ajan sekunteina """
        return int(pygame.time.get_ticks()/1000)

    def pura_palikat(self):
        """return: pahis, oma_hahmo, siitepoly, life, talot, pensaat, apu""" 
        palikat = Palikat()
        
        return palikat.pahis, palikat.oma_hahmo, palikat.siitepoly, palikat.life, \
            palikat.talot, palikat.pensaat, palikat.talo, palikat.pensas, palikat.apu

    def tapahtumat(self):
            napit = pygame.key.get_pressed()

            # vasemmalle
            if napit[pygame.K_LEFT]==True:
                self.suunta = "vasen"
                if self.oma_hahmo.rect.x > 3:
                    if self.oma_hahmo.rect.centerx in range(170,470) or self.apu["seis"]:
                        self.oma_hahmo.rect.x -= 3
                    else:
                        # kasvillisuudessa liikkuu hitaammin
                        self.oma_hahmo.rect.x -= 1.5
            # oikealle
            if napit[pygame.K_RIGHT]==True:
                self.suunta = "oikea"
                if self.oma_hahmo.rect.x < 640 - self.oma_hahmo.width:
                    if self.oma_hahmo.rect.centerx in range(170,470) or self.apu["seis"]:
                        self.oma_hahmo.rect.x += 3
                    else:
                        self.oma_hahmo.rect.x += 1.5
            # ylös
            if napit[pygame.K_UP]:
                if self.oma_hahmo.rect.y > 200:
                    if self.oma_hahmo.rect.x in range(170,420) or self.apu["seis"]:
                        self.oma_hahmo.rect.y -= 3
                    else:
                        self.oma_hahmo.rect.y -= 1.5
            # alas
            if napit[pygame.K_DOWN]:
                if self.oma_hahmo.rect.y < 350:
                    if self.oma_hahmo.rect.x in range(170,420) or self.apu["seis"]:
                        self.oma_hahmo.rect.y += 3
                    else:
                        self.oma_hahmo.rect.y += 1.5
            # maisema nopeutuu
            if napit[pygame.K_q]:
                self.apu["vauhti"]=2
            else: self.apu["vauhti"]=1
            
            #ESC
            if napit[pygame.K_ESCAPE]:
                exit()
            #UUSI PELI
            if napit[pygame.K_SPACE]:
                Peli()
            #ruksista ulos
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()

    def luuppi(self):
        kello = pygame.time.Clock()
        while True:
            #aikamuuttujia
            if not self.apu["seis"]:
                self.apu["seconds"] = self.sekunnit() - self.aloitus # start-ruudun aika pois laskusta
            etenemisprosentti = self.apu["seconds"]/self.kesto*100
            # pahis ajoitus
            if etenemisprosentti in (5.0, 20.0, 40.0, 60.0, 70.0, 85.0):
                self.pahis.irti = True
            if self.peli_lapi() or self.kuolo():
                self.apu["seis"] = True

            self.tapahtumat()
            self.pahis_liike()
            self.seuraukset()
            self.piirra_kaikki()

            pygame.display.flip()

            kello.tick(80)

    def peli_lapi(self):
        if self.apu["siitepolypss"]==35:
             return True

    def kuolo(self):
        if self.oma_hahmo.lifebar<=0 or self.apu["seconds"]==self.kesto and not self.peli_lapi():
             return True

    def pahis_liike(self):
        if self.apu["seis"]:
            return
        if self.pahis.irti:
            if self.pahis.rect.x > self.oma_hahmo.rect.x and self.pahis.rect.x > 120:
                self.pahis.rect.x -= 2                    
            if self.pahis.rect.x < self.oma_hahmo.rect.x and self.pahis.rect.x < 455 + self.pahis.width:
                self.pahis.rect.x += 2
            self.pahis.rect.y += self.apu["vauhti"]
            if self.pahis.rect.y>430:
                self.pahis.irti = False
                self.pahis.rect.x =320
                self.pahis.rect.y = -20


    # Esineitä on paljon --> kaikkien maskitarkistus syö muistia ja 
    # hidastaa enemmän kuin kulmiotarkistukset, joten
    # laatikkomaiset asiat tarkistetaan kulmioina.
    def kulmio_osumat(self, esine):
        """ esine: 'esteet', 'resurssit' tai 'koti'
        Muistitaloudellinen tapa tarkistaa osumia.
        Kohtaamisesta riippuen lisää tai vähentää resursseja."""

        #osuuko hahmo kotipesään lopussa
        if esine=="koti":
            return self.oma_hahmo.rect.colliderect(self.koti_rect)
        
        # osuuko hahmo siitepölyyn (kerättävä) tai mesipalloon (energiaa)
        elif esine=="resurssit":
            saatu_siitepoly = False
            saatu_life = False

            if self.oma_hahmo.rect.colliderect(self.siitepoly.rect)==True:
                saatu_siitepoly = True
            if self.oma_hahmo.rect.colliderect(self.life.rect)==True:
                saatu_life = True

            if self.siitepoly.rect.y > 450 or saatu_siitepoly:
                if saatu_siitepoly:
                    self.apu["siitepolypss"] += 1
                self.siitepoly.rect.x, self.siitepoly.rect.y = arvo_xy("siitepoly")
            
            if self.life.rect.y > 450 or saatu_life:
                if saatu_life:
                    if self.oma_hahmo.lifebar <=150:
                        self.oma_hahmo.lifebar += 50
                    else:
                        self.oma_hahmo.lifebar = 200
                self.life.rect.x, self.life.rect.y = arvo_xy("life")

        elif esine=="esteet":
            if self.pahis.irti:
                esteet = self.talot + [self.pahis.rect]  #estekulmiolista
            else: esteet = self.talot
            osuma = self.oma_hahmo.rect.collidelist(esteet)
            #Jos ei osumaa: -1. Muutoin antaa osumakulmion indeksin.

            # Indeksi 15 on pahis (myrkkypurkki) ja muut taloja.
            if self.oma_hahmo.rect.collidelist(esteet)>=0:
                if osuma==15:
                    self.oma_hahmo.lifebar -= 0.5
                else: self.oma_hahmo.lifebar -= 0.2

                return True

    def maskiosumat(self):
        """ Tarkista vahingoittavat maskikohtaamiset ja vähennä energiaa."""
        kolhu = False
        pensas = self.pensas.mask_vas  #pensaan maski
        if self.suunta == "vasen":     #oma maski
            oma_maski = self.oma_hahmo.mask_vas
        else:
            oma_maski = self.oma_hahmo.mask_oik

        #tarkista pensaiden maskiosumat
        for i in self.pensaat:
            if oma_maski.overlap(pensas, (i.x - self.oma_hahmo.rect.x, \
                i.y - self.oma_hahmo.rect.y)):
                kolhu = True
                self.oma_hahmo.lifebar -= 0.2

        return kolhu

    def seuraukset(self):
        """ osumien tarkistus ja seuraukset: resurssien muutos ja uudet sijainnit """
        # peruuta jos peli on jo ohi
        if self.apu["seis"]:
            return

        # tarkista kulmio-osumat resursseille
        self.kulmio_osumat('resurssit')

        #tarkista maski- ja kulmio-osumat esteille
        if self.maskiosumat() or self.kulmio_osumat('esteet'):
            self.oma_hahmo.auts = True
        else: self.oma_hahmo.auts = False
        
    def piirra_kaikki(self):
        # piirrä pohja
        self.naytto.fill(Peli.nurmi_vihr)
        if not self.apu["seis"]:
            pygame.draw.rect(self.naytto, Peli.ruskea, (195, -5, 250, 485))
            pygame.draw.rect(self.naytto, Peli.tumma_ruskea, (195, -5, 250, 485),1)

        # jos peli lopussa, seisauta esteet ja piirrä loppuviestit
        if self.apu["seis"]: 
            if self.kuolo():
                self.naytto.fill(Peli.tumma_harmaa)
                self.naytto.blit(pygame.image.load("kuvat/uusi_peli.png"), (110,360))
                if self.oma_hahmo.lifebar<=0:
                    self.naytto.blit(pygame.image.load("kuvat/ilmo_energia_loppui.png"), (0,0))
                else:
                    self.naytto.blit(pygame.image.load("kuvat/ilmo_aika_loppui.png"), (0,0))

            elif self.peli_lapi():
                self.koti_rect.center = (100,300)
                # muut kimalaiset ja tekstit
                self.naytto.blit(self.koti, (100,300))
                self.naytto.blit(self.oma_hahmo.oik, (60, 270))
                self.naytto.blit(self.oma_hahmo.vas, (220, 250))
                lopputeksti = pygame.image.load("kuvat/peli_ok2.png")
                self.naytto.blit(lopputeksti, (0,0))
                
                # kimalainen lentää pesään
                if self.kulmio_osumat("koti"):
                    exit()

        # peruskuvitukset:
        # pensaat ja talot kuvataan eri suunnista sijainnista riippuen
        # ja arvotaan uudet y-arvot ruudusta poistuneille
        else:
            for i in self.talot:
                if i.x >=340:
                    self.naytto.blit(self.talo.vas, i)
                else:
                    self.naytto.blit(self.talo.oik, i)
                i.y += self.apu["vauhti"]
                if i.y>450:
                    i.y = randint(-2000, -50)

            for i in self.pensaat:
                if i.x <=340:
                    self.naytto.blit(self.pensas.vas, i)
                else:
                    self.naytto.blit(self.pensas.oik, i)
                i.y += self.apu["vauhti"]
                if i.y>450:
                    i.y = randint(-2000, -50)
            
            # merkkaa kimalaisen punaisella, jos vahingoittuu
            if self.oma_hahmo.auts:
                pygame.draw.circle(self.naytto,Peli.punainen,self.oma_hahmo.rect.center, 35)

            # piirrä (ja päivitä sijainti): 1) siitepoly, 2) life ja 3) pahis
            self.naytto.blit(self.siitepoly.vas, self.siitepoly.rect)   # 1)
            self.siitepoly.rect.y += self.apu["vauhti"]

            self.naytto.blit(self.life.vas, self.life.rect)             # 2)   
            self.life.rect.y += self.apu["vauhti"]

            if self.pahis.irti:                                         # 3)
                if self.oma_hahmo.rect.x > self.pahis.rect.x:
                    pahis = self.pahis.oik
                else:
                    pahis = self.pahis.vas
                self.naytto.blit(pahis, self.pahis.rect)

        # piirrä pelaaja kaiken päälle, jos elossa:
        if not self.kuolo():
            if self.suunta=="oikea":
                oma_hahmo_suunta = self.oma_hahmo.oik
            else: oma_hahmo_suunta = self.oma_hahmo.vas
            self.naytto.blit(oma_hahmo_suunta, self.oma_hahmo.rect)
        
        # ALAPALKKI  -----  loput rivit -----
        pygame.draw.rect(self.naytto, Peli.tumma_harmaa, (0, 430, 640, 50))

        # life bar
        if self.oma_hahmo.lifebar <=80:
            vari=Peli.punainen
        else: vari = Peli.pinkki
        pygame.draw.rect(self.naytto, (200,200,200), (530, 455, 100, 20))
        pygame.draw.rect(self.naytto, vari, (530, 455, self.oma_hahmo.lifebar/2, 20))
        teksti1 = self.fontti.render(f"Energia", True, Peli.valkoinen)

        #timebar
        pygame.draw.rect(self.naytto, (200,200,200), (400, 455, 100, 20))
        pygame.draw.rect(self.naytto, Peli.vaal_harmaa, (400, 455, (self.kesto-self.apu["seconds"])/2, 20))
        aikaa = self.fontti.render(f"Aika", True, Peli.valkoinen)

        #siitepoly
        siitepolytilanne = self.apu["siitepolypss"]-35
        if self.apu["siitepolypss"]<35:
            siitepolytilanne = self.apu["siitepolypss"]-35
            siitepolyvari = (200,200,200)
        else:
            siitepolytilanne = self.apu["siitepolypss"]
            siitepolyvari = Peli.nurmi_vihr
        teksti2 = self.fontti.render(f"Siitepöly", True, Peli.valkoinen)
        teksti2B = self.fontti.render(f"{siitepolytilanne}", True, siitepolyvari)
        
        #komentoinfo
        teksti3 = self.fontti.render(f"                 Q          Esc", True, Peli.valkoinen)
        teksti3B = self.fontti.render(f"ohjaus   vauhtia      ulos", True, (200,200,200))
        
        self.naytto.blit(teksti1, (538, 430))   # Energia
        self.naytto.blit(aikaa, (425, 430))     # Aika
        self.naytto.blit(teksti2, (295, 430))   # Siitepöly
        self.naytto.blit(teksti2B, (317, 454))  # nr (siitepöly)
        self.naytto.blit(teksti3, (10, 430))    # Q , Esc
        self.naytto.blit(teksti3B, (10, 454))   # ohjaus, vauhtia, ulos
        self.naytto.blit(self.nuolet, (25, 435)) #nuolinapit
        pygame.draw.line(self.naytto, Peli.vaal_harmaa, (89,430),(89,480), width = 2) # nappitoimintojen väliviivat
        pygame.draw.line(self.naytto, Peli.vaal_harmaa, (188,430),(188,480), width = 2)
        pygame.draw.line(self.naytto, Peli.vaal_harmaa, (281,430),(281,480), width = 2)
        

if __name__ == "__main__":
    Peli()