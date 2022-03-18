"""
Created 14. April 2020 by Daniel Van Opdenbosch, Technical University of Munich

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed without any warranty or implied warranty of merchantability or fitness for a particular purpose. See the GNU general public license for more details: <http://www.gnu.org/licenses/>
"""

import os
import glob

files=glob.glob('*.avi')

xsoll=1920
ysoll=1080

for i in files:
	print(i)
	x=int(os.popen("ffmpeg -i "+i+" 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f1").read())
	y=int(os.popen("ffmpeg -i "+i+" 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f2").read())
	if x<xsoll or y<ysoll:
		if '_nopad' not in i:
			os.system("mv "+i+" "+os.path.splitext(i)[0]+"_nopad.avi")
			os.system("ffmpeg -i "+os.path.splitext(i)[0]+"_nopad.avi -vf 'pad=width=1920:height=1080:x="+str(int((xsoll-x)/2))+":y="+str(int((ysoll-y)/2))+":color=white' -qscale 0 "+i)
		else:
			os.system("ffmpeg -i "+i+" -vf 'pad=width=1920:height=1080:x="+str(int((xsoll-x)/2))+":y="+str(int((ysoll-y)/2))+":color=white' -qscale 0 "+os.path.splitext(i)[0].split('_nopad')[0]+".avi")
