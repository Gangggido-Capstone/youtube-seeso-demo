from video_download import download
from video_detect import detect

import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

#이제 영상 전체 집중도 점수랑 분할 영상 집중도 구하고 저장 그리고 내림차순 정렬
def score_cluster(video_id, video_csv, sceneTime):
    # 프로젝트 루트 경로 설정
    root_path = get_root_path()

    # 날짜 시간 값
    date_time = video_csv.split('_')[1].split('.')[0]

    # CSV 파일 불러오기
    csv_path = os.path.join(root_path, "Data", "GazeData")
    gaze_csv = pd.read_csv(os.path.join(csv_path, video_csv))
    
    final_score = []
    n_clusters = []

    # 분할 영상 별 집중도 점수 및 클러스터 시각화 이미지 저장
    for index, scene in enumerate(sceneTime):
        start, end = scene
        print("start: " + str(start) + ", " + "end: " + str(end))

        filtered_data = gaze_csv[(gaze_csv['Time'] >= start) & (gaze_csv['Time'] <= end)]
        valid_data = filtered_data.dropna(subset=['X', 'Y'])

        x_values = valid_data['X'].astype(int).tolist()
        y_values = valid_data['Y'].astype(int).tolist()

        # DBSCAN 알고리즘 적용
        gaze_data = list(zip(x_values, y_values))

        if len(gaze_data) == 0:
            print(f"Scene {index+1}: No valid gaze data available.")
            final_score.append(0)
            n_clusters.append(0)
            continue  # 다음 씬으로 넘어감

        dbscan = DBSCAN(eps=30 , min_samples=5)
        labels = dbscan.fit_predict(gaze_data)

        #  ========================== 점수 구하는 구간 =========================

        # DBSCAN 클러스터 점수
        # labels 배열에서 -1 값은 클러스터에 속하지 않는 노이즈(즉, 집중되지 않은 점)를 의미
        # labels != -1 조건을 만족하는 점들은 클러스터에 속하는 점
        num_focus_points = sum(labels != -1)
        focus_score1 = num_focus_points / len(labels)
        # print(f"Focus Score: {focus_score1:.2f}")

        # Attention 값(0) 비율 점수
        attention_values = valid_data['Attention'].astype(int).tolist() 
        zero_data = attention_values.count(0)
        focus_score2 = zero_data / len(attention_values)
        # print(f"Zero Attention Score: {focus_score2:.2f}")

        # 클러스터 점수 * 0.7 + Attention 비율 점수 * 0.3
        res = ((focus_score1 * 0.7) + (focus_score2 * 0.3)) * 100
        final_score.append(res)

        print(f"Attention Score: {res:.2f}")

        #  ====================================================================

        # 클러스터 개수 출력
        cnt = len(set(labels)) - (1 if -1 in labels else 0)
        n_clusters.append(cnt)
        print(f"Number of clusters found: {cnt}")

        # 최대(가장 많은 시선이 포함된) 클러스터의 정보
        max_n = 0       # 클러스터에 속하는 시선의 수
        xx = 0          # 클러스터 바운딩박스의 x좌표
        yy = 0          # 클러스터 바운딩박스의 y좌표
        ww = 0          # 클러스터 바운딩박스의 너비
        hh = 0          # 클러스터 바운딩박스의 높이

        # 라벨 집합
        unique_labels = set(labels)

        # 최대 클러스터 구하기
        for label in unique_labels:
            # 클러스터에 속하지 않는 포인트
            if label == -1:
                continue

            cluster_points = []

            # label번 클러스터에 속한 점만 필터링
            for i in range(200):
                # if labels[i] == label:
                if i < len(labels) and labels[i] == label:
                    cluster_points.append(gaze_data[i])

            # 최대 클러스터 정보 업데이트
            n = len(cluster_points)
            if n > max_n:
                max_n = n

                # 바운딩 박스 계산
                xs = [point[0] for point in cluster_points]
                ys = [point[1] for point in cluster_points]
                xx = np.min(xs)
                yy = np.min(ys)
                ww = np.max(xs) - xx
                hh = np.max(ys) - yy

        print(xx, yy, ww, hh)

        fig, ax = plt.subplots()

        # 최대 클러스터의 바운딩박스 그리기
        rect = patches.Rectangle((xx, yy), ww, hh, linewidth=0.1, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

        # gaze_data를 Numpy 배열로 변환
        gaze_data = np.array(gaze_data)

        # 시선 포인트들 그리기
        ax.scatter(gaze_data[:, 0], gaze_data[:, 1], c=labels, cmap='rainbow')

        # 클러스터 이미지 저장
        cluster_dir = os.path.join(root_path, "Data", "video", video_id, "cluster", date_time)
        os.makedirs(cluster_dir, exist_ok=True)
        plt.title(f"{video_id} Scene {index + 1} cluster")
        plt.text(0.5, -0.1, f"Number of clusters found: {n_clusters[index]}", ha='center', va='top', transform=plt.gca().transAxes)
        plt.savefig(os.path.join(cluster_dir, f"Cluster_Scene-{index+1:03}.png"))

        # 실행 시 이미지 보기
        # plt.show()

    # 리스트에 저장해 반환
    atention_score_list = []
    # split_video 디렉토리 경로 설정
    split_video_directory = os.path.join(root_path, "Data", "video", video_id, "split_video")
    thumbnails_dir = os.path.join(root_path, "Data", "video", video_id, "thumbnails")
    # final_score를 기준으로 내림차순 정렬
    sorted_data = sorted(enumerate(zip(sceneTime, final_score, n_clusters)), key=lambda x: x[1][1], reverse=True)
    for i, (_, score, cluster) in sorted_data:
        if score == 0:
            continue
        atention_score_list.append((f"{split_video_directory}\\{video_id}-Scene-{i+1:03}.mp4", f"{thumbnails_dir}\\{video_id}_{i+1:03}.jpg", f"{cluster_dir}\\Cluster_Scene-{i+1:03}.png", score, cluster))

    return atention_score_list


if __name__ == "__main__":
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코

    # video_id = "fRaIcUhaXXQ"
    # video_csv = "fRaIcUhaXXQ_2024-10-20-16-50-56.csv"
    video_id = "fRaIcUhaXXQ"
    video_csv = "fRaIcUhaXXQ_2024-10-20-16-50-56.csv"

    # 영상 다운
    video_only, audio_only, video_filename = download(video_id)

    # 영상 분할
    sceneTime = detect(video_id, video_only, video_filename)

    # 영상 점수 및 클러스터 이미지 저장
    atention_score_list = score_cluster(video_id, video_csv, sceneTime)
    for a in atention_score_list:
        print(a)
    