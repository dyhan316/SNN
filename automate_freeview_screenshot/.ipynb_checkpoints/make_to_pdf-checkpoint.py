from PIL import Image, ImageDraw, ImageFont
import os
import glob
import PyPDF2

age_img_path = '/Users/eunmi/Desktop/QSIPREP/make_pdf_test_thing'
pdf_name = "infantFS_age_0_1_1.pdf"


cwd = os.getcwd()
os.chdir(age_img_path)

# Get a list of all JPG files in the current directory
jpg_files = glob.glob('sub-*.jpg')

# Create a list of PIL Image objects
images = [Image.open(jpg_file) for jpg_file in jpg_files]

# Create a new PDF document
pdf_path = os.path.join(cwd,pdf_name)
pdf_image_list = []
for i, image in enumerate(images):
    # Add some text to the image
    draw = ImageDraw.Draw(image)
    text = jpg_files[i]
    font = ImageFont.truetype(os.path.join(cwd,"arial.ttf"), 100)  # Set font size to 36
    draw.text((50, 50), text, font = font)
    
    pdf_image_list.append(image.convert('RGB'))

# Save the images as a multi-page PDF
pdf_image_list[0].save(
    pdf_path, save_all=True, append_images=pdf_image_list[1:]
)
