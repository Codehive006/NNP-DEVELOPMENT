# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import cv2
# from PIL import Image, ImageTk
# import threading
# import time
# import sys
# import os

# # Import our custom modules
# from gesture_controller import GestureController
# from presentation_manager import PresentationManager
# from drawing_manager import DrawingManager

# class GesturePresentationApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("AI Gesture-Based Presentation Tool v2.0")
#         self.root.geometry("1300x800")
#         self.root.configure(bg='#2c3e50')
        
#         # Initialize controllers
#         self.gesture_controller = GestureController()
#         self.presentation_manager = PresentationManager()
#         self.drawing_manager = DrawingManager()
        
#         # Webcam variables
#         self.cap = None
#         self.is_camera_active = False
#         self.current_frame = None
        
#         # Gesture tracking
#         self.current_gesture = "none"
#         self.gesture_history = []
        
#         # Setup GUI
#         self.setup_gui()
        
#         # Start camera in a separate thread
#         self.start_camera()
    
#     def setup_gui(self):
#         """Setup the graphical user interface"""
        
#         # Main frame
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Configure grid weights
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         main_frame.columnconfigure(1, weight=1)
#         main_frame.rowconfigure(1, weight=1)
        
#         # Title
#         title_label = ttk.Label(
#             main_frame, 
#             text="AI Gesture-Based Presentation Tool v2.0", 
#             font=('Arial', 20, 'bold'),
#             foreground='#3498db'
#         )
#         title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
#         # Left panel - Controls
#         control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
#         control_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
#         # Camera feed frame
#         camera_frame = ttk.LabelFrame(main_frame, text="Camera Feed & Gesture Recognition", padding="10")
#         camera_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
#         camera_frame.columnconfigure(0, weight=1)
#         camera_frame.rowconfigure(0, weight=1)
        
#         # Control buttons
#         self.camera_btn = ttk.Button(
#             control_frame, 
#             text="Start Camera", 
#             command=self.toggle_camera,
#             width=20
#         )
#         self.camera_btn.grid(row=0, column=0, pady=5, sticky=tk.EW)
        
#         # File open button
#         self.file_btn = ttk.Button(
#             control_frame,
#             text="Open Presentation File",
#             command=self.open_presentation_file,
#             width=20
#         )
#         self.file_btn.grid(row=1, column=0, pady=5, sticky=tk.EW)
        
#         # Start presentation button
#         self.start_pres_btn = ttk.Button(
#             control_frame,
#             text="Start Presentation",
#             command=self.start_presentation,
#             width=20
#         )
#         self.start_pres_btn.grid(row=2, column=0, pady=5, sticky=tk.EW)
        
#         # Stop presentation button
#         self.stop_pres_btn = ttk.Button(
#             control_frame,
#             text="Stop Presentation",
#             command=self.stop_presentation,
#             width=20
#         )
#         self.stop_pres_btn.grid(row=3, column=0, pady=5, sticky=tk.EW)
        
#         # Drawing controls
#         drawing_frame = ttk.LabelFrame(control_frame, text="Drawing Controls", padding="10")
#         drawing_frame.grid(row=4, column=0, pady=(20, 0), sticky=tk.EW)
        
#         self.drawing_btn = ttk.Button(
#             drawing_frame,
#             text="Start Drawing",
#             command=self.toggle_drawing,
#             width=18
#         )
#         self.drawing_btn.grid(row=0, column=0, pady=2)
        
#         self.clear_draw_btn = ttk.Button(
#             drawing_frame,
#             text="Clear Drawing",
#             command=self.clear_drawing,
#             width=18
#         )
#         self.clear_draw_btn.grid(row=1, column=0, pady=2)
        
#         # Gesture guide
#         guide_frame = ttk.LabelFrame(control_frame, text="Gesture Guide", padding="10")
#         guide_frame.grid(row=5, column=0, pady=(20, 0), sticky=tk.EW)
        
#         guide_text = """
# Swipe Left: Next Slide
# Swipe Right: Previous Slide
# Swipe Up: First Slide
# Swipe Down: Last Slide
# Pinch: Start Presentation
# Open Palm: Stop Presentation
# Victory ✌️: Toggle Drawing
# Fist 👊: Clear Drawing
# Thumbs Up: Exit App
#         """
#         guide_label = ttk.Label(guide_frame, text=guide_text, justify=tk.LEFT, font=('Arial', 9))
#         guide_label.grid(row=0, column=0, sticky=tk.W)
        
