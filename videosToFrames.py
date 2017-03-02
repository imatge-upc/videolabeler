'''
This script is intended to generate a set of images corresponding 
to the labels in the database at:

https://github.com/imatge-upc/videolabeler (file drones_labels.zip).


The database consists on 3.313 labels of images taken from different
videos of roads from the point of view of a small commercial drone. 
More information about the database, the labels and how they were 
created can be found at the link above.

This script will read the 9 videos, in .mp4 format, used to create the
database (the links are provided in the github page above), which the 
user should place at the folder ../videos (or change the variable INPUT_PATH 
to point in the right direction). The order of these videos should be the one 
provided in the link above. The corresponding frames of each video will be 
saved in the output path.


'''

import cv2
import glob

# Set the following paths to the correct location of the input videos
# and the output folder where the frames should be written.
INPUT_PATH = '../videos/'
OUTPUT_PATH = '../frames/'

# List all the .mp4 files in the input directory
videosList = sorted(glob.glob(INPUT_PATH + "*.mp4"))

# Define a list of the frame intervals to be extracted from each video. The 
# numbers should be taken as pairs. [a,b,c,d] corresponds to 2 intervals:
# frames from a to b, and frames from c to d.
frames_vid1 = [1878,1908,2505,2555,2918,2948,4768,4798,7118,7158,8509,8528]
frames_vid2 = [841,916,3040,3136,2846,2851,2856,2856,2862,2863,2868,2868,2875, \
               2879,2884,2887,2892,2892,2899,2899,2901,2902,2906,2906,2910,2911,\
               2914,2915,2922,2922,2926,2927,2932,2932,2934,2934,2940,2940,357,\
               436,541,638,640,749,943,1001,1057,1232,1916,2033,3644,3744,3814,\
               3874,3904,4032,4536,4556,4616,4656,5083,5113,5183,5213,5304,5334]
frames_vid3 = [227,257]
frames_vid4 = [2110,2150,2404,2444]
frames_vid5 = [2785,2839,3337,3450,3588,3722,4894,5030]
frames_vid6 = [4299,4329,4673,4703,4956,4986,5026,5036,6711,6741]
frames_vid7 = [1705,1735,1821,1836,2914,2944,3404,3444]
frames_vid8 = [2681,2721,2751,2781]
frames_vid9 = [2,402,809,989,1026,1280,1673,1769]

# Put all the lists of frames in one.
frames = []
frames.append(frames_vid1)
frames.append(frames_vid2)
frames.append(frames_vid3)
frames.append(frames_vid4)
frames.append(frames_vid5)
frames.append(frames_vid6)
frames.append(frames_vid7)
frames.append(frames_vid8)
frames.append(frames_vid9)


num_frame = 0
name_frame=""
# Loop over the 9 videos in the input directory
for i in range(0,9):
    print('Video ' + str(i+1))
    print('Writing frames...')
        
    # Initialize the video
    cap = cv2.VideoCapture(videosList[i])
    
    # Loop over the intervals defined in the corresponding list of frames
    for j in range(0,len(frames[i]),2):

        # Set the video capture variable to the first frame of the interval
        cap.set(1, frames[i][j])
        
        # Loop over the interval
        for k in range(frames[i][j],frames[i][j+1]+1):
            # Read and resize the frame
            ret,frame = cap.read()
            frame = cv2.resize(frame,(480,360))
            
            # Write the frame in the output directory
            name_frame = "%05d" %num_frame;
            cv2.imwrite(OUTPUT_PATH+ str(name_frame) + '.png',frame)
            
            num_frame += 1
    
print('Finished!')