import pyautogui
import time
import math

class DrawingManager:
    def __init__(self):
        self.is_drawing = False
        self.last_draw_point = None
        self.draw_color = (255, 0, 0)  # Red color
        self.brush_size = 5
        self.drawing_cooldown = 0.1  # seconds
        self.last_draw_time = 0
        
    def start_drawing(self):
        """Start drawing mode"""
        if not self.is_drawing:
            self.is_drawing = True
            self.last_draw_point = None
            print("Drawing mode: ON")
            return True
        return False
    
    def stop_drawing(self):
        """Stop drawing mode"""
        if self.is_drawing:
            self.is_drawing = False
            self.last_draw_point = None
            print("Drawing mode: OFF")
            return True
        return False
    
    def draw_at_position(self, normalized_pos):
        """Draw at the specified normalized position"""
        if not self.is_drawing or not normalized_pos:
            return
        
        current_time = time.time()
        if current_time - self.last_draw_time < self.drawing_cooldown:
            return
        
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        
        # Convert normalized position to screen coordinates
        x = int(normalized_pos[0] * screen_width)
        y = int(normalized_pos[1] * screen_height)
        
        # Ensure coordinates are within screen bounds
        x = max(0, min(x, screen_width - 1))
        y = max(0, min(y, screen_height - 1))
        
        if self.last_draw_point:
            # Draw line from last point to current point
            self._draw_line(self.last_draw_point, (x, y))
        else:
            # Draw a single point
            pyautogui.click(x, y)
        
        self.last_draw_point = (x, y)
        self.last_draw_time = current_time
    
    def _draw_line(self, start_point, end_point):
        """Draw a line between two points"""
        # Use pyautogui to draw by dragging
        pyautogui.mouseDown(start_point[0], start_point[1])
        pyautogui.moveTo(end_point[0], end_point[1], duration=0.1)
        pyautogui.mouseUp()
    
    def clear_drawing(self):
        """Clear drawing (simulate undo)"""
        pyautogui.hotkey('ctrl', 'z')  # Undo in most applications
        print("Drawing cleared")
    
    def change_color(self):
        """Cycle through different colors"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        current_index = colors.index(self.draw_color) if self.draw_color in colors else 0
        next_index = (current_index + 1) % len(colors)
        self.draw_color = colors[next_index]
        print(f"Color changed to: {self.draw_color}")
    
    def increase_brush_size(self):
        """Increase brush size"""
        self.brush_size = min(20, self.brush_size + 2)
        print(f"Brush size increased to: {self.brush_size}")
    
    def decrease_brush_size(self):
        """Decrease brush size"""
        self.brush_size = max(1, self.brush_size - 2)
        print(f"Brush size decreased to: {self.brush_size}")