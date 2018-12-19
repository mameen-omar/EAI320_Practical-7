import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy
#Mohamed Ameen Omar
#16055323
#EAI 320 - Practical 7 2018
#Question 1
class KNN:
    def __init__(self, trainDataFile, trainLabelFile,testDataFile, testLabelFile):
        self.trainColors = ["b", "g", "r"]
        self.testColors = ["y", "k", "m"]
        self.labels = ["Iris Setosa", "Iris Versicolour", "Iris Virginica"]
        self.trainData = numpy.genfromtxt(trainDataFile,delimiter=',')
        self.trainLabels = numpy.genfromtxt(trainLabelFile,delimiter=',')
        self.testData = numpy.genfromtxt(testDataFile,delimiter=',')
        self.testLabels = numpy.genfromtxt(testLabelFile,delimiter=',')
        self.trainDict = {1:[], 2:[], 3:[]}
        self.testDict = {1:[], 2:[], 3:[]}
        self.storeTestData() #keys are the labels(1,2,3) and values are the attributes
        self.storeTrainData()

    def storeTrainData(self):
        for x in range(0,len(self.trainLabels)):
            self.trainDict[self.trainLabels[x]].append(self.trainData[x])

    def storeTestData(self):
        for x in range(0,len(self.testLabels)):
            self.testDict[self.testLabels[x]].append(self.testData[x])

    def plotData(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        for key in self.trainDict.keys():
            toPlot = numpy.transpose(self.trainDict[key]) #toPlot is a matrix of the co ordinates for each variable
            # ie - toPlot[0] is all the x values
            color = self.trainColors[key-1]
            name = self.labels[key-1]
            ax.scatter(toPlot[0], toPlot[1], toPlot[2], s = 110, c = color, marker = '.',
                       label = name)
        for key in self.testDict.keys():
            toPlot = numpy.transpose(self.testDict[key]) #toPlot is a matrix of the co ordinates for each variable
            # ie - toPlot[0] is all the x values
            color = self.testColors[key-1]
            name = (self.labels[key-1] + " - Test samples")
            ax.scatter(toPlot[0], toPlot[1], toPlot[2], s = 110, c = color, marker = 'D',
                       label = name)
        ax.set_xlabel('Sepal Length in cm')
        ax.set_ylabel('Sepal Width in cm')
        ax.set_zlabel('Petal Length in cm')
        plt.legend(loc = 'upper left')
        plt.title("Question 1a")
        plt.show()

    #runs the knn with the number of neighbors passed in
    #for every test sample classify it
    #retuns number of errors
    def _knn(self, k = 1):
        numErrors = 0
        for key in self.testDict.keys():
            for sample in range(0, len(self.testDict[key])):
                isError = self.knnClassify(key,self.testDict[key][sample],k)
                if(isError is True):
                    numErrors = numErrors+1
        return numErrors

    #key is what the testSample actually is
    #testSample is an array of the attributes
    #k is the number of neighbours
    #classifies testSample, returns a boolean if it is a error or not
    def knnClassify(self,key,testSample,k):
        neighborsDist = []
        neighborsLabel = []
        ###get Euclidean Distance for every train to the testSample
        for xkey in self.trainDict.keys():
            for sample in range(0, len(self.trainDict[xkey])):
                neighborsDist.append(self.getEuclideanDistance(testSample,self.trainDict[xkey][sample]))
                neighborsLabel.append(xkey)

        #sort arrays in ascending order
        swap = True
        while(swap is True):
            swap = False
            for x in range(0,len(neighborsDist)-1):
                if(neighborsDist[x] > neighborsDist[x+1]):
                    swap = True
                    temp = neighborsDist[x]
                    neighborsDist[x] = neighborsDist[x+1]
                    neighborsDist[x+1] = temp
                    temp = neighborsLabel[x]
                    neighborsLabel[x] = neighborsLabel[x+1]
                    neighborsLabel[x+1] = temp
        tempLabel = self.classify(neighborsLabel,k)
        #print("classified label:" ,tempLabel)
        #print("THIS KEY IS", key)
        return(tempLabel != key)

    #classifies based off of number of nearest neighbours
    #kWinner is a running count of the number of each class occurenes
    def classify(self, labels, k):
        if(k == 1):
            return labels[0]
        kWinner = [0,0,0] #0 - label 1
        for x in range(0,k):
            label = labels[x]
            kWinner[label-1] = kWinner[label-1] +1 #increment that label
        max_value = max(kWinner) #maximum value
        return (kWinner.index(max_value) +1) #return the index at which the max is found+1 (the classified label)

    #returns Euclidean Distance
    def getEuclideanDistance(self,testSample,trainSample):
        dist = 0
        for x in range(0,4):
            dist += numpy.square(testSample[x]-trainSample[x])
        return numpy.sqrt(dist)

    def knnVariableK(self):
        tempError = 1
        errors = []
        k = 1
        while(tempError != 0 or k%2 != 0):
            tempError = self._knn(k)
            errors.append(tempError)
            print("The Error for ", end = "")
            print(k, end = "")
            print(" nearest neighbours (k) is ", tempError)
            k=k+1
        #plot
        x = []
        for t in range(0,len(errors)):
            x.append(t+1)
        print("Plotting Errors vs Number of neighbours")
        plt.plot(x,errors, linewidth = 2)
        plt.plot(x,errors, 'bo', c = 'g', markersize = 5)
        plt.title('Plot of the Number of Errors Vs Number of nearest neighbours')
        plt.ylabel('Number of Errors')
        plt.xlabel('Number of Neighbours')
        plt.xlim(-0.1,8) #limits set to make the plot look more pretty
        plt.ylim(0,3.5)
        plt.show()

x = KNN("trainData.data", "trainLabels.data", "testData.data", "testLabels.data")
#x.plotData() #Question 1a
#print("Conducting KNN with number of closest Neighbours = 1")
#print("The number of errors are =", x._knn(1)) #Question 1b
x.knnVariableK()#Question 1c
