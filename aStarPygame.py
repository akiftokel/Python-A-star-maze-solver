import pygame
import sys
import time

# [x,y] olarak robot ve hedef koordinatları girilmeli
başlangıç = [2,2]
hedef = [8,8]

# Haritanın duvarları ve yolları için (rakamın anlamı yok)
duvar = 0
yol = 1

# Haritanın büyüklüğü
satır = 10
sütun = 10

# Haritayı oluşturan kod
harita = []
def haritaOluştur():
    for i in range(satır):
        harita.append([])
    for i in harita:
        for j in range(sütun):
            i.append(yol)
    # Dış duvarlar
    for i in range(satır):
        harita[i][0] = duvar
    for i in range(satır):
        harita[i][sütun-1] = duvar
    for i in range(sütun):
        harita[0][i] = duvar
    for i in range(sütun):
        harita[satır-1][i] = duvar

haritaOluştur()

# Manhattan haritası bütün noktaların hedefe olan manhattan uzaklıklarını hesaplar ve o indexe hesaplanan i atar.
manhattanHaritası = []
for i in range(satır):
    manhattanHaritası.append([])
for i in manhattanHaritası:
    for j in range(sütun):
        i.append(0)
def manhattanOluştur():
    x = 0
    y = 0
    for i in harita:
        for j in i:
            # Haritadaki her bir noktanın hedefe olan mutlak uzaklığını hesaplar ve manhattan haritasına atar
            manhattanHaritası[y][x] = abs(hedef[0] - x) + abs(hedef[1] - y)
            x += 1
        x = 0
        y += 1

manhattanOluştur()

def komşuAdresleri():
    global sağAdres, solAdres, yukarıAdres, aşağıAdres
    sağAdres = [başlangıç[0]+1,başlangıç[1]]
    solAdres = [başlangıç[0]-1,başlangıç[1]]
    yukarıAdres = [başlangıç[0],başlangıç[1]-1]
    aşağıAdres = [başlangıç[0],başlangıç[1]+1]

komşuAdresleri()

def komşular():
    global sağ, sol, yukarı, aşağı
    sağ = harita[başlangıç[1]][başlangıç[0]+1]
    sol = harita[başlangıç[1]][başlangıç[0]-1]
    yukarı = harita[başlangıç[1]-1][başlangıç[0]]
    aşağı = harita[başlangıç[1]+1][başlangıç[0]]

komşular()

def komşuManhattan():
    global sağManhattan, solManhattan, yukarıManhattan, aşağıManhattan
    sağManhattan = manhattanHaritası[başlangıç[1]][başlangıç[0]+1]
    solManhattan = manhattanHaritası[başlangıç[1]][başlangıç[0]-1]
    yukarıManhattan = manhattanHaritası[başlangıç[1]-1][başlangıç[0]]
    aşağıManhattan = manhattanHaritası[başlangıç[1]+1][başlangıç[0]]

komşuManhattan()

def kapalıAdres(x):
    for i in kapalıAdresler:
        if i == x:
            return True

kapalıAdresler = []
liste = [[başlangıç,str(başlangıç),manhattanHaritası[başlangıç[1]][başlangıç[0]]]]

def aynıAdresVeUzaklık(x):
    for i in liste:
        if x == i[0] and len(liste[0][1]+","+str(x)) >= len(i[1]):
            return True

def adresAç():
    if sağ != duvar and kapalıAdres(sağAdres) != True and aynıAdresVeUzaklık(sağAdres) != True:
        liste.append([sağAdres,liste[0][1]+","+str(sağAdres),sağManhattan+liste[0][1].count("[")])
    if sol != duvar and kapalıAdres(solAdres) != True and aynıAdresVeUzaklık(solAdres) != True:
        liste.append([solAdres,liste[0][1]+","+str(solAdres),solManhattan+liste[0][1].count("[")])
    if yukarı != duvar and kapalıAdres(yukarıAdres) != True and aynıAdresVeUzaklık(yukarıAdres) != True:
        liste.append([yukarıAdres,liste[0][1]+","+str(yukarıAdres),yukarıManhattan+liste[0][1].count("[")])
    if aşağı != duvar and kapalıAdres(aşağıAdres) != True and aynıAdresVeUzaklık(aşağıAdres) != True:
        liste.append([aşağıAdres,liste[0][1]+","+str(aşağıAdres),aşağıManhattan+liste[0][1].count("[")])        

