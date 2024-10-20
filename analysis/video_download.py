import os
import yt_dlp
import subprocess

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

def download(video_id):
    
    root_path = get_root_path()  # 프로젝트 루트 경로 가져오기

    video_url = f"https://youtu.be/{video_id}"  # 유튜브 영상 URL
    video_only = os.path.join(root_path, "Data", "video", video_id, "video.mp4")  # 비디오 파일 경로
    audio_only = os.path.join(root_path, "Data", "video", video_id, "audio.m4a")  # 오디오 파일 경로
    video_filename = os.path.join(root_path, "Data", "video", video_id, f"{video_id}.mp4")  # 최종 저장할 비디오 파일 경로

    try:
        # 파일이 이미 존재하는지 확인
        if not os.path.exists(video_filename):
            os.makedirs(os.path.join(root_path, "Data", "video", video_id), exist_ok=True)

            # yt-dlp 옵션 설정: 비디오와 오디오를 별도로 다운로드
            ydl_opts_video = {
                'format': 'bestvideo',
                'outtmpl': video_only,
            }

            ydl_opts_audio = {
                'format': 'bestaudio',
                'outtmpl': audio_only,
            }

            # 비디오 다운로드
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                ydl.download([video_url])

            # 오디오 다운로드
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download([video_url])

            try:
                # ffmpeg를 사용해 비디오와 오디오 병합
                ffmpeg_path = "C:/ffmpeg/bin/ffmpeg" 
                merge_command = [
                    ffmpeg_path,
                    '-i', video_only,  # 좌표가 그려진 비디오 파일
                    '-i', audio_only,  # 입력 오디오 파일
                    '-c:v', 'libx264',  # 비디오를 H.264로 재인코딩
                    '-preset', 'fast',  # 빠른 인코딩 옵션
                    '-c:a', 'aac',  # 오디오를 AAC 형식으로 변환
                    '-b:a', '192k',  # 오디오 비트레이트 설정
                    '-r', '30',  # 비디오 프레임 속도 강제 설정 (30fps, 고정 프레임 속도)
                    '-vsync', 'cfr',  # 고정 프레임 속도 동기화
                    '-map', '0:v:0',  # 비디오 스트림을 첫 번째 입력에서 가져오기
                    '-map', '1:a:0',  # 오디오 스트림을 두 번째 입력에서 가져오기
                    '-shortest',  # 가장 짧은 스트림 기준으로 맞추기
                    video_filename  # 최종 출력 파일 경로
                ]
                print("Execute Merge Commands")
                # 병합 명령어 실행
                subprocess.run(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
                print(f"{video_filename} 다운 완료")
            except subprocess.TimeoutExpired:
                print("FFmpeg 실행이 타임아웃되었습니다.")

        else:
            print(f"{video_filename} 파일이 이미 존재합니다.")

        return video_only, audio_only, video_filename
    
    except Exception as e:
        print(f"Detect 함수에서 오류 발생: {str(e)}")
        raise e