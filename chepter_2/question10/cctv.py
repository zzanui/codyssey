# cctv.py
import os
import glob
import cv2

# -------- 설정 --------
IMAGE_DIR = os.path.join("chepter_2", "question10", "cctv")  # 검사할 폴더
EXTS = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")
WIN_NAME = "CCTV Person Finder"
ENTER_KEYS = {13, 10}
QUIT_KEYS = {27, ord('q'), ord('Q')}

# -------- 이미지 목록 가져오기 --------
def list_images(directory, exts):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"폴더가 없습니다: {directory}")
    paths = []
    for ext in exts:
        paths.extend(glob.glob(os.path.join(directory, ext)))
    if not paths:
        raise FileNotFoundError(f"이미지 파일을 찾지 못했습니다: {directory}")
    return sorted(paths)

# -------- HOG 보행자 검출기 초기화 --------
def init_hog():
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    return hog

# -------- 사람 감지 --------
def detect_people(hog, img):
    rects, _ = hog.detectMultiScale(
        img,
        winStride=(2, 2),
        padding=(8, 8),
        scale=1.05,
    )
    return rects

# -------- 사각형 표시 --------
def draw_detections(img, rects, info=""):
    out = img.copy()
    # for (x, y, w, h) in rects:
    #     cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if info:
        cv2.putText(out, info, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(out, info, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 1, cv2.LINE_AA)
    return out

# -------- 메인 --------
def main():
    paths = list_images(IMAGE_DIR, EXTS)
    hog = init_hog()
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)

    hits = 0
    for i, p in enumerate(paths, 1):
        img = cv2.imread(p)
        if img is None:
            print(f"[WARN] 이미지를 불러올 수 없습니다: {p}")
            continue

        rects = detect_people(hog, img)

        if len(rects) > 0:
            hits += 1
            shown = draw_detections(
                img, rects,
                f"{os.path.basename(p)} | people:{len(rects)} | ({i}/{len(paths)})"
            )
            cv2.imshow(WIN_NAME, shown)
            key = cv2.waitKeyEx(0)
            if key in QUIT_KEYS:
                print("[중단] 사용자 종료")
                cv2.destroyAllWindows()
                return

    cv2.destroyAllWindows()
    print(f"[완료] 검사 종료: 총 {len(paths)}장 중 {hits}장 감지됨")

if __name__ == "__main__":
    main()
