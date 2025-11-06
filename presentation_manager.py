# import pyautogui
# import time
# import os
# import subprocess
# import platform

# class PresentationManager:
#     def __init__(self):
#         self.is_presenting = False
#         self.current_slide = 0
#         self.gesture_actions = {
#             "swipe_left": self.next_slide,
#             "swipe_right": self.previous_slide,
#             "swipe_up": self.first_slide,
#             "swipe_down": self.last_slide,
#             "pinch": self.start_presentation,
#             "open_palm": self.stop_presentation,
#             "thumbs_up": self.exit_application,
#             "victory": self.toggle_drawing,
#             "fist": self.clear_drawing
#         }
    
#     def execute_gesture(self, gesture, drawing_manager=None):
#         """Execute presentation action based on detected gesture"""
#         if gesture in self.gesture_actions:
#             if gesture in ["victory", "fist"] and drawing_manager:
#                 self.gesture_actions[gesture](drawing_manager)
#             else:
#                 self.gesture_actions[gesture]()
#             return True
#         return False
    
#     def next_slide(self):
#         """Go to next slide"""
#         if self.is_presenting:
#             pyautogui.press('right')
#             self.current_slide += 1
#             print(f"Next slide - Slide {self.current_slide}")
#         else:
#             print("Presentation not started. Use 'pinch' gesture to start.")
    
#     def previous_slide(self):
#         """Go to previous slide"""
#         if self.is_presenting:
#             pyautogui.press('left')
#             self.current_slide = max(0, self.current_slide - 1)
#             print(f"Previous slide - Slide {self.current_slide}")
#         else:
#             print("Presentation not started. Use 'pinch' gesture to start.")
    
#     def first_slide(self):
#         """Go to first slide"""
#         if self.is_presenting:
#             pyautogui.press('home')
#             self.current_slide = 0
#             print("First slide")
    
#     def last_slide(self):
#         """Go to last slide"""
#         if self.is_presenting:
#             pyautogui.press('end')
#             self.current_slide = 100  # Assuming we don't know exact count
#             print("Last slide")
    
#     def start_presentation(self):
#         """Start presentation mode"""
#         if not self.is_presenting:
#             pyautogui.hotkey('f5')  # Start slideshow in most presentation software
#             self.is_presenting = True
#             self.current_slide = 0
#             print("Presentation started")
    
#     def stop_presentation(self):
#         """Stop presentation mode"""
#         if self.is_presenting:
#             pyautogui.press('esc')
#             self.is_presenting = False
#             print("Presentation stopped")
    
#     def exit_application(self):
#         """Exit application"""
#         self.stop_presentation()
#         print("Exiting presentation controller")
    
#     def toggle_drawing(self, drawing_manager):
#         """Toggle drawing mode"""
#         if drawing_manager.is_drawing:
#             drawing_manager.stop_drawing()
#         else:
#             drawing_manager.start_drawing()
    
#     def clear_drawing(self, drawing_manager):
#         """Clear drawing"""
#         drawing_manager.clear_drawing()
    
#     def open_presentation_file(self, file_path):
#         """Open presentation file with default application"""
#         try:
#             if platform.system() == "Windows":
#                 os.startfile(file_path)
#             elif platform.system() == "Darwin":  # macOS
#                 subprocess.call(["open", file_path])
#             else:  # Linux
#                 subprocess.call(["xdg-open", file_path])
            
#             print(f"Opened presentation: {file_path}")
#             time.sleep(3)  # Wait for application to load
#             return True
#         except Exception as e:
#             print(f"Error opening file: {e}")
#             return False

import pyautogui
import time
import os
import subprocess
import platform

