# 🎬 youtube_video_downloader

<br>

## 💡 설명
유튜브 영상을 최고 해상도로 다운받는 스크립트입니다.

### 주요 기능
주요 기능은 아래와 같습니다:

기능 1: 선호하는 해상도를 설정해 유튜브 영상을 mp4 형식으로 다운로드 합니다. <br>
기능 2: 디바이스가 AV1 코덱 지원한다면 4k 해상도로 다운로드 가능합니다.<br>
<br>

### 코드 설명
1) 선호하는 해상도를 설정하면 해당 해상도 이하의 가장 높은 해상도를 찾습니다.
2) 다운로드한 mp4 파일에 오디오가 포함되어있다면
   임시 파일 이름을 변경합니다.
4) 다운로드한 mp4 파일에 오디오가 포함되어있지 않다면
   오디오를 m4a 형식으로 다운로드 받은 후
   ffmpeg로 오디오와 비디오를 병합하고
   임시 파일은 삭제합니다. 
 
<br>
<br>

## 🛠️ 필수 조건
ffmpeg 설치 필요합니다.
```
# mac
brew install ffmpeg
```
<br>

### requirements.txt
```
ffmpeg-python==0.2.0
pytubefix==9.4.1
```
<br>
<br>

## ⚙️ 실행 방법
### 아래 변수 설정 후 스크립트 실행
```
preferred_resolution : 선호 해상도 (기본값 )
SAVE_PATH : 파일 저장 위치
video_list : 다운로드할 유튜브 url 리스트

* 디바이스가 AV1 코덱 지원한다면 line 155~159  활성화
```

<br>
<br>


## 🖥️ 실행 화면
<img width="843" height="431" alt="image" src="https://github.com/user-attachments/assets/a2bc4de3-4bbd-4af9-a917-3b9a6dcec76d" />
<img width="1365" height="754" alt="image" src="https://github.com/user-attachments/assets/c13de43a-6dc2-4406-ba45-8b4a2a06cbc3" />

<br>
<br>
<br>
<br>


## 🔗 참고한 오픈소스
이 코드는 [Stack Overflow pytube 관련 질문 링크]에서 참고한 코드입니다. 원본 코드를 확인하고 싶으면 아래 링크를 방문해 주세요: <br>
https://stackoverflow.com/questions/65355569/get-highest-resolution-function-doesnt-work-in-pytube
