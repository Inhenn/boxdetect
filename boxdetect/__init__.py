from numpy.linalg import inv
import cv2
import numpy as np
import math


def cross_point(tuple1,tuple2):
    (x1, y1, x2, y2)=tuple1
    (x3, y3, x4, y4)=tuple2
    A=np.matrix([[(y1-y2),(x2-x1)],[(y3-y4),(x4-x3)]])
    B=np.matrix([[x1*(y1-y2)+y1*(x2-x1)],[x3*(y3-y4)+y3*(x4-x3)]])
    try:
        A_inv=inv(A)
        X=np.dot(A_inv,B)
        return X
    except:
        return 0


def cosine_formula(tuple1,tuple2):
    try:
        (x0,y0)=cross_point(tuple2,tuple1)
        x0,y0=(float(x0),float(y0))
        x1,y1,g,g=tuple1
        x2,y2,g,g=tuple2
        c=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        a=math.sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))
        b=math.sqrt((x2-x0)*(x2-x0)+(y2-y0)*(y2-y0))
        cosC=(a*a+b*b-c*c)/(2*a*b)
        C=math.acos(abs(cosC))
        return C*360/(2*math.pi)
    except:
        return 0


def perpendicular(tuple1, tuple2,accuracy):
    if abs(cosine_formula(tuple1,tuple2)-90)<accuracy:
        return 1
    else:
        return 0


def img_percent(img, x, height):
    (h, w) = img.shape
    if height == 1:
        return int(x * h)
    else:
        return int(x * w)


def edge_line(img, num_lines,base_w,base_h,linelength,accuracy):

    line_list = []
    edges = cv2.Canny(img, 100, 200, apertureSize=3)
    lines = cv2.HoughLines(edges, linelength, np.pi / (accuracy*360), 200)
    for i in range(0, num_lines, 1):
        for rho, theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            (x1, y1, x2, y2) = (max(0, x1), max(0, y1), max(0, x2), max(0, y2))
            line_list += [(x1+base_w, y1+base_h, x2+base_w, y2+base_h)]
            # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)
    return line_list


def image_selected(img, x1, x2, y1, y2):
    w1 = img_percent(img, x1, 0)
    w2 = img_percent(img, x2, 0)
    h1 = img_percent(img, y1, 1)
    h2 = img_percent(img, y2, 1)
    new_img = img[h1:h2, w1:w2]
    return new_img


def frame(tuple1,tuple2,tuple3,tuple4,accuracy):
    if (perpendicular(tuple1, tuple2,accuracy)+perpendicular(tuple1, tuple3,accuracy)+perpendicular(tuple1, tuple4,accuracy)
        +perpendicular(tuple2, tuple3,accuracy)+perpendicular(tuple2, tuple4,accuracy)+perpendicular(tuple3, tuple4,accuracy)
        ==4):

        return (abs(cosine_formula(tuple1, tuple2) - 90)+abs(cosine_formula(tuple1, tuple3) - 90)+
               abs(cosine_formula(tuple1, tuple4) - 90)+abs(cosine_formula(tuple2, tuple3) - 90)+
                abs(cosine_formula(tuple2, tuple4) - 90)+abs(cosine_formula(tuple3, tuple4) - 90)-180)
    else:
        return 0


def vector_percent(a,b,x):
    return (a+(b-a)*x)


