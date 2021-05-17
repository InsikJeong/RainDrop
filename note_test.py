import librosa

y, sr = librosa.load('/music/reminiscence.wav',sr=44100)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
time = len(onset_env)/librosa.get_duration(y=y, sr=sr)
listArr = list(onset_env)
avg = sum(listArr)/len(listArr)

arr = {}
status = False

