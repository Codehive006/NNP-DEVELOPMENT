import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time

class GesturePresentationUI:
    def __init__(self, root, gesture_detector, presentation_controller, drawing_controller):
        self.root = root
        self.gesture_detector = gesture_detector
        self.presentation_controller = presentation_controller
        self.drawing_controller = drawing_controller
        
        self.is_camera_active = False
        self.cap = None
        self.current_gesture = "no_hand"
        self.landmarks_list = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("AI Gesture-Based Presentation Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎯 Gesture-Based Presentation Controller",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#34495e'
        )
        title_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame - Camera feed
        left_frame = tk.Frame(main_frame, bg='#34495e', width=700)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Camera label
        self.camera_label = tk.Label(
            left_frame,
            text="Camera Feed - Click 'Start Camera' to begin",
            bg='black',
            fg='white',
            font=('Arial', 12),
            relief='sunken',
            bd=2
        )
        self.camera_label.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right frame - Controls
        right_frame = tk.Frame(main_frame, bg='#34495e', width=400)
        right_frame.pack(side='right', fill='y', padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # Control buttons
        control_frame = tk.Frame(right_frame, bg='#34495e')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_btn = tk.Button(
            control_frame,
            text="📷 Start Camera",
            command=self.toggle_camera,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=18,
            height=2
        )
        self.start_btn.pack(pady=5)
        
        # File open button
        self.file_btn = tk.Button(
            control_frame,
            text="📂 Open Presentation File",
            command=self.open_presentation_file,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            width=18,
            height=2
        )
        self.file_btn.pack(pady=5)
        
        # Drawing control button
        self.draw_btn = tk.Button(
            control_frame,
            text="✏️ Toggle Drawing Mode",
            command=self.toggle_drawing_mode,
            font=('Arial', 12, 'bold'),
            bg='#9b59b6',
            fg='white',
            width=18,
            height=2
        )
        self.draw_btn.pack(pady=5)
        
        # Clear drawing button
        self.clear_btn = tk.Button(
            control_frame,
            text="🧹 Clear Drawing",
            command=self.clear_drawing,
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            width=18,
            height=2
        )
        self.clear_btn.pack(pady=5)
        
        # Gesture info frame
        gesture_frame = tk.Frame(right_frame, bg='#34495e')
        gesture_frame.pack(fill='x', padx=10, pady=20)
        
        gesture_title = tk.Label(
            gesture_frame,
            text="🎭 Current Gesture",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#34495e'
        )
        gesture_title.pack()
        
        self.gesture_label = tk.Label(
            gesture_frame,
            text="No Hand",
            font=('Arial', 20, 'bold'),
            fg='#f39c12',
            bg='#34495e',
            height=2
        )
        self.gesture_label.pack(pady=10, fill='x')
        
        # Status indicators
        status_frame = tk.Frame(right_frame, bg='#34495e')
        status_frame.pack(fill='x', padx=10, pady=10)
        
        # Drawing mode indicator
        self.draw_status_label = tk.Label(
            status_frame,
            text="Drawing Mode: OFF",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.draw_status_label.pack(anchor='w')
        
        # Camera status indicator
        self.cam_status_label = tk.Label(
            status_frame,
            text="Camera: OFF",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.cam_status_label.pack(anchor='w')
        
        # Gesture guide
        guide_frame = tk.Frame(right_frame, bg='#34495e')
        guide_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        guide_title = tk.Label(
            guide_frame,
            text="🎯 Gesture Guide",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#34495e'
        )
        guide_title.pack()
        
        guide_text = """
👉 Pointing: Next Slide
✌️ Peace Sign: Previous Slide
👍 Thumbs Up: Start Presentation
🤚 Open Palm: Stop Presentation
✊ Fist: Black Screen
🤟 Three Fingers: Toggle Drawing

🎨 Drawing Mode:
• Show 3 fingers to activate
• Use index finger to draw
• Show 3 fingers again to exit
        """
        
        guide_label = tk.Label(
            guide_frame,
            text=guide_text,
            font=('Arial', 12),
            fg='white',
            bg='#34495e',
            justify='left'
        )
        guide_label.pack(pady=10, fill='both', expand=True)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(fill='x', side='bottom', padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to start gesture control",
            font=('Arial', 10),
            fg='white',
            bg='#34495e'
        )
        self.status_label.pack(side='left')
        
    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.is_camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera feed"""
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                return
            
            self.is_camera_active = True
            self.start_btn.config(text="📷 Stop Camera", bg='#e74c3c')
            self.file_btn.config(state='disabled')
            self.cam_status_label.config(text="Camera: ON", fg='#27ae60')
            self.status_label.config(text="Camera active - Gesture control enabled")
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.update_camera)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        """Stop camera feed"""
        self.is_camera_active = False
        if self.cap:
            self.cap.release()
        self.start_btn.config(text="📷 Start Camera", bg='#27ae60')
        self.file_btn.config(state='normal')
        self.cam_status_label.config(text="Camera: OFF", fg='#e74c3c')
        self.status_label.config(text="Camera stopped")
        self.camera_label.config(text="Camera Feed - Click 'Start Camera' to begin")
    
    def update_camera(self):
        """Update camera feed in separate thread"""
        while self.is_camera_active:
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame for gesture detection
                processed_frame, gesture, landmarks = self.gesture_detector.detect_gesture(frame)
                self.current_gesture = gesture
                self.landmarks_list = landmarks
                
                # Execute presentation action if gesture is stable
                if self.gesture_detector.is_gesture_stable(gesture):
                    self.presentation_controller.execute_action(gesture, landmarks)
                
                # Handle drawing if in drawing mode
                if (self.presentation_controller.is_drawing_mode and 
                    gesture == "pointing" and landmarks):
                    self.drawing_controller.start_drawing()
                    self.drawing_controller.update_drawing_position(landmarks)
                else:
                    self.drawing_controller.stop_drawing()
                
                # Convert frame for display
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((680, 500), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update UI in main thread
                self.root.after(0, self.update_camera_display, imgtk, gesture)
            
            time.sleep(0.03)  # ~30 FPS
    
    def update_camera_display(self, imgtk, gesture):
        """Update camera display in main thread"""
        self.camera_label.configure(image=imgtk)
        self.camera_label.image = imgtk
        
        # Update gesture label with color coding
        gesture_text = gesture.replace('_', ' ').title()
        self.gesture_label.config(text=gesture_text)
        
        # Update drawing mode status
        if self.presentation_controller.is_drawing_mode:
            self.draw_status_label.config(text="Drawing Mode: ON", fg='#27ae60')
        else:
            self.draw_status_label.config(text="Drawing Mode: OFF", fg='#e74c3c')
    
    def open_presentation_file(self):
        """Open file dialog to select presentation file"""
        file_path = filedialog.askopenfilename(
            title="Select Presentation File",
            filetypes=[
                ("PowerPoint Files", "*.pptx *.ppt"),
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.status_label.config(text=f"Opening: {file_path}")
            success = self.presentation_controller.open_file(file_path)
            if success:
                messagebox.showinfo("Success", "Presentation file opened successfully!")
                self.status_label.config(text="Presentation file opened - Ready for gesture control")
            else:
                messagebox.showerror("Error", "Failed to open presentation file")
                self.status_label.config(text="Error opening file")
    
    def toggle_drawing_mode(self):
        """Toggle drawing mode manually"""
        self.drawing_controller.toggle_drawing_mode(self.presentation_controller)
        self.presentation_controller.is_drawing_mode = not self.presentation_controller.is_drawing_mode
        
    def clear_drawing(self):
        """Clear drawing manually"""
        self.drawing_controller.clear_drawing()