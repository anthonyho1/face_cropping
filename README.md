# Face Cropping

Welcome to face cropping. You'll need a few things. First you'll need Python. Both Python 3 and Python 2 will work. Google stuff if you don't have Python to get it. You'll also need git to clone this repository, so also google how to get git. 

Once you have Python, you'll need to download Numpy and OpenCV. Open up your terminal and run the following commands to download these packages (You probably already have pip from the Python installation):
~~~ 
pip install numpy 
pip install opencv-python
~~~
For Python 3, you may have to use "pip3" instead of "pip". Cool! Next we'll have to get this repository onto your computer. In the terminal, type in this command:
~~~
git clone https://github.com/anthonyho1/face_cropping.git
~~~
This will bring the code onto your local computer. Instead of typing out the URL, you can press the green button that says "Clone or download" in Github to copy the URL. 

Next we'll need to run the code. Before you run the code, make a folder somewhere that will end up being the destination folder. It would be a good idea to not use the source folder, as the new images would overwrite the original images. After making the folder, type the following commands into the terminal:
~~~shell
cd ~/face_cropping
python face_crop.py
~~~
The latter line runs the code. The program will prompt you to choose two folders. The first folder you choose is the source folder with the pictures. After choosing this folder, it will prompt you to choose another folder, which will be your destination folder that you just made. It should start running afterwards. The facial detection is based on a simple Haar Cascade using pretrained models provided by OpenCV. The program runs on multiple threads as well, which you can change easily just by changing the constant near the top of the file.

Let me know if there's anything wrong with it.