#         # Status frame
#         status_frame = ttk.LabelFrame(control_frame, text="Status", padding="10")
#         status_frame.grid(row=6, column=0, pady=(20, 0), sticky=tk.EW)
        
#         self.camera_status = ttk.Label(status_frame, text="Camera: Inactive", foreground='red')
#         self.camera_status.grid(row=0, column=0, sticky=tk.W)
        
#         self.pres_status = ttk.Label(status_frame, text="Presentation: Not Started", foreground='red')
#         self.pres_status.grid(row=1, column=0, sticky=tk.W)
        
#         self.drawing_status = ttk.Label(status_frame, text="Drawing: Off", foreground='red')
#         self.drawing_status.grid(row=2, column=0, sticky=tk.W)
        
#         self.gesture_status = ttk.Label(status_frame, text="Last Gesture: None", foreground='blue')
#         self.gesture_status.grid(row=3, column=0, sticky=tk.W)
        
#         # Camera display
#         self.camera_label = ttk.Label(camera_frame, background='black')
#         self.camera_label.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
#         # Gesture history
#         history_frame = ttk.LabelFrame(camera_frame, text="Gesture History", padding="10")
#         history_frame.grid(row=1, column=0, pady=(10, 0), sticky=tk.EW)
        
#         self.history_text = tk.Text(history_frame, height=6, width=60)
#         self.history_text.grid(row=0, column=0, sticky=tk.EW)
#         scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_text.yview)
#         scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
#         self.history_text.configure(yscrollcommand=scrollbar.set)
    
#     def toggle_camera(self):
#         """Toggle camera on/off"""
#         if self.is_camera_active:
#             self.stop_camera()
#             self.camera_btn.config(text="Start Camera")
#             self.camera_status.config(text="Camera: Inactive", foreground='red')
#         else:
#             self.start_camera()
#             self.camera_btn.config(text="Stop Camera")
#             self.camera_status.config(text="Camera: Active", foreground='green')
    
#     def start_camera(self):
#         """Start camera capture"""
#         if self.cap is None:
#             self.cap = cv2.VideoCapture(0)
#             if not self.cap.isOpened():
#                 messagebox.showerror("Error", "Could not open camera")
#                 return
        
#         self.is_camera_active = True
#         self.update_camera()
    
#     def stop_camera(self):
#         """Stop camera capture"""
#         self.is_camera_active = False
#         if self.cap is not None:
#             self.cap.release()
#             self.cap = None
    
#     def update_camera(self):
#         """Update camera feed in GUI"""
#         if self.is_camera_active and self.cap is not None:
#             ret, frame = self.cap.read()
#             if ret:
#                 # Detect gestures
#                 gesture, annotated_frame, hand_landmarks = self.gesture_controller.detect_gestures(frame)
                
#                 # Execute presentation action if gesture detected
#                 if gesture != "none" and gesture != self.current_gesture:
#                     self.current_gesture = gesture
#                     success = self.presentation_manager.execute_gesture(gesture, self.drawing_manager)
                    
#                     if success:
#                         # Update GUI
#                         self.gesture_status.config(text=f"Last Gesture: {gesture}", foreground='green')
                        
#                         # Add to history
#                         timestamp = time.strftime("%H:%M:%S")
#                         self.history_text.insert(tk.END, f"[{timestamp}] {gesture}\n")
#                         self.history_text.see(tk.END)
                
#                 # Handle drawing if enabled
#                 if self.drawing_manager.is_drawing and hand_landmarks:
#                     finger_pos = self.gesture_controller.get_index_finger_position(hand_landmarks, frame.shape)
#                     if finger_pos:
#                         self.drawing_manager.draw_at_position(finger_pos)
                
#                 # Update drawing status
#                 if self.drawing_manager.is_drawing:
#                     self.drawing_status.config(text="Drawing: ON", foreground='green')
#                     self.drawing_btn.config(text="Stop Drawing")
#                 else:
#                     self.drawing_status.config(text="Drawing: OFF", foreground='red')
#                     self.drawing_btn.config(text="Start Drawing")
                
#                 # Convert frame for display
#                 rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
#                 img = Image.fromarray(rgb_frame)
#                 img = img.resize((640, 480), Image.Resampling.LANCZOS)
#                 imgtk = ImageTk.PhotoImage(image=img)
                
#                 self.camera_label.imgtk = imgtk
#                 self.camera_label.configure(image=imgtk)
            
