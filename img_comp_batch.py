"""
Created 17. March 2022 by Daniel Van Opdenbosch, Technical University of Munich

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed without any warranty or implied warranty of merchantability or fitness for a particular purpose. See the GNU general public license for more details: <http://www.gnu.org/licenses/>
"""

import glob, os, ray, re, subprocess

numbers=re.compile(r'\d+(?:\.\d+)?')

files=[]
files.append(glob.glob('**/*.bmp',recursive=True))
files.append(glob.glob('**/*.BMP',recursive=True))
files.append(glob.glob('**/*.jpg',recursive=True))
files.append(glob.glob('**/*.JPG',recursive=True))
files.append(glob.glob('**/*.png',recursive=True))
files.append(glob.glob('**/*.PNG',recursive=True))
files.append(glob.glob('**/*.tif',recursive=True))
files.append(glob.glob('**/*.TIF',recursive=True))
files = [y for x in files for y in x]

@ray.remote
def func(i):
	if ' ' in i:
		os.system('mv "'+i+'" "'+i.replace(' ','-')+'"')
		i=i.replace(' ','-')
	if '.bmp' in i:
		os.system('convert "'+i+'" "'+os.path.splitext(i)[0]+'.png"')
		os.system('rm "'+i+'"')
		i=i.replace('.bmp','.png')
	if '.jpg' in i or '.JPG' in i:
		operator='-normalize'
	else:
		operator='-auto-level'
	size=str(subprocess.check_output('identify -format "%wx%h" "'+i+'"',shell=True)).split('x')
	width,height=int(numbers.findall(size[0])[0]),int(numbers.findall(size[1])[0])
	if width>2048 and width>=height:
		os.system('convert "'+i+'" -colorspace RGB -resize 2048x'+str(int(height*width/2048))+'\> '+operator+' "'+i+'"')
	if height>2048 and height>=width:
		os.system('convert "'+i+'" -colorspace RGB -resize '+str(int(height*width/2048))+'x2048\> '+operator+' "'+i+'"')

ray.get([func.remote(i) for i in files])
