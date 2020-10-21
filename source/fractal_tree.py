
from PIL import Image, ImageDraw, ImageColor
import PySimpleGUI as g
import threading as tr
import numpy as np
import time
import os
#globals
version=" v1.0"
decrese_len = None
decrese_angle = None
len_limit = None
color = 0
line_width = 0
queue = []
image = None
#functions
def branch(x, y, length, angle):
	global queue
	next_x : float = length * np.cos(angle) + x
	next_y : float = length * np.sin(angle) + y
	queue.append((x,y,next_x,next_y))
	if length > len_limit:
		tr.Thread(None, branch, args=(next_x , next_y , length / decrese_len, angle-decrese_angle), daemon=True).start()
		tr.Thread(None, branch, args=(next_x , next_y , length / decrese_len, angle+decrese_angle), daemon=True).start()

def generate_canvas(brush, start_w, start_h, start_len):
	branch(start_w,  start_h, start_len, 3/2*np.pi)
	while True:
		for line in queue:
			brush.line(line, color, line_width)
			queue.remove(line)
		win.Read(timeout=100)
		if not len(queue):
			break

def on_button_click(image, values):
	win["msg"].Update("generating canvas...")
	win.finalize()
	t = time.time()
	try:
		global decrese_len
		decrese_len = float(values["len_dec"])
		global decrese_angle
		decrese_angle = float(values["ang_dec"])
		global len_limit
		len_limit = float(values["len_min"])
		global line_width
		line_width = int(values["line_width"])
		global color
		if values["color"] != '':
			color = ImageColor.getrgb(values["color"])
		print(color)
		generate_canvas(ImageDraw.Draw(image), image.size[0]/2, image.size[1]-100, image.size[1]/6)
		win["msg"].Update(f"Canvas generated in {round(time.time()-t, 2)} seconds")
	except Exception as e:
		win["msg"].Update(str(e))

def save_image(image, path):
	image.save(path+".png")

#gui creation
win = g.Window("Fractal"+version,
[[g.Text("Enter length decrese"), g.InputText("1.25",key="len_dec",size=(10,1)),g.Text("Enter angle decrese"), g.InputText("0.5",key="ang_dec",size=(10,1)),g.Text("Enter min length"), g.InputText("10",key="len_min",size=(10,1))],
[g.Text("Line options :"),g.ColorChooserButton("Choose line color", key="color"),g.Text("Line width"), g.InputText("0",key="line_width",size=(10,1))],
[g.Button("Show",key="enter"),g.SaveAs("Save image", target=(2,2),key="file", file_types=(("png",".png"),), enable_events=True),g.Button("",key="save_image" ,visible=False,enable_events=True),g.Text(key="msg",size=(50,1)),],
[g.Image(key="display", size=(1000,800))]],icon="icon.ico",finalize=True)
#mainloop
while True:
	event, value = win.Read()
	if event == None:
		break
	elif event == "enter":
		try:
			os.remove("./tmp.png")
		finally:
			image = Image.new("RGB", win["display"].Size, color=16777215)
			on_button_click(image, value)
			save_image(image, "./tmp")
			win["display"].Update("tmp.png")
	elif event == 'save_image':
		if image:
			save_image(image, value["file"])
		else:
			win["msg"].Update("No image to save")
win.close()
#poggers

