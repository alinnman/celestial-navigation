from math import pi, sin, cos, acos, sqrt, tan, atan2
from datetime import datetime, timezone

# Dimension of Earth

EARTH_CIRCUMFERENCE_EQUATORIAL = 40075.017
EARTH_CIRCUMFERENCE_MERIDIONAL = 40007.86
EARTH_CIRCUMFERENCE = (EARTH_CIRCUMFERENCE_EQUATORIAL + EARTH_CIRCUMFERENCE_MERIDIONAL) / 2
EARTH_RADIUS = EARTH_CIRCUMFERENCE / (2 * pi) 

# Data types

class LatLon:
    ''' Represents spherical coordinates on Earth '''
    def __init__ (self, lat : float | int, lon : float | int): 
        self.lat = lat
        self.lon = lon
        
    def __str__(self):
        return "LAT = " + str(self.lat) + "; LON = " + str(self.lon)        

    def getTuple (self) -> tuple[float | int] :
        ''' Used to simplify some code where tuples are more practical '''
        return self.lon, self.lat
        
# Utility routines (algrebraic, spheric geometry) 

def addVecs (vec1 : list, vec2 : list) -> list: 
    ''' Performs addition of two cartesian vectors '''
    assert (len (vec1) == len (vec2))
    retVal = []
    for i in range (len(vec1)):
        retVal.append (vec1[i] + vec2[i])
    return retVal

def subtractVecs (vec1 : list, vec2 : list) -> list:
    ''' Performs subtraction of two cartesian vectors '''
    assert (len (vec1) == len (vec2))
    return addVecs (vec1, multScalarVect(-1, vec2))

def multScalarVect (scalar : int | float, vec : list) -> list:
    ''' Performs multiplication of a cartesian vector with a scalar '''
    retVal = []
    for i in range (len(vec)):
        retVal.append (scalar*vec[i])
    return retVal 

def lengthOfVect (vec : list) -> float:
    ''' Returns the absolute value (length) of a vector '''
    s = 0
    for i in range (len(vec)):
        s += (vec[i]*vec[i])
    return sqrt (s)

def normalizeVect (vec : list) -> list:
    ''' Computes |vec| '''
    lenV = lengthOfVect (vec)
    assert (lenV > 0)
    return multScalarVect (1/lenV, vec)

def crossProduct (vec1 : list, vec2 : list) -> list:
    ''' Computes vec1 x vec2 (cross product) '''
    assert (len (vec1) == len (vec2) == 3)
    retVal = [0, 0, 0]
    retVal [0] = vec1 [1]*vec2[2] - vec1[2]*vec2[1]
    retVal [1] = vec1 [2]*vec2[0] - vec1[0]*vec2[2]
    retVal [2] = vec1 [0]*vec2[1] - vec1[1]*vec2[0]
    return retVal

def dotProduct (vec1 : list, vec2 : list) -> float:
    ''' Computes vec1 * vec2 (dot product) '''
    assert (len (vec1) == len (vec2))
    s = 0.0
    for i in range (len(vec1)):
        s += vec1[i]*vec2[i]
    return s
    
def modLON (lon : int | float): 
    ''' Transforms a longitude value to the range (-180,180) '''
    x = lon + 180
    x = x % 360
    x = x - 180
    return x    

def degToRad (deg : int | float) -> float:
    ''' Convert degrees to radians '''
    return deg/(180.0/pi)

def radToDeg (rad : int | float) -> float:
    ''' Convert radians to degrees '''
    return rad*(180.0/pi)
    
def toLatLon (vec : list) -> LatLon:
    ''' Convert cartesian coordinate to LatLon (spherical) '''
    assert (len (vec) == 3)
    vec = normalizeVect (vec)
    
    theta = atan2 (vec[1],vec[0])
    phi = acos (vec[2])
    LON = radToDeg (theta)
    LAT = 90-radToDeg (phi) 
    
    return LatLon (LAT, modLON(LON))   

