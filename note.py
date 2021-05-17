import librosa, random

def makeNote(file_name):
    y, sr = librosa.load('music/'+file_name,sr = 44100)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    time = len(onset_env)/librosa.get_duration(y=y, sr=sr)
    listArr = list(onset_env)
    avg = sum(listArr)/len(listArr)

    arr = {}
    status = False
    # 최고점 구하기
    for i in range(len(listArr)):
        if listArr[i] > avg*2:
            if not status:
                status = True
                min = i
        elif status:
            maxValue = max(listArr[min:i+1])
            arr[min] = maxValue
            status = False

    valueArr = list(arr.values())
    timeArr = [i/time for i in list(arr.keys())]
    outputArr = [[],[],[],[],[],[]]
    arrTmp = [0,1,2,3,4,5]

    # 노트 타이밍에 맞게 배치
    for i in range(len(valueArr)):
        note = int(valueArr[i]) % 6
        timming = timeArr[i]
        if len(outputArr[note]) > 0:
            if outputArr[note][-1] < timming-0.3:
                outputArr[note].append(timming)
            else:
                cnt = 0
                tmp = 0.0
                while True:
                    rnd = random.choice(arrTmp)                    
                    cnt += 1
                    if cnt % 50 == 0:
                        tmp = tmp + 0.001
                    if len(outputArr[rnd]):
                        if outputArr[rnd][-1] < timming-0.3+tmp:
                            outputArr[rnd].append(timming)
                            break
                    else:
                        outputArr[note].append(timming)
        else:
            outputArr[note].append(timming)
                    
            

    # .txt 로 출력
    f = open('note/'+file_name[0:-4]+'.txt','w')
    for i in range(6):
        f.write('#'+str(i+1)+'\n')
        for j in outputArr[i]:
            f.write(str(j)+'\n')
    f.close()

# makeNote("ShoutBaby.wav")