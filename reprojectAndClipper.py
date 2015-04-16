#!/usr/bin/env python3
import os
import os.path

path = os.getcwd()
path += '/L7'
os.chdir(path)

def reprojectAndClipper(nameFolders):
    for i in range(len(nameFolders)-1):
        if os.path.isfile(nameFolders[i]):
            os.system('rm -R '+nameFolders[i].split('.')[0])
        os.system("mkdir "+nameFolders[i].split('.')[0])
        os.system("tar -xvf "+nameFolders[i]+" -C "+nameFolders[i].split('.')[0])
        nameFiles = os.popen('ls '+nameFolders[i].split('.')[0]+'/*.TIF').read().split("\n")
        for j in range(len(nameFiles)-1):
            os.system('gdalwarp -overwrite -t_srs EPSG:3857 -dstnodata 0 -q -cutline '
            + '../narino/narino_3857_buffer.shp -crop_to_cutline -of GTiff '
	        + nameFiles[j]+' '+nameFiles[j]+'.copy')
            os.system('rm '+nameFiles[j])
            os.system('mv '+nameFiles[j]+'.copy '+nameFiles[j])
        os.system('rm '+nameFolders[i])
        os.chdir(path+'/'+nameFolders[i].split('.')[0])
        os.system('tar -czvf '+nameFolders[i]+' '+'*')
        os.system('mv '+nameFolders[i]+' ../')
        os.system('rm -R ../'+nameFolders[i].split('.')[0])
        os.chdir(path)
                
filterImg = 'LE7*2014*'
nameFolders = os.popen('ls '+filterImg+'bz').read().split("\n")	    

reprojectAndClipper(nameFolders)