def box_vertex(img, left_x1, left_x2, left_y1, left_y2, top_x1, top_x2, top_y1, top_y2, right_x1, right_x2, right_y1,
             right_y2, bot_x1,
             bot_x2, bot_y1, bot_y2, line_num=None, left_length=None, right_length=None, top_length=None,
             bot_length=None, accuracy=None):
    if line_num is None:
        line_num = 5
    if left_length is None:
        left_length = 2
    if right_length is None:
        right_length = 2
    if top_length is None:
        top_length = 2
    if bot_length is None:
        bot_length = 2
    if accuracy is None:
        accuracy = 4
    # img = cv2.imread('image-10.png', 0)
    (h, w) = img.shape

    img1 = image_selected(img, left_x1, left_x2, left_y1, left_y2)
    left = edge_line(img1, line_num, int(left_x1 * w), int(left_y1 * h), left_length, accuracy)
    # for element in left:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img2 = image_selected(img, top_x1, top_x2, top_y1, top_y2)
    top = edge_line(img2, line_num, int(top_x1 * w), int(top_y1 * h), right_length, accuracy)
    # for element in top:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img3 = image_selected(img, bot_x1, bot_x2, bot_y1, bot_y2)
    bot = edge_line(img3, line_num, int(bot_x1 * w), int(bot_y1 * h), top_length, accuracy)
    # for element in bot:
    #
    #     cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)

    img4 = image_selected(img, right_x1, right_x2, right_y1, right_y2)
    right = edge_line(img4, line_num, int(right_x1 * w), int(right_y1 * h), bot_length, accuracy)
    # for element in right:
    #
    # cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)
    frame_list=[]
    accuracy_list=[]
    for t in top:
        for l in left:
            for r in right:
                for b in bot:
                    if frame(t,l,r,b,0.01)!=0:
                        accuracy_list+=[frame(t,l,r,b,0.01)]
                        frame_list+=[(t,l,r,b)]
                        # print((t,l,r,b))

    min_value=10000
    location_key=0
    try:
        for i in range(0,len(accuracy_list),1):
            if accuracy_list[i]<min_value:
                min_value=accuracy_list[i]
                location_key=i


        best_frame=frame_list[location_key]
        # print(frame_list)
        (xa, ya) =cross_point(best_frame[0],best_frame[1])
        (xb, yb) =cross_point(best_frame[0], best_frame[2])
        (xc, yc) =cross_point(best_frame[3], best_frame[2])
        (xd, yd) =cross_point(best_frame[3], best_frame[1])
        xa,ya,xb,yb,xc,yc,xd,yd = int(xa),int(ya),int(xb),int(yb),int(xc),int(yc),int(xd),int(yd)
        return (xa,ya,xb,yb,xc,yc,xd,yd)
    except:
        print("detection failed, please try more lines")
        return 0

def box_draw(img,left_x1,left_x2,left_y1,left_y2,top_x1,top_x2,top_y1,top_y2,right_x1,right_x2,right_y1,right_y2,bot_x1,
             bot_x2,bot_y1,bot_y2,line_num=None,left_length=None,right_length=None,top_length=None,bot_length=None,accuracy=None):
    if line_num is None:
        line_num=5
    if left_length is None:
        left_length=2
    if right_length is None:
        right_length=2
    if top_length is None:
        top_length = 2
    if bot_length is None:
        bot_length = 2
    if accuracy is None:
        accuracy = 4
    # img = cv2.imread('image-10.png', 0)
    (h,w)=img.shape

    img1=image_selected(img,left_x1,left_x2,left_y1,left_y2)
    left=edge_line(img1,line_num,int(left_x1*w),int(left_y1*h),left_length,accuracy)
    # for element in left:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img2=image_selected(img,top_x1,top_x2,top_y1,top_y2)
    top=edge_line(img2,line_num,int(top_x1*w),int(top_y1*h),right_length ,accuracy)
    # for element in top:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img3=image_selected(img,bot_x1,bot_x2,bot_y1,bot_y2)
    bot = edge_line(img3, line_num, int(bot_x1*w), int(bot_y1 * h), top_length,accuracy)
    # for element in bot:
    #
    #     cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)

    img4 = image_selected(img, right_x1, right_x2, right_y1, right_y2)
    right = edge_line(img4, line_num, int(right_x1 * w), int(right_y1 * h), bot_length,accuracy)
    # for element in right:
    #
    #      cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)
    frame_list=[]
    accuracy_list=[]
    for t in top:
        for l in left:
            for r in right:
                for b in bot:
                    if frame(t,l,r,b,0.01)!=0:
                        accuracy_list+=[frame(t,l,r,b,0.01)]
                        frame_list+=[(t,l,r,b)]
                        # print((t,l,r,b))

    min_value=10000
    location_key=0
    try:
        for i in range(0,len(accuracy_list),1):
            if accuracy_list[i]<min_value:
                min_value=accuracy_list[i]
                location_key=i


        best_frame=frame_list[location_key]
        # print(frame_list)
        (xa, ya) =cross_point(best_frame[0],best_frame[1])
        (xb, yb) =cross_point(best_frame[0], best_frame[2])
        (xc, yc) =cross_point(best_frame[3], best_frame[2])
        (xd, yd) =cross_point(best_frame[3], best_frame[1])
        xa,ya,xb,yb,xc,yc,xd,yd = int(xa),int(ya),int(xb),int(yb),int(xc),int(yc),int(xd),int(yd)
        cv2.line(img, (xa, ya), (xb, yb), (0, 0, 0), 3)
        cv2.line(img, (xb, yb), (xc, yc), (0, 0, 0), 3)
        cv2.line(img, (xc, yc), (xd, yd), (0, 0, 0), 3)
        cv2.line(img, (xd, yd), (xa, ya), (0, 0, 0), 3)
    except:
        print("detection failed, please try more lines")
        return 0