def toRectangular (latlon : LatLon) -> list:
    ''' Convert LatLon (spherical) coordinate to cartesian '''
    phi = degToRad (90 - latlon.lat)
    theta = degToRad (latlon.lon)
    aVec = []
    aVec.append (cos (theta) * sin (phi))
    aVec.append (sin (theta) * sin (phi))
    aVec.append (cos (phi))
    aVec = normalizeVect (aVec)
    return aVec
    
def getDMS (angle : int | float) -> tuple[int | float]:
    ''' Convert an angle (in degrees) to a tuple of degrees, arc minutes and arc seconds '''
    degrees = int (angle)
    minutes = int ((angle-degrees)*60)
    seconds = (angle-degrees-minutes/60)*3600
    return degrees, minutes, seconds

def getDecimalDegrees (degrees : int | float, minutes : int | float, seconds : int | float) -> float:
    return degrees + minutes/60 + seconds/3600

def getDecimalDegreesFromTuple (t : tuple) -> float: 
    return getDecimalDegrees (t[0], t[1], t[2])
    
def rotateVector (vec : list, rotVec : list, angleRadians : int | float) -> list:
    '''
    Rotate a vector around a rotation vector. Based on Rodrigues formula. https://en.wikipedia.org/wiki/Rodrigues%27_formula 
    '''
    assert (len(vec) == len(rotVec) == 3)
    
    v1 = multScalarVect (cos(angleRadians), vec)
    v2 = multScalarVect (sin(angleRadians), crossProduct(rotVec, vec))
    v3 = multScalarVect (dotProduct(rotVec,vec)*(1-cos(angleRadians)), rotVec)
    result = addVecs (v1, addVecs(v2, v3))
    return result
    
# Course management

def modCourse (lon : int | float) -> float:
    ''' Transform a course angle into the compass range of (0,360) '''
    x = lon % 360
    return x    
   
def takeoutCourse (latLon : LatLon, course : int | float, speedKnots : int | float, timeHours : int | float) -> LatLon:
    ''' Calculates a trip movement. Simplified formula, not using great circles '''
    distance = speedKnots * timeHours
    distanceDegrees = distance / 60
    # The "stretch" is just taking care of narrowing longitudes on higher latitudes
    stretchAtStart = cos (degToRad (latLon.lat))
    diffLat = (cos (degToRad(course))*distanceDegrees)
    diffLon = (sin (degToRad(course))*distanceDegrees/stretchAtStart)
    return LatLon (latLon.lat+diffLat, latLon.lon+diffLon)
    
def angleBPoints (latLon1 : LatLon, latLon2 : LatLon) -> float: 
    normVec1 = toRectangular (latLon1)
    normVec2 = toRectangular (latLon2)
    dp = dotProduct (normVec1, normVec2)
    angle = acos (dp)
    return angle    
    
def distanceBetweenPoints (latLon1 : LatLon, latLon2 : LatLon) -> float:
    ''' Calculate distance between two points in km. Using great circles '''
    angle = angleBPoints (latLon1, latLon2) 
    distance = EARTH_RADIUS * angle
    return distance    

def KMtoNM (km : int | float) -> float: 
    ''' Convert from kilometers to nautical miles '''
    return (km / EARTH_CIRCUMFERENCE)*360*60
    
def NMtoKM (nm : int | float) -> float:
    ''' Convert from nautical miles to kilometers '''
    return (nm/(360*60))*EARTH_CIRCUMFERENCE
 
# Sextant calibration

class Sextant:
    def __init__  (self, graduationError : float): 
        self.graduationError = graduationError
 
def angleBetweenPoints (origin : LatLon, point1 : LatLon, point2 : LatLon) -> float:
    ''' Return the angle in degrees between two terrestrial targets (point1 and point2) as seen from the observation point (origin) '''
    originR = toRectangular (origin)
    point1R = toRectangular (point1)
    point2R = toRectangular (point2) 
    
    point1GC = normalizeVect (crossProduct (originR, point1R))
    point2GC = normalizeVect (crossProduct (originR, point2R))
    DP = dotProduct (point1GC, point2GC)
    return acos (DP) * (180 / pi)        
        
