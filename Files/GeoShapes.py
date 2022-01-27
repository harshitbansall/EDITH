import math
#################################################################################################################################
class geoShapeAreas:
    def areaofSquare(magLen):
        return (magLen*magLen)
    def areaofRectangle(magLen,magWidth):
        return (2*(magLen+magWidth))
    def areaofCircle(magRad):
        return (math.pi*magRad*magRad)
    def areaofCube(magLen):
        return (6*magLen*magLen)
    def areaofCuboid(magLen,magWidth,magHeight):
        return (2*(magLen*magWidth+magWidth*magHeight+magLen*magHeight))
    def areaofCylinder(magRad,magHeight):
        return (2*math.pi*magRad*(magRad+magHeight))
    def areaofCone(magRad,magHeight):
        slantHeight=(magRad**2+magHeight**2)**0.5
        return (math.pi*magRad*(magRad+slantHeight))
    def areaofSphere(magRad):
        return (4*math.pi*magRad*magRad)
    def areaofHemisphere(magRad):
        return (3*math.pi*magRad*magRad)
class geoShapeVolumes:
    def volumeofCube(magLen):
        return (magLen**3)
    def volumeofCuboid(magLen,magWidth,magHeight):
        return (magLen*magWidth*magHeight)
    def volumeofCylinder(magRad,magHeight):
        return (math.pi*magRad*magRad*magHeight)
    def volumeofCone(magRad,magHeight):
        return (math.pi*magRad*magRad*magHeight/3)
    def volumeofSphere(magRad):
        return (4*math.pi*(magRad**3)/3)
    def volumeofHemisphere(magRad):
        return (2*math.pi*(magRad**3)/3)
#################################################################################################################################
class findDimentions:
    def findObject(query):
        geoShapes=["square","rectangle","circle","cube","cuboid","cylinder","cone","sphere","hemisphere"]
        for x in query.split():
            for y in geoShapes:
                if x==y:
                    return y      
    def findLength(query):
        if "length" in query:
            return (float(query.split()[query.split().index("length")+1]))
        if "side" in query:
            return (float(query.split()[query.split().index("side")+1]))
    def findBreadth(query):
        if "breadth" in query:
            return (float(query.split()[query.split().index("breadth")+1]))
        if "width" in query:
            return (float(query.split()[query.split().index("width")+1]))
    def findHeight(query):
        if "height" in query:
            return (float(query.split()[query.split().index("height")+1]))
    def findRadius(query):
        if "radius" in query:
            return (float(query.split()[query.split().index("radius")+1]))
#################################################################################################################################
def mainGeoShapes(query):
    if "what is the" in query:
        whatisAsked=query.split()[query.split().index("what")+3]
    elif "what is" in query:
        whatisAsked=query.split()[query.split().index("what")+2]
    elif "find the" in query:
        whatisAsked=query.split()[query.split().index("find")+2]
    elif "find" in query:
        whatisAsked=query.split()[query.split().index("find")+1]
    elif "calculate" in query:
        whatisAsked=query.split()[query.split().index("calculate")+1]
    objectName=findDimentions.findObject(query)
    if whatisAsked=="area":
        if objectName=="square":
            magLen=findDimentions.findLength(query)
            area=geoShapeAreas.areaofSquare(magLen)
        if objectName=="rectangle":
            magLen,magBreadth=findDimentions.findLength(query),findDimentions.findBreadth(query)
            area=geoShapeAreas.areaofRectangle(magLen,magBreadth)
        if objectName=="circle":
            magRad=findDimentions.findRadius(query)
            area=geoShapeAreas.areaofCircle(magRad)
        if objectName=="cube":
            magLen=findDimentions.findLength(query)
            area=geoShapeAreas.areaofCube(magLen)
        if objectName=="cuboid":
            magLen,magWidth,magHeight=findDimentions.findLength(query),findDimentions.findBreadth(query),findDimentions.findHeight(query)
            area=geoShapeAreas.areaofCuboid(magLen,magWidth,magHeight)
        if objectName=="cylinder":
            magRad,magHeight=findDimentions.findRadius(query),findDimentions.findHeight(query)
            area=geoShapeAreas.areaofCylinder(magRad,magHeight)
        if objectName=="cone":
            magRad,magHeight=findDimentions.findRadius(query),findDimentions.findHeight(query)
            area=geoShapeAreas.areaofCone(magRad,magHeight)
        if objectName=="sphere":
            magRad=findDimentions.findRadius(query)
            area=geoShapeAreas.areaofSphere(magRad)
        if objectName=="hemisphere":
            magRad=findDimentions.findRadius(query)
            area=geoShapeAreas.areaofHemisphere(magRad)
        return ("Area of this "+objectName.title()+" is "+str(round(area,3))+" square units.")
    elif whatisAsked=="volume":
        if objectName=="cube":
            magLen=findDimentions.findLength(query)
            volume=geoShapeVolumes.volumeofCube(magLen)
        if objectName=="cuboid":
            magLen,magWidth,magHeight=findDimentions.findLength(query),findDimentions.findBreadth(query),findDimentions.findHeight(query)
            volume=geoShapeVolumes.volumeofCuboid(magLen,magWidth,magHeight)
        if objectName=="cylinder":
            magRad,magHeight=findDimentions.findRadius(query),findDimentions.findHeight(query)
            volume=geoShapeVolumes.volumeofCylinder(magRad,magHeight)
        if objectName=="cone":
            magRad,magHeight=findDimentions.findRadius(query),findDimentions.findHeight(query)
            volume=geoShapeVolumes.volumeofCone(magRad,magHeight)
        if objectName=="sphere":
            magRad=findDimentions.findRadius(query)
            volume=geoShapeVolumes.volumeofSphere(magRad)
        if objectName=="hemisphere":
            magRad=findDimentions.findRadius(query)
            volume=geoShapeVolumes.volumeofHemisphere(magRad)
        return ("Volume of this "+objectName.title()+" is "+str(round(volume,3))+" cube units.")
#################################################################################################################################
