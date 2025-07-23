# youtube_video_downloader

## Description
유튜브 영상을 최고 해상도로 다운받는 스크립트

## Prerequisite
ffmpeg 설치 필요 
```
# mac
brew install ffmpeg
```

ffmpeg-python==0.2.0<br>
pytubefix==9.4.1<br>

## Usage
아래 사용자 설정 후 스크립트 실행<br>
선호 해상도 : preferred_resolution<br>
파일 저장 위치 : SAVE_PATH<br>
다운로드할 유튜브 url 리스트 : video_list<br>
디바이스가 AV1 코덱 지원한다면 line 127~131  활성화<br>
