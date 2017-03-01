# Spatio-Temporal Road Detection from Aerial Imagery using CNNs

This repository gathers a semi-automatic tool for labelling videos, as well as a labelled database of videos of roads from the point of view of a small commercial drone. The work done is detailed in the article _Spatio-Temporal Road Detection from Aerial Imagery using CNNs_, presented at the VISAPP 2017, the International Conference on Computer Vision Theory and Applications.

The author of this project is [Belén Luque] (https://www.linkedin.com/in/belén-luque-lópez-ab5046bb/), under the supervision of [Javier Ruiz Hidalgo] (https://imatge.upc.edu/web/people/javier-ruiz-hidalgo) and [Josep Ramon Morros] (https://imatge.upc.edu/web/people/josep-ramon-morros).

## Abstract

The main goal of this paper is to detect roads from aerial imagery recorded by drones. To achieve this, we propose a modification of SegNet, a deep fully convolutional neural network for image segmentation. In order to train this neural network, we have put together a database containing videos of roads from the point of view of a small commercial drone. Additionally, we have developed an image annotation tool based on the watershed technique, in order to perform a semi-automatic labeling of the videos in this database. The experimental results using our modified version of SegNet show a big improvement on the performance of the neural network when using aerial imagery, obtaining over 90% accuracy.

## Publication

_To be updated when the link is published_

## Labelling tool

The technical details on how the tool works are detailed in the article mentioned above. To use the labelling tool, follow the instructions in videoLabeler.py and run the script. Note that the numpy and OpenCV libraries are required.

## Database

The labelled database consists on 3.313 images, gathered from snippets of different Youtube videos. These images have been labelled using the developed semi-automatic tool. The results have been supervised and corrected when needed by the author.

The videos used are the following:
* [Video 1] (https://www.youtube.com/watch?v=7ZKsSl5Bxzk)
* [Video 2] (https://www.youtube.com/watch?v=uEkl2M3u4QY)
* [Video 3] (https://www.youtube.com/watch?v=Itas_NSL7k8)
* [Video 4] (https://www.youtube.com/watch?v=5hT6MoJmxNI)
* [Video 5] (https://www.youtube.com/watch?v=KNALyO9zaaA)
* [Video 6] (https://www.youtube.com/watch?v=X2-qVT90lbE)
* [Video 7] (https://www.youtube.com/watch?v=bHV8gidxP-M)
* [Video 8] (https://www.youtube.com/watch?v=oQkOoqHm7O8)
* [Video 9] (https://www.youtube.com/watch?v=75pjRpMBV7A)

A script _will be soon_ provided to obtain the correspondent frames of each video, so the names and ordering of the frames match the labels.

The frames used for each video are:

