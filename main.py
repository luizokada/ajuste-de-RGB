import numpy as np
import cv2 as cv


def isRegularInterval(matiz,x):
    return np.mod((matiz + x)/2, 180) >np.mod((matiz - x)/2, 180) 

def getInterval(matiz,x):
    start = np.mod((matiz - x)/2, 180)
    end = np.mod((matiz + x)/2, 180)
    return start,end

def getIndexOnInterval(H,matiz,x):
    start,end = getInterval(matiz,x)
    indexOfStartInterval = H >= start
    indexOfEndInterval = H <= end
    if(isRegularInterval(matiz, x)):
        return indexOfStartInterval & indexOfEndInterval    
    else:
        return indexOfStartInterval | indexOfEndInterval

def alterH(H, matiz, x):
    indexes = getIndexOnInterval(H, matiz, x)
    H = H.astype(np.uint16)
    H[indexes] = np.mod(H[indexes] + 90, 180).astype(np.uint8)
    H = H.astype(np.uint8)
    return H

def getNewHSV(originalHSV,m,x):
    H,S,V = cv.split(originalHSV)
    H = alterH(H,m,x)
    newHSV = cv.merge([H,S,V])
    return newHSV
    
def convertImgToHSV(img):
    return cv.cvtColor(img, cv.COLOR_BGR2HSV)

def getNewImage(imgName,imgExt,img, matiz, x):
    originalHSV = convertImgToHSV(img)
    newHSV = getNewHSV(originalHSV,matiz,x)
    imageRGB = cv.cvtColor(newHSV, cv.COLOR_HSV2BGR)
    cv.imshow('Imagem Com as matiz alterada', imageRGB)
    cv.imwrite('./results/{0}M{1}X{2}.{3}'.format(imgName,str(matiz),str(x),imgExt),imageRGB)
    cv.waitKey(5000)
    return



def getUserData():
    imgPath = input("Digite o caminho da imagem (demtro da pasta images) = ")
    img = cv.imread('./images/' + imgPath)
    matiz = int(input("Digite a Matiz = "))
    x = int(input("Didite o valor de X = "))
    splitedPath = imgPath.split(".")
    imgName = splitedPath[0]
    imgExt = splitedPath[1]
    return imgName,imgExt,img,matiz,x
    
def main():
    
    imgName,imgExt,img,matiz,x = getUserData()
    getNewImage(imgName,imgExt,img,matiz,x)

if __name__ ==  '__main__':
    main()