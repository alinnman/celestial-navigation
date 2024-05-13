from math import pi, sin, cos, asin, acos, sqrt, atan2

EARTH_CIRCUMFERENCE = 40075

# Utility routines

def addVecs (vec1, vec2):
    assert (type (vec1) == type (vec2) == list)
    assert (len (vec1) == len (vec2))
    retVal = []
    for i in range (len(vec1)):
        retVal.append (vec1[i] + vec2[i])
    return retVal

def multScalarVect (scalar, vec):
    assert (type (scalar) == int or type(scalar) == float)
    assert (type (vec) == list)
    retVal = []
    for i in range (len(vec)):
        retVal.append (scalar*vec[i])
    return retVal 

def lengthOfVect (vec):
    assert (type (vec) == list)
    s = 0
    for i in range (len(vec)):
        s += (vec[i]*vec[i])
    return sqrt (s)

def normalizeVect (vec):
    return multScalarVect (1/lengthOfVect(vec), vec)
    

def crossProduct (vec1, vec2) :
    assert (type (vec1) == type(vec2) == list) 
    assert (len (vec1) == len (vec2) == 3)
    retVal = [0, 0, 0]
    retVal [0] = vec1 [1]*vec2[2] - vec1[2]*vec2[1]
    retVal [1] = vec1 [2]*vec2[0] - vec1[0]*vec2[2]
    retVal [2] = vec1 [0]*vec2[1] - vec1[1]*vec2[0]
    return retVal

def dotProduct (vec1, vec2):
    assert (type (vec1) == list and type(vec2) == list) 
    assert (len (vec1) == len (vec2) == 3)
    s = 0
    for i in range (len(vec1)):
        s += vec1[i]*vec2[i]
    return s

def degToRad (deg):
    assert (type(deg) == int or type (deg) == float)
    return deg/(180.0/pi)

def radToDeg (rad):
    assert (type(rad) == int or type (rad) == float)    
    return rad*(180.0/pi)

def toLonLat (vec):
    assert (type (vec) == list) 
    assert (len (vec) == 3)
    vec = normalizeVect (vec)
    
    theta = atan2 (vec[1],vec[0])
    #print ("BLALA = " + str(vec[2]))
    phi = acos (vec[2])
    LON = radToDeg (theta)
    LAT = 90-radToDeg (phi) 
    return LON, LAT

def toRectangular (LON, LAT):
    assert (type (LAT) == int or type (LAT) == float)
    assert (type (LON) == int or type (LON) == float)
    phi = degToRad (90 - LAT)
    theta = degToRad (LON)
    aVec = []
    aVec.append (cos (theta) * sin (phi))
    aVec.append (sin (theta) * sin (phi))
    aVec.append (cos (phi))
    #print ("TJOSAN = " + str(aVec))
    aVec = normalizeVect (aVec)
    return aVec
    
def rotateVector (vec, rotVec, angle):
    assert (type(vec) == type(rotVec) == list)
    assert (len(vec) == len(rotVec) == 3)
    assert (type(angle) == float or type(angle) == int) 
    v1 = multScalarVect (cos(angle), vec)
    v2 = multScalarVect (sin(angle), crossProduct(rotVec, vec))
    v3 = multScalarVect (dotProduct(rotVec,vec)*(1-cos(angle)), rotVec)
    result = addVecs (v1, addVecs(v2, v3))
    return result
    
def distanceBetweenPoints (lonLat1, lonLat2):
    assert (type(lonLat1) == type(lonLat2) == tuple)
    lon1 = lonLat1[0]
    lat1 = lonLat1[1]
    normVec1 = toRectangular (lon1, lat1)
    lon2 = lonLat2[0]
    lat2 = lonLat2[1]
    normVec2 = toRectangular (lon2, lat2)
    dp = dotProduct (normVec1, normVec2)
    angle = acos (dp)
    distance = (EARTH_CIRCUMFERENCE/(2*pi)) * angle
    return distance

# Object representing a star fix

