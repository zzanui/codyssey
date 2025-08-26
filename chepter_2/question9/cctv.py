#보너스 이미지를 처리하는 기능을 다른 곳에서도 활용할 수 있게 기능을 클래스로 작성한다. 클래스의 이름은 MasImageHelper 로 정한다.
import zipfile
import os
import cv2
import glob

class MasImageHelper():
    LEFT_KEYS  = {81}   # ←
    RIGHT_KEYS = {83}   # → 
    QUIT_KEYS  = {27}   # ESC
    EXTS = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")

    def __init__(self, window_name: str = "CCTV Viewer", max_w: int = 1600, max_h: int = 1000):
        self.window_name = window_name
        self.max_w = max_w
        self.max_h = max_h

    #1. CCTV.zip으로 제공되는 파일의 압축을 풀어서 CCTV 폴더를 만드는 코드를 작성한다.
     #압출풀기
    def unpack_zip(self, file_name, output_directory):
        zip_file = zipfile.ZipFile(file_name)
        zip_file.extractall(path=output_directory)

        #폴더가 없으면 생성
        os.makedirs(output_directory, exist_ok=True)

        with zipfile.ZipFile(file_name, 'r') as zf:
            zf.extractall(path=output_directory)
        print(f"압축 해제 완료 → '{output_directory}'")


    #이미지 리스트
    def find_images(self, directory):
        image_paths = []
        for ext in self.EXTS:
            image_paths.extend(glob.glob(os.path.join(directory, ext)))
        image_paths = sorted(image_paths)

        if not image_paths:
            raise FileNotFoundError(f"이미지 파일을 찾지 못했습니다. {directory}를 확인하세요.")
        return image_paths

    #이미지가 잘리거나 너무 크게 나오는 현상 방지
    def _fit_to_box(self, img):
        #이미지를 (max_w, max_h) 박스에 맞춰 비율 유지 축소
        h, w = img.shape[:2]
        scale = min(self.max_w / w, self.max_h / h, 1.0)
        if scale < 1.0:
            new_w, new_h = int(w * scale), int(h * scale)
            return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return img

    #2. CCTV 폴더의 사진중에 한 장을 우선 읽어들여서 화면에 출력한다.
    def run_viewer(self, image_paths) -> None:
        """이미지 리스트를 뷰어로 보여주며 방향키로 탐색한다."""
        if not image_paths:
            raise ValueError("[오류] 표시할 이미지가 없습니다.")

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        idx = 0

        while True:
            path = image_paths[idx]
            img = cv2.imread(path)
            if img is None:
                print(f"[경고] 로드 실패: {path} → 다음 파일로 넘어갑니다.")
                idx = (idx + 1) % len(image_paths)
                continue

            disp = self._fit_to_box(img).copy()

            cv2.imshow(self.window_name, disp)
            #3. 오른쪽 방향 키를 누르면 다음 사진 왼쪽 방향 키를 누르면 이전 사진을 보여 준다.
            key = cv2.waitKeyEx(0)  # 특수키를 안정적으로 받기 위해 waitKeyEx 사용

            if key in self.QUIT_KEYS:
                break
            elif key in self.RIGHT_KEYS:
                idx = (idx + 1) % len(image_paths)
            elif key in self.LEFT_KEYS:
                idx = (idx - 1) % len(image_paths)
            else:
                pass

        cv2.destroyAllWindows()


if __name__ == "__main__":
    zip_filename = "cctv/cctv.zip"   
    output_dir = "cctv/CCTV"

    helper = MasImageHelper()

    #1. 압축 해제 폴더 없으면 생성
    helper.unpack_zip(zip_filename, output_dir)
    #2 이미지 목록 불러오기
    images = helper.find_images(output_dir)
    print(f"이미지 {len(images)}장을 찾음.")

    #이미지 출력, 방향키로 이전/다음 이동
    helper.run_viewer(images)

#4. 위의 내용들이 잘 동작하면 cctv.py 파일로 저장한다.
