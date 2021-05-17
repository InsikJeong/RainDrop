import pygame, os
from pygame.locals import *
from sys import exit
import gameEx
import note

logo = pygame.image.load('image/title_logo6.png')
titleLogo = pygame.transform.scale(logo, (500, 250))

backgroundFileName='image/back.jpg'
menuFontFileName = 'ReenieBeanie-Regular.ttf'
comImg='image/combo.png'

music1 = ''

#-----효과음 ---------
sounds = pygame.mixer
# sounds.pre_init(22050, -16, 2, 4096)

sounds.pre_init(44100, -16, 2, 512)
sounds.init()
# 채널 세팅 /채널0 = 배경음악 /채널1 = 메뉴 효과음/채널2 = 메뉴노래 
sounds.set_num_channels(10) 
# bgm 재생 채널0
sounds.Channel(0).play(sounds.Sound('bgm/bgm.wav'))

pygame.init()

#----색깔------
backgroundColor = (9 , 21 ,33)
BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 74,  191,211)
GREEN= ( 34,177,76)
LIGHT_GREEN= (0,255,0)
RED  = (255,  40,  0)
LIGHT_RED=(255,0,0)
YELLOW = (200,200,0)
LIGHT_YELLOW=(255,255,0)
myColor = (131,36,255)

#-------폰트 크기 조절 -----
smallfont = pygame.font.SysFont(menuFontFileName, 25)
medfont = pygame.font.SysFont(menuFontFileName, 35)
largefont = pygame.font.SysFont(menuFontFileName, 70)
scorefont = pygame.font.SysFont(menuFontFileName, 50)
#----화면 크기, 설정--
display_width = 1280
display_height = 720

screen = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption("Rhythm Game!")

backgroundImage = pygame.image.load(backgroundFileName).convert()
comImage = pygame.image.load(comImg).convert()

font = pygame.font.Font(menuFontFileName, 40)

font = pygame.font.Font(None, 40)
screen.blit(backgroundImage,(0,0)) # 스크린 빌트 = (이미지, (x좌표,y좌표)) 이미지를 좌표점 시작으로 화면에 띄움
            
#-----------화면구성--------------------
def text_objects(text, color, size='small'):

    if size == "small":
        textSurface = smallfont.render(text,True,color)
    if size == "medium":
        textSurface = medfont.render(text,True,color)
    if size == "large":
        textSurface = largefont.render(text,True,color)
    if size == "score":
        textSurface = scorefont.render(text,True,color)
    
    return textSurface, textSurface.get_rect()



def message_to_screen(msg,color,x_displace,y_displace=0,size="small"):   
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2)+x_displace, (display_height/2)+y_displace
    screen.blit(textSurf,textRect)


#------ 결과 창 ---------
def end_game():
    sounds.Channel(3).play(sounds.Sound('bgm/end_game.wav'))
    
    screen.blit(backgroundImage,(0,0))

    enterCheck = 0

    econt = True

    spaceBetweenText=80 

    while econt:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                sounds.Channel(1).play(sounds.Sound('bgm/UpDown.wav'))
                if event.key == pygame.K_ESCAPE:
                    game_title()
                    
        screen.blit(backgroundImage,(0,0))


        myfont = pygame.font.SysFont('ReenieBeanie-Regular.ttf', 20)

        message_to_screen(" !! CLEAR !! ",myColor,-350,-270,"large")
       
        message_to_screen("GREAT     GOOD     BAD     MISS",BLUE,-350,-120,"medium")

        message_to_screen(str(gameEx.score_status[0]),BLACK,-500,-90,"medium")
        message_to_screen(str(gameEx.score_status[1]),BLACK,-382,-90,"medium")
        message_to_screen(str(gameEx.score_status[2]),BLACK,-285,-90,"medium")
        message_to_screen(str(gameEx.score_status[3]) ,BLACK,-193,-90,"medium")

        message_to_screen("MAX COMBO",BLUE,-350,10,"medium")
        message_to_screen(str(gameEx.maxCombo),BLACK,-350,40,"medium")
        
        message_to_screen("SCORE",BLUE,-350,90,"medium")
        message_to_screen(str(int(gameEx.score)),BLACK,-350,120,"score")
        
        pygame.display.update()         
        pygame.time.delay(200)

        pygame.display.update()

    pygame.quit()
    quit()

# ---- 메뉴에서 
def play_menu_music(musicName,check):
    if len(musicName) > check: 
        sounds.Channel(2).stop()
        sounds.Channel(2).play(sounds.Sound('music/'+musicName[check] ))
    else:
        sounds.Channel(2).stop()

def drawMusicList(musicList, check):
    if check > 1:
        text = font.render(musicList[check-2][0:-4], 1, BLUE )
        screen.blit(text, (100,100))
    if check > 0:
        text = font.render(musicList[check-1][0:-4], 1, BLUE )
        screen.blit(text, (100,200))
    
    text = font.render(musicList[check][0:-4], 1, myColor )
    screen.blit(text, (100,300))
    if check < len(musicList)-1:
        text = font.render(musicList[check+1][0:-4], 1, BLUE )
        screen.blit(text, (100,400))
    if check < len(musicList)-2:
        text = font.render(musicList[check+2][0:-4], 1, BLUE )
        screen.blit(text, (100,500))

