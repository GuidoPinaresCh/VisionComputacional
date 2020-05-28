import numpy as np
import cv2

def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append(coords[2])
    return radius

def av_pix(img,circle,size):
    av_value = []
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value


img = cv2.imread('coins.png',cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread('coins.png',1)
img=cv2.GaussianBlur(img,(5,5),0)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120,param1=50,param2=27,minRadius=60,maxRadius=100)

print(circles)

circles = np.uint16(np.around(circles))
count = 1
for i in circles[0,:]:

    cv2.circle(original_image,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(original_image,(i[0],i[1]),2,(0,0,255),3)
    #cv2.putText(original_image, str(count),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),2)
    count += 1

radii = get_radius(circles)
bright_values = av_pix(img,circles,20)
print(radii)
print(bright_values)

values = []

for a,b in zip(bright_values,radii):
    
    if b==76:
        values.append(0.1)
    elif a > 120 and b > 90:
        values.append(5)
    elif a > 100 and a < 120 and b > 90:
        values.append(1)
    elif a > 100 and b < 90:
        values.append(0.5)
    elif a < 100 and b < 94 and b > 89:
        values.append(0.2)    
    elif a < 90 and b < 90:
        values.append(0.1)

print(values)
count_2=0
for i in circles[0,:]:

    cv2.putText(original_image, 'S/' + str(values[count_2]),(i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),2)
    count_2 += 1

cv2.putText(original_image,'ESTIMATED TOTAL VALUE: ' + 'S/' +str(round(sum(values),1)), (1000,100), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)


cv2.imshow('Detected Coins', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()