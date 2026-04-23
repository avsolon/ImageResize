from PIL import Image
import os
import sys


def get_user_input():
    """Получает настройки от пользователя"""
    print("=" * 50)
    print("🖼️  Конвертер и ресайзер изображений")
    print("=" * 50)

    # Ввод расширения для конвертации
    while True:
        target_ext = input("\n📝 Введите целевое расширение (jpg, png, webp): ").lower().strip()
        if target_ext in ['jpg', 'jpeg', 'png', 'webp']:
            if target_ext == 'jpeg':
                target_ext = 'jpg'  # нормализуем jpeg к jpg
            break
        else:
            print("❌ Ошибка! Поддерживаемые форматы: jpg, png, webp")

    # Ввод ширины
    while True:
        try:
            width = int(input("📏 Введите желаемую ширину в пикселях (например, 800): ").strip())
            if width > 0:
                break
            else:
                print("❌ Ширина должна быть больше 0")
        except ValueError:
            print("❌ Пожалуйста, введите целое число")

    # Ввод папок
    input_folder = input("📁 Введите путь к папке с исходными файлами (по умолчанию 'input'): ").strip()
    if not input_folder:
        input_folder = 'input'

    output_folder = input("📁 Введите путь для сохранения результатов (по умолчанию 'output'): ").strip()
    if not output_folder:
        output_folder = 'output'

    return target_ext, width, input_folder, output_folder


def resize_and_convert_images(input_folder, output_folder, target_width, target_ext):
    """
    Конвертирует и изменяет размер всех изображений
    Поддерживаемые входные форматы: jpg, jpeg, jfif, png, webp
    """

    # Проверяем существование входной папки
    if not os.path.exists(input_folder):
        print(f"\n❌ Ошибка: Папка '{input_folder}' не существует!")
        return False

    # Создаём выходную папку если нужно
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\n📁 Создана папка: {output_folder}")

    # Поддерживаемые входные форматы
    input_extensions = ('.png', '.jpg', '.jpeg', '.jfif', '.webp')

    # Счётчики
    processed = 0
    errors = 0
    skipped = 0

    print(f"\n🔄 Начинаю обработку...")
    print(f"   Входная папка: {input_folder}")
    print(f"   Выходная папка: {output_folder}")
    print(f"   Целевая ширина: {target_width}px")
    print(f"   Целевой формат: {target_ext.upper()}")
    print("-" * 50)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Пропускаем папки
        if os.path.isdir(input_path):
            continue

        # Проверяем расширение файла (без учёта регистра)
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext in input_extensions:
            # Формируем новое имя файла с нужным расширением
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}.{target_ext}"
            output_path = os.path.join(output_folder, output_filename)

            try:
                # Открываем изображение
                img = Image.open(input_path)

                # Получаем оригинальные размеры
                original_width, original_height = img.size

                # Вычисляем новую высоту пропорционально
                ratio = target_width / original_width
                new_height = int(original_height * ratio)

                # Изменяем размер
                resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

                # Конвертируем в нужный формат и сохраняем
                if target_ext == 'jpg':
                    # Для JPEG нужно конвертировать в RGB (если изображение в RGBA)
                    if resized_img.mode in ('RGBA', 'LA', 'P'):
                        # Создаём белый фон для прозрачных областей
                        background = Image.new('RGB', resized_img.size, (255, 255, 255))
                        if resized_img.mode == 'P':
                            resized_img = resized_img.convert('RGBA')
                        background.paste(resized_img,
                                         mask=resized_img.split()[-1] if resized_img.mode == 'RGBA' else None)
                        resized_img = background
                    elif resized_img.mode != 'RGB':
                        resized_img = resized_img.convert('RGB')
                    resized_img.save(output_path, 'JPEG', quality=85)

                elif target_ext == 'png':
                    resized_img.save(output_path, 'PNG')

                elif target_ext == 'webp':
                    resized_img.save(output_path, 'WEBP', quality=85)

                processed += 1
                print(
                    f"✅ {filename} → {output_filename} ({original_width}x{original_height} → {target_width}x{new_height})")

            except Exception as e:
                errors += 1
                print(f"❌ Ошибка при обработке {filename}: {str(e)}")
        else:
            skipped += 1
            print(f"⏭️  Пропущен (неподдерживаемый формат): {filename}")

    # Выводим итоговую статистику
    print("-" * 50)
    print("\n📊 СТАТИСТИКА:")
    print(f"   ✅ Успешно обработано: {processed} файлов")
    print(f"   ❌ Ошибок: {errors} файлов")
    print(f"   ⏭️  Пропущено: {skipped} файлов")
    print(f"\n📁 Результаты сохранены в: {output_folder}")

    return True


def main():
    """Главная функция"""
    try:
        # Получаем настройки от пользователя
        target_ext, width, input_folder, output_folder = get_user_input()

        # Запускаем обработку
        success = resize_and_convert_images(input_folder, output_folder, width, target_ext)

        if success:
            print("\n✨ Готово! Все изображения обработаны.")
        else:
            print("\n⚠️ Обработка завершена с ошибками.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Операция прервана пользователем.")
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {str(e)}")


if __name__ == "__main__":
    main()