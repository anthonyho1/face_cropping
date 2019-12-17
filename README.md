# Face Cropping

Welcome to face cropping. You'll need a few things. First you'll need Python 3. It may or may not work with Python 2.7+, but I wrote it all in Python 3 and have not tested it with older versions. Google stuff if you don't have Python to get it. 

Once you have Python, you'll need to download Numpy and OpenCV. Open up your terminal and run the following commands to download these packages (You probably already have pip from the Python instillation):
~~~
pip install numpy
pip install opencv-python
~~~

Cool! Next we'll have to get this repository onto your computer. In the terminal, type in this command:
~~~
git clone https://github.com/anthonyho1/face_cropping.git
~~~
This will bring the code onto your local computer. Instead of typing it out you can press the green button that says "Clone or download" in Github to copy and paste the code. 

Next we'll need to run the code. Before you run the code, make a folder somewhere that will end up being the destination folder. After making the folder, type the following command into the terminal:
~~~
cd face_cropping
python face_crop.py
~~~
The latter line runs the code. The program will prompt you to choose a folder. The first folder you choose is the source folder with the pictures. After choosing a folder, it will prompt you to choose another folder, which will be your destination folder that you just made. It should start running afterwards.

I am still working on the bugs so let me know if there's anything of concern.
