import numpy as np


def camera_matrix(photo, point):
    """
    INPUT:
        photo : background photo class
        point : 3D point is space
    """
    theta = np.array([np.deg2rad(photo.tilt),-np.deg2rad(photo.direction),np.pi]) # the orientation of the camera [pitch, yaw, roll]. default look in z-direction 
    c = photo.location
    a = point # the 3D position of a point A that is to be projected
    
    
    
    f = photo.focal_length # focal length [m]
    shape = photo.shape
    hfov = np.deg2rad(photo.hfov)
    vfov = np.deg2rad(photo.vfov)

    m_x = 1/((np.tan(hfov/2)*f)/(shape[1]/2))
    m_y = 1/((np.tan(vfov/2)*f)/(shape[0]/2))
    
    
    a_x = f * m_x; a_y = f * m_y
    
    R_z = np.array([[np.cos(theta[2]),-np.sin(theta[2]),0],
                      [np.sin(theta[2]), np.cos(theta[2]),0],
                      [0,0,1]])
    
    R_y = np.array([[np.cos(theta[1]),0,np.sin(theta[1])],
                      [0,1,0],
                      [-np.sin(theta[1]),0,np.cos(theta[1])]])
    R_x = np.array([[1,0,0],
                  [0, np.cos(theta[0]), -np.sin(theta[0])],
                  [0,np.sin(theta[0]),np.cos(theta[0])]])
    
    R = R_z @ R_y @ R_x
    t = c
    
    C_N  = np.column_stack((R,t)) # camera matrix
    
    
    K = np.array([[a_x, 0, shape[1]/2],
                  [0, a_y, shape[0]/2],
                  [0, 0, 1]])
    # print(f, m_x, m_y, a_x, a_y, K)
    P = np.hstack((point,1))
    
    p = K @ C_N @ P
    p = p / p[2]

    return p

# theta = np.array([0,np.pi/2,np.pi/0.5]) # the orientation of the camera [pitch, yaw, roll]. default look in z-direction 
# c = np.array([0,0,0]) # the 3D position of a point C representing the camera.
# a = np.array([2,5,1]) # the 3D position of a point A that is to be projected



# f = 0.02 # focal length [m]
# shape = (1200, 800)
# hfov = np.deg2rad(90)
# vfov = np.deg2rad(67)

# m_x = 1/(np.tan(hfov/2)*f/shape[0])
# m_y = 1/(np.tan(vfov/2)*f/shape[1])


# a_x = f * m_x; a_y = f * m_y

# R_z = np.array([[np.cos(theta[2]),-np.sin(theta[2]),0],
#                   [np.sin(theta[2]), np.cos(theta[2]),0],
#                   [0,0,1]])

# R_y = np.array([[np.cos(theta[1]),0,np.sin(theta[1])],
#                   [0,1,0],
#                   [-np.sin(theta[1]),0,np.cos(theta[1])]])
# R_x = np.array([[1,0,0],
#               [0, np.cos(theta[0]), -np.sin(theta[0])],
#               [0,np.sin(theta[0]),np.cos(theta[0])]])

# R = R_z @ R_y @ R_x
# t = c # camera is conter

# C_N  = np.column_stack((R,t)) # camera matrix


# K = np.array([[a_x, 0, shape[0]/2],
#               [0, a_y, shape[1]/2],
#               [0, 0, 1]])

# P = np.array([10, -1, 0, 1])

# p = K @ C_N @ P
# p = p / p[2]

# print(p.astype(int))