### This script labels each frame of one or more videos by 
### extending the markers of the first frame and then using
### the watershedApp technique to segment the image


### USAGE: 
    # 1) Create the labels for the first frame of each video and 
    #    either save these labels with the name of the corresponding video + '_m.png' or change
    #    the way in which the video is retrieved in lines 32-34 
    # 2) Change the paths in lines 17-23 if necessary
    # 3) Select the number of classes in line 31. The labels are assumed to be 1...numClasses 
    #    (i.e. numClasses=3, labels = 1,2,3)
    # 4) Set the 'show' variable to True to show the results in real time. Set the 'save' variable
    #    to true to save the results in the OUTPUT_FRAMES and OUTPUT_LABEL paths
    # 5) Run the script. When the first frame of a video is shown, press any key (except for ESC)
    #    to extend the labels to the rest of the frames. Press ESC to skip to the next video.
    #
    # *** To re-label a frame in the middle of a video and extend the markers from that point:
    # - Set the reLabel variable to True. 
    # - Set the video of the frame to modify (number) -> firstvideo
    # - Set the frame to modify (number in the name of the saved frame in the images folder) -> firstframe
    # - Set how many frames in the video have to be skipped (different from 'firstframe' when more 
    # than one video is being labeled) -> framestoskip


import glob
import numpy as np
import cv2
import watershedApp

#Folder containing the labels of the first frame of each video 
fileList = sorted(glob.glob("../FirstLabel/*png"))
#Folder containing the videos to segment
VIDEOS_PATH = '../videos'

#Folders where the output frames and labels will be saved 
OUTPUT_FRAMES = '../images/'
OUTPUT_LABELS = '../labels/'

#Set to True or False to show/save the output 
show = True
save = True

#Change number of classes if necessary. 
numClasses = 3

reLabel = False
firstvideo = 0
firstframe = 0
framestoskip = 0

