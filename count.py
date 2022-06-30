import os
import sys
import math
import cv2
import numpy as np
import socket, pickle
from vehicle_counter import VehicleCounter
from f import start_classify,stop_classify
import time
# ============================================================================

##########Sources #########################
#https://github.com/NationalAssociationOfRealtors/VehicleCounting

# Colours for drawing on processed frames
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

#Read one frame of the video to get the scale of the frame
#cap = cv2.VideoCapture('flow.avi')#(URL)
#while True:
#    ret, frame = cap.read()
#    if ret:
#        height = frame.shape[0]
#        length = frame.shape[1]
#        break
#    else:
#        print('no frame')
#cap.release()

#height = frame.shape[0]
#length = frame.shape[1]

# Set the 6 dividers, formed by 1_A and 1_B
#DIVIDER1 = (DIVIDER1_A, DIVIDER1_B) = ((180,480),(180,1))#((length / 3, height), (length / 3, 290))
#DIVIDER2 = (DIVIDER2_A, DIVIDER2_B) = ((int(length / 2), height), (int(length / 2), 290))
#DIVIDER3 = (DIVIDER3_A, DIVIDER3_B) = ((int(length / 3 * 2), height), (int(length / 3 * 2), 290))
#DIVIDER4 = (DIVIDER4_A, DIVIDER4_B) = ((298,274),(355,169))#((length / 6, 250), (length / 6, 140))
#DIVIDER5 = (DIVIDER5_A, DIVIDER5_B) = ((int(length / 3), 250), (int(length / 3), 140))
#DIVIDER6 = (DIVIDER6_A, DIVIDER6_B) = ((int(length / 5 * 4), 250), (int(length / 5 * 4), 140))
#DIVIDER4 = (DIVIDER4_A, DIVIDER4_B) = ((length / 3, 250), (length / 3, 140))
#DIVIDER5 = (DIVIDER5_A, DIVIDER5_B) = ((length / 2, 250), (length / 2, 140))
#DIVIDER6 = (DIVIDER6_A, DIVIDER6_B) = ((length / 3 * 2, 250), (length /3 * 2, 140))

# ============================================================================

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (int(cx), int(cy))

# ============================================================================


def combined_nearby_centroid(centroid_pool):
    centroid_combined = []
    for (i, centroid) in enumerate(centroid_pool):
        flag = 0
        for entry in centroid_combined:
            if centroid in entry:
                flag = 1
                break
        if flag == 0:
            centroid_combined.append([centroid])
        for j in range(i, len(centroid_pool)):
            if abs(centroid[0] - centroid_pool[j][0]) < 100 and abs(centroid[1] - centroid_pool[j][1]) < 40:    
                for entry in centroid_combined:
                    if centroid in entry and centroid_pool[j] not in entry:
                        entry.append(centroid_pool[j])
    return centroid_combined

def detect_vehicles(fg_mask,min,max):

    MIN_CONTOUR_WIDTH = min
    MIN_CONTOUR_HEIGHT = min
    MAX_CONTOUR_WIDTH = max
    MAX_CONTOUR_HEIGHT = max

    # Find the contours of any vehicles in the image
    contours, hierarchy = cv2.findContours(fg_mask
        , cv2.RETR_EXTERNAL
        , cv2.CHAIN_APPROX_SIMPLE)

    matches = []
    centroid_aftercal = []
    for (i, contour) in enumerate(contours):
        #print contours
        (x, y, w, h) = cv2.boundingRect(contour)
        contour_valid = (w*h >= MIN_CONTOUR_WIDTH) and (w*h <= MAX_CONTOUR_WIDTH) #and (h >= MIN_CONTOUR_HEIGHT) and (h <= MAX_CONTOUR_HEIGHT)

        if not contour_valid:
            continue

        centroid = get_centroid(x, y, w, h)

        matches.append(centroid)
    #print(matches)
    centroid_combined = combined_nearby_centroid(matches)
    for entry in centroid_combined:
                tempx = []
                tempy = []
                for centroid in entry:
                    tempx.append(centroid[0])
                    tempy.append(centroid[1])
                centroid_aftercal.append((sum(tempx) / len(tempx), sum(tempy) / len(tempy)))
    return centroid_aftercal,[0,1,0,0]

# ============================================================================