#             # Schedule next update
#             self.root.after(10, self.update_camera)
    
#     def open_presentation_file(self):
#         """Open file dialog to select presentation file"""
#         file_types = [
#             ("Presentation Files", "*.pptx *.ppt *.pdf"),
#             ("PowerPoint Files", "*.pptx *.ppt"),
#             ("PDF Files", "*.pdf"),
#             ("All Files", "*.*")
#         ]
        
#         file_path = filedialog.askopenfilename(
#             title="Select Presentation File",
#             filetypes=file_types
#         )
        
#         if file_path:
#             success = self.presentation_manager.open_presentation_file(file_path)
#             if success:
#                 messagebox.showinfo("Success", f"Opened: {os.path.basename(file_path)}")
#                 self.pres_status.config(text="Presentation: Ready", foreground='orange')
#             else:
#                 messagebox.showerror("Error", "Could not open presentation file")
    
#     def start_presentation(self):
#         """Start the presentation"""
#         self.presentation_manager.start_presentation()
#         self.pres_status.config(text="Presentation: Active", foreground='green')
    
#     def stop_presentation(self):
#         """Stop the presentation"""
#         self.presentation_manager.stop_presentation()
#         self.pres_status.config(text="Presentation: Stopped", foreground='red')
    
#     def toggle_drawing(self):
#         """Toggle drawing mode"""
#         if self.drawing_manager.is_drawing:
#             self.drawing_manager.stop_drawing()
#             self.drawing_btn.config(text="Start Drawing")
#             self.drawing_status.config(text="Drawing: OFF", foreground='red')
#         else:
#             self.drawing_manager.start_drawing()
#             self.drawing_btn.config(text="Stop Drawing")
#             self.drawing_status.config(text="Drawing: ON", foreground='green')
    
#     def clear_drawing(self):
#         """Clear drawing"""
#         self.drawing_manager.clear_drawing()
    
#     def on_closing(self):
#         """Handle application closing"""
#         self.stop_camera()
#         self.root.destroy()

# def main():
#     root = tk.Tk()
#     app = GesturePresentationApp(root)
#     root.protocol("WM_DELETE_WINDOW", app.on_closing)
#     root.mainloop()

# if __name__ == "__main__":
#     main()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import time
import os

from gesture_controller import GestureController
from presentation_manager import PresentationManager
from drawing_manager import DrawingManager

