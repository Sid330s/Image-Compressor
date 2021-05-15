import os
import sys
from importlib import reload
reload(sys)
#sys.setdefaultencoding('utf8')
import txttoimg
from flask import Flask,render_template,request,redirect,send_from_directory,make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
app=Flask(__name__)
s=dict()
p=dict()
dtbw=[]
l=[]
size=tuple()
def bitstring_to_bytes(s):
	s='1'+s;
	return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

get_bin = lambda x, n: format(x, 'b').zfill(n)

def imgtotxt(str1):
	from PIL import Image
	from collections import Counter
	im=Image.open(str1).convert('P')
	data=list(im.getdata())
	counts=Counter(data)
	global l
	l=[str(i) for i in data]
	global size
	size=im.size
	print(str(im.size[0]))
	print(str(im.size[1]))
	f=open('test2.txt','w')
	data=list(set(data))
	for i in data:
		f.write(str(i)+','+str(counts[i])+'\n')

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html',u="Upload Image",c="COMPRESS!",ul='/compressed')

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		f = request.files['fileToUpload']
		imgname=secure_filename(f.filename)
		f.save(imgname)
		imgtotxt(imgname)
		return render_template('index.html',u="Image Uploaded!",l="Upload Text")

@app.route('/compressed',methods=['GET','POST'])
def compress():
	if request.method=='POST':
		os.system('gcc huffman.c')
		print("hi")
		v=os.popen('a.exe')
		v=v.read().split('\n')
		v=v[:len(v)-1]
		keys,data=[int(i.split(': ')[0]) for i in v],[i.split(': ')[1] for i in v]
		global s
		global p
		print(s)
		s=dict(zip(keys,data))
		p=dict(zip(data,keys))
		for i in l:
			try:
				dtbw.append(s[int(i)])
			except:
				dtbw.append(i)
		compression=""
		for i in dtbw:
			compression+=i
		print(size[0])
		print(size[1])
		x=str(get_bin(int(size[0]),32))
		y=str(get_bin(int(size[1]),32))
		print(x)
		print(y)
		compression=x+y+compression
		print(len(compression))
		file = open("compressed.bin", "wb")
		file.write(bitstring_to_bytes(compression))
		print(compression)
		response=make_response(send_from_directory('.','compressed.bin'))
		response.headers["Content-Disposition"]="attachment; filename=compressed.bin"
		os.system('rm compressed.txt')
		return response
		#return render_template('index.html',u="Image Uploaded!",c="DECOMPRESS!",ul='/decompressed')
	return "TEEHEE"

@app.route('/decomupload',methods=['GET','POST'])
def decom():
	if request.method=='POST':
		f = request.files['txtToUpload']
		txtname=secure_filename(f.filename)
		f.save(txtname)
		return render_template('index.html',u="Image Uploaded!",l="Text Uploaded!")

@app.route('/decompressed',methods=['GET','POST'])
def decompress():
	if request.method=='POST':
		global s
		global p
		d=[]
		with open('compressed.bin','rb') as file:
			byte = file.read()
			print("yy")
			compression=str(bin(int.from_bytes(byte, byteorder="big")))[3:]
			print(len(compression))
			x = int(compression[:32],2)
			y = int(compression[32:64],2)
			compression=compression[64:]
			size=(x,y)
			print(size)
			print(p)
			i=0
			for j in range(len(compression)):
				temp = p.get(compression[i:j+1],-1)
				if(temp!=-1):
					d.append(str(temp)+'\n')
					i=j+1
			d.append(str(size))
			open('decompressed.txt','w').writelines(d)
			txttoimg.txttoimg('decompressed.txt')
			response=make_response(send_from_directory('.','test.jpg'))
			response.headers["Content-Disposition"]="attachment; filename=your_image.jpg"
			return response
		return "Heyy"
	return "TEEHEE"
if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000)