class starFix :
    def __init__ (self, \
                  object_name, \
                  date, \
                  time_hour, \
                  time_minute, \
                  time_second, \
                  gha_time_0_degrees, \
                  gha_time_0_minutes, \
                  gha_time_1_degrees, \
                  gha_time_1_minutes, \
                  decl_time_0_degrees, \
                  decl_time_0_minutes, \
                  decl_time_1_degrees, \
                  decl_time_1_minutes, \
                  measured_alt_degrees, \
                  measured_alt_minutes, \
                  measured_alt_seconds, \
                  sha_diff_degrees = 0, \
                  sha_diff_minutes = 0):
        self.object_name          = object_name
        self.time_hour            = time_hour           # B7
        self.time_minute          = time_minute         # B8
        self.time_second          = time_second         # B9
        self.gha_time_0_degrees   = gha_time_0_degrees  # B12
        self.gha_time_0_minutes   = gha_time_0_minutes  # B13
        self.gha_time_1_degrees   = gha_time_1_degrees  # B14
        self.gha_time_1_minutes   = gha_time_1_minutes  # B15
        self.decl_time_0_degrees  = decl_time_0_degrees # D12
        self.decl_time_0_minutes  = decl_time_0_minutes # D13 
        self.decl_time_1_degrees  = decl_time_1_degrees # D14 
        self.decl_time_1_minutes  = decl_time_1_minutes # D15
        self.measured_alt_degrees = measured_alt_degrees
        self.measured_alt_minutes = measured_alt_minutes
        self.measured_alt_seconds = measured_alt_seconds
        self.sha_diff_degrees     = sha_diff_degrees    # B10
        self.sha_diff_minutes     = sha_diff_minutes    # B11
        assert (self.object_name != "Sun" or (self.sha_diff_degrees == 0 and self.sha_diff_minutes == 0))
        
        self.GP_lon, self.GP_lat = self.__calculateGP ()
        #print (str(self.GP_lon), "", str(self.GP_lat))
    
    def __calculateGP (self):
        # -((B12+B10)+((B14+B10)-(B12+B10))*C9+((B13+B11)/60)+(((B15+B11)-(B13+B11))/60)*C9)
        # -((B12+B10)+((B14-B12          ))*C9+((B13+B11)/60)+(((B15-B13)/60))*C9)
        
        minSecContribution = self.time_minute/60 + self.time_second/3600
        #print (minSecContribution)
        
        resultLON = - \
        ((self.gha_time_0_degrees + self.sha_diff_degrees) + \
        ((self.gha_time_1_degrees - self.gha_time_0_degrees))*minSecContribution + \
        ((self.gha_time_0_minutes + self.sha_diff_minutes)/60) + \
        (((self.gha_time_1_minutes - self.gha_time_0_minutes)/60))*minSecContribution)
        # D12+(D14-D12)*C9+(D13/60)+((D15-D13)/60)*C9
        resultLAT = \
        self.decl_time_0_degrees + (self.decl_time_1_degrees - self.decl_time_0_degrees)*minSecContribution + \
        self.decl_time_0_minutes/60 + ((self.decl_time_1_minutes - self.decl_time_0_minutes)/60)*minSecContribution
        
        return resultLON, resultLAT

    def getAngle (self):
        measured_alt_decimal = self.measured_alt_degrees + \
                               self.measured_alt_minutes/60 + \
                               self.measured_alt_seconds/3600
        return (90-measured_alt_decimal)
    
    def getRadius (self):
        return (self.getAngle()/360)*EARTH_CIRCUMFERENCE
    
    def getGP (self):
        pass
        
class starFixPair:
    def __init__ (self, sf1, sf2):
        self.sf1 = sf1
        self.sf2 = sf2

    def getIntersections (self):

        #print ("FOO1-LON = " + str(self.sf1.GP_lon)+ "; FOO1-LAT = " + str(self.sf1.GP_lat))               
        aVec = toRectangular (self.sf1.GP_lon, self.sf1.GP_lat)
        #print ("AVEC = " + str(aVec))
        LON1, LAT1 = toLonLat (aVec)
        #print ("AVEC: LON1 = " + str(LON1)+ "; LAT1 = " + str(LAT1))       
        
        #print ("FOO2-LON = " + str(self.sf2.GP_lon)+ "; FOO2-LAT = " + str(self.sf2.GP_lat)) 
        bVec = toRectangular (self.sf2.GP_lon, self.sf2.GP_lat)
        #print ("BVEC = " + str(bVec))        
        LON1, LAT1 = toLonLat (bVec)
        #print ("BVEC: LON1 = " + str(LON1)+ "; LAT1 = " + str(LAT1))               
        
        
        abCross = crossProduct (aVec, bVec)
        abCross = normalizeVect (abCross)

        p1 = multScalarVect (cos(degToRad(self.sf2.getAngle())), aVec)
        p2 = multScalarVect (-cos(degToRad(self.sf1.getAngle())), bVec)
        p3 = addVecs (p1, p2)
        p3 = normalizeVect (p3)
        p4 = crossProduct (abCross, p3)
        q = normalizeVect (p4)

        qLon, qLat = toLonLat (q)
        #print ("LON = " + str(qLon)+ "; LAT = " + str(qLat))
        # LON = -91.44736977201018; LAT = 24.808471771121802
        # 24.808471771121802,-91.44736977201018

        rho = acos (cos (degToRad(self.sf1.getAngle())) / (dotProduct (aVec, q)))
        rotAxis = normalizeVect(crossProduct (crossProduct (aVec, bVec), q))
        #print ("ROTAXIS = " + str(rotAxis))
        #print (q)
        #print (lengthOfVect(q))
        #print ("RHO = " + str(radToDeg(rho)))
        
        int1 = normalizeVect(rotateVector (q, rotAxis, rho))
        int2 = normalizeVect(rotateVector (q, rotAxis, -rho))
        return toLonLat(int1), toLonLat(int2)
        
