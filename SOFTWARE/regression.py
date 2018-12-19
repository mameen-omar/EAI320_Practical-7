#http://www.statisticshowto.com/probability-and-statistics/regression-analysis/find-a-linear-regression-equation/
#Mohamed Ameen Omar
#16055323
#EAI 320 - Practical 7 2018
#Question 2
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy

class regression:
    def __init__(self, filename):
        self.data = numpy.genfromtxt(filename,delimiter=',') #2d array
        self.A = 0
        self.B = 0

    def LinearRegression(self):
        co_efficients = self.LRgetCoEff()
        self.A = co_efficients[0]
        self.B = co_efficients[1]
        errors = []
        for x in range(0,len(self.data)):
            temp = self.regressionLine(self.data[x][0])
            error =  numpy.abs(temp-self.data[x][1]) #since x's are the same
            errors.append(error)
        print("Plotting the Linear Regression Line given by y = Bx+A")
        print("With A =", self.A, end = "")
        print(" and B =", self.B)
        print()
        self.plotRegressionLine(copy.deepcopy(self.data))
        print("The Euclidean Error for the true output value and the ", end  = "")
        print(" predicted value is given below:")
        for x in range(0, len(self.data)):
            print("Input =", self.data[x][0], end = "")
            print(", error is = ", errors[x])
        print()
        print("The Average Error for the known data and the Linear Regression Line is:", (sum(errors)/len(errors)))

    def plotRegressionLine(self,data):
        x = numpy.arange(0,88)
        plt.plot(self.regressionLine(x), c = 'g', linewidth = 2, label = 'Regression Line')
        toPlot = numpy.transpose(data)
        plt.scatter(toPlot[0],toPlot[1], s = 100, c = 'b', label = 'Data Points')
        plt.legend(loc = 'upper left')
        plt.xlabel('Age (years)')
        plt.ylabel('Sight distance (m)')
        plt.title('Linear Regression Line (best fit) with the raw data points', loc ='center')
        plt.scatter(16,self.regressionLine(16), s = 100, c = 'y', marker = 'D', label = 'Predicted sight distance for 16 year old') #16
        plt.scatter(85,self.regressionLine(85), s = 100, c = 'y', marker = 'D', label = 'Predicted sight distance for 85 year old') #85
        plt.show()

    #returns an array of coefficents for least squares regression line
    def LRgetCoEff(self):
        sumY = 0
        sumX = 0
        sumXY = 0
        sumXsqrd = 0
        for x in range(0, len(self.data)):
            sumX = sumX + self.data[x][0]
            sumY = sumY+self.data[x][1]
            sumXY = sumXY + (self.data[x][0] * self.data[x][1])
            sumXsqrd = sumXsqrd + numpy.square(self.data[x][0])
        a = 0
        b = 0
        #compute a
        a = sumY * sumXsqrd
        a = a-(sumX*sumXY)
        temp = len(self.data) * sumXsqrd
        temp = temp - numpy.square(sumX)
        a = a/temp
        b = len(self.data) * sumXY
        b = b-(sumX*sumY)
        temp = len(self.data) * sumXsqrd
        temp = temp - numpy.square(sumX)
        b = b/temp
        return([a,b])

    def regressionLine(self,x):
        return ((self.B*x)+self.A)

#########################KNN#############################################
    #returns the error if the input data is used
    def regressionKNNError(self,k = 1):
        temp = numpy.transpose(copy.deepcopy(self.data))
        inputs = temp[0]
        outputs = temp[1]
        numErrors = 0
        for x in range(0,len(inputs)):
            error = numpy.abs(self.regressionKNNoutput(k,inputs[x]) - outputs[x])
            if(error != 0):
                numErrors = numErrors+1
        return numErrors

    #returns the output based off of the KNN regression algo
    def regressionKNNoutput(self,k, input):
        temp = numpy.transpose(copy.deepcopy(self.data))
        inputs = temp[0]
        outputs = temp[1]
        distance = []
        estimatedOutput = []
        for x in range(0,len(inputs)):
            distance.append(numpy.abs(input-inputs[x]))
            estimatedOutput.append(outputs[x])
        #sort arrays in ascending order
        swap = True
        while(swap is True):
            swap = False
            for x in range(0,len(distance)-1):
                if(distance[x] > distance[x+1]):
                    swap = True
                    temp = distance[x]
                    distance[x] = distance[x+1]
                    distance[x+1] = temp
                    temp = estimatedOutput[x]
                    estimatedOutput[x] = estimatedOutput[x+1]
                    estimatedOutput[x+1] = temp
        knnOut = 0
        for x in range(0, k):
            knnOut = knnOut + estimatedOutput[x]
        knnOut = knnOut/k
        return knnOut #return the average

    def plotKNNregression(self,k):
        x = []
        for y in range(0,100):
            x.append(self.regressionKNNoutput(k,y))
        toPlot = numpy.transpose(self.data)
        #for y in toPlot[0]:
        #    x.append(self.regressionKNNoutput(k,y))
        #plt.plot(toPlot[0], x,c = 'g', linewidth = 2, label = 'KNN Regression Line')
        plt.plot( x,c = 'g', linewidth = 2, label = 'KNN Regression Line')
        plt.scatter(toPlot[0],toPlot[1], s = 100, c = 'b', label = 'Data Points')
        plt.legend(loc = 'upper left')
        plt.xlabel('Age (years)')
        plt.ylabel('Sight distance (m)')
        title = 'KNN Regression Line (best fit) with the raw data points (K = ' + str(k) + ')'
        plt.title(title, loc ='center')
        plt.show()

temp = regression("signdist.data")
temp.LinearRegression() #Question 2a/b
print()
print("Predicted sight distance for 16 year old is (LR):")
print(temp.regressionLine(16)) #2c
print()
print("Predicted sight distance for 85 year old is (LR):") #2d
print(temp.regressionLine(85))


#KNN regression below

k = 3
print()
print("Plot for KNNN regression with inputs from 0 to 100 and K =", k, end = " ")
print(":")
temp.plotKNNregression(k)
print()
print("Predicted sight distance for 16 year old is (KNNR, K =", k, end = "" )
print("):")
print(temp.regressionKNNoutput(k,16))
print()
print("Predicted sight distance for 85 year old is (KNNR, K =", k, end = "" )
print("):")
print(temp.regressionKNNoutput(k,85))