j=firstframe;
firstloop = True
for i in range(firstvideo,fileList.__len__()):

    print 'Video number ' + str(i)
    
    #Get video with the same name as the image with the labels of the first frame
    pieces = fileList[i].split('/FirstLabel')
    pieces1 = pieces[1].split('_m.png')
    videopath = VIDEOS_PATH + pieces1[0] + '.avi'    
    print 'Video path: ' + videopath
    
    cap = cv2.VideoCapture(videopath)
        
    if (reLabel == False) or (firstloop==False):
            
        #Get the first frame
        ret,frame = cap.read()
        
        #Read image with the labels of the first frame
        firstLabels = cv2.imread(fileList[i])
        
        #Initialize markers with the labels
        height, width = frame.shape[:2]
        markers = np.zeros((height,width), np.int32)
        markers[firstLabels[:,:,0]==-1] = -1
        for i in range(1,numClasses+1):   
            markers[firstLabels[:,:,0]==i] = i
    
    else:
        firstloop=False
        num = "%05d" %firstframe;
        frameToLabel = OUTPUT_FRAMES + str(num) + '.png'
        markers = watershedApp.App(frameToLabel).run()
        
        ret,frame = cap.read()
        for i in range(0,framestoskip):
            ret,frame = cap.read()
            
        height, width = frame.shape[:2]
        
    
    #Create a mask for each segmented class 
    masks = []
    for i in range(1,numClasses+1):  
        mask = np.zeros([height,width,1], np.uint8)
        mask[markers==i] = 255
        masks.append(mask)

    
    #Create a histogram of each region in the image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi_hists = []
    for i in range(0,numClasses):
        roi_hist = cv2.calcHist([hsv],[0],masks[i],[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        roi_hists.append(roi_hist)

    
    #Apply watershedApp to the frame, using the markers
    cv2.watershed(frame, markers)
    #Color the result
    colors = np.int32( list(np.ndindex(2, 2, 2)) ) * 255
    overlay = colors[np.maximum(markers, 0)]
    vis = cv2.addWeighted(frame, 0.5, overlay, 0.5, 0.0, dtype=cv2.CV_8UC3)
    
    #Variable to visualize the markers in an easier way
    ma=frame.copy()
    ma[:] = (255,255,255)
    for i in range(0,numClasses+1):
        ma[markers==i] = colors[i]


    if show == True:
        cv2.namedWindow('markers', cv2.WINDOW_NORMAL)
        cv2.moveWindow('markers',0,0)
        cv2.imshow('markers', ma) 
        cv2.namedWindow('watershedApp', cv2.WINDOW_NORMAL)
        cv2.moveWindow('watershedApp',480,0)
        cv2.imshow('watershedApp', vis) 
        k = cv2.waitKey(0) & 0xff 
        if k == 27:
            break
    
    #Read next frame
    ret ,frame = cap.read()
    
    if save == True:
        jj = "%05d" %j;
        cv2.imwrite(OUTPUT_FRAMES+ str(jj) + '.png',frame)
        cv2.imwrite(OUTPUT_LABELS+ 'm' + str(jj) + '.png',markers)
        
    #Do the loop for the rest of the video
    while(ret == True):
        j=j+1
    
        if save == True:
            jj = "%05d" %j;
            cv2.imwrite(OUTPUT_FRAMES + str(jj) + '.png',frame)
    
        #Convert frame to HSV color space and compute the histogram backprojection of each region
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        probabilities = []
        for i in range(0,numClasses):
            prob = cv2.calcBackProject([hsv],[0],roi_hists[i],[0,180],1)
            
            #Smooth the probability regions
            prob = cv2.medianBlur(prob,11)
            
            if show==True:
                cv2.namedWindow('Class ' + str(i+1) + ' probabilities', cv2.WINDOW_NORMAL)
                cv2.moveWindow('Class ' + str(i+1) + ' probabilities',i*480,400)
                cv2.imshow('Class ' + str(i+1) + ' probabilities', prob)
                    
            #Group probabilities in 3 classes
                # -> 0 The pixel sure doesn't belong to the class
                # -> 100 Uncertainty zone
                # -> 255 The pixel sure belongs to the class              
            aux = np.zeros(prob.shape, dtype=np.uint8)
            aux[(prob>0)]=100
            aux[(prob>50)]=255
            
            #Set the markers of the class, only if the pixel was also previously classified as this class, to avoid spurious classifications 
            aux[markers!=(i+1)] = 0
            
            probabilities.append(aux)
    
    
        #Dilate the limits of the regions, to create an uncertainty zone around them
        dilation = np.zeros([height, width])
        dilation[:] = 0
        dilation[markers==-1] = 255        
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        cv2.filter2D(dilation,-1,disc,dilation)
        

        #Set the markers for the new watershedApp
        markers[:]=0
        for i in range(0,numClasses):
            markers[probabilities[i]==255]=i+1 
            
        #Remove the markers in the limits between regions
        markers[dilation==255]=0 
        
                
        #Variable to visualize the markers in an easier way
        ma[:] = (255,255,255)
        for i in range(0,numClasses+1):
            ma[markers==i] = colors[i]

        if show == True:
            cv2.imshow('markers', ma) 

        #Apply watershedApp to the frame, using the markers
        cv2.watershed(frame, markers)
        
        #Color the result
        overlay = colors[np.maximum(markers, 0)]
        vis = cv2.addWeighted(frame, 0.5, overlay, 0.5, 0.0, dtype=cv2.CV_8UC3)
        
        if show == True:
            cv2.imshow('watershedApp', vis) 
        
        
        #Create a mask for each segmented class 
        masks = []
        for i in range(1,numClasses+1):  
            mask = np.zeros([height,width,1], np.uint8)
            mask[markers==i] = 255
            masks.append(mask)
    
        #Recompute the histograms of the regions
        roi_hists = []
        for i in range(0,numClasses):
            roi_hist = cv2.calcHist([hsv],[0],masks[i],[180],[0,180])
            cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
            roi_hists.append(roi_hist)
         
        if show == True:
            k = cv2.waitKey(30) & 0xff 
            #If ESC is pressed, goes into the next video
            if k == 27:
                break
        if save == True:
            cv2.imwrite(OUTPUT_LABELS + 'm' + str(jj) + '.png',markers)
        
        ret,frame = cap.read() 
        
    cv2.destroyAllWindows()

    
    
    
