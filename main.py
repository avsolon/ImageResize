from PIL import Image
import os


def resize_images(input_folder, output_folder, width):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                img = Image.open(input_path)
                original_width, original_height = img.size
                ratio = width / original_width
                new_height = int(original_height * ratio)
                resized_img = img.resize((width, new_height), Image.LANCZOS)
                resized_img.save(output_path)
                print(f"Обработано: {filename}")
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {str(e)}")


input_folder = 'input'
output_folder = 'output'
desired_width = 300

resize_images(input_folder, output_folder, desired_width)