# Horizon

def getDipOfHorizon (hM : int | float) -> float:
    ''' Calculate dip of horizon in arc minutes 
    Parameter:
        hM : height in meters
    '''
    h = hM / 1000
    r = EARTH_RADIUS
    d = sqrt (h*(2*r + h))
    return (atan2 (d, r))*(180/pi)*60
    
def getIntersections (latlon1 : LatLon, latlon2 : LatLon, Angle1 : int | float, Angle2 : int | float, estimatedPosition : LatLon = None) -> LatLon | tuple:
    '''
    Get intersection of two circles on a spheric surface. At least one of the circles must be a small circle. 
    Based on https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere 
    '''
    assert (Angle1 >= 0 and Angle2 >= 0)
    assert (Angle1 < 90 or Angle2 < 90)  # Make sure one of the circles is a small circle
    # Get cartesian vectors a and b (from ground points)
    aVec = toRectangular (latlon1)     
    bVec = toRectangular (latlon2)           
          
    # Calculate axb
    abCross = crossProduct (aVec, bVec)
    abCross = normalizeVect (abCross)

    # These steps calculate q which is located halfway between our two intersections 
    p1 = multScalarVect (cos(degToRad(Angle2)), aVec)
    p2 = multScalarVect (-cos(degToRad(Angle1)), bVec)
    p3 = addVecs (p1, p2)
    p3 = normalizeVect (p3)
    p4 = crossProduct (abCross, p3)
    q = normalizeVect (p4)

    # Calculate a rotation angle
    try:
        if Angle1 < Angle2: 
            rho = acos (cos (degToRad(Angle1)) / (dotProduct (aVec, q)))
        else: 
            rho = acos (cos (degToRad(Angle2)) / (dotProduct (bVec, q)))
    except ValueError as exc:
        raise ValueError ("Bad sight data. Circles do not intersect") from exc

    # Calculate a rotation vector
    rotAxis = normalizeVect(crossProduct (crossProduct (aVec, bVec), q))
    
    # Calculate the two intersections by performing rotation of rho and -rho
    int1 = normalizeVect(rotateVector (q, rotAxis, rho))
    int2 = normalizeVect(rotateVector (q, rotAxis, -rho))
    retTuple = (toLatLon(int1), toLatLon(int2))
    if estimatedPosition == None:
        return retTuple
    else: 
        # Check which of the intersections is closest to our estimatedCoordinates        
        bestDistance = EARTH_CIRCUMFERENCE
        bestIntersection = None
        for ints in retTuple:
            theDistance = distanceBetweenPoints (ints, estimatedPosition)
            if theDistance < bestDistance:
                bestDistance = theDistance
                bestIntersection = ints
        assert (bestIntersection != None)
        return bestIntersection

# Atmospheric refraction
    
def getRefraction (apparentAngle : int | float) -> float:
    '''
    Calculate an estimation of the effect of atmospheric refraction using Bennett's formula
    See: https://en.wikipedia.org/wiki/Atmospheric_refraction#Calculating_refraction 
    
    Parameter:
        apparentAngle: The apparent (measured) altitude in degrees
    Returns:
        The refraction in arc minutes
    '''
    q = pi/180
    h = apparentAngle
    d = h + 7.31 / (h + 4.4)
    d2 = d*q
    return 1 / tan (d2)

# Data formatting

def getGoogleMapString (latLon : LatLon, numDecimals : int) -> str : 
    ''' Return a coordinate which can be used in Google Maps '''
    return str(round(latLon.lat,numDecimals)) + "," + str(round(latLon.lon,numDecimals))

def getRepresentation (ins : LatLon | tuple | list, numDecimals : int, lat=False) -> str:
    ''' Converts coordinate(s) to a string representation '''
    assert (numDecimals >= 0)
    if (type (ins) == LatLon): 
        ins = ins.getTuple ()
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

# Terrestrial Navigation