def filter_mask(fg_mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Fill any small holes
    closing = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    #opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    # Dilate to merge adjacent blobs
    dilation = cv2.dilate(opening, kernel, iterations = 2)

    return dilation

# ============================================================================

def process_frame(frame, bg_subtractor, car_counter,min,max,d1,d2,d3,d4,d5,d6):

    # Create a copy of source frame to draw into
    processed = frame.copy()

    # Draw dividing line -- we count cars as they cross this line.
    cv2.line(processed, d1[0], d1[1], DIVIDER_COLOUR, 1)
    cv2.line(processed, d2[0], d2[1], DIVIDER_COLOUR, 1)
    cv2.line(processed, d3[0], d3[1], DIVIDER_COLOUR, 1)
    cv2.line(processed, d4[0], d4[1], DIVIDER_COLOUR, 1)
    cv2.line(processed, d5[0], d5[1], DIVIDER_COLOUR, 1)
    cv2.line(processed, d6[0], d6[1], DIVIDER_COLOUR, 1)

    # Remove the background
    fg_mask = bg_subtractor.apply(frame, None, 0.01)
    fg_mask = filter_mask(fg_mask)

    matches,v_class = detect_vehicles(fg_mask,min,max)

    for (i, match) in enumerate(matches):
        


        centroid = match

        # Mark the bounding box and the centroid on the processed frame
        # NB: Fixed the off-by one in the bottom right corner
        #cv2.rectangle(processed, (x, y), (x + w - 1, y + h - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(processed, (int(centroid[0]),int(centroid[1])), 2, CENTROID_COLOUR, -1)

    car_counter.update_count(matches,frame,max, processed)

    return processed
    #return fg_mask
# ============================================================================

def count(vid,start,end,d1,d2,d3,d4,d5,d6,s,min,max):
    bg_subtractor = cv2.createBackgroundSubtractorMOG2() #cv2.BackgroundSubtractorMOG()


    car_counter = None # Will be created after first frame is captured

    # Set up image source
    current_counts=[0,0,0,0,0,0]

    cap = cv2.VideoCapture(vid)
    #cap = cv2.VideoCapture(URL)
    #fps =cap.get(cv2.CAP_PROP_FPS)

    #N_Frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)




    cap.set(cv2.CAP_PROP_POS_MSEC, start*1000);

    while cap.get(cv2.CAP_PROP_POS_MSEC)<end*1000:

        ret, frame = cap.read()

        if not ret:

            print('failed')
            start_classify()
            from model import AlexNet
            model = AlexNet()
            model.loadmodel()
            if len(car_counter.vehicle_count1)>0:
                output1 = model.predict(np.reshape(car_counter.vehicle_count1,(len(car_counter.vehicle_count1),224,224,3)))
                output1=np.sum(output1,axis=0)
            else:
                output1=np.zeros([11])
            if len(car_counter.vehicle_count2) > 0:
                output2 = model.predict(np.reshape(car_counter.vehicle_count2, (len(car_counter.vehicle_count2), 224, 224, 3)))
                output2 = np.sum(output2, axis=0)
            else:
                output2=np.zeros([11])
            if len(car_counter.vehicle_count3) > 0:
                output3 = model.predict(np.reshape(car_counter.vehicle_count3, (len(car_counter.vehicle_count3), 224, 224, 3)))
                output3 = np.sum(output3, axis=0)
            else:
                output3=np.zeros([11])
            if len(car_counter.vehicle_count4) > 0:
                output4 = model.predict(np.reshape(car_counter.vehicle_count4, (len(car_counter.vehicle_count4), 224, 224, 3)))
                output4 = np.sum(output4, axis=0)
            else:
                output4=np.zeros([11])
            if len(car_counter.vehicle_count5) > 0:
                output5 = model.predict(np.reshape(car_counter.vehicle_count5, (len(car_counter.vehicle_count5), 224, 224, 3)))
                output5 = np.sum(output5, axis=0)
            else:
                output5=np.zeros([11])
            if len(car_counter.vehicle_count6) > 0:
                output6 = model.predict(np.reshape(car_counter.vehicle_count6, (len(car_counter.vehicle_count6), 224, 224, 3)))
                output6 = np.sum(output6, axis=0)
            else:
                output6=np.zeros([11])
            model.distroy()
            del model, AlexNet
            stop_classify()
            print([output1,output2,output3,output4,output5,output6])
            return [output1,output2,output3,output4,output5,output6]

            #break
        else:
            if car_counter is None:
                # We do this here, so that we can initialize with actual frame size
                #car_counter = VehicleCounter(frame.shape[:2], frame.shape[1] / 2)
                car_counter = VehicleCounter(frame.shape[:2], d1, d2, d3, d4, d5, d6)
                yes=True
                #print frame.shape
            # Archive raw frames from video to disk for later inspection/testing

            processed = process_frame(frame, bg_subtractor, car_counter,min,max,d1,d2,d3,d4,d5,d6)

            #cv2.imshow('Source Image', frame)
            #cv2.imshow('Processing Segment ('+str(s)+')', processed)
            current_counts = [len(car_counter.vehicle_count1),len(car_counter.vehicle_count2),len(car_counter.vehicle_count3),len(car_counter.vehicle_count4),len(car_counter.vehicle_count5),len(car_counter.vehicle_count6)];
            #data Transmissin
            try:
                if cap.get(cv2.CAP_PROP_POS_MSEC)%1000<1 or yes :


                    yes=False
                    data =str(s) + '|Count'+str(current_counts)+'|' + str((cap.get(cv2.CAP_PROP_POS_MSEC) - start * 1000) / 1000) + '|' + str(
                                cap.get(cv2.CAP_PROP_POS_MSEC))


                    # Create an instance of ProcessData() to send to server.

                    # Pickle the object and send it to the server
                    data_string = pickle.dumps(data)
                    print(len(data_string))


                    HOST = 'localhost'
                    PORT = 50008
                    # Create a socket connection.
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    soc.connect((HOST, PORT))

                    soc.send(str(data).encode())
                    msg = soc.recv(4096).decode()
                    if msg=='stop':
                        return

            except:
                print("No Connection")

            cv2.waitKey(1)


    cap.release()
    cv2.destroyAllWindows()
    #print(current_counts)
    start_classify()
    from model import AlexNet
    model = AlexNet()
    model.loadmodel()
    if len(car_counter.vehicle_count1) > 0:
        output1 = model.predict(np.reshape(car_counter.vehicle_count1, (len(car_counter.vehicle_count1), 224, 224, 3)))
        output1 = np.sum(output1, axis=0)
    else:
        output1 = np.zeros([11])
    if len(car_counter.vehicle_count2) > 0:
        output2 = model.predict(np.reshape(car_counter.vehicle_count2, (len(car_counter.vehicle_count2), 224, 224, 3)))
        output2 = np.sum(output2, axis=0)
    else:
        output2 = np.zeros([11])
    if len(car_counter.vehicle_count3) > 0:
        output3 = model.predict(np.reshape(car_counter.vehicle_count3, (len(car_counter.vehicle_count3), 224, 224, 3)))
        output3 = np.sum(output3, axis=0)
    else:
        output3 = np.zeros([11])
    if len(car_counter.vehicle_count4) > 0:
        output4 = model.predict(np.reshape(car_counter.vehicle_count4, (len(car_counter.vehicle_count4), 224, 224, 3)))
        output4 = np.sum(output4, axis=0)
    else:
        output4 = np.zeros([11])
    if len(car_counter.vehicle_count5) > 0:
        output5 = model.predict(np.reshape(car_counter.vehicle_count5, (len(car_counter.vehicle_count5), 224, 224, 3)))
        output5 = np.sum(output5, axis=0)
    else:
        output5 = np.zeros([11])
    if len(car_counter.vehicle_count6) > 0:
        output6 = model.predict(np.reshape(car_counter.vehicle_count6, (len(car_counter.vehicle_count6), 224, 224, 3)))
        output6 = np.sum(output6, axis=0)
    else:
        output6 = np.zeros([11])
    model.distroy()
    del model,AlexNet
    stop_classify()
    print([output1,output2,output3,output4,output5,output6])
    return [output1, output2, output3, output4, output5, output6]

# ============================================================================
class counter:
    def __init__(self):
        self.c =[0,0,0,0,0,0]

    def co(self,v,sss,eee,d1,d2,d3,d4,d5,d6):
        self.c=count(v,sss,eee,d1,d2,d3,d4,d5,d6)


#if __name__ == "__main__":

    #print("final"+str(count("flow.mp4",0,10,DIVIDER1,DIVIDER2,DIVIDER3,DIVIDER4,DIVIDER5,DIVIDER6)))
