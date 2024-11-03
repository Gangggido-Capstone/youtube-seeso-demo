from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images, write_scene_list_html
import cv2
video_path = 'C:\\youtube-seeso-demo\\frontend\\public\\data\\video\\iJsWRpSetq0\\iJsWRpSetq0.mp4'
stats_path = 'result.csv'

video_manager = VideoManager([video_path])
stats_manager = StatsManager()
scene_manager = SceneManager(stats_manager)
fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS) 
scene_manager.add_detector(ContentDetector(threshold=25, min_scene_len = fps * 4))
video_manager.set_downscale_factor()

video_manager.start()
scene_manager.detect_scenes(frame_source=video_manager)

# result
with open(stats_path, 'w') as f:
    stats_manager.save_to_csv(f, video_manager.get_base_timecode())

scene_list = scene_manager.get_scene_list()
print(f'{len(scene_list)} scenes detected!')

save_images(
    scene_list,
    video_manager,
    num_images=1,
    image_name_template='$SCENE_NUMBER',
    output_dir='scenes')

write_scene_list_html('result.html', scene_list)

for scene in scene_list:
    start, end = scene

    # your code
    print(f'{start.get_seconds()} - {end.get_seconds()}')