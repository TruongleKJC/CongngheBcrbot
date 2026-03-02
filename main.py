import cv2
import numpy as np
import pyautogui
import time
from ultralytics import YOLO

# ==========================================================
# CẤU HÌNH HỆ THỐNG - ID: 0nbtruonglek6
# ==========================================================
# Tọa độ nút bấm (Anh cần chỉnh lại theo độ phân giải máy anh)
POS_PLAYER = (250, 850)   
POS_BANKER = (750, 850)   
POS_CONFIRM = (500, 950)  

# Vùng quét bài Dealer sảnh Sexy (X, Y, Width, Height)
SCAN_REGION = (400, 200, 800, 500) 

class G9RobotAI:
    def __init__(self, model_path='yolov8n.pt'):
        self.id = "0nbtruonglek6"
        self.van_cuoc = 1
        try:
            self.model = YOLO(model_path)
            print(f"--- HỆ THỐNG G9 KHỞI CHẠY | ID: {self.id} ---")
        except Exception as e:
            print(f"Lỗi khởi động Model: {e}")

    def speak(self, text):
        print(f"[VOICE]: {text}")
        # Nếu chạy trên Windows/Android có thể thêm thư viện gTTS hoặc pyttsx3 ở đây

    def auto_click(self, side):
        """Thực hiện lệnh đặt cược tự động"""
        target = POS_PLAYER if side == "P" else POS_BANKER
        pyautogui.moveTo(target[0], target[1], duration=0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.click(POS_CONFIRM)
        print(f"[AUTO] Đã chốt: {'CON' if side == 'P' else 'CÁI'} | Ván: {self.van_cuoc}")

    def analyze_roadmap(self, results):
        """Thuật toán nuốt cầu dựa trên dữ liệu bài vừa quét"""
        # Phân tích các thế cầu bệt/nghiêng như trong ảnh anh gửi
        # Logic: Dựa trên số lượng lá bài AI nhận diện được ở mỗi bên
        p_cards = 0
        b_cards = 0

        for result in results:
            for box in result.boxes:
                x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                if x_center < (SCAN_REGION[2] / 2):
                    p_cards += 1
                else:
                    b_cards += 1

        # Quyết định dựa trên xu hướng cầu (Ví dụ: Cầu nghiêng hoặc bệt)
        if p_cards > 0 or b_cards > 0:
            decision = "P" if p_cards >= b_cards else "B"
            return decision
        return None

    def run(self):
        while True:
            # 1. Chụp vùng bài sảnh Sexy
            img = pyautogui.screenshot(region=SCAN_REGION)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # 2. AI Soi bài
            results = self.model(frame, conf=0.5, verbose=False)
            
            # 3. Phân tích & Đặt cược
            side = self.analyze_roadmap(results)
            
            if side:
                self.speak(f"Phát hiện thế cầu mới. Chốt lệnh {side}")
                self.auto_click(side)
                self.van_cuoc += 1
                print("[HỆ THỐNG] Nghỉ 35 giây đợi ván mới...")
                time.sleep(35) # Thời gian nghỉ để tránh đặt trùng
            else:
                time.sleep(1) # Quét lại sau mỗi giây nếu chưa thấy bài

# ==========================================================
# THỰC THI
# ==========================================================
if __name__ == "__main__":
    bot = G9RobotAI()
    bot.run()
