"""
Created 18. March 2022 by Daniel Van Opdenbosch, Technical University of Munich

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed without any warranty or implied warranty of merchantability or fitness for a particular purpose. See the GNU general public license for more details: <http://www.gnu.org/licenses/>
"""

import numpy
import glob
import os
import ray
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import fftpack
from PIL import Image,ImageOps

imgfiles=glob.glob('**/*.JPG',recursive=True)

@ray.remote
def fft(imgfile):
	filename=os.path.splitext(imgfile)[0]

	fft=numpy.fft.fftshift(numpy.fft.fft2(ImageOps.grayscale(Image.open(imgfile))))
	indx,indy=numpy.indices(numpy.shape(fft))
	maxdist=min([max(indx.flatten()-numpy.median(indx)),max(indy.flatten()-numpy.median(indy))])

	s=numpy.linalg.norm([indx.flatten()-numpy.median(indx),indy.flatten()-numpy.median(indy)],axis=0)
	i=abs(fft).flatten()

	S=numpy.arange(1,maxdist)
	I=numpy.zeros(S.size)

	for n,valuen in enumerate(S):
		lowbound=valuen-numpy.diff(S)[0]/2
		highbound=valuen+numpy.diff(S)[0]/2
		I[n]=numpy.sum(i[numpy.where((s>lowbound)&(s<highbound))])/((highbound**2-lowbound**2)*numpy.pi)

	R=numpy.fft.rfftfreq(2*S.size,d=1/(2*max(S)))[1:]
	G=2/numpy.pi*fftpack.dst(S*(I-1))

	plt.clf()
	plt.imshow(numpy.log(abs(fft)),cmap='coolwarm')
	plt.savefig(filename+'_fft.png')

	numpy.save(filename+'.npy',[S,I,R,G])

ray.get([fft.remote(imgfile) for imgfile in imgfiles])

G_Zyklus_0=numpy.array([])
G_Zyklus_5=numpy.array([])

for imgfile in imgfiles:
	filename=os.path.splitext(imgfile)[0]

	S,I,R,G=numpy.load(filename+'.npy',allow_pickle=True)

	if 'Zyklus_0' in filename:
		G_Zyklus_0=numpy.append(G_Zyklus_0,G)
	elif 'Zyklus_5' in filename:
		G_Zyklus_5=numpy.append(G_Zyklus_5,G)

	plt.clf()
	plt.plot(S,I)
	plt.yscale('log')
	plt.xlabel('S/pixels^-1')
	plt.ylabel('I/1')
	plt.savefig(filename+'_S-I.png')
	numpy.savetxt(filename+'_S-I.dat',numpy.array([S,I]).transpose())

	plt.clf()
	plt.plot(R,G)
	plt.yscale('log')
	plt.xlabel('R/pixels')
	plt.ylabel('G/pixels^-2')
	plt.savefig(filename+'_R-G.png')
	numpy.savetxt(filename+'_R-G.dat',numpy.array([R,G]).transpose())

G_Zyklus_0=numpy.average(G_Zyklus_0.reshape(-1,len(R)),axis=0)
G_Zyklus_5=numpy.average(G_Zyklus_5.reshape(-1,len(R)),axis=0)

Rdiff,Gdiff=[R,G_Zyklus_5/G_Zyklus_0-1]
numpy.savetxt('diff.dat',numpy.array([Rdiff,Gdiff]).transpose())

plt.clf()
plt.plot(Rdiff,Gdiff)
plt.xlabel('R/pixels')
plt.ylabel('G/G/1')
plt.savefig('G_Zyklus_diff.png')
