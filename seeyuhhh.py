import tkinter as tk
import math

class AdvancedArrowSimulation2D:
    def __init__(self, root):
        self.root = root
        self.root.title("tuff physics simulator fr")
        
        # Physics parameters
        self.gravity = 9.81
        self.dt = 0.025
        self.air_resistance = 0.001  # Reduced for higher speeds
        
        # Setup GUI
        self.create_controls()
        self.create_canvas()
        self.reset_simulation()
        self.update_preview()
    
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Velocity control
        tk.Label(control_frame, text="Velocity (m/s)").pack()
        self.velocity_slider = tk.Scale(control_frame, from_=10, to=500, orient=tk.HORIZONTAL)
        self.velocity_slider.set(100)
        self.velocity_slider.pack()
        
        # Angle control
        tk.Label(control_frame, text="Launch Angle").pack()
        self.angle_slider = tk.Scale(control_frame, from_=0, to=90, orient=tk.HORIZONTAL)
        self.angle_slider.set(45)
        self.angle_slider.pack()
        
        # Gravity control
        tk.Label(control_frame, text="Gravity (m/s²)").pack()
        self.gravity_slider = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL)
        self.gravity_slider.set(9.81)
        self.gravity_slider.pack()
        
        # Wind control
        tk.Label(control_frame, text="Wind (m/s →)").pack()
        self.wind_slider = tk.Scale(control_frame, from_=-50, to=50, orient=tk.HORIZONTAL)
        self.wind_slider.set(0)
        self.wind_slider.pack()
        
        # Control buttons
        tk.Button(control_frame, text="Launch", command=self.start_simulation).pack(pady=5)
        tk.Button(control_frame, text="Reset", command=self.reset_simulation).pack(pady=5)
        
        # Bind slider updates to preview
        self.velocity_slider.config(command=lambda v: self.update_preview())
        self.angle_slider.config(command=lambda v: self.update_preview())
    
    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="skyblue")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Draw ground
        self.canvas.create_rectangle(0, 400, 800, 500, fill="#4a752c", outline="")
        
        # Draw scenery
        self.draw_sun()
        self.draw_cloud(100, 100)
        self.draw_cloud(300, 150)
        self.draw_cloud(600, 80)
        self.draw_tree(650, 380)
        
        # Target and preview arrow
        self.target = self.canvas.create_oval(700, 380, 740, 420, fill="red", outline="black")
        self.preview_arrow = self.canvas.create_line(0, 0, 0, 0, width=3, arrow=tk.LAST, fill="#666666")
        self.distance_text = self.canvas.create_text(400, 450, text="", font=("Arial", 14), fill="white")
    
    def draw_sun(self):
        self.canvas.create_oval(650, 50, 750, 150, fill="#ffd700", outline="")
    
    def draw_cloud(self, x, y):
        self.canvas.create_oval(x, y, x+60, y+40, fill="white", outline="")
        self.canvas.create_oval(x+30, y-10, x+90, y+30, fill="white", outline="")
        self.canvas.create_oval(x-30, y+10, x+30, y+50, fill="white", outline="")
    
    def draw_tree(self, x, y):
        self.canvas.create_rectangle(x-10, y-80, x+10, y, fill="#5d3a1a", outline="")
        self.canvas.create_oval(x-40, y-180, x+40, y-80, fill="#228b22", outline="")
    
    def reset_simulation(self):
        self.simulating = False
        self.canvas.delete("arrow")
        self.canvas.delete("trail")
        self.canvas.itemconfig(self.target, fill="red")
        self.canvas.itemconfig(self.distance_text, text="")
        self.update_preview()
    
    def update_preview(self):
        if self.simulating:
            return
        
        angle = math.radians(self.angle_slider.get())
        velocity = self.velocity_slider.get()
        preview_length = velocity / 4  # Scale preview size with velocity
        
        x1 = 50 + preview_length * math.cos(angle)
        y1 = 400 - preview_length * math.sin(angle)
        
        self.canvas.coords(self.preview_arrow, 
            50, 400,
            x1, y1
        )
    
    def start_simulation(self):
        if self.simulating:
            return
        
        self.simulating = True
        self.canvas.itemconfig(self.target, fill="red")
        
        # Initial conditions
        angle = math.radians(self.angle_slider.get())
        self.vx = self.velocity_slider.get() * math.cos(angle)
        self.vy = -self.velocity_slider.get() * math.sin(angle)
        self.x, self.y = 50, 400
        self.trail = []
        self.flight_time = 0
        
        # Create arrow
        self.arrow = self.canvas.create_line(0, 0, 0, 0, width=3, arrow=tk.LAST, fill="brown", tags="arrow")
        self.animate()
    
    def animate(self):
        if not self.simulating:
            return
        
        # Update physics
        self.gravity = self.gravity_slider.get()
        self.wind = self.wind_slider.get()
        speed = math.hypot(self.vx, self.vy)
        
        # Air resistance and wind
        drag = self.air_resistance * speed ** 2
        ax = -drag * self.vx / speed + self.wind if speed != 0 else self.wind
        ay = self.gravity - drag * self.vy / speed if speed != 0 else self.gravity
        
        self.vx += ax * self.dt
        self.vy += ay * self.dt
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt
        self.flight_time += self.dt
        
        # Store trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:
            self.trail.pop(0)
        
        # Update graphics
        self.update_arrow()
        self.draw_trail()
        self.check_target_hit()
        
        # Continue animation
        if self.x < 850 and self.y < 500:
            self.root.after(10, self.animate)
        else:
            self.show_results()
            self.simulating = False
    
    def update_arrow(self):
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        arrow_length = 30
        
        x1 = self.x - arrow_length * math.cos(math.radians(angle))
        y1 = self.y + arrow_length * math.sin(math.radians(angle))
        
        self.canvas.coords(self.arrow, 
            self.x, self.y,
            x1, y1
        )
    
    def draw_trail(self):
        self.canvas.delete("trail")
        for i, (x, y) in enumerate(self.trail):
            opacity = int(255 * (i/len(self.trail)))
            color = f"#{opacity:02x}{opacity:02x}ff"
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline="", tags="trail")
    
    def check_target_hit(self):
        target_coords = self.canvas.coords(self.target)
        if (target_coords[0] < self.x < target_coords[2] and 
            target_coords[1] < self.y < target_coords[3]):
            self.canvas.itemconfig(self.target, fill="green")
            self.simulating = False
            self.show_results()
    
    def show_results(self):
        distance = self.x - 50
        self.canvas.itemconfig(self.distance_text, 
            text=f"Distance: {distance:.1f}m | Time: {self.flight_time:.1f}s | Max Speed: {math.hypot(self.vx, self.vy):.1f}m/s"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedArrowSimulation2D(root)
    root.mainloop()
