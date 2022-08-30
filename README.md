# Freeze-Detector
Using YOLOv5 to track rats and automatic count freeze in rats

#How to use？
i. Install Anaconda.
ii.Open Anaconda cmd and enter the path of this software.
iii.Create environment by typing "conda create -f environment.yml".
iv."conda activate freeze"
v."python detect_ori.py --weights ./best.onnx --source ./input/xxx.mp4 --save-txt --max-det 1"
vi."python main.py xxx"
Results will be found in results/xxx.
