import numpy as np

class Position:
    def __init__(self, altitude, latitude, longitude) -> None:
        self.altitude = altitude+20903520
        self.latitude = latitude
        self.longitude = longitude
        self.theta = self.longitude*np.pi/180
        self.phi = -np.pi*(self.latitude/180-1/2)
        self.spherical = np.array([self.altitude, self.theta, self.phi])
        self.cartesian = self.altitude*np.array([np.cos(self.theta)*np.sin(self.phi), np.sin(self.theta)*np.sin(self.phi),np.cos(self.phi)])



position1 = Position(0,0,0)
print(position1.cartesian)