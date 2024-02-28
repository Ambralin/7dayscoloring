from PIL import Image
from datetime import datetime
import re
import sys

if __name__ == "__main__":
    # Check if an image file is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        sys.exit(1)

    # Get the image file path from the command-line argument
    image_path = sys.argv[1]

def generate_material_palette(materials_image_path, material_size, gap_before_first=3, gap_between_materials=3):
    # Open the big image containing all materials
    materials_image = Image.open(materials_image_path)

    # Get the size of individual material images
    material_width, material_height = material_size

    # Calculate the number of materials in each row and column
    num_materials_x = (materials_image.width + gap_before_first) // (material_width + gap_between_materials)
    num_materials_y = materials_image.height // (material_height + gap_between_materials)

    # Initialize an empty list to store individual material images
    material_palette = []

    # Extract each material image from the big image
    for y in range(num_materials_y):
        for x in range(num_materials_x):
            left = x * (material_width + gap_between_materials) + gap_before_first
            upper = y * (material_height + gap_between_materials)
            right = left + material_width
            lower = upper + material_height

            # Crop the material from the big image
            material = materials_image.crop((left, upper, right, lower))

            # Check if the material has transparency (alpha channel)
            if material.mode == 'RGBA' and 0 in material.getchannel('A').getdata():
                print(f"Skipping material with transparency: Row {y + 1}, Column {x + 1}")
                continue

            # Append the material to the palette
            material_palette.append(material)

            # Print the current row and column
            print(f"Processing row {y + 1}, column {x + 1}")

    return material_palette

def convert_pixel_art(original_image, material_palette):
    # Open the original image
    img = Image.open(original_image)
    
    # Get the size of individual material images
    material_width, material_height = material_palette[0].size

    # Create a new image with the same size and mode
    converted_img = Image.new("RGB", (img.width * material_width, img.height * material_height))

    # Iterate through each pixel
    for y in range(img.height):
        for x in range(img.width):
            # Get the original pixel color
            original_color = img.getpixel((x, y))

            # Find the closest material in the palette
            closest_material = min(material_palette, key=lambda material: color_difference(original_color, get_average_color(material)))

            # Paste the material onto the converted image
            converted_img.paste(closest_material, (x * material_width, y * material_height))

            # Print the current column
            print(f"Converted row {y + 1}, column {x + 1}")

        # Print the current row
        print(f"Converted row {y + 1}")

    # Print the completion message
    print("Conversion completed.")

    return converted_img

def get_average_color(img):
    # Calculate the average color of an image
    pixels = list(img.getdata())
    average_color = (
        sum(pixel[0] for pixel in pixels) // len(pixels),
        sum(pixel[1] for pixel in pixels) // len(pixels),
        sum(pixel[2] for pixel in pixels) // len(pixels)
    )
    return average_color

def color_difference(color1, color2):
    # Calculate the squared Euclidean distance between two colors
    return sum((a - b) ** 2 for a, b in zip(color1, color2))

# Example usage
materials_image_path = r"C:\Users\dzelm\Desktop\code\7dayscoloring\materials2.png"
material_size = (79, 79)

# Generate material palette from the big image with specified gaps
material_palette = generate_material_palette(materials_image_path, material_size, gap_before_first=3, gap_between_materials=3)

# Example usage
original_image_path = image_path

# Convert the pixel art
converted_image = convert_pixel_art(original_image_path, material_palette)

# Save the result
filename = (r"C:\Users\dzelm\Desktop\code\7dayscoloring\output\final" + str(re.sub(r'[^0-9]', '', str(datetime.now()))) + ".png")
converted_image.save(filename)