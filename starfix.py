from math import pi, sin, cos, acos, sqrt, tan, atan2

EARTH_CIRCUMFERENCE_EQUATORIAL = 40075.017
EARTH_CIRCUMFERENCE_MERIDIONAL = 40007.86
EARTH_CIRCUMFERENCE = (EARTH_CIRCUMFERENCE_EQUATORIAL + EARTH_CIRCUMFERENCE_MERIDIONAL) / 2

# Utility routines (algrebraic, spheric geometry) 

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
    lenV = lengthOfVect (vec)
    if lenV == 0:
        raise ValueError ("Cannot normalize a zero vector")
    return multScalarVect (1/lenV, vec)
    

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
    aVec = normalizeVect (aVec)
    return aVec
    
def rotateVector (vec, rotVec, angle):
    '''
    Rotate a vector around a rotation vector. Based on Rodrigues formula. https://en.wikipedia.org/wiki/Rodrigues%27_formula 
    '''
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
    
# Atmospheric refraction

def getRefraction (apparentAngle):
    '''
    Bennett's formula
    '''
    assert (type(apparentAngle) == float or type (apparentAngle) == int)    
    h = apparentAngle*(pi/180)
    return (1 / tan( h + 7.31 / (h + 4.4) ))

# Data formatting
    
def getRepresentation (ins, numDecimals, lat=False):
    assert (type (numDecimals) == int and numDecimals >= 0) 
    if type (ins) == float or type (ins) == int: 
        degrees = int (ins)
        if lat:
            if ins < 0:
                prefix = "S"
            else:
                prefix = "N"
        else:
            if ins < 0:
                prefix = "W"
            else:
                prefix = "E"        
        minutes = float (abs((ins - degrees)*60))
        aDegrees = abs (degrees)
        return prefix + " " + str(aDegrees) + "°," + str(round(minutes, numDecimals)) + "′"
    elif type (ins) == tuple or type (ins) == list:
        pair = (type(ins) == tuple)
        length = len (ins)
        retVal = "("
        for i in range (length-1, -1, -1):
            lat = False
            if pair and i == length-1:
                lat = True
            retVal = retVal + getRepresentation (ins[i], numDecimals, lat)
            if i > 0:
                retVal = retVal + ";"
        retVal = retVal + ")"
        return retVal                 
        
def getDMS (angle):
    degrees = int (angle)
    minutes = int ((angle-degrees)*60)
    seconds = (angle-degrees-minutes/60)*3600
    return degrees, minutes, seconds

# Object representing a sight (star fix)

class Sight :
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
        self.time_hour            = time_hour            
        self.time_minute          = time_minute          
        self.time_second          = time_second          
        self.gha_time_0_degrees   = gha_time_0_degrees  
        self.gha_time_0_minutes   = gha_time_0_minutes  
        self.gha_time_1_degrees   = gha_time_1_degrees  
        self.gha_time_1_minutes   = gha_time_1_minutes  
        self.decl_time_0_degrees  = decl_time_0_degrees 
        self.decl_time_0_minutes  = decl_time_0_minutes  
        self.decl_time_1_degrees  = decl_time_1_degrees  
        self.decl_time_1_minutes  = decl_time_1_minutes 
        self.measured_alt_degrees = measured_alt_degrees
        self.measured_alt_minutes = measured_alt_minutes
        self.measured_alt_seconds = measured_alt_seconds
        self.sha_diff_degrees     = sha_diff_degrees    
        self.sha_diff_minutes     = sha_diff_minutes    
        assert (self.object_name != "Sun" or (self.sha_diff_degrees == 0 and self.sha_diff_minutes == 0))
                
        self.correctForRefraction ()
        self.GP_lon, self.GP_lat = self.__calculateGP ()
        
    def correctForRefraction (self):
        madDecimal = 90-self.getAngle ()
        refraction = getRefraction (90-madDecimal)/60
        newMad = madDecimal + refraction
        d, m, s = getDMS (newMad)
        self.measured_alt_degrees = d
        self.measured_alt_minutes = m
        self.measured_alt_seconds = s
    
    def __calculateGP (self):
        
        minSecContribution = self.time_minute/60 + self.time_second/3600
        
        resultLON = - \
        ((self.gha_time_0_degrees + self.sha_diff_degrees) + \
        ((self.gha_time_1_degrees - self.gha_time_0_degrees))*minSecContribution + \
        ((self.gha_time_0_minutes + self.sha_diff_minutes)/60) + \
        (((self.gha_time_1_minutes - self.gha_time_0_minutes)/60))*minSecContribution)
 
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
        