def getCircleForAngle (point1 : LatLon, point2 : LatLon, angle : int | float) -> tuple [LatLon, float] : 
    '''
    Calculate the circumscribed circle for two observed points with a specified angle, giving a circle to use for determining terrestrial position 
    '''
    point1V = toRectangular (point1)
    point2V = toRectangular (point2)     
    
    midPoint = normalizeVect (multScalarVect (1/2, addVecs (point1V, point2V)))
    # Use the basic formula for finding a circumscribing circle 
    A = distanceBetweenPoints (point1, point2) 
    B = (A/2) * (1 / tan (degToRad (angle / 2)))
    C = (A/4) * (1 / (sin (degToRad (angle / 2)) *\
                      cos (degToRad (angle / 2))))
    X = B - C 
    # calculate position and radius of circle
    rotationAngle = X / EARTH_RADIUS
    rotCenter = rotateVector (midPoint, normalizeVect(subtractVecs (point2V, point1V)), rotationAngle)
    radius = radToDeg(angleBPoints (toLatLon(rotCenter), point1))
    return toLatLon(rotCenter), radius
    
def getTerrestrialPosition (pointA1 : LatLon,\
                            pointA2 : LatLon,\
                            angleA : int | float,\
                            pointB1 : LatLon,\
                            pointB2 : LatLon,\
                            angleB : int | float,
                            estimatedPosition : LatLon = None) -> tuple [LatLon | tuple, LatLon, float, LatLon, float] : 
    '''
    Given two pairs of terrestial observations (pos + angle) determine the observer's position 
    '''
    A = getCircleForAngle (pointA1, pointA2, angleA)
    B = getCircleForAngle (pointB1, pointB2, angleB)
    # Finally compute the intersection. Since we require an estimated position we will eliminate the false intersection. 
    return getIntersections (A[0], B[0], A[1], B[1], estimatedPosition), A[0], A[1], B[0], B[1]

# Celestial Navigation

class Sight :
    '''  Object representing a sight (star fix '''
    def __init__ (self, \
                  object_name : str, \
                  time_year : int, \
                  time_month : int, \
                  time_day : int, \
                  time_hour : int, \
                  time_minute : int, \
                  time_second : int, \
                  gha_time_0_degrees : int, \
                  gha_time_0_minutes : int | float, \
                  gha_time_1_degrees : int, \
                  gha_time_1_minutes : int | float, \
                  decl_time_0_degrees : int, \
                  decl_time_0_minutes : int | float, \
                  decl_time_1_degrees : int, \
                  decl_time_1_minutes : int | float, \
                  measured_alt_degrees : int | float, \
                  measured_alt_minutes : int | float, \
                  measured_alt_seconds : int | float, \
                  sha_diff_degrees : int | float = 0, \
                  sha_diff_minutes : int | float = 0, \
                  observer_height : int | float = 0, \
                  artificial_horizon : bool = False, \
                  index_error_minutes : int = 0, \
                  semi_diameter_correction : int | float = 0,\
                  sextant : Sextant = None):
        self.object_name          = object_name
        self.time_year            = time_year
        self.time_month           = time_month
        self.time_day             = time_day
        self.time_hour            = time_hour            
        self.time_minute          = time_minute          
        self.time_second          = time_second          
        self.gha_time_0           = getDecimalDegrees (gha_time_0_degrees, gha_time_0_minutes, 0)
        self.gha_time_1           = getDecimalDegrees (gha_time_1_degrees, gha_time_1_minutes, 0)
        self.decl_time_0          = getDecimalDegrees (decl_time_0_degrees, decl_time_0_minutes, 0)      
        self.decl_time_1          = getDecimalDegrees (decl_time_1_degrees, decl_time_1_minutes, 0)        
        self.measured_alt         = getDecimalDegrees (measured_alt_degrees, measured_alt_minutes, measured_alt_seconds)
        self.sha_diff             = getDecimalDegrees (sha_diff_degrees, sha_diff_minutes, 0)                
        self.observer_height      = observer_height
        '''
        if not (self.object_name != "Sun" or self.sha_diff == 0): 
            raise ValueError ("The Sun should have a sha_diff parameter != 0") 
        '''
        if (self.observer_height != 0 and artificial_horizon == True):
            raise ValueError ("observer_height should be == 0 when artificial_horizon == True") 
        if sextant != None:
            self.__correctForGraduationError (sextant)
        if index_error_minutes != 0:
            self.__correctForIndexError (index_error_minutes)
        if artificial_horizon:
            self.__correctForArtficialHorizon ()
        if semi_diameter_correction != 0:
            self.__correctSemiDiameter (semi_diameter_correction)

        self.__correctDipOfHorizon ()
        self.__correctForRefraction ()
        self.GP = self.__calculateGP ()
    
    def __correctForGraduationError (self, sextant : Sextant):
        self.measured_alt /= sextant.graduationError
    
    def __correctSemiDiameter (self, sd):
        self.measured_alt += sd/60
    
    def __correctForIndexError (self, ie):
        self.measured_alt -= ie/60
        
    def __correctForArtficialHorizon (self):
        self.measured_alt /= 2
        
    def __correctDipOfHorizon (self):
        if self.observer_height == 0:
            return  
        self.measured_alt += getDipOfHorizon (self.observer_height)/60
    
    def __correctForRefraction (self):
        self.measured_alt -= getRefraction (self.measured_alt)/60
    
    def __calculateGP (self) -> LatLon:
        
        minSecContribution = self.time_minute/60 + self.time_second/3600
        
        resultLON = modLON (- \
        ((self.gha_time_0 + self.sha_diff) + \
        ((self.gha_time_1 - self.gha_time_0))*minSecContribution))
 
        resultLAT = \
        self.decl_time_0 + (self.decl_time_1 - self.decl_time_0)*minSecContribution
        
        return LatLon (resultLAT, resultLON)

    def getAngle (self):
        return (90-self.measured_alt)
    
    def getRadius (self):
        return (self.getAngle()/360)*EARTH_CIRCUMFERENCE
    
    def getDistanceFrom (self, p : LatLon) -> float:
        pDistance = distanceBetweenPoints (p, self.GP)
        theRadius = self.getRadius ()
        return pDistance - theRadius
        
