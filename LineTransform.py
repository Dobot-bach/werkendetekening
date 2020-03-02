"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def afstand(c1,c2):
    a1 = c1[0]-c2[0]
    a2 = c1[1]-c2[1]
    afst = math.sqrt(a1**2+a2**2)
    return afst


def main(argv):
    ## [load]
    default_file = 'bumba.jpg'
    minlen = 2
    maxlen = 10







    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    ## [load]

    ## [edge_detection]
    # Edge detection
    dst = cv.Canny(src, 50, 200, None, 3)
    ## [edge_detection]

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    ## [hough_lines]
    #  Standard Hough Line Transform
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    ## [hough_lines]
    ## [draw_lines]
    # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

            cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
    ## [draw_lines]

    ## [hough_lines_p]
    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 2, 1, None, 0, 0)
    ## [hough_lines_p]
    ## [draw_lines_p]
    # Draw the lines
    coorda = [] #array van coordinaten
    if linesP is not None:
        File1 = open("tabel2", "w")
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
            coorda.append([l[0], l[1]])
            File1.write("[" + str(l[0]) + " " + str(l[1]) + "]" + "\n")
        File1.close()

    coorda = sorted(coorda) #array of coordinates

    groepnr = 0
    coordgroepen = [] #dictionary of coordinates
    coordgroepen.append([coorda[0]])
    teller = 0
    while len(coorda) > 0:
        afstanden = []
        weg = []
        for i in coorda:
            afst = afstand(i, coordgroepen[groepnr][-1])
            if afst < minlen:
                weg.append(i)
            elif afst < maxlen:
                afstanden.append([afst, i])
                teller += 1
        for i in weg:
            coorda.remove(i)
        if len(afstanden) == 0:
            if len(coorda) > 0:
                coordgroepen.append([coorda[0]])
            groepnr += 1
            teller = 0
        else:
            afstanden.sort()
            coordgroepen[groepnr].append(afstanden[0][1])
            coorda.remove(afstanden[0][1])


    for i in coordgroepen:
        xs = [x[0] for x in i]
        ys = [x[1] for x in i]
        plt.plot(xs, ys)
    plt.show()

    ## [draw_lines_p]

    ## [imshow]
    # Show results
    # cv.imshow("Source", src)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)



    ## [imshow]
    ## [exit]
    # Wait and Exit
    cv.waitKey()

    return 0
    ## [exit]


if __name__ == "__main__":
    main(sys.argv[1:])
