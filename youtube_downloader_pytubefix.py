#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Python = 3.9
# Created By  : DenverAlmighty
# Created Date: 2025-07-23
# Updated Date : 2025-07-23
# version = '1.0.0'
# ---------------------------------------------------------------------------

import ffmpeg
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

# ANSI 색상 코드 설정 (콘솔에서 출력되는 텍스트의 색상 설정)
RED     =   '\033[1;31m'
YELLOW  =   '\033[1;33m'
GREEN   =   '\033[1;32m'
BLUE    =   '\033[1;34m'
OFF     =   '\033[0;0m '

# 변수 초기화
preferred_video_itag = ''
best_resolution_so_far = '0'
audio_only_itag = ''

################## 사용자 설정 (필수) #########################
# 선호 해상도
# preferred_resolution = '2160' # 4k
preferred_resolution = '1440' # QHD
# 파일 저장 위치
SAVE_PATH = '/Users/username/Downloads'
# 다운로드할 동영상 URL (형식 -> https://www.youtube.com/watch?v=) 
video_list = [
    'https://www.youtube.com/shorts/jHc19tczuzk',
    'https://www.youtube.com/watch?v=evYWmr4L-So',
    ]
## !!디바이스가 AV1 코덱 지원한다면 line 155~159  활성화
############################################################


# 비디오에서 오디오 트랙이 포함되어 있는지 확인하는 함수
# VIDEO example: 
# <Stream: itag='400' mime_type='video/mp4' res='1440p' fps='24fps' vcodec='av01.0.12M.08' progressive='False' sabr='False' type='video'>
# itag='400' ---> res='1440p'
def check_audio_stream(input_file):
    try:
        # ffmpeg를 사용하여 비디오의 오디오 스트림 확인
        probe = ffmpeg.probe(input_file, v='error', select_streams='a', show_entries='stream=codec_type')
        
        # 오디오 스트림 확인
        if 'streams' in probe and len(probe['streams']) > 0:
            print('\n🎶 오디오 트랙이 포함되어 있습니다.')
            return True
        else:
            print('\n❌ 오디오 트랙이 없습니다.')
            return False
    except ffmpeg.Error as e:
    #     print(f'\n❌ 오류 발생: {e}')
        return False

# 가장 높은 해상도 비디오 itag를 찾는 함수
def find_best_resolution(yt, preferred_resolution):
    global preferred_video_itag
    global best_resolution_so_far
    for stream in yt.streams.filter(file_extension='mp4'):
        # 더 높은 해상도면 itag 갱신
        if stream.resolution and int(stream.resolution[:-1]) > int(best_resolution_so_far):
            preferred_video_itag = stream.itag
            best_resolution_so_far = stream.resolution[:-1]
        # 선호 해상도 찾으면 해당 비디오의 preferred_video_itag에 itag 설정
        if stream.resolution and stream.resolution[:-1] == preferred_resolution:
            preferred_video_itag = stream.itag
            print(f'Using preferred video itag = {preferred_video_itag}')
            break

# 가장 높은 bitrate itag 찾는 함수
# AUDIO example: itag='250' ---> abr='70kbps'  itag='251' ---> abr='160kbps'
def find_best_audio_bitrate(yt):
    last_stream = yt.fmt_streams[-1:] 
    global preferred_audio_itag

    if last_stream and last_stream[0].abr:
        preferred_audio_itag = last_stream[0].itag
        print(f'Using preferred audio itag = {preferred_audio_itag}')

# 비디오 병합 (ffmpeg 정보 콘솔 출력 안하기 위함)
def merge_audio_video(downloaded_video, downloaded_audio, output_file, vcodec='copy'):
    '''Merge audio and video into a single file using ffmpeg and suppress console output.'''
    try:
        # Build the ffmpeg command
        command = [
            'ffmpeg',
            '-i', downloaded_video,   # Input video
            '-i', downloaded_audio,   # Input audio
            '-c:v', vcodec,           # Video codec (copy or H.264)
            '-c:a', 'aac',            # Audio codec (AAC)
            '-y',                     # Automatically overwrite output file if it exists
            output_file               # Output file path
        ]

        # Run the command using subprocess and suppress output
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f'병합 완료: {output_file}')

    except subprocess.CalledProcessError as e:
        print(f'❌ 병합 중 오류 발생: {e}')
        print(f'stderr: {e.stderr}')
        print(f'stdout: {e.stdout}')
        
        
# 메인 다운로드 및 병합 로직
def download_video(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress, use_oauth=False)
        print(f'{YELLOW} ▶ Video title: {yt.title} {OFF}')
        
        # 이름에서 특수 기호 제거
        original_title = ''.join(filter(lambda x: x not in '?.!/;:', yt.title))
        yt.title = 'tmp'  

        # 'preferred_video_resolution' 까지 최고 화질 찾기
        find_best_resolution(yt, preferred_resolution)
        
        # 비디오 다운로드
        video = yt.streams.get_by_itag(preferred_video_itag)
        print(f'⏬ {best_resolution_so_far}p 화질로 다운로드 시작...')
        video.download(output_path=SAVE_PATH)
        downloaded_video = os.path.join(SAVE_PATH, f'{yt.title}.mp4')
        
        # 최종 파일명
        fname = f'{original_title}_{best_resolution_so_far}.mp4'
        output_file = os.path.join(SAVE_PATH, fname)    

        # 오디오 미포함 파일 : 1440p 이상은 AV1 코덱으로 오디오 다운로드 안되어서 오디오 별도로 다운받아서 합쳐야함.
        if not check_audio_stream(downloaded_video):
            # 최고 bitrate 찾기
            find_best_audio_bitrate(yt)
            audio_only_itag = yt.streams.get_audio_only().itag
            audio = yt.streams.get_by_itag(audio_only_itag)
            
            # 오디오 다운로드
            print(f'⏬ 오디오 파일 다운로드 시작...')
            audio.download(output_path=SAVE_PATH)
            downloaded_audio = os.path.join(SAVE_PATH, f'{yt.title}.m4a')
            check_audio_stream(downloaded_audio)
            
            # 비디오 + 오디오 병합하기
            vcodec = 'copy'  # 비디오 코덱 그대로 사용
            
            # # 디바이스가 AV1 코덱 지원한다면
            # if int(best_resolution_so_far) <= 1080:
            #     vcodec = 'avc1.640028'  # H.264 for 1080p 이하
            # else:
            #     vcodec = 'av01.0.12M.08'  # AV1 for 1440p 이상
            
            # ffmpeg로 병합 파일 생성 
            merge_audio_video(downloaded_video, downloaded_audio, output_file, vcodec)
            
            # 병합 후 임시 파일 삭제
            os.remove(downloaded_video)
            os.remove(downloaded_audio)
        
        # 1080p 이하 오디오가 이미 포함된 경우, 비디오 파일 이름만 변경
        else:
            os.rename(downloaded_video, output_file)

        print(f'{GREEN}✅ \'{fname}\' 다운로드 완료!{OFF}')

    except Exception as e:
        print(f'{RED}❌ Error occurred {OFF}')
        print(f'{RED}error : {str(e)}{OFF}')

if __name__ == '__main__':
    print('🎬 YouTube 영상 다운로더')
    # 사용자 설정 안했으면 현재 디렉토리로 초기화
    if SAVE_PATH == '/Users/username/Downloads':
        SAVE_PATH = '.'

    for url in video_list:
        print('===========================================================================')
        print(f'▶ URL: {url}')
        download_video(url)
