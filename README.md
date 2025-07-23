# youtube_video_downloader

## Description
유튜브 영상을 최고 해상도로 다운받는 스크립트.

## 특징
선호 해상도 설정가능<br>
디바이스가 AV1 코덱 지원한다면 4k 해상도 다운로드 지원

<br>
<br>
## Prerequisite
ffmpeg 설치 필요 
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

## Usage
### 아래 사용자 설정 후 스크립트 실행
```
선호 해상도 : preferred_resolution
파일 저장 위치 : SAVE_PATH
다운로드할 유튜브 url 리스트 : video_list
디바이스가 AV1 코덱 지원한다면 line 155~159  활성화
```
<br>
<br>

## 실행 화면
<img width="843" height="431" alt="image" src="https://github.com/user-attachments/assets/a2bc4de3-4bbd-4af9-a917-3b9a6dcec76d" />
![Uploading image.png…]()