class starFixCollection:
    def __init__ (self, sfList):
        assert (len (sfList) >= 2)
        self.sfList = sfList

    def getIntersections (self, limit=100):
        if (len(self.sfList) == 2):
            intersections = starFixPair (self.sfList[0],self.sfList[1]).getIntersections()
            return intersections
        else:
            nrOfFixes = len (self.sfList)
            #print ("nrOfFixes = " + str(nrOfFixes))
            coords = []
            for i in range (nrOfFixes):
                for j in range (i, nrOfFixes):
                    if i != j:
                        #print ("i = " + str(i) + "; j = " + str(j))
                        p = starFixPair (self.sfList [i], self.sfList [j])
                        pInt = p.getIntersections ()
                        #print (pInt)
                        coords.append (pInt[0])
                        coords.append (pInt[1])                        
            #print (len(coords))
            #print (coords)
            nrOfCoords = len (coords)
            dists = dict ()
            for i in range (nrOfCoords):
                for j in range (i, nrOfCoords):
                    if i != j:
                        dist = distanceBetweenPoints (coords[i], coords[j])
                        #print (dist)
                        dists [i,j] = dist
            #print (dists)
            sortedDists = dict(sorted(dists.items(), key=lambda item: item[1]))
            #print (sortedDists)
            nrOfSortedDists = len (sortedDists)
            chosenPoints = set ()
            for sd in sortedDists:
                #print (sd) 
                theDistance = sortedDists [sd]
                #print (theDistance)
                if (theDistance < limit): 
                    chosenPoints.add (sd[0])
                    chosenPoints.add (sd[1])
            #print (chosenPoints) 
            nrOfChosenPoints = len (chosenPoints)
            summationVec = [0,0,0]
            for cp in chosenPoints: 
                #print (cp) 
                selectedCoord = coords [cp]
                #print (selectedCoord) 
                rectVec = toRectangular (selectedCoord[0], selectedCoord[1])
                #print (rectVec) 
                summationVec = addVecs (summationVec, multScalarVect (1/nrOfChosenPoints, rectVec))
            summationVec = normalizeVect (summationVec)
            retLON, retLAT = toLonLat (summationVec)
            return retLON, retLAT
            
            #nrOfDists = len (sortedDists)
            
        
        
a = starFix (date                 = "2024-05-05", \
              object_name          = "Sun", \
              time_hour            = 15, \
              time_minute          = 55, \
              time_second          = 18, \
              gha_time_0_degrees   = 45, \
              gha_time_0_minutes   = 50.4, \
              gha_time_1_degrees   = 60, \
              gha_time_1_minutes   = 50.4, \
              decl_time_0_degrees  = 16, \
              decl_time_0_minutes  = 30.6, \
              decl_time_1_degrees  = 16, \
              decl_time_1_minutes  = 31.3, \
              measured_alt_degrees = 55, \
              measured_alt_minutes = 8, \
              measured_alt_seconds = 1.8 \
              )
              
#print (a.getRadius())

b = starFix (date                 = "2024-05-05", \
              object_name          = "Sun", \
              time_hour            = 23, \
              time_minute          = 1, \
              time_second          = 19, \
              gha_time_0_degrees   = 165, \
              gha_time_0_minutes   = 50.8, \
              gha_time_1_degrees   = 180, \
              gha_time_1_minutes   = 50.8, \
              decl_time_0_degrees  = 16, \
              decl_time_0_minutes  = 36.2, \
              decl_time_1_degrees  = 16, \
              decl_time_1_minutes  = 36.9, \
              measured_alt_degrees = 19, \
              measured_alt_minutes = 28, \
              measured_alt_seconds = 18 \
              )

c = starFix (date                 = "2024-05-06", \
              object_name          = "Vega", \
              time_hour            = 4, \
              time_minute          = 4, \
              time_second          = 13, \
              gha_time_0_degrees   = 284, \
              gha_time_0_minutes   = 30.4, \
              gha_time_1_degrees   = 299, \
              gha_time_1_minutes   = 32.9, \
              decl_time_0_degrees  = 38, \
              decl_time_0_minutes  = 48.1, \
              decl_time_1_degrees  = 38, \
              decl_time_1_minutes  = 48.1, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 16, \
              measured_alt_seconds = 24.6, \
              sha_diff_degrees     = 80, \
              sha_diff_minutes     = 33.4 \
              )

#print (b.getRadius())

#starFixPair = starFixPair (a, b)
#intersection1, intersection2 = starFixPair.getIntersections ()
#print (intersection1)
#print (intersection2)
#dist = distanceBetweenPoints ((0,0), (0,90))
#print (dist)
# 41.764874280342816, -87.71719349718802

collection = starFixCollection ([a, b])
intersections = collection.getIntersections ()
print (intersections)

collection = starFixCollection ([a, b, c])
intersections = collection.getIntersections ()
print (intersections)
# 41.874156346243865, -87.67180300975592


