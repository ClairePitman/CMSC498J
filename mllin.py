import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import svm
import numpy as np
import time
regr = linear_model.Lasso(alpha = 0.1)
write1 = np.genfromtxt('train.csv',delimiter=',',usecols=(0,1,2,3,4,5),skip_header=1)
write1
np.random.shuffle(write1)
writeY=write1[:,5]
writeX=write1[:,np.array([False,False, True, True, True, False])]

trainLabels= writeY
trainData=writeX

regr.fit (trainData, trainLabels)

# The coefficients
print('Coefficients: \n', regr.coef_)

test = np.genfromtxt('test.csv',delimiter=',',usecols=(0,1,2,3,4,5))
testY=test[:,5]
testX=test[:,np.array([False,False, True, True, True, False])]
regr.predict(testX)
testY
#print (regr.predict(testX))
#print trainLabels
#print testY
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(testX) - testY) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(testX, testY))

# time
plt.scatter(trainData[:,0], trainLabels,  color='black')
plt.scatter(testX[:,0], testY, color='red')
plt.scatter(testX[:,0], regr.predict(testX), color='blue')
plt.xlabel('Time')


plt.show()

# sentiment
plt.scatter(trainData[:,1], trainLabels,  color='black')
plt.scatter(testX[:,1], testY, color='red')
plt.scatter(testX[:,1], regr.predict(testX), color='blue')
plt.xlabel('Sentiment')


plt.show()

# Folowers
plt.scatter(trainData[:,2], trainLabels,  color='black')
plt.scatter(testX[:,2], testY, color='red')
plt.scatter(testX[:,2], regr.predict(testX), color='blue')
plt.xlabel('# of followers')


plt.show()

