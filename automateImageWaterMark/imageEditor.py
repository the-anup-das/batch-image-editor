import os
from os.path import isfile, join
from PIL import Image


class EditerAutomation:
    def __init__(self):
        self.file_extensions = ('.jpg', '.jpeg', '.png')
        self.in_directory = f"{os.path.dirname(os.path.abspath(__file__))}/{'in_photos'}"
        self.out_directory = f"{os.path.dirname(os.path.abspath(__file__))}/{'out_photos'}"
        self.watermark = Image.open(r"C:\Users\Awesome\Desktop\automateImageWaterMark\watermark.png")
        self.watermark_width = self.watermark.width
        self.watermark_height = self.watermark.height

    def run(self):
        images = self.get_files_in_directory()
        self.put_watermark_images(images)
        #self.clear_in_directory(images)

    def get_files_in_directory(self):
        onlyfiles = [f for f in os.listdir(self.in_directory) if isfile(join(self.in_directory, f))]
        return [f for f in onlyfiles if f.endswith(self.file_extensions)]
    
    def clear_in_directory(self,images):
        for image in images:
            os.remove(f'{self.in_directory}/{image}')
    
    def put_watermark_images(self, images):
        for image in images:
            self.stamp_single_image(image)

    def stamp_single_image(self, image_name):
        image=Image.open(f'{self.in_directory}/{image_name}')
        image_width=image.width
        image_height=image.height

        print((int((image_width - self.watermark_width)/2 ), int((image_height - self.watermark_height) )))

        image.paste(self.watermark,
                    (abs(int((image_width - self.watermark_width)/2 )), int((image_height - self.watermark_height+400) )),
                    mask=self.watermark)
        image.save(f'{self.out_directory}/{image_name}')

def main():
    automation = EditerAutomation()
    automation.run()


if __name__ == '__main__':
    main()