class ScrollableFrame(ttk.Frame):
    """
    A scrollable frame widget for gesture guidance
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel event
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class GesturePresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Gesture Presentation Tool - Enhanced Version")
        self.root.geometry("1400x850")
        self.root.configure(bg='#2c3e50')
        
        # Initialize controllers
        self.gesture_controller = GestureController()
        self.presentation_manager = PresentationManager()
        self.drawing_manager = DrawingManager()
        
        # Webcam variables
        self.cap = None
        self.is_camera_active = False
        self.current_frame = None
        
        # Gesture tracking
        self.current_gesture = "none"
        self.gesture_history = []
        self.debug_mode = True
        
        # Setup GUI
        self.setup_gui()
        
        # Start camera
        self.start_camera()
    
    def setup_gui(self):
        """Setup the graphical user interface with scrollable gesture guide"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🎯 AI Gesture Presentation Tool - Enhanced Version", 
            font=('Arial', 18, 'bold'),
            foreground='#3498db'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="🎮 Controls & Status", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # Camera feed frame
        camera_frame = ttk.LabelFrame(main_frame, text="📷 Camera Feed & Gesture Recognition", padding="10")
        camera_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        camera_frame.columnconfigure(0, weight=1)
        camera_frame.rowconfigure(0, weight=1)
        
        # Control buttons
        control_buttons = [
            ("📷 Start Camera", self.toggle_camera),
            ("📁 Open Presentation", self.open_presentation_file),
            ("🚀 Start Presentation", self.start_presentation),
            ("⏹️ Stop Presentation", self.stop_presentation),
            ("🎨 Toggle Drawing", self.toggle_drawing),
            ("🧹 Clear Drawing", self.clear_drawing),
            ("🔧 Calibrate Gestures", self.calibrate_gestures)
        ]
        
        for i, (text, command) in enumerate(control_buttons):
            btn = ttk.Button(
                control_frame, 
                text=text, 
                command=command,
                width=20
            )
            btn.grid(row=i, column=0, pady=8, sticky=tk.EW)
        
        # Status frame
        status_frame = ttk.LabelFrame(control_frame, text="📊 System Status", padding="10")
        status_frame.grid(row=len(control_buttons), column=0, pady=(20, 0), sticky=tk.EW)
        
        self.status_labels = {}
        status_items = [
            ("camera", "📷 Camera: Inactive", 'red'),
            ("presentation", "📊 Presentation: Not Started", 'red'),
            ("drawing", "🎨 Drawing: Off", 'red'),
            ("gesture", "👋 Last Gesture: None", 'blue'),
            ("fps", "⚡ FPS: 0", 'green')
        ]
        
        for i, (key, text, color) in enumerate(status_items):
            self.status_labels[key] = ttk.Label(status_frame, text=text, foreground=color)
            self.status_labels[key].grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Scrollable Gesture Guide
        guide_frame = ttk.LabelFrame(control_frame, text="👋 Gesture Guide", padding="10")
        guide_frame.grid(row=len(control_buttons)+1, column=0, pady=(20, 0), sticky=tk.EW)
        guide_frame.columnconfigure(0, weight=1)
        guide_frame.rowconfigure(0, weight=1)
        
        # Create scrollable frame for gesture guide
        scrollable_guide = ScrollableFrame(guide_frame, height=250)
        scrollable_guide.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Detailed gesture guide content
        guide_content = """
🎯 GESTURE GUIDE - HOW TO USE

👉 SWIPE LEFT (Next Slide)
• Move your hand horizontally from right to left
• Keep fingers relatively straight
• Make a quick, deliberate movement
• Movement should be 6-12 inches

👈 SWIPE RIGHT (Previous Slide)  
• Move your hand horizontally from left to right
• Same as swipe left but in opposite direction
• Clear, quick movement works best

👆 SWIPE UP (First Slide)
• Move your hand vertically upward
• Start from bottom, move to top
• Keep palm facing camera

👇 SWIPE DOWN (Last Slide)
• Move your hand vertically downward  
• Start from top, move to bottom
• Smooth, deliberate motion

🤏 PINCH (Start/Stop Presentation)
• Bring thumb and index finger together
• Other fingers should be slightly curled
• Hold for 1 second
• Make sure thumb and index tip touch

✋ OPEN PALM (Stop Presentation)
• Show all five fingers clearly extended
• Palm should face the camera
• Fingers should be straight and separated
• Hold steady for 1-2 seconds

✌️ VICTORY (Toggle Drawing)
• Raise index and middle finger
• Keep ring and pinky fingers down
• Thumb can be relaxed or down
• Classic "peace" sign

👊 FIST (Clear Drawing)
• Close all fingers into a fist
• Thumb can be over or beside fingers
• Make a tight fist for best detection

👍 THUMBS UP (Exit App)
• Extend thumb upward
• Close all other fingers
• Thumb should point up clearly
• Other fingers should be in fist

💡 PRO TIPS FOR BETTER RECOGNITION:

1. LIGHTING
   • Face towards light source
   • Avoid backlighting
   • Even, bright lighting works best

2. POSITIONING
   • Sit 2-4 feet from camera
   • Keep hand in frame center
   • Eye-level camera angle

3. MOVEMENT
   • Make deliberate movements
   • Don't rush gestures
   • Return to neutral position between gestures

4. TROUBLESHOOTING
   • If gestures aren't detected, check lighting
   • Move closer to camera if needed
   • Practice each gesture slowly first
   • Check debug panel for feedback

🎓 PRACTICE EXERCISES:

1. Basic Navigation:
   Pinch → Swipe Left → Swipe Right → Open Palm

2. Drawing Control:
   Victory → Move hand to draw → Fist to clear

3. Full Presentation:
   Pinch → Navigate slides → Draw → Clear → Stop

Remember: The system learns from clear, consistent gestures!
        """
        
        guide_label = ttk.Label(
            scrollable_guide.scrollable_frame, 
            text=guide_content, 
            justify=tk.LEFT, 
            font=('Arial', 9),
            wraplength=350,
            background='#f5f5f5',
            padding=10
        )
        guide_label.grid(row=0, column=0, sticky=tk.W)
        
        # Camera display
        self.camera_label = ttk.Label(camera_frame, background='black')
        self.camera_label.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Debug info with scrollbar
        debug_frame = ttk.LabelFrame(camera_frame, text="🔍 Debug Information", padding="10")
        debug_frame.grid(row=1, column=0, pady=(10, 0), sticky=tk.EW)
        debug_frame.columnconfigure(0, weight=1)
        
        # Create text widget with scrollbar for debug info
        self.debug_text = tk.Text(debug_frame, height=8, width=80, font=('Courier', 9))
        debug_scrollbar = ttk.Scrollbar(debug_frame, orient="vertical", command=self.debug_text.yview)
        self.debug_text.configure(yscrollcommand=debug_scrollbar.set)
        
        self.debug_text.grid(row=0, column=0, sticky=tk.EW)
        debug_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add some sample debug info
        self.debug_text.insert(tk.END, "=" * 60 + "\n")
        self.debug_text.insert(tk.END, "Gesture Recognition System Ready\n")
        self.debug_text.insert(tk.END, "=" * 60 + "\n")
        self.debug_text.insert(tk.END, "Waiting for hand detection...\n")
        self.debug_text.insert(tk.END, "• Ensure good lighting\n")
        self.debug_text.insert(tk.END, "• Keep hand visible in camera\n")
        self.debug_text.insert(tk.END, "• Make clear gestures\n")
        self.debug_text.insert(tk.END, "=" * 60 + "\n")
        self.debug_text.see(tk.END)
        
        # Configure row weights for proper resizing
        control_frame.rowconfigure(len(control_buttons)+1, weight=1)
        guide_frame.rowconfigure(0, weight=1)
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.is_camera_active:
            self.stop_camera()
            self.status_labels['camera'].config(text="📷 Camera: Inactive", foreground='red')
            self.debug_text.insert(tk.END, "📷 Camera stopped\n")
        else:
            self.start_camera()
            self.status_labels['camera'].config(text="📷 Camera: Active", foreground='green')
            self.debug_text.insert(tk.END, "📷 Camera started\n")
        self.debug_text.see(tk.END)
    
    def start_camera(self):
        """Start camera capture"""
        if self.cap is None:
            # Try different camera indices
            for i in range(3):
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    self.debug_text.insert(tk.END, f"✅ Camera {i} opened successfully\n")
                    break
                else:
                    self.cap = None
            
            if self.cap is None:
                messagebox.showerror("Error", "Could not open any camera")
                self.debug_text.insert(tk.END, "❌ Could not open any camera\n")
                return
        
        self.is_camera_active = True
        self.fps_time = time.time()
        self.frame_count = 0
        self.update_camera()
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_camera_active = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def update_camera(self):
        """Update camera feed in GUI"""
        if self.is_camera_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Calculate FPS
                self.frame_count += 1
                current_time = time.time()
                if current_time - self.fps_time >= 1.0:
                    fps = self.frame_count
                    self.frame_count = 0
                    self.fps_time = current_time
                    self.status_labels['fps'].config(text=f"⚡ FPS: {fps}")
                
                # Detect gestures
                gesture, annotated_frame, hand_landmarks = self.gesture_controller.detect_gestures(frame)
                
                # Execute presentation action if gesture detected
                if gesture != "none" and gesture != self.current_gesture:
                    self.current_gesture = gesture
                    success = self.presentation_manager.execute_gesture(gesture, self.drawing_manager)
                    
                    if success:
                        # Update GUI
                        self.status_labels['gesture'].config(
                            text=f"👋 Last Gesture: {gesture}", 
                            foreground='green'
                        )
                        
                        # Add to debug log
                        timestamp = time.strftime("%H:%M:%S")
                        self.debug_text.insert(tk.END, f"[{timestamp}] ✅ {gesture}\n")
                        self.debug_text.see(tk.END)
                
                # Handle drawing if enabled
                if self.drawing_manager.is_drawing and hand_landmarks:
                    finger_pos = self.gesture_controller.get_index_finger_position(hand_landmarks, frame.shape)
                    if finger_pos:
                        self.drawing_manager.draw_at_position(finger_pos)
                
                # Update drawing status
                if self.drawing_manager.is_drawing:
                    self.status_labels['drawing'].config(text="🎨 Drawing: ON", foreground='green')
                else:
                    self.status_labels['drawing'].config(text="🎨 Drawing: OFF", foreground='red')
                
                # Update presentation status
                if self.presentation_manager.is_presenting:
                    self.status_labels['presentation'].config(text="📊 Presentation: Active", foreground='green')
                else:
                    self.status_labels['presentation'].config(text="📊 Presentation: Stopped", foreground='red')
                
                # Convert frame for display
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
            
            # Schedule next update
            self.root.after(15, self.update_camera)
    
    def open_presentation_file(self):
        """Open file dialog to select presentation file"""
        file_types = [
            ("All Presentation Files", "*.pptx *.ppt *.pdf *.key"),
            ("PowerPoint Files", "*.pptx *.ppt"),
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Presentation File",
            filetypes=file_types
        )
        
        if file_path:
            success = self.presentation_manager.open_presentation_file(file_path)
            if success:
                messagebox.showinfo("Success", f"✅ Opened: {os.path.basename(file_path)}")
                self.status_labels['presentation'].config(text="📊 Presentation: Ready", foreground='orange')
                self.debug_text.insert(tk.END, f"📁 Loaded: {os.path.basename(file_path)}\n")
            else:
                messagebox.showerror("Error", "❌ Could not open presentation file")
                self.debug_text.insert(tk.END, f"❌ Failed to load: {os.path.basename(file_path)}\n")
            self.debug_text.see(tk.END)
    
    def start_presentation(self):
        """Start the presentation"""
        self.presentation_manager.start_presentation()
        self.debug_text.insert(tk.END, "🚀 Presentation started\n")
        self.debug_text.see(tk.END)
    
    def stop_presentation(self):
        """Stop the presentation"""
        self.presentation_manager.stop_presentation()
        self.debug_text.insert(tk.END, "⏹️ Presentation stopped\n")
        self.debug_text.see(tk.END)
    
    def toggle_drawing(self):
        """Toggle drawing mode"""
        if self.drawing_manager.is_drawing:
            self.drawing_manager.stop_drawing()
            self.debug_text.insert(tk.END, "🎨 Drawing stopped\n")
        else:
            self.drawing_manager.start_drawing()
            self.debug_text.insert(tk.END, "🎨 Drawing started\n")
        self.debug_text.see(tk.END)
    
    def clear_drawing(self):
        """Clear drawing"""
        self.drawing_manager.clear_drawing()
        self.debug_text.insert(tk.END, "🧹 Drawing cleared\n")
        self.debug_text.see(tk.END)
    
    def calibrate_gestures(self):
        """Calibrate gesture detection"""
        calibration_tips = """
🎯 GESTURE CALIBRATION TIPS:

1. LIGHTING CHECK:
   • Ensure your face is towards light
   • No strong backlighting
   • Even lighting on hands

2. CAMERA POSITION:
   • Camera at eye level
   • 2-4 feet distance
   • Center yourself in frame

3. GESTURE PRACTICE:
   • Make slow, clear gestures first
   • Hold each gesture for 1-2 seconds
   • Return to neutral position between gestures

4. TEST EACH GESTURE:
   • Open Palm → Should show all fingers
   • Victory → Only index & middle up
   • Thumbs Up → Only thumb extended
   • Fist → All fingers closed
   • Pinch → Thumb & index touching

5. TROUBLESHOOTING:
   • If detection fails, check lighting
   • Move closer to camera
   • Make more deliberate movements
   • Check debug panel for feedback
        """
        
        messagebox.showinfo("Gesture Calibration", calibration_tips)
        self.debug_text.insert(tk.END, "🔧 Calibration tips displayed\n")
        self.debug_text.see(tk.END)
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = GesturePresentationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Add welcome message
    welcome_message = """
    Welcome to Enhanced Gesture Presentation Tool! 🎉

    IMPORTANT FOR GESTURE RECOGNITION:

    📋 QUICK START GUIDE:
    1. Click 'Start Camera' to begin
    2. Open your presentation file
    3. Use 'Pinch' gesture to start presentation
    4. Navigate with swipe gestures
    5. Use 'Victory' gesture to toggle drawing

    💡 KEY TIPS FOR SUCCESS:
    • Good lighting is CRITICAL - face towards light
    • Keep hand fully visible in camera
    • Make clear, deliberate gestures
    • Practice each gesture slowly first
    • Check the scrollable gesture guide for details

    🎯 RECOMMENDED TEST ORDER:
    1. Open Palm → Stop Presentation
    2. Pinch → Start Presentation  
    3. Swipe Left/Right → Navigate
    4. Victory → Toggle Drawing
    5. Thumbs Up → Exit

    The scrollable gesture guide has detailed instructions!
    """
    
    messagebox.showinfo("Welcome to Gesture Presentation Tool", welcome_message)
    
    root.mainloop()

if __name__ == "__main__":
    main()