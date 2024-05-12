EARTH_CIRCUMFERENCE = 40075

# Utility routines

def crossProduct (vec1, vec2) :
    print (type(vec1))
    print (type(vec2))
    assert (type (vec1) == list and type(vec2) == list) 
    assert (len (vec1) == 3 and len (vec2) == 3)
    retVal = [0, 0, 0]
    retVal [0] = vec1 [1]*vec2[2] - vec1[2]*vec2[1]
    retVal [1] = vec1 [2]*vec2[0] - vec1[0]*vec2[2]
    retVal [2] = vec1 [0]*vec2[1] - vec1[1]*vec2[0]
    return retVal    

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
        
    def getRadius (self):
        measured_alt_decimal = self.measured_alt_degrees + \
                               self.measured_alt_minutes/60 + \
                               self.measured_alt_seconds/3600
        return ((90-measured_alt_decimal)/360)*EARTH_CIRCUMFERENCE
        
    def getGP (self):
        pass
        
class starFixPair:
    def __init__ (self, sf1, sf2):
        self.sf1 = sf1
        self.sf2 = sf2

    def getIntersections (self):
        pass
        
class starFixCollection:
    def __init__ (self, sfList):
        self.sfList = sfList

    def getIntersections (self):
        pass        
        
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
              measured_alt_seconds = 1.8, \
              )
              
print (a.getRadius())

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
              measured_alt_seconds = 18, \
              )

print (b.getRadius())

starFixPair = starFixPair (a, b)
intersections = starFixPair.getIntersections ()

vec1 = [1, 0, 0]
vec2 = [0, 1, 0]

print (crossProduct (vec1, vec2))