class SightPair:
    def __init__ (self, sf1 : Sight, sf2 : Sight):
        self.sf1 = sf1
        self.sf2 = sf2
        
    def getIntersections (self, estimatedPosition = None) -> tuple: 
        return getIntersections (self.sf1.GP,\
                                 self.sf2.GP,\
                                 self.sf1.getAngle(), self.sf2.getAngle(),\
                                 estimatedPosition)        

class SightCollection:
    def __init__ (self, sfList : list):
        if (len (sfList) < 2):
            raise ValueError ("SightCollection should have at least two sights") 
        self.sfList = sfList

    def getIntersections (self, limit : int | float = 100, estimatedPosition = None):
        nrOfFixes = len(self.sfList)
        assert (nrOfFixes >= 2)
        if (nrOfFixes == 2):
            # For two star fixes just use the algorithm of SightPair.getIntersections
            intersections = SightPair (self.sfList[0],self.sfList[1]).getIntersections(estimatedPosition)
            return intersections
        elif (nrOfFixes >= 3):
            # For >= 3 star fixes perform pairwise calculation on every pair of fixes and then run a sorting algorithm 
            coords = []
            # Perform pairwise sight reductions
            for i in range (nrOfFixes):
                for j in range (i+1, nrOfFixes):
                    p = SightPair (self.sfList [i], self.sfList [j])
                    pInt = p.getIntersections (estimatedPosition)
                    if pInt != None:
                        if (type (pInt) == tuple or type (pInt) == list):
                            for k in range (len(pInt)):
                                coords.append (pInt[k])
                        elif (type (pInt) == LatLon):
                            coords.append (pInt)
                        else:
                            assert (False)                            
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
            # nrOfSortedDists = len (sortedDists)
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
            #print ("BEST COORDINATES")
            fineSorting = False
            if (fineSorting):
                for cp1 in chosenPoints:
                    print (getRepresentation (coords[cp1],1))  
                    for cp2 in chosenPoints:
                        if cp1 != cp2:
                            dist = distanceBetweenPoints (coords[cp1], coords[cp2])
                            if dist > limit:
                                # Probably multiple possible observation points. 
                                # Best option is to perform sight reduction on 2 sights and select the correct point manually.
                                raise ValueError ("Cannot sort multiple intersections to find a reasonable set of coordinates")
            print ("MEAN VALUE COORDINATE from multi-point sight data.")              
            summationVec = [0,0,0]
            # Make a mean value on the best intersections. 
            for cp in chosenPoints: 
                selectedCoord = coords [cp]
                rectVec = toRectangular (selectedCoord)
                summationVec = addVecs (summationVec, multScalarVect (1/nrOfChosenPoints, rectVec))
            summationVec = normalizeVect (summationVec)
            return toLatLon (summationVec)
        
