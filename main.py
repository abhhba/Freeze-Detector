import os
import pandas as pd
import numpy as np
import math
import sys

filename=sys.argv[1]
labelpath="./results/"+filename+"/labels"
filenum=len(os.listdir(labelpath))
print("Reading labels...")
move_data=[]
for i in range(filenum):
    f = open(labelpath+"\\"+filename+"_croped_"+str(i+1)+".txt",encoding = "utf-8")
    tem=[]
    for i in str(f.read())[:].split(" ")[1:5]:
        tem.append(float(i[:-1]))
    move_data.append(tem)
    f.close()
df=pd.DataFrame(move_data,columns=["x","y","width","height"])
print("Reading labels successful!")
def filter(x):
    x=list(x)
    for i in range(len(x)-1):
        if(i==0):
            pass
        if((abs(x[i+1]-x[i-1])<abs(x[i]-x[i-1])/5)&(abs(x[i]-x[i-1])>0.01)):
            x[i]=x[i-1]
        else:
            pass
    return pd.Series(x)
def filter_zero(x):
    x=list(x)
    for i in range(len(x)-1):
        if(i==0):
            pass
        if(x[i]==0&(abs(x[i-1]-0)>0.01)):
            x[i]=x[i-1]
    return pd.Series(x)
df["x_f"]=filter(df["x"])
df["y_f"]=filter(df["y"])
df["height_f"]=filter(df["height"])
df["width_f"]=filter(df["width"])
df["x_f"]=filter_zero(df["x"])
df["y_f"]=filter_zero(df["y"])
df["height_f"]=filter_zero(df["height_f"])
df["width_f"]=filter_zero(df["width_f"])
move_data_ori=move_data
move_data=df[["x_f","y_f","width_f","height_f"]].to_numpy()
move_value=[]
for i in range(len(move_data)-1):
    x1=move_data[i][0]
    y1=move_data[i][1]
    x2=move_data[i+1][0]
    y2=move_data[i+1][1]
    center_move=math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1))
    line_move_up=y2+move_data[i+1][3]/2-y1-move_data[i][3]/2
    line_move_down=y2-move_data[i+1][3]/2-y1+move_data[i][3]/2
    line_move_left=x2+move_data[i+1][2]/2-x1-move_data[i][2]/2
    line_move_right=x2-move_data[i+1][2]/2-x1+move_data[i][2]/2
    line_move=abs(line_move_down)+abs(line_move_up)+abs(line_move_left)+abs(line_move_right)
    move=abs(center_move)+abs(line_move)
    move_value.append(move)
move_status=[]
for i in range(len(move_value)):
    if(move_value[i]>0.0094):
        move_status.append(1)
        #print(i)
    else:
        move_status.append(0)
map=[]
for i in range(len(move_status)):
    map.append("active")
p=0
q=0
while(q<len(move_status)):
    if(move_status[q]==0):
        if(q-p>=30):
            for i in range(p,q):
                map[i]="freeze"
        q+=1
    else:
        p=q
        q+=1



print("Moving status collected!")
import plotly.io as pio
import plotly.express as px

#fig = px.line(df[["x_f","y_f","height_f","width_f"]],title="Move Value Change")
fig3=px.line(map)
#fig.show()
fig3.show()
sum=0
for i in map:
    if(i=="freeze"):
        sum+=1
print("Freeze time ratio: ",sum/len(map)*100,"%")
import cv2
import numpy as np
import decimal
ctx = decimal.Context()
ctx.prec = 4
def float_to_str(f):
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

# 在视频中插入文字、图片
def video_edit(video_path):
	# 打开视频获取视频信息
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 新建视频
    videoWriter = cv2.VideoWriter(video_path[:-11]+"_result.mp4", cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    # 读取视频
    success, frame = video.read()
    index = 1
    while success:
        if(index==filenum):
            break
        
    	# 为视频添加字幕信息
        #cv2.putText(frame, 'move_value: ' + float_to_str(move_value[index-1]*100), (0, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(frame, 'status: ' + str(map[index-1]), (0, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(frame, 'frame: ' + str(index), (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1)
        #cv2.putText(frame, 'time: ' + str(round(index / 24.0, 2)) + "s", (0,500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 5)
        # cv2.imshow("new video", frame)
        #cv2.waitKey(int(1000 / int(fps)))
        # 添加图片在此增加frame
        videoWriter.write(frame)
        success, frame = video.read()
        index += 1

    video.release()

video_edit("./results/"+filename+"/"+filename+"_croped.mp4")
print("Video has been saved!")
input()
