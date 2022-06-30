
import math


def intersectLines(pt1, pt2, ptA, ptB):
    DET_TOLERANCE = 0.00000001

    # the first line is pt1 + r*(pt2-pt1)
    # in component form:
    x1, y1 = pt1;
    x2, y2 = pt2
    dx1 = x2 - x1;
    dy1 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x, y = ptA;
    xB, yB = ptB;
    dx = xB - x;
    dy = yB - y;


    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < DET_TOLERANCE: return 0

    # now, the determinant should be OK
    DETinv = 1.0 / DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy * (x - x1) + dx * (y - y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x - x1) + dx1 * (y - y1))

    # return the average of the two descriptions
    xi = (x1 + r * dx1 + x + s * dx) / 2.0
    yi = (y1 + r * dy1 + y + s * dy) / 2.0
    if float(max(x1,x2))>float(xi)>float(min(x1,x2)) and float(max(y1,y2))>float(yi)>float(min(y1,y2)) and float(max(x,x1,x2,xB))>float(xi)>float(min(x,x1,x2,xB)) and float(max(y,y1,y2,yB))>float(yi)>float(min(y,y1,y2,yB)):
        return 1
    else:
        return 0



def testIntersection(pt1, pt2, ptA, ptB):
    """ prints out a test for checking by hand... """
    result = intersectLines(pt1, pt2, ptA, ptB)
    print(result)
def orientation(p,q,r):
    val=(q[1]-p[1])*(r[0]-q[0])-(q[0]-p[0])*(r[1]-q[1])
    if val==0:
        return 0
    if val>0:
        return 1
    else:
        return 2
def onSegment(p,q,r):
    if (q[0]<=max(p[0],r[0]) and q[0]>=min(p[0],r[0]) and q[1]<=max(p[1],r[1]) and q[1]>=min(p[1],r[1])):
        return True
    return False

def dointersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if (o1 != o2 and o3 != o4):
        return True
    if (o1 == 0 and onSegment(p1, p2, q1)):
        return True
    if (o2 == 0 and onSegment(p1, q2, q1)):
        return True
    if (o3 == 0 and onSegment(p2, p1, q2)):
        return True
    if (o4 == 0 and onSegment(p2, q1, q2)):
        return True
    return False




if __name__ == "__main__":
    pt1 = (10, 10)
    pt2 = (20, 20)

    pt3 = (10, 20)
    pt4 = (20, 10)

    pt5 = (40, 20)

    print(dointersect(pt1, pt2, pt3, pt4))
    print(dointersect(pt1, pt3, pt2, pt4))
    testIntersection(pt1, pt2, pt4, pt5)