class SightTrip:
    ''' Object used for dead-reckoning in daytime (with only Sun sights)  '''
    def __init__ (self, \
                       sightStart : Sight,\
                       sightEnd : Sight,\
                       estimatedStartingPoint : LatLon,\
                       courseDegrees : int | float,\
                       speedKnots : int | float):
        self.sightStart                = sightStart
        self.sightEnd                  = sightEnd
        self.estimatedStartingPoint    = estimatedStartingPoint   
        self.courseDegrees             = courseDegrees
        self.speedKnots                = speedKnots
        self.__calculateTimeHours ()
        
        
    def __calculateTimeHours (self):
        dt1 = datetime(self.sightStart.time_year,\
                       self.sightStart.time_month,\
                       self.sightStart.time_day,\
                       self.sightStart.time_hour,\
                       self.sightStart.time_minute,\
                       self.sightStart.time_second,\
                       tzinfo=timezone.utc)
        it1 = int(dt1.timestamp())
        dt2 = datetime(self.sightEnd.time_year,\
                       self.sightEnd.time_month,\
                       self.sightEnd.time_day,\
                       self.sightEnd.time_hour,\
                       self.sightEnd.time_minute,\
                       self.sightEnd.time_second,\
                       tzinfo=timezone.utc)
        it2 = int(dt2.timestamp())      
        self.timeHours = (it2 - it1) / 3600
        
    def __calculateDistanceToTarget (self, angle : int | float, aVec : list, bVec : list) -> tuple:
        rotationAngle = degToRad (angle)
        rotatedVec = rotateVector (bVec, aVec, rotationAngle)
        rotatedLatLon = toLatLon (rotatedVec)
        takenOut = takeoutCourse (rotatedLatLon, self.courseDegrees, self.speedKnots, self.timeHours)
         
        dbp = distanceBetweenPoints (takenOut, self.sightEnd.GP) - self.sightEnd.getRadius()
        return dbp, takenOut, rotatedLatLon
        
    def getIntersections (self) -> tuple:
        # Calculate intersections
        pair = SightPair (self.sightStart, self.sightEnd)
        bestIntersection = pair.getIntersections (estimatedPosition = self.estimatedStartingPoint)
        
        # Determine angle of the intersection point on sightStart small circle         
        aVec = toRectangular (self.sightStart.GP)
        bVec = toRectangular (bestIntersection)
        assert (type(bestIntersection) == LatLon)
 
        # Apply Newtons method to find the location
        currentRotation = 0
        delta = 0.0001
        limit = 0.001
        iterLimit = 100
        iterCount = 0
        # ready = False
        takenOut = None
        rotated  = None
        while iterCount < iterLimit:
            distanceResult, takenOut, rotated = self.__calculateDistanceToTarget (currentRotation, aVec, bVec)
            if abs (distanceResult) < limit:
                break
            distanceResult2, takenOut, rotated = self.__calculateDistanceToTarget (currentRotation+delta, aVec, bVec)
            derivative = (distanceResult2 - distanceResult) / delta
            currentRotation = currentRotation - (distanceResult)/derivative
            iterCount += 1
        if iterCount >= iterLimit:
            raise ValueError ("Cannot calculate a trip vector") 
        else:
            return takenOut, rotated