#------ 노래 선택화면 ---------
def choice_music():
    sounds.Channel(0).stop()

    screen.blit(backgroundImage,(0,0))

    path_dir = os.getcwd()+'/music'
    
    musicList = os.listdir(path_dir)
    
    enterCheck = 0

    drawMusicList(musicList, enterCheck)

    play_menu_music(musicList, enterCheck)

    pygame.display.update() 
        
    #------>Clock<-------
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()  

            timePassed = clock.tick()
            
            if event.type == KEYDOWN: 
                sounds.Channel(1).play(sounds.Sound('bgm/UpDown.wav'))
                if event.key == K_DOWN:
                    if enterCheck < len(musicList)-1 :
                        enterCheck += 1
                    else:
                        enterCheck = len(musicList) -1
                    screen.blit(backgroundImage,(0,0))
                    play_menu_music(musicList,enterCheck)
    
                    drawMusicList(musicList, enterCheck)

                    pygame.display.update()         
                    pygame.time.delay(200)

                elif event.key == K_UP:
                    if enterCheck > 0 :
                        enterCheck -= 1
                    else : 
                        enterCheck = 0
                    screen.blit(backgroundImage,(0,0))
                    play_menu_music(musicList,enterCheck)

                    drawMusicList(musicList, enterCheck)

                    pygame.display.update()
                elif event.key == pygame.K_ESCAPE: #esc 누를떄
                        sounds.Channel(2).stop()
                        sounds.Channel(0).play(sounds.Sound('bgm/bgm.wav'))
                        game_title()

                if event.key == pygame.K_RETURN: #엔터 쳤을때 
                    sounds.Channel(2).stop()
                    if  len(musicList) > enterCheck:
                        musicList[enterCheck]
                        path_dir = os.getcwd()+'/note'    
                        noteList = os.listdir(path_dir)
                        if musicList[enterCheck][0:-4]+'.txt' not in noteList:
                            note.makeNote(musicList[enterCheck])
                        runCheck = gameEx.play_game(musicList[enterCheck])
                        if runCheck == 1:
                            print('esc 종료')
                            sounds.Channel(0).play(sounds.Sound('bgm/bgm.wav'))
                            game_title()
                        if runCheck == 2:
                            print('겜 끝나서 종료')
                            sounds.Channel(0).play(sounds.Sound('bgm/bgm.wav'))
                            end_game()



def game_controls():
    gcont = True


    spaceBetweenText=80 # 텍스트 사이에 간격 조절할 변수

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                sounds.Channel(1).play(sounds.Sound('bgm/UpDown.wav'))
                if event.key == pygame.K_ESCAPE:
                    game_title()
                    
                    
        screen.blit(backgroundImage,(0,0))

        message_to_screen("Control",myColor,-350,-270,"large")
        message_to_screen("KEY : 'A' ,'S' ,'D' ,'J' ,'K' ,'L' " ,BLACK,-350,-50,"medium")
        message_to_screen("ENTER : next",BLACK,-350,10,"medium")
        message_to_screen("ESC : return to Title",BLACK,-350,70,"medium")
        
        pygame.display.update()         
        pygame.time.delay(200)

        pygame.display.update()

    pygame.quit()
    quit()

def game_title():
    titleRun = True
    
    screen.blit(backgroundImage,(0,0)) # 배경그리기
    screen.blit(titleLogo,(0,100))

    optionsList = ["Play Game","Controlls","Exit Game"] # 폴문 돌릴 메뉴 배열

    spaceBetweenText=80 # 텍스트 사이에 간격 조절할 변수
    
    enterCheck = 0  # 0이면 플레이 1이면 컨트롤스 2면 게임나가기 작동/색칠 시키는 변수
                
    for i in range(0,len(optionsList) ):      # 옵션 리스트 그려주는 폴문
        text = font.render(optionsList[i], 1, BLUE )
        screen.blit(text, (100,450+i*spaceBetweenText))

    text = font.render(optionsList[enterCheck], 1, myColor )  # 선택한 옵션만 빨간색으로 칠함 
    screen.blit(text, (100,450+enterCheck*spaceBetweenText)) 

    pygame.display.update() 
        
    clock = pygame.time.Clock()

    while titleRun:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()  

            timePassed = clock.tick()
            
            if event.type == KEYDOWN: 
                sounds.Channel(1).play(sounds.Sound('bgm/UpDown.wav'))
                if event.key == K_DOWN: #방향키 밑으로
                    if enterCheck < 2 :
                        enterCheck += 1
                    else:
                        enterCheck = 2

                    screen.blit(backgroundImage,(0,0))
                    screen.blit(titleLogo,(0,100))
                    for i in range(0,len(optionsList) ):
                        text = font.render(optionsList[i], 1, BLUE )
                        screen.blit(text, (100,450+i*spaceBetweenText) ) #옵션리스트 그릴 좌표 (x,y)
                    
                    text = font.render(optionsList[enterCheck], 1, myColor )
                    screen.blit(text, (100,450+enterCheck*spaceBetweenText)) 

                    pygame.display.update()         
                    pygame.time.delay(200)

                if event.key == K_UP: #방향키 위로
                    if enterCheck > 0 :
                        enterCheck -= 1
                    else : 
                        enterCheck = 0
                    for i in range(0,len(optionsList) ):
                        text = font.render(optionsList[i], 1, BLUE)
                        screen.blit(text, (100,450+i*spaceBetweenText) )

                    text = font.render(optionsList[enterCheck], 1, myColor )
                    screen.blit(text, (100,450+enterCheck*spaceBetweenText)) 

                    pygame.display.update()
                    pygame.time.delay(200)

                if event.key == pygame.K_RETURN: #엔터 쳤을때 
                    if enterCheck == 0:
                        choice_music()
                    if enterCheck == 1:
                        game_controls()
                    if enterCheck == 2:
                        titleRun = False
                        quit()
                    
game_title()