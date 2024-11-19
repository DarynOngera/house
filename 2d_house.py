import cairo
from PIL import Image
import io

# Create a new surface
width, height = 800, 600  # Wider canvas for realistic vanishing points
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

# Create a new context
context = cairo.Context(surface)

# Set the background color to white
context.set_source_rgb(1, 1, 1)
context.paint()

# Define vanishing points for the perspective
vanishing_point_left = (-300, height // 2)  # Off-canvas to the left
vanishing_point_right = (width + 300, height // 2)  # Off-canvas to the right

# Define base coordinates of the house
front_bottom_left = (300, 400)  # Bottom-left of the house
front_bottom_right = (500, 400)  # Bottom-right of the house
front_top_left = (300, 300)  # Top-left of the house
front_top_right = (500, 300)  # Top-right of the house

# Roof peak (visible top)
roof_peak = (400, 200)

# Helper function to draw perspective lines
def draw_perspective_lines(ctx, start_point, vanishing_point, end_point):
    ctx.move_to(*start_point)
    ctx.line_to(*vanishing_point)
    ctx.line_to(*end_point)
    ctx.stroke()

# Draw the front face of the house
context.set_source_rgb(0.8, 0.6, 0.4)  # Light brown for the front face
context.move_to(*front_bottom_left)
context.line_to(*front_bottom_right)
context.line_to(*front_top_right)
context.line_to(*front_top_left)
context.close_path()
context.fill()

# Draw the right wall of the house (perspective lines leading to vanishing point)
context.set_source_rgb(0.6, 0.4, 0.2)  # Darker brown for the right wall
context.move_to(*front_bottom_right)
context.line_to(*vanishing_point_right)  # Converging line towards the right vanishing point
context.line_to(*front_top_right)
context.close_path()
context.fill()

# Draw the roof as a solid color
context.set_source_rgb(0.6, 0.2, 0.2)  # Solid red for the entire roof

# Front roof (showing the top visible part)
context.move_to(*front_top_left)
context.line_to(*roof_peak)
context.line_to(*front_top_right)
context.close_path()
context.fill()

# Right side roof (solid color)
context.move_to(*front_top_right)
context.line_to(*roof_peak)  # Connect top right corner to roof peak
context.line_to(*vanishing_point_right)  # Extend the top right corner towards the vanishing point
context.line_to(600, 300)  # Right wall end point
context.close_path()
context.fill()

# Add a door to the front face
context.set_source_rgb(0.4, 0.2, 0.1)  # Dark wood color
context.rectangle(370, 350, 40, 50)  # Door dimensions
context.fill()

# Add windows to the front face
context.set_source_rgb(0.7, 0.9, 1)  # Light blue for glass
context.rectangle(320, 320, 30, 30)  # Left window
context.fill()

context.rectangle(450, 320, 30, 30)  # Right window
context.fill()

# Save to an in-memory byte stream for Pillow
byte_stream = io.BytesIO()
surface.write_to_png(byte_stream)
byte_stream.seek(0)

# Load into PIL Image
house_image = Image.open(byte_stream)

# Display the image using PIL
house_image.show()

# Optionally, save the image to a file
house_image.save("corrected_house_with_perspective.png")