class PresentationManager:
    def __init__(self):
        self.is_presenting = False
        self.current_slide = 0
        self.gesture_actions = {
            "swipe_left": self.next_slide,
            "swipe_right": self.previous_slide,
            "swipe_up": self.first_slide,
            "swipe_down": self.last_slide,
            "pinch": self.toggle_presentation,
            "open_palm": self.stop_presentation,
            "thumbs_up": self.exit_application,
            "victory": self.toggle_drawing,
            "fist": self.clear_drawing
        }
        
        # Add keyboard shortcuts for different presentation software
        self.presentation_shortcuts = {
            'next': ['right', 'space', 'n', 'page down'],
            'previous': ['left', 'p', 'page up', 'backspace'],
            'start': ['f5'],
            'stop': ['esc']
        }
    
    def execute_gesture(self, gesture, drawing_manager=None):
        """Execute presentation action based on detected gesture"""
        print(f"Executing gesture: {gesture}")
        
        if gesture in self.gesture_actions:
            try:
                if gesture in ["victory", "fist"] and drawing_manager:
                    self.gesture_actions[gesture](drawing_manager)
                else:
                    self.gesture_actions[gesture]()
                return True
            except Exception as e:
                print(f"Error executing gesture {gesture}: {e}")
                return False
        return False
    
    def next_slide(self):
        """Go to next slide using multiple methods"""
        print("Next slide command")
        if self.is_presenting:
            # Try multiple keyboard shortcuts
            for key in self.presentation_shortcuts['next']:
                try:
                    pyautogui.press(key)
                    break
                except:
                    continue
            self.current_slide += 1
            print(f"Next slide - Slide {self.current_slide}")
        else:
            print("Presentation not started. Use 'pinch' gesture to start.")
    
    def previous_slide(self):
        """Go to previous slide using multiple methods"""
        print("Previous slide command")
        if self.is_presenting:
            # Try multiple keyboard shortcuts
            for key in self.presentation_shortcuts['previous']:
                try:
                    pyautogui.press(key)
                    break
                except:
                    continue
            self.current_slide = max(0, self.current_slide - 1)
            print(f"Previous slide - Slide {self.current_slide}")
        else:
            print("Presentation not started. Use 'pinch' gesture to start.")
    
    def first_slide(self):
        """Go to first slide"""
        print("First slide command")
        if self.is_presenting:
            pyautogui.press('home')
            self.current_slide = 0
            print("First slide")
    
    def last_slide(self):
        """Go to last slide"""
        print("Last slide command")
        if self.is_presenting:
            pyautogui.press('end')
            self.current_slide = 100  # Assuming we don't know exact count
            print("Last slide")
    
    def toggle_presentation(self):
        """Toggle presentation mode"""
        if not self.is_presenting:
            self.start_presentation()
        else:
            self.stop_presentation()
    
    def start_presentation(self):
        """Start presentation mode"""
        print("Starting presentation")
        # Try multiple start shortcuts
        for key in self.presentation_shortcuts['start']:
            try:
                if key == 'f5':
                    pyautogui.press(key)
                else:
                    pyautogui.hotkey(key)
                break
            except:
                continue
        
        self.is_presenting = True
        self.current_slide = 0
        print("Presentation started")
        time.sleep(2)  # Wait for presentation to start
    
    def stop_presentation(self):
        """Stop presentation mode"""
        print("Stopping presentation")
        if self.is_presenting:
            # Try multiple stop shortcuts
            for key in self.presentation_shortcuts['stop']:
                try:
                    pyautogui.press(key)
                    break
                except:
                    continue
            self.is_presenting = False
            print("Presentation stopped")
    
    def exit_application(self):
        """Exit application"""
        print("Exit application command")
        self.stop_presentation()
        print("Exiting presentation controller")
    
    def toggle_drawing(self, drawing_manager):
        """Toggle drawing mode"""
        print("Toggle drawing command")
        if drawing_manager.is_drawing:
            drawing_manager.stop_drawing()
        else:
            drawing_manager.start_drawing()
    
    def clear_drawing(self, drawing_manager):
        """Clear drawing"""
        print("Clear drawing command")
        drawing_manager.clear_drawing()
    
    def open_presentation_file(self, file_path):
        """Open presentation file with default application"""
        try:
            print(f"Opening presentation file: {file_path}")
            
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            else:  # Linux
                subprocess.call(["xdg-open", file_path])
            
            print(f"Successfully opened: {file_path}")
            time.sleep(3)  # Wait for application to load
            return True
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
            return False