def box_crop(img, left_x1, left_x2, left_y1, left_y2, top_x1, top_x2, top_y1, top_y2, right_x1, right_x2, right_y1,
             right_y2, bot_x1,
             bot_x2, bot_y1, bot_y2, line_num=None, left_length=None, right_length=None, top_length=None,
             bot_length=None, accuracy=None):
    if line_num is None:
        line_num = 5
    if left_length is None:
        left_length = 2
    if right_length is None:
        right_length = 2
    if top_length is None:
        top_length = 2
    if bot_length is None:
        bot_length = 2
    if accuracy is None:
        accuracy = 4
    # img = cv2.imread('image-10.png', 0)
    (h, w) = img.shape

    img1 = image_selected(img, left_x1, left_x2, left_y1, left_y2)
    left = edge_line(img1, line_num, int(left_x1 * w), int(left_y1 * h), left_length, accuracy)
    # for element in left:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img2 = image_selected(img, top_x1, top_x2, top_y1, top_y2)
    top = edge_line(img2, line_num, int(top_x1 * w), int(top_y1 * h), right_length, accuracy)
    # for element in top:
    #
    #     cv2.line(img,(element[0],element[1]),(element[2],element[3]),(0,0,0),3)

    img3 = image_selected(img, bot_x1, bot_x2, bot_y1, bot_y2)
    bot = edge_line(img3, line_num, int(bot_x1 * w), int(bot_y1 * h), top_length, accuracy)
    # for element in bot:
    #
    #     cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)

    img4 = image_selected(img, right_x1, right_x2, right_y1, right_y2)
    right = edge_line(img4, line_num, int(right_x1 * w), int(right_y1 * h), bot_length, accuracy)
    # for element in right:
    #
    #      cv2.line(img, (element[0], element[1]), (element[2], element[3]), (0, 0, 0), 3)
    frame_list=[]
    accuracy_list=[]
    for t in top:
        for l in left:
            for r in right:
                for b in bot:
                    if frame(t,l,r,b,0.01)!=0:
                        accuracy_list+=[frame(t,l,r,b,0.01)]
                        frame_list+=[(t,l,r,b)]
                        # print((t,l,r,b))

    min_value=10000
    location_key=0
    try:
        for i in range(0,len(accuracy_list),1):
            if accuracy_list[i]<min_value:
                min_value=accuracy_list[i]
                location_key=i


        best_frame=frame_list[location_key]
        # print(frame_list)
        (xa, ya) =cross_point(best_frame[0],best_frame[1])
        (xb, yb) =cross_point(best_frame[0], best_frame[2])
        (xc, yc) =cross_point(best_frame[3], best_frame[2])
        (xd, yd) =cross_point(best_frame[3], best_frame[1])
        xa,ya,xb,yb,xc,yc,xd,yd = int(xa),int(ya),int(xb),int(yb),int(xc),int(yc),int(xd),int(yd)
        img = img[ya:yc, xa:xb]
        return img
    except:
        print("detection failed, please try more lines")
        return 0