def aStar():
    global başlangıç
    while başlangıç != hedef:
        adresAç()
        kapalıAdresler.append(liste[0][0])
        liste.pop(0)
        liste.sort(key=lambda x: (x[2], len(x[1])))
        başlangıç = liste[0][0]
        komşuAdresleri();komşular();komşuManhattan()
        haritaYaz()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)
    # En kısa yolun yazdırılması
    rota = liste[0][1].split("],[")
    rota[0] = rota[0][1:]
    rota[-1] = rota[-1][:-1]
    for i in range(len(rota)):
        rota[i] = rota[i].split(", ")
        for j in range(len(rota[i])):
            rota[i][j] = int(rota[i][j])
    rota.pop(-1)
    for i in rota:
        pygame.draw.rect(ekran, (0, 255, 0), (i[0]*100+5, i[1]*100+5, 90, 90))
        pygame.display.update()

pygame.init()
ekran = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption("A*")
ekran.fill((50, 50, 50))
panel = pygame.image.load("panel.png").convert_alpha()

def haritaDuvarListesiYap():
    global haritaDuvarListesi
    haritaDuvarListesi = []
    duvarx = 0
    duvary = 0
    for y in harita:
        for x in y:
            if x == duvar:
                haritaDuvarListesi.append((duvarx*100,duvary*100))
            duvarx += 1
        duvarx = 0
        duvary += 1

def haritaYolListesiYap():
    global haritaYolListesi
    haritaYolListesi = []
    yolx = 0
    yoly = 0
    for y in harita:
        for x in y:
            if x == yol:
                haritaYolListesi.append((yolx*100,yoly*100))
            yolx += 1
        yolx = 0
        yoly += 1

def haritaYaz():
    haritaDuvarListesiYap()
    haritaYolListesiYap()
    for i in haritaDuvarListesi:
        pygame.draw.rect(ekran,(0,0,0),(i[0]+5,i[1]+5,90,90))
    for i in haritaYolListesi:
        pygame.draw.rect(ekran,(255,255,255),(i[0]+5,i[1]+5,90,90))
    for i in liste:
        pygame.draw.rect(ekran,(255,255,0),(i[0][0]*100+5,i[0][1]*100+5,90,90))
    for i in kapalıAdresler:
        pygame.draw.rect(ekran,(255,100,0),(i[0]*100+5,i[1]*100+5,90,90))
    pygame.draw.rect(ekran,(0,0,255),(hedef[0]*100+5,hedef[1]*100+5,90,90))
    pygame.draw.rect(ekran,(255,0,0),(başlangıç[0]*100+5,başlangıç[1]*100+5,90,90))
    ekran.blit(panel,(1000,0))

aStarBaşla = False
haritaYaz()
clock = pygame.time.Clock()
FPS = 30
run = True
while run:
    clock.tick(FPS)
    pygame.display.update()

    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if aStarBaşla == True:
            aStar()
            aStarBaşla = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                haritax = mx//100
                haritay = my//100
                if 0<haritax<sütun-1 and 0<haritay<satır-1:
                    if haritax == başlangıç[0] and haritay == başlangıç[1]:
                        pass
                    else:
                        if haritax == hedef[0] and haritay == hedef[1]:
                            pass
                        else:
                            if başlangıç[0] == 0 and başlangıç[1] == 0:
                                başlangıç[0] = haritax
                                başlangıç[1] = haritay
                            elif hedef[0] == sütun-1 and hedef[1] == satır-1:
                                hedef[0] = haritax
                                hedef[1] = haritay
                            else:
                                harita[haritay][haritax] = duvar
                if 1100 < mx < 1400 and 400 < my < 600:
                    if başlangıç == [0,0] or hedef == [sütun-1,satır-1]:
                        pass
                    else:
                        aStarBaşla = True
    
            if event.button == 3:
                haritax = mx//100
                haritay = my//100
                if 0<haritax<sütun-1 and 0<haritay<satır-1:
                    harita[haritay][haritax] = yol
                    if haritax == başlangıç[0] and haritay == başlangıç[1]:
                        başlangıç = [0,0]
                    if haritax == hedef[0] and haritay == hedef[1]:
                        hedef = [sütun-1,satır-1]
            kapalıAdresler = []
            liste = [[başlangıç,str(başlangıç),manhattanHaritası[başlangıç[1]][başlangıç[0]]]]
            manhattanOluştur()
            komşuAdresleri();komşular();komşuManhattan()
            haritaYaz()
                         
pygame.quit()      