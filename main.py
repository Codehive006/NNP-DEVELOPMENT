import cv2
import mediapipe as mp
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pyautogui
import subprocess
import os
import threading

from gesture_recognizer import GestureRecognizer

cap = None
recognizer = GestureRecognizer()
current_gesture = "No Gesture"
prev_hand_pos = None
prev_time = time.time()
root = None
video_label = None
status_label = None
guidance_text_widget = None
is_running = False
powerpoint_path = None

def open_powerpoint():
    global powerpoint_path
    powerpoint_path = filedialog.askopenfilename(
        title="Select PowerPoint Presentation",
        filetypes=[("PowerPoint files", "*.pptx *.ppt")]
    )
    if powerpoint_path:
        messagebox.showinfo("PPT Selected", f"Selected: {os.path.basename(powerpoint_path)}")
        start_detection_button.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("No PPT Selected", "Please select a PowerPoint file to continue.")
        start_detection_button.config(state=tk.DISABLED)

def start_powerpoint_slideshow():
    global powerpoint_path
    if powerpoint_path and os.path.exists(powerpoint_path):
        if os.name == 'nt':
            powerpoint_executable_path = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE" # REPLACE THIS WITH YOUR ACTUAL PATH
            
            if not os.path.exists(powerpoint_executable_path):
                messagebox.showerror("Error", f"PowerPoint executable not found at: {powerpoint_executable_path}. Please check the path in main.py.")
                return

            try:
                subprocess.Popen([powerpoint_executable_path, powerpoint_path])
                time.sleep(3)
                pyautogui.press('f5')
                messagebox.showinfo("PowerPoint Started", "PowerPoint slideshow initiated. Press ESC to exit.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open PowerPoint: {e}")
        elif os.name == 'posix':
            subprocess.Popen(['xdg-open', powerpoint_path])
            messagebox.showinfo("PowerPoint Started", "PowerPoint opened. Please start slideshow manually (e.g., F5 or Fn+F5).")
        else:
            messagebox.showwarning("OS Not Supported", "Automatic slideshow start not supported for your OS.")
    else:
        messagebox.showwarning("Error", "No valid PowerPoint path selected.")

def send_key_event(gesture):
    global current_gesture
    if current_gesture != gesture:
        print(f"Detected: {gesture}")
        current_gesture = gesture
        if gesture == "Swipe Right":
            pyautogui.press('right')
            status_label.config(text="Status: Next Slide")
            print("Next Slide")
        elif gesture == "Swipe Left":
            pyautogui.press('left')
            status_label.config(text="Status: Previous Slide")
            print("Previous Slide")
        elif gesture == "Thumbs Up":
            status_label.config(text="Status: Thumbs Up (No Action)")
            print("Thumbs Up - No Action assigned")
        elif gesture == "Open Palm":
            status_label.config(text="Status: Open Palm (No Action)")
            print("Open Palm - No Action assigned")
        elif gesture == "Index Point":
            status_label.config(text="Status: Index Point (No Action)")
            print("Index Point - No Action assigned")

def update_frame():
    global cap, recognizer, prev_hand_pos, prev_time, is_running, current_gesture

    if is_running and cap and cap.isOpened():
        success, img = cap.read()
        if success:
            img = cv2.flip(img, 1)
            img = recognizer.find_hands(img)
            lmList = recognizer.find_position(img, draw=False)

            current_time = time.time()
            gesture, prev_hand_pos, prev_time = recognizer.detect_gesture(img, prev_hand_pos, current_time, prev_time)

            cv2.putText(img, f"Gesture: {gesture}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            if gesture != "No Gesture":
                send_key_event(gesture)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

        video_label.after(10, update_frame)

    elif not is_running and cap and cap.isOpened():
        cap.release()
        video_label.config(image='')
        messagebox.showinfo("Stopped", "Gesture detection stopped.")
        status_label.config(text="Status: Idle")

def start_detection():
    global cap, is_running, prev_hand_pos, prev_time
    if not powerpoint_path:
        messagebox.showwarning("No PPT Selected", "Please select a PowerPoint file first.")
        return

    is_running = True
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Could not open webcam. Please check if it's in use or connected.")
        is_running = False
        return

    prev_hand_pos = None
    prev_time = time.time()
    status_label.config(text="Status: Detecting Gestures...")
    start_powerpoint_slideshow()
    threading.Thread(target=update_frame, daemon=True).start()

def stop_detection():
    global is_running
    is_running = False
    status_label.config(text="Status: Stopping...")

def setup_gui():
    global root, video_label, status_label, guidance_text_widget, start_detection_button

    root = tk.Tk()
    root.title("AI Gesture-Based Presentation Tool")
    root.geometry("1000x700")

    top_frame = tk.Frame(root, padx=10, pady=10)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    btn_open_ppt = tk.Button(top_frame, text="1. Select PowerPoint", command=open_powerpoint, font=("Arial", 12))
    btn_open_ppt.pack(side=tk.LEFT, padx=5)

    start_detection_button = tk.Button(top_frame, text="2. Start Gesture Control", command=start_detection, font=("Arial", 12), state=tk.DISABLED)
    start_detection_button.pack(side=tk.LEFT, padx=5)

    btn_stop_detection = tk.Button(top_frame, text="Stop Detection", command=stop_detection, font=("Arial", 12), bg="red", fg="white")
    btn_stop_detection.pack(side=tk.LEFT, padx=5)

    status_label = tk.Label(top_frame, text="Status: Idle", font=("Arial", 12), fg="blue")
    status_label.pack(side=tk.RIGHT, padx=5)

    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    video_frame = tk.LabelFrame(main_frame, text="Webcam Feed", font=("Arial", 12, "bold"), padx=5, pady=5)
    video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    video_label = tk.Label(video_frame)
    video_label.pack(fill=tk.BOTH, expand=True)

    guidance_frame = tk.LabelFrame(main_frame, text="Guidance", font=("Arial", 12, "bold"), padx=5, pady=5)
    guidance_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    guidance_text_widget = scrolledtext.ScrolledText(guidance_frame, width=40, height=20, font=("Arial", 11), wrap=tk.WORD, state=tk.DISABLED)
    guidance_text_widget.pack(fill=tk.BOTH, expand=True)

    guidance_info = """
    Welcome to the AI Gesture-Based Presentation Tool!

    Instructions:
    1. Click "Select PowerPoint" to choose your presentation file.
    2. Click "Start Gesture Control" to begin webcam detection and open your PPT.
    3. Use the gestures below to control your slides.

    Gestures:
    - Swipe Right: Move your **index finger** quickly from left to right to go to the **Next Slide**.
    - Swipe Left: Move your **index finger** quickly from right to left to go to the **Previous Slide**.
    - Thumbs Up: (Currently no action assigned) Can be customized for 'Start/Stop slideshow'.
    - Open Palm: (Currently no action assigned) Can be customized for 'Exit slideshow'.
    - Index Point: (Currently no action assigned) Can be customized for 'Mouse Click'.

    Tips:
    - Ensure good lighting for best gesture recognition.
    - Keep your hand relatively steady when not making a gesture.
    - Your hand should be clearly visible to the webcam.
    """
    guidance_text_widget.config(state=tk.NORMAL)
    guidance_text_widget.insert(tk.END, guidance_info)
    guidance_text_widget.config(state=tk.DISABLED)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def on_closing():
    global is_running, cap
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        is_running = False
        if cap and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        root.destroy()

if __name__ == "__main__":
    setup_gui()