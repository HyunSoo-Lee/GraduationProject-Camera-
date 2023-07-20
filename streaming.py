import cv2
import urllib.request

# MJPEG 스트림 URL
stream_url = "http://211.247.109.217:8090/?action=stream"

# MJPEG 스트림 열기
stream = urllib.request.urlopen(stream_url)

# 카메라 캡처 초기화
capture = cv2.VideoCapture()

# OpenCV 버전 확인
major_ver, _, _ = cv2.__version__.split('.')
if major_ver == '3':
    # MJPEG 스트림을 파일 경로로 인식하도록 변경
    capture.open(stream_url, cv2.CAP_FFMPEG)  # OpenCV 3.x
else:
    capture.open(stream_url)  # OpenCV 2.x

# 영상 처리를 위한 반복문
while True:
    # 프레임 읽기
    ret, frame = capture.read()

    if not ret:
        break

    # 여기서 프레임에 대한 영상 처리 작업을 수행합니다
    # ...

    # 결과를 표시합니다
    cv2.imshow("Live Stream", frame)

    # 'q' 키를 누르면 종료합니다
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스를 해제합니다
capture.release()
cv2.destroyAllWindows()


