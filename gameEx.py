import pygame, time, timeit, threading, librosa, copy

score_status = [0,0,0,0]
score = 0
combo = 0
maxCombo = 0
clicked = 0
display_score = 0

running = True

def play_game(musicName):
    #게임 셋팅
    FPS = 100
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    S_HEIGHT = WINDOW_HEIGHT - 50

    SCORE_STRING = ["GREAT", " GOOD", " ALSO", " MISS", "COMBO", "SCORE"]
    WHITE = [255, 255, 255]

    SHOWN_TIME = 2000
    SPEED_RATE = 1.5

    effect_opacity = [ 0 for _ in range(7)]

    #게임 Init
    sounds = pygame.mixer
    sounds.pre_init(44100, -16, 2, 512)
    sounds.init()


    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Piano Game')

    #이미지 로드
    noteImage = pygame.image.load('image/note.png')
    noteImage = pygame.transform.scale(noteImage, (60, 20))
    noteImage2 = pygame.image.load('image/note2.png')
    noteImage2 = pygame.transform.scale(noteImage2, (60, 20))
    note_effect = pygame.image.load('image/note-effect.png').convert_alpha()
    note_effect.set_alpha(125)
    note_effect = pygame.transform.scale(note_effect, (60,250))
    background = pygame.image.load('image/back.png')
    comboImage = pygame.image.load('image/combo.png')
    comboImage = pygame.transform.scale(comboImage, (200, 200))
    buttonImage = pygame.image.load('image/btn.png')
    buttonImage = pygame.transform.scale(buttonImage, (60, 20))
    clickedImage = pygame.image.load('image/btnPress.png')
    clickedImage = pygame.transform.scale(clickedImage, (60, 20))
    buttonImage2 = pygame.image.load('image/btn2.png')
    buttonImage2 = pygame.transform.scale(buttonImage2, (60, 20))
    clickedImage2 = pygame.image.load('image/btnPress2.png')
    clickedImage2 = pygame.transform.scale(clickedImage2, (60, 20))

    allNoteList = pygame.sprite.Group()
    allComboList = pygame.sprite.Group()
    #노트 파일 로드 [ 시작 전에 노래 이름 받아 옴 ]
    tmpArray = []
    display_notes = []
    readTurn = 0
    f = open('note/'+musicName[0:-4]+'.txt', "r")
    for line in f.readlines():
        if line[0] == '#':
            if (readTurn > 0):
                display_notes.append(tmpArray)
                tmpArray = []
            readTurn = int(line[1])
            continue
        line = line.replace("\n", "")
        tmpArray.append(int(float(line) * 1000))
    f.close()
    display_notes.append(tmpArray)
    checking_notes = copy.deepcopy(display_notes)
            
    def getRuntime(): 
        end = timeit.default_timer()
        runtime = int((end - start) * 1000)
        return runtime

    # 노트 클래스
    class Note(pygame.sprite.Sprite):
        def __init__(self, time,image):
            super().__init__()
            self.s_Time = time
            self.image = image
            self.width = 50
            self.rect = self.image.get_rect()
        def update(self):
            if(self.rect.y > WINDOW_HEIGHT):
                allNoteList.remove(self)
                return            
            self.rect.y = WINDOW_HEIGHT - ((self.s_Time - getRuntime()) / (SHOWN_TIME / SPEED_RATE)) * S_HEIGHT - (WINDOW_HEIGHT - S_HEIGHT)

    class Combo(pygame.sprite.Sprite):
        def __init__(self, combo, x):
            super().__init__()
            self.combo = combo
            self.image = comboImage.copy()
            self.rect = self.image.get_rect()
            self.num_x = x
            self.alpha = 255
        def update(self):
            if(self.alpha < 150):
                allComboList.remove(self)
                return
            self.image.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
            myfont = pygame.font.Font("ReenieBeanie-Regular.ttf", 250)    
            label = myfont.render(str(self.combo), 1, WHITE)
            alpha_img = pygame.Surface(label.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255,255,255,self.alpha))
            label.blit(alpha_img,(0,0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(label, (self.num_x, self.rect.y-130))
            self.rect.y = self.rect.y - 1            
            self.alpha = self.alpha - 13       
    # 키 설정
    keys_status = [0, 0, 0, 0, 0, 0]
    class KeyReader(threading.Thread):
        def run(self):
            while running:
                end = timeit.default_timer()
                runtime = getRuntime()
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_a]:
                    effect_opacity[0] = 255
                    if(keys_status[0] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 0)
                    keys_status[0] = 1
                else:
                    keys_status[0] = 0
                if keys[pygame.K_s]:
                    effect_opacity[1] = 255
                    if(keys_status[1] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 1)
                    keys_status[1] = 1
                else:
                    keys_status[1] = 0
                if keys[pygame.K_d]:
                    effect_opacity[2] = 255
                    if(keys_status[2] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 2)
                    keys_status[2] = 1
                else:
                    keys_status[2] = 0
                if keys[pygame.K_j]:
                    effect_opacity[3] = 255
                    if(keys_status[3] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 3)
                    keys_status[3] = 1
                else:
                    keys_status[3] = 0
                if keys[pygame.K_k]:
                    effect_opacity[4] = 255
                    if(keys_status[4] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 4)
                    keys_status[4] = 1
                else:
                    keys_status[4] = 0
                if keys[pygame.K_l]:
                    effect_opacity[5] = 255
                    if(keys_status[5] == 0):
                        sounds.Sound("bgm/hihat.wav").play()
                        checkNote(runtime, 5)
                    keys_status[5] = 1
                else:
                    keys_status[5] = 0
                time.sleep(0.001)

    # 눌렀을 때 판정
    def checkNote(time, key):
        global combo, score, clicked, maxCombo
        global score_status
        abs_min = 999999
        index_min = 0
        if len(checking_notes[key]) > 0:
            try:
                for i in range(0, len(checking_notes[key])):
                    if abs(checking_notes[key][i] - time) < abs_min:
                        abs_min = abs(checking_notes[key][i] - time)
                        index_min = i
                if(abs_min < 120):
                    if abs_min < 40:
                        score_status[0] = score_status[0] + 1
                        score = score + (combo * 0.01 + 1) * 300
                        combo = combo + 1
                        clicked = 0
                    elif abs_min < 80:
                        score_status[1] = score_status[1] + 1
                
                        score = score + (combo * 0.01 + 1) * 300
                        combo = combo + 1
                        clicked = 1
                    else:
                        score_status[2] = score_status[2] + 1
                        score = score + (combo * 0.01 + 1) * 300
                        combo = combo + 1
                        clicked = 2


                    xxx = 140
                    checking_notes[key].pop(index_min)
                    if combo < 10:
                        cmb = Combo(combo,xxx+53)                
                    elif combo < 100:
                        cmb = Combo(combo,xxx+13)
                    else:
                        cmb = Combo(combo,xxx-39)
                    cmb.rect.x = xxx
                    cmb.rect.y = 170
                    allComboList.add(cmb)
            except:
                pass
        if combo > maxCombo :
            maxCombo = combo
    #노트 떨구기
    class NoteReader(threading.Thread):
        def run(self):
            while running:
                for i in range(0, len(display_notes)):
                    if not len(display_notes[i]) is 0:
                        end = timeit.default_timer()
                        runtime = int((end - start) * 1000)
                        temp = SHOWN_TIME / SPEED_RATE
                        if display_notes[i][0] - temp <= runtime:
                            createNote(i, display_notes[i][0])
                            display_notes[i].pop(0)
                checkMiss()
                time.sleep(0.001)


    # 미스 체크
    def checkMiss():
        global combo, score_status, clicked
        for i in range(0, len(checking_notes)):
            if(len(checking_notes[i]) > 0):
                if checking_notes[i][0] - getRuntime() <= -80:
                    checking_notes[i].pop(0)
                    score_status[3] = score_status[3] + 1
                    combo = 0
                    clicked = 3

    # 노트 생성
    def createNote(line, time):
        if line == 1 or line == 4:
            note = Note(time, noteImage2)        
        else:
            note = Note(time, noteImage)        
        note.rect.x = 60 + noteImage.get_rect().width * line
        note.rect.y = 0
        allNoteList.add(note)


    # 이펙트
    def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)


    # 화면 그리기
    def draw():
        global display_score, score_status

        try: 
            for i in range(0, 6):
                keyBox = pygame.Rect(60 + noteImage.get_rect().width * i + 2, 0, noteImage.get_rect().width - 2, WINDOW_HEIGHT)
                pygame.draw.rect(screen, [0,0,0], keyBox)

            allComboList.draw(screen)
            allComboList.update()
            allNoteList.update()
            allNoteList.draw(screen)
            # 라인이랑 키

            for i in range(0, 6):
                keyBox = pygame.Rect(60 + noteImage.get_rect().width * i + 2, S_HEIGHT + 2, noteImage.get_rect().width - 2, WINDOW_HEIGHT - S_HEIGHT - 2)
                pygame.draw.rect(screen, [0,0,0], keyBox)

            pygame.draw.line(screen, WHITE, [60 + noteImage.get_rect().width * 0, 0], [60 + noteImage.get_rect().width * 0, WINDOW_HEIGHT], 4)
            for i in range(1, 6):
                pygame.draw.line(screen, WHITE, [60 + noteImage.get_rect().width * i, 0], [60 + noteImage.get_rect().width * i,WINDOW_HEIGHT], 2)
            pygame.draw.line(screen, WHITE, [60 + noteImage.get_rect().width * 6, 0], [60 + noteImage.get_rect().width * 6,WINDOW_HEIGHT], 4)
            
            for i in range(0, 6):
                if keys_status[i]:
                    if i == 1 or i == 4:
                        screen.blit(clickedImage2,(60 + clickedImage.get_rect().width * i + 2, (S_HEIGHT + 2)-10))    
                    else:
                        screen.blit(clickedImage,(60 + clickedImage.get_rect().width * i + 2, (S_HEIGHT + 2)-10))
                else:
                    if i == 1 or i == 4:
                        screen.blit(buttonImage2,(60 + clickedImage.get_rect().width * i + 2, (S_HEIGHT + 2)-10))    
                    else:
                        screen.blit(buttonImage,(60 + buttonImage.get_rect().width * i + 2, (S_HEIGHT + 2)-10))



            # 이펙트 그리기
            for i in range(0, len(effect_opacity)):
                if not effect_opacity[i] == 1:
                    if effect_opacity[i] -30 >= 0:
                        effect_opacity[i] = effect_opacity[i] - 30
                        blit_alpha(screen, note_effect, (60 + note_effect.get_rect().width * i, S_HEIGHT-250), effect_opacity[i])
                    else:
                        effect_opacity[i] = 0
                        blit_alpha(screen, note_effect, (60 + note_effect.get_rect().width * i, S_HEIGHT-250), effect_opacity[i])
                        

            myfont = pygame.font.SysFont('ReenieBeanie-Regular.ttf', 20)

            totalHit = score_status[0] + score_status[1] + score_status[2] + score_status[3] + 0.0001
            for i in range(0, 4):
                label = myfont.render(SCORE_STRING[i] , 1, WHITE)
                screen.blit(label, (450, 100 + i * 50))
                label = myfont.render(str(score_status[i]) + "    ( " + str(int(score_status[i] / totalHit * 100)) + "% )", 1, WHITE)
                screen.blit(label, (550, 100 + i * 50))

            label = myfont.render(SCORE_STRING[4], 1, WHITE)
            screen.blit(label, (450, 300))
            label = myfont.render(str(maxCombo), 1, WHITE)
            screen.blit(label, (550, 300))
            label = myfont.render(SCORE_STRING[5], 1, WHITE)
            screen.blit(label, (450, 350))
            label = myfont.render(str(int(score)), 1, WHITE)
            screen.blit(label, (550, 350))
            

            pygame.display.flip()
        except:
            pass
    global running
    running = True
    music = sounds.Sound('music/'+musicName)
    music_length = music.get_length()
    music.play()
    clock = pygame.time.Clock()
    start = timeit.default_timer()
    KeyReader().start()
    NoteReader().start()


    global score_status, maxCombo, score, combo

    score_status[0] = 0
    score_status[1] = 0
    score_status[2] = 0
    score_status[3] = 0
    maxCombo = 0
    combo = 0
    score = 0

    while running:
        clock.tick(FPS)
        screen.fill([0, 0, 0])
        screen.blit(background,(0,0))
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit() 
                break
                
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: #esc 누를떄
                    music.stop()
                    runCheck = 1
                    running = False
                    return runCheck

        draw()
        #노래 자동종료
        if getRuntime() > music_length*1030:
            music.stop()
            runCheck = 2
            running = False
            return runCheck
    exit()
    
