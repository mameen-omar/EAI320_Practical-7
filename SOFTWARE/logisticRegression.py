import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import csv
import numpy
#https://machinelearningmastery.com/logistic-regression-tutorial-for-machine-learning/
#Mohamed Ameen Omar
#16055323
#EAI 320 - Practical 7 2018
#Question 3
class logisticRegression:
    def __init__(self, inputsFileName, outputsFileName, epochs, learningRate):
        self.inputs = self.normalize(numpy.genfromtxt(inputsFileName,delimiter=','))
        self.outputs = numpy.genfromtxt(outputsFileName,delimiter=',')
        self.learningRate = learningRate
        self.epochs = epochs
        self.b0 = 0
        self.b1 = 0
        self.b2 = 0
    #to get probablility based off of the output
    def logisticFunction(self,val):
        return ( 1 / ( 1+numpy.exp(-1*val) ) )

    #to get the output
    def logisticRegressionFunction(self,input1, input2):
        return(self.b0 + (self.b1*input1) + (self.b2*input2))

    #returns the probability
    def getProbability(self,input1,input2):
        return(self.logisticFunction(self.logisticRegressionFunction(input1,input2)))

    def normalize(self,data):
        return (data/100)

    def train(self):
        print("Training with", self.epochs, end = "")
        print(" epochs and a learning rate of", self.learningRate)
        epochError = []
        for epoch in range(0, self.epochs):
            # for every sample
            numErrors = 0
            for x in range(0, len(self.inputs)):
                input1 = self.inputs[x][0]
                input2 = self.inputs[x][1]
                trueOutput = self.outputs[x]
                prediction = self.getProbability(input1,input2)
                if(trueOutput != numpy.round(prediction)):
                    numErrors = numErrors+1
                self.b0 = self.updateB0(trueOutput,prediction)
                self.b1 = self.updateB1(trueOutput,prediction,input1)
                self.b2 = self.updateB2(trueOutput,prediction,input2)
            epochError.append(numErrors)
            #get prediciton
            #get error
            #update
        print("Training complete")
        print("Number of Errors during training were :", epochError)
        self.plotErrors(epochError)
        print()

    #b = b + alpha * (y – prediction) * prediction * (1 – prediction) * x
    def updateB0(self,trueOutput, prediction):
        return(self.b0 + (self.learningRate*(trueOutput-prediction)*prediction*(1-prediction)*1))
    #to update b1
    def updateB1(self,trueOutput, prediction,input1):
        return(self.b1 + (self.learningRate*(trueOutput-prediction)*prediction*(1-prediction)*input1))
    #to update b2
    def updateB2(self,trueOutput, prediction,input2):
        return(self.b2 + (self.learningRate*(trueOutput-prediction)*prediction*(1-prediction)*input2))

    def plotErrors(self, errors):
        print("Plot of the number of Errors Vs Number of Epochs encountered during Training")
        xs = []
        for x in range(0, len(errors)):
            xs.append(x+1)
        plt.plot(xs,errors)
        title = "Plot of the number of Errors Vs Number of Epochs encountered during Training with "
        title = title + str(self.epochs) + " epochs and a learning rate of " + str(self.learningRate)
        plt.xlabel("Number of Epochs")
        plt.ylabel("Number of Errors")
        plt.title(title)
        plt.show()
    #for decision boundary
    def decBoundary(self,val):
        return (self.b0 + (self.b1*val)) / (-self.b2)
    #plot decision boundary and data points
    def plot(self):
        fig = plt.figure()
        tempRange = numpy.arange(13,80)
        toPlot = numpy.transpose(self.inputs)*100
        plt.scatter(toPlot[0][40:], toPlot[1][40:], s=25, c='b', marker='o', label='Has made exam entrance')
        plt.scatter(toPlot[0][:40], toPlot[1][:40], s=25, c='g', marker='o', label='Has not made exam entrance')
        plt.plot(self.decBoundary(tempRange/100)*100, c = 'r', linewidth = 2, label='Decision Boundary')
        plt.scatter(20, 80, s=100, marker = 'd', c='k', label='P([20, 80]) = ' + str(numpy.round(self.getProbability(20/100, 80/100), 2))) # Probability of 20, 80 getting exam entrance #
        plt.scatter(50, 50, s=100, marker = 'd', c='k', label='P([50, 50]) = ' + str(numpy.round(self.getProbability(50/100, 50/100), 2))) # Probability of 50, 50 getting exam entrance #
        title = "Plot of the decision boundary and original training data"
        title = title + "with " +str(self.epochs) + " number of epochs and a learning rate of " +str(self.learningRate)
        plt.title(title)
        plt.xlabel('Semester Test 1 Results')
        plt.ylabel('Semester Test 2 Results')
        plt.legend(loc='best')
        plt.show()

epochs = 100 #change for epochs
learningRate = 0.3 #change for learning rate
temp = logisticRegression("examX.data", "examY.data",epochs,learningRate)
temp.train()
print("The probability of getting into the exam with results:")
print("Semester Test 1 = 20%")
print("Semester Test 2 = 80%")
print("Probability =", temp.getProbability(0.20,0.80) ) #Question 3c
print()
print("The probability of getting into the exam with results:")
print("Semester Test 1 = 50%")
print("Semester Test 2 = 50%")
print("Probability =",temp.getProbability(0.50,0.50) ) #Question 3d
print()
print()
print("Final co-efficent values:")
print("b0 =", temp.b0)
print("b1 =", temp.b1)
print("b2 =", temp.b2)
temp.plot()
