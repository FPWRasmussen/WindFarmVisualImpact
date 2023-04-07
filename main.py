import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from pyproj import Geod
from camera_matrix import camera_matrix
from find_coeffs import find_coeffs
import matplotlib.pyplot as plt

class photo():
    def __init__(self, file, hfov, tilt, direction, location, focal_length):
        self.im = Image.open("images/"+file, mode = "r").convert('RGBA')
        self.hfov = hfov
        self.tilt = tilt
        self.direction = direction
        self.location = location
        self.shape = np.shape(self.im)
        self.vfov = hfov/self.shape[1] * self.shape[0]
        self.hfov_range = [direction-hfov/2, direction+hfov/2]
        self.vfov_range = [tilt-self.vfov/2, tilt+self.vfov//2]
        self.focal_length = focal_length
        
class turbine():
    def __init__(self, file, height, location):
        self.im = Image.open("images/"+file, mode = "r").convert('RGBA')
        self.height = height
        self.location = location
        self.shape = np.shape(self.im)
        self.width = fov/self.shape[0] * self.shape[1]
        self.radius = height/(2*self.shape[0]/self.shape[1]-1)



fov = 90 # field of view [deg]
tilt = 0 # vertical tilt [deg]
height = 100
# radius = 68

direction = 0 # direction [deg]
location1 = [0,2,0]
location2 = [50, 100, 3000]
focal_length = 0.02
wind_direction = 0 # 
picture1 = photo("image1.png", fov, tilt, direction, location1, focal_length)
turbine1 = turbine("turbine.png", height, location2)
turbine1.im = ImageEnhance.Brightness(turbine1.im ).enhance(0.7)
radius = turbine1.radius
location3 = location2 + np.array([0, height+radius, 0])
#Open image using Image module
# im = Image.open("images/image1.png")
#Show actual Image
# im.show()

def calc_angle_dist(location1, location2):
    angle,angle2,distance = Geod(ellps='WGS84').inv(location1[0], location1[1], location2[0] ,location2[1]) # N = 0, E = 90, W = -90, S = 180/-180
    if angle < 0:
        angle = angle + 360
    return angle, distance

angle, distance = calc_angle_dist(location1, location2)

def is_in_frame(angle, fov_range):
    if angle >= fov_range[0] and angle <= fov_range[1]:
        return True
    else:
        return False
    
is_in_frame(angle,picture1.vfov_range)

draw = ImageDraw.Draw(picture1.im)

point1 = np.array([np.cos(wind_direction)*radius, height+radius, np.sin(wind_direction)*radius])+location2
point2 = -np.array([np.cos(wind_direction)*radius, -height-radius, np.sin(wind_direction)*radius])+location2
point3 = -np.array([np.cos(wind_direction)*radius, 0, np.sin(wind_direction)*radius])+location2
point4 = np.array([np.cos(wind_direction)*radius, 0, np.sin(wind_direction)*radius])+location2

p_list = [point1, point2, point3, point4]
pa = []
for p in p_list:
    print(p)
    q = camera_matrix(picture1, p)
    # d = draw.rectangle(((q[0],q[1]),(q[0]+5,q[1]+5)),fill = "red")
    pa.append([q[0],q[1]])
    

pc = np.array(pa).reshape(4,2)
pc[:,0] -= np.amin(pc[:,0])
pc[:,1] -= np.amin(pc[:,1])

pb = [(0, 0), (turbine1.shape[1], 0), (turbine1.shape[1], turbine1.shape[0]), (0, turbine1.shape[0])]

scale_x = np.amax(np.array(pb).reshape(4,2)[:,0])/np.amax(pc[:,0])
scale_y = np.amax(np.array(pb).reshape(4,2)[:,1])/np.amax(pc[:,1])

pd = list(pa)
for i in range(len(pa)):
    pa[i] = [pc[i,0],pc[i,1]]
    

coeffs = find_coeffs(pa, pb)

width, height = turbine1.im.size 
turbine1.im = turbine1.im.transform((int(np.amax(np.array(pa).reshape(4,2)[:,0])),int(np.amax(np.array(pa).reshape(4,2)[:,1]))), method=Image.Transform.PERSPECTIVE,data=coeffs)

picture1.im.paste(turbine1.im, box=[np.amin(np.array(pd).reshape(4,2)[:,0]).astype(int),np.amin(np.array(pd).reshape(4,2)[:,1]).astype(int)], mask = turbine1.im)
picture1.im.show()

