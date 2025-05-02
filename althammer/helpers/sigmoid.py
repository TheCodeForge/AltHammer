import math

def sigmoid(x):
  return 1 + (5/(1+math.exp((-1*x/2)-3.5)))
