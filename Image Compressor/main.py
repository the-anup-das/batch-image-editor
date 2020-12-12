import os
from os.path import isfile, join
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import PIL
from PIL import Image

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 10
        self.top = 100
        self.width = 400
        self.height = 600
        self.image_width=0
        self.compress_width=0

        self.out_directory = "compressed_photos"
        self.file_extensions = ('.jpg', '.jpeg', '.png')
        self.statusBar().showMessage("Message")
        self.statusBar().setObjectName("status")
        self.setObjectName("main_window")
        stylesheet=""
        with open("style.qss","r") as f:
            stylesheet=f.read()
        self.setStyleSheet(stylesheet)
        self.setFixedSize(self.width,self.height)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # open main window
        #single image
        self.single_bubble=QFrame(self)
        self.single_bubble.setObjectName("bubble")
        self.single_bubble.move(50,100)
        self.single_bubble.mousePressEvent=self.single_bubble_clicked

        self.single_bubble_heading=QLabel(self.single_bubble)
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.move(80,8)

        self.single_bubble_para=QLabel(self.single_bubble)
        self.single_bubble_para.setText("Click here to compress a single image.")
        self.single_bubble_para.setObjectName("bubble_para")
        self.single_bubble_para.move(25,32)

        self.single_bubble_extended=QFrame(self)
        self.single_bubble_extended.setObjectName("bubble_extended")
        self.single_bubble_extended.move(50,100)
        self.single_bubble_extended.setVisible(False)

        self.back_arrow_s=QLabel(self.single_bubble_extended)
        self.back_arrow_s.move(15,0)
        self.back_arrow_s.setObjectName("back_arrow")
        self.back_arrow_s.setTextFormat(Qt.RichText)
        self.back_arrow_s.setText("&#8592;")  #printing back arrow using unicode
        self.back_arrow_s.mousePressEvent=self.back_arrow_clicked

        self.single_bubble_heading=QLabel(self.single_bubble_extended)
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.move(80,8)        

        #choose image
        self.select_image_label=QLabel(self.single_bubble_extended)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(30,50)

        self.image_path=QLineEdit(self.single_bubble_extended)
        self.image_path.setObjectName("path_text")
        self.image_path.move(60,85)
        self.image_path.setEnabled(False)

        #select image
        self.browse_button=QPushButton(self.single_bubble_extended)
        self.browse_button.setObjectName("browse_button")
        self.browse_button.setText("...")
        self.browse_button.move(240,85)
        self.browse_button.clicked.connect(self.select_file)

        #choose Quality
        self.select_image_quality=QLabel(self.single_bubble_extended)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(30,130)

        self.single_quality_path=QLineEdit(self.single_bubble_extended)
        self.single_quality_path.setObjectName("quality_path_text")
        self.single_quality_path.move(60,160)
        self.single_quality_path.setEnabled(False)

        #select Quality
        self.single_quality_combo=QComboBox(self.single_bubble_extended)
        self.single_quality_combo.setObjectName("quality_combo")
        self.single_quality_combo.addItem("High")
        self.single_quality_combo.addItem("Medium")
        self.single_quality_combo.addItem("Low")
        self.single_quality_combo.move(170,160)
        self.single_quality_combo.currentIndexChanged.connect(self.single_quality_current_value)

        #compress button
        self.source_compress_image=QPushButton(self.single_bubble_extended)
        self.source_compress_image.setObjectName("compress_button")
        self.source_compress_image.setText("Compress")
        self.source_compress_image.move(110,260)
        self.source_compress_image.clicked.connect(self.single_compress_clicked)


        #directory of images

        self.dir_bubble=QFrame(self)
        self.dir_bubble.setObjectName("bubble")
        self.dir_bubble.move(50,275)
        self.dir_bubble.mousePressEvent=self.dir_bubble_clicked

        self.dir_bubble_heading=QLabel(self.dir_bubble)
        self.dir_bubble_heading.setText("Compress Multiple Image")
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.move(55,8)

        self.dir_bubble_para=QLabel(self.dir_bubble)
        self.dir_bubble_para.setText("Click here to compress multiple images at once.")
        self.dir_bubble_para.setObjectName("bubble_para")
        self.dir_bubble_para.move(10,32)

        self.dir_bubble_extended=QFrame(self)
        self.dir_bubble_extended.setObjectName("bubble_extended")
        self.dir_bubble_extended.move(50,100)
        self.dir_bubble_extended.setVisible(False)

        self.back_arrow_d=QLabel(self.dir_bubble_extended)
        self.back_arrow_d.move(15,0)
        self.back_arrow_d.setObjectName("back_arrow")
        self.back_arrow_d.setTextFormat(Qt.RichText)
        self.back_arrow_d.setText("&#65513;")  #printing back arrow using unicode
        self.back_arrow_d.mousePressEvent=self.back_arrow_clicked

        self.single_bubble_heading=QLabel(self.dir_bubble_extended)
        self.single_bubble_heading.setText("Compress Multiple Images")
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.move(65,8)        

        #choose source directory
        self.select_source_label=QLabel(self.dir_bubble_extended)
        self.select_source_label.setObjectName("bubble_para")
        self.select_source_label.setText("Choose Source Directory")
        self.select_source_label.move(30,50)

        self.source_path=QLineEdit(self.dir_bubble_extended)
        self.source_path.setObjectName("path_text")
        self.source_path.move(60,85)
        self.source_path.setEnabled(False)

        #select source directory
        self.browse_source_button=QPushButton(self.dir_bubble_extended)
        self.browse_source_button.setObjectName("browse_button")
        self.browse_source_button.setText("...")
        self.browse_source_button.move(240,85)
        self.browse_source_button.clicked.connect(self.select_source_folder)


        #choose Destination directory
        self.select_des_label=QLabel(self.dir_bubble_extended)
        self.select_des_label.setObjectName("bubble_para")
        self.select_des_label.setText("Choose Output Directory")
        self.select_des_label.move(30,130)

        self.des_path=QLineEdit(self.dir_bubble_extended)
        self.des_path.setObjectName("path_text")
        self.des_path.move(60,160)
        self.des_path.setEnabled(False)

        #select Destination directory
        self.browse_des_button=QPushButton(self.dir_bubble_extended)
        self.browse_des_button.setObjectName("browse_button")
        self.browse_des_button.setText("...")
        self.browse_des_button.move(240,160)
        self.browse_des_button.clicked.connect(self.select_des_folder)

        #choose Quality
        self.select_image_quality=QLabel(self.dir_bubble_extended)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(30,205)

        self.dir_quality_path=QLineEdit(self.dir_bubble_extended)
        self.dir_quality_path.setObjectName("quality_path_text")
        self.dir_quality_path.move(60,235)
        self.dir_quality_path.setEnabled(False)

        #select Quality
        self.dir_quality_combo=QComboBox(self.dir_bubble_extended)
        self.dir_quality_combo.setObjectName("quality_combo")
        self.dir_quality_combo.addItem("High")
        self.dir_quality_combo.addItem("Medium")
        self.dir_quality_combo.addItem("Low")
        self.dir_quality_combo.move(170,235)
        self.dir_quality_combo.currentIndexChanged.connect(self.dir_quality_current_value)


        #compress button
        self.des_compress_image=QPushButton(self.dir_bubble_extended)
        self.des_compress_image.setObjectName("compress_button")
        self.des_compress_image.setText("Compress")
        self.des_compress_image.move(110,290)
        self.des_compress_image.clicked.connect(self.dir_compress_clicked)
        # end main window 

        self.show()

    def single_bubble_clicked(self,event):
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.dir_bubble_extended.setVisible(False)
        self.single_bubble_extended.setVisible(True)

    def dir_bubble_clicked(self,event):
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_extended.setVisible(False)
        self.dir_bubble_extended.setVisible(True)

    def back_arrow_clicked(self, event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.dir_bubble_extended.setVisible(False)
        self.single_bubble_extended.setVisible(False)
    
    def select_file(self):
        fileName, _ =QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","All Files (*);;JPEG (*.jpeg);;JPG (*.jpg);;PNG(*.png)")
        if fileName:
            self.image_path.setText(fileName)
            if not fileName.endswith(self.file_extensions):
                    self.statusBar().showMessage("Message: Choose an valid Image")
                    return
            image=Image.open(fileName)
            self.image_width=image.width
            self.compress_width=int(self.image_width)
            self.single_quality_path.setText(str(self.image_width))
    
    def select_source_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Select Directory")
        self.source_path.setText(folder)

        files=os.listdir(folder)
        first_pic=folder+"/"+files[0]
        img=Image.open(first_pic)
        self.image_width=img.width
        self.compress_width=self.image_width
        self.dir_quality_path.setText(str(self.image_width))
        
    def select_des_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Select Directory")
        self.des_path.setText(folder)

    def single_quality_current_value(self):
        if self.single_quality_combo.currentText()=="High":
            self.single_quality_path.setText(str(self.image_width))
            self.compress_width=int(self.image_width)
        elif self.single_quality_combo.currentText()=="Medium":
            self.single_quality_path.setText(str(int(self.image_width/2)))
            self.compress_width=int(self.image_width/2)
        else:
            self.single_quality_path.setText(str(int(self.image_width/4)))
            self.compress_width=int(self.image_width/4)
    
    def dir_quality_current_value(self):
        if self.dir_quality_combo.currentText()=="High":
            self.dir_quality_path.setText(str(self.image_width))
            self.compress_width=int(self.image_width)
        elif self.dir_quality_combo.currentText()=="Medium":
            self.dir_quality_path.setText(str(int(self.image_width/2)))
            self.compress_width=int(self.image_width/2)
        else:
            self.dir_quality_path.setText(str(int(self.image_width/4)))
            self.compress_width=int(self.image_width/4)

    def single_compress_clicked(self):
        old_pic=self.image_path.text()
        if old_pic=="":
            self.statusBar().showMessage("Message: Choose an Image")
            return
        if not old_pic.endswith(self.file_extensions):
            self.statusBar().showMessage("Message: Choose an valid Image")
            return
        directories=old_pic.split("/")
        #print(directories[-1])
        new_pic_name=directories[-1]
        #directories[:-1]
        new_pic=""
        for directory in directories[:-1]:
            new_pic=new_pic+directory+"/"
        new_pic=new_pic+self.out_directory
        if not os.path.exists(new_pic):
            os.makedirs(new_pic)
        new_pic=new_pic+'/'+new_pic_name

        self.compress_image(old_pic,new_pic,self.compress_width)
        self.statusBar().showMessage("Message: Completed")
    
    def dir_compress_clicked(self):
        directory=self.source_path.text()
        des_directory=self.des_path.text()

        if directory=="" and des_directory=="":
            self.statusBar().showMessage("Message: Select source & destination directory")
            return
        elif directory=="":
            self.statusBar().showMessage("Message: Select source directory")
            return
        elif des_directory=="":
            self.statusBar().showMessage("Message: Select destination directory")
            return

        files=self.get_files_in_directory(directory)
        for file in files:
            img=Image.open(f'{directory}/{file}')
            self.image_width=img.width
            self.dir_quality_path.setText(str(self.image_width))

            old_pic=f'{directory}/{file}'
            new_pic=f'{des_directory}/{file}'
            self.compress_image(old_pic,new_pic,self.compress_width)
        self.statusBar().showMessage("Message: Done")

    def get_files_in_directory(self,directory):
        onlyfiles = [f for f in os.listdir(directory) if isfile(join(directory, f))]
        return [f for f in onlyfiles if f.endswith(self.file_extensions)]

    def compress_image(self, old_pic, new_pic, mywidth):
        try:
            img=Image.open(old_pic)
            wpercent=(mywidth/float(img.size[0]))
            hsize=int((float(img.size[1])*float(wpercent)))
            img=img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
            img.save(new_pic)
        except Exception as e:
            self.statusBar().showMessage("Message: "+str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())