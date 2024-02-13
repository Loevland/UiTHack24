from ultralytics import YOLO
from PIL import Image, ImageDraw
import os


def overlap_images(image1_path, image2_path, output_path, alpha=0.5):
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")
    blended = Image.blend(image1, image2, alpha)
    blended.save(output_path)

def stitch_images(images_folder, output_path, grid_size=(10, 10), image_size=(224, 224)):
    stitched_image = Image.new("RGB", (grid_size[0] * image_size[0], grid_size[1] * image_size[1]))
    image_paths = [os.path.join(images_folder, f'tile_{i}.png') for i in range(1, grid_size[0] * grid_size[1] + 1)]
    for i, image_path in enumerate(image_paths):
        img = Image.open(image_path)
        x_position = (i % grid_size[0]) * image_size[0]
        y_position = (i // grid_size[0]) * image_size[1]
        stitched_image.paste(img, (x_position, y_position))
    stitched_image.save(output_path)

def split_image(input_path, output_folder, tile_size):
    img = Image.open(input_path)
    width, height = img.size
    num_tiles_x = width // tile_size
    num_tiles_y = height // tile_size
    os.makedirs(output_folder, exist_ok=True)
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            left = x * tile_size
            upper = y * tile_size
            right = (x + 1) * tile_size
            lower = (y + 1) * tile_size
            tile = img.crop((left, upper, right, lower))
            tile.save(os.path.join(output_folder, f'tile_{y * num_tiles_x + x + 1}.png'))

def load_paths(folder_path):
    file_paths = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        file_paths = [os.path.join(folder_path, file) for file in files]
    return file_paths

def convert_and_draw(r, coordinates):
    img = Image.new("L", (224, 244), color="black")
    draw = ImageDraw.Draw(img)
    top_left = (float(coordinates[0]), float(coordinates[1]))
    bottom_right = (float(coordinates[2]), float(coordinates[3])) 
    draw.rectangle([top_left, bottom_right], fill="white")
    img.save(r.path)

def convert_and_draw_empty(r): 
    img = Image.new("L", (224, 244), color="black")
    img.save(r.path)

split_image("secret.png", "tmp", 224)
images = load_paths("tmp")

model = YOLO('best.pt') 
idx = 1
for image in images: 
    results = model(image, classes=0) 
    for r in results:
        try: 
            convert_and_draw(r, r.boxes.data.cpu().numpy().tolist()[0])
        except: 
            convert_and_draw_empty(r)
        idx +=1

stitch_images("tmp", "overlap.png")
overlap_images("secret_number.png", "overlap.png", "answer.png")