class SightPair:
    def __init__ (self, sf1, sf2):
        assert (type (sf1) == type (sf2) == Sight)
        self.sf1 = sf1
        self.sf2 = sf2

    def getIntersections (self):
        '''
        Get intersection of two circles on a spheric surface. Based on https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere 
        '''
        # Get cartesian vectors a and b (from ground points)
        aVec = toRectangular (self.sf1.GP_lon, self.sf1.GP_lat)     
        bVec = toRectangular (self.sf2.GP_lon, self.sf2.GP_lat)       
              
        # Calculate axb
        abCross = crossProduct (aVec, bVec)
        abCross = normalizeVect (abCross)

        # These steps calculate q which is located halfway between our two intersections 
        p1 = multScalarVect (cos(degToRad(self.sf2.getAngle())), aVec)
        p2 = multScalarVect (-cos(degToRad(self.sf1.getAngle())), bVec)
        p3 = addVecs (p1, p2)
        p3 = normalizeVect (p3)
        p4 = crossProduct (abCross, p3)
        q = normalizeVect (p4)

        # Calculate a rotation angle
        try:
            rho = acos (cos (degToRad(self.sf1.getAngle())) / (dotProduct (aVec, q)))
        except ValueError:
            print ("Bad sight data.")
            return None
        # Calculate a rotation vector
        rotAxis = normalizeVect(crossProduct (crossProduct (aVec, bVec), q))
        
        # Calculate the two intersections by performing rotation of rho and -rho
        int1 = normalizeVect(rotateVector (q, rotAxis, rho))
        int2 = normalizeVect(rotateVector (q, rotAxis, -rho))
        return toLonLat(int1), toLonLat(int2)
        
class SightCollection:
    def __init__ (self, sfList):
        assert (len (sfList) >= 2)
        self.sfList = sfList

    def getIntersections (self, limit=100):
        nrOfFixes = len(self.sfList)
        if (nrOfFixes == 2):
            '''
            For two star fixes just use the algorithm of SightPair.getIntersections
            '''
            intersections = SightPair (self.sfList[0],self.sfList[1]).getIntersections()
            return intersections
        elif (nrOfFixes >= 3):
            '''
            For >= 3 star fixes perform pairwise calculation on every pair of fixes and then run a sorting algorithm 
            '''
            coords = []
            # Perform pairwise sight reductions
            for i in range (nrOfFixes):
                for j in range (i+1, nrOfFixes):
                    p = SightPair (self.sfList [i], self.sfList [j])
                    pInt = p.getIntersections ()
                    if pInt != None:
                        coords.append (pInt[0])
                        coords.append (pInt[1])                        
            nrOfCoords = len (coords)
            dists = dict ()
            # Collect all distance values between intersections
            for i in range (nrOfCoords):
                for j in range (i, nrOfCoords):
                    if i != j:
                        dist = distanceBetweenPoints (coords[i], coords[j])
                        dists [i,j] = dist
            # Sort the distances, with lower distances first
            sortedDists = dict(sorted(dists.items(), key=lambda item: item[1]))
            nrOfSortedDists = len (sortedDists)
            chosenPoints = set ()
            cpLimit = int((nrOfFixes**2 - nrOfFixes) / 2)
            # Find the points which are located close to other points
            for sd in sortedDists:
                theDistance = sortedDists [sd]
                if theDistance < limit: 
                    chosenPoints.add (sd[0])
                    chosenPoints.add (sd[1])
                else:
                    break
                if len (chosenPoints) > cpLimit:
                    break
                
            nrOfChosenPoints = len (chosenPoints)
            if nrOfChosenPoints == 0:
                # No points found. Bad star fixes. Return nothing. 
                print ("Bad sight data.")
                return None
                
            # Make sure the chosen points are nearby each other
            print ("BEST COORDINATES")
            for cp1 in chosenPoints:
                print (getRepresentation (coords[cp1],1))  
                for cp2 in chosenPoints:
                    if cp1 != cp2:
                        dist = distanceBetweenPoints (coords[cp1], coords[cp2])
                        if dist > limit:
                            # Probably multiple possible observation points. 
                            # Best option is to perform sight reduction on 2 sights and select the correct point manually.
                            print ("Seems to be multiple possible coordinates. Please perform two-point sight reduction instead.")
                            return None
            print ("MEAN VALUE COORDINATE from multi-point sight data.")              
            summationVec = [0,0,0]
            # Make a mean value on the best intersections. 
            for cp in chosenPoints: 
                selectedCoord = coords [cp]
                rectVec = toRectangular (selectedCoord[0], selectedCoord[1])
                summationVec = addVecs (summationVec, multScalarVect (1/nrOfChosenPoints, rectVec))
            summationVec = normalizeVect (summationVec)
            retLON, retLAT = toLonLat (summationVec)
            return retLON, retLAT
        else:
            print ("Invalid input.")
            return None



