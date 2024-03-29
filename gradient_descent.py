import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

np.random.seed(42)

##### BATCH-GRADIENT-DESCENT-REGRESSION:########################################
# -uses all training examples (slow)
# -lower bias (gets closer to the minimum)
# -cannot jump out of local minima
class reg_BGD:
    def __init__(self,x,y,iter,l_rate):
        self.x = np.c_[x,np.ones((x.shape[0],1))]
        self.y = y.reshape(-1,1)
        self.iter = iter
        self.l_rate = l_rate
        self.w = np.random.rand(self.x.shape[1],1)
        self.instances = len(self.x)
        self._opt_weights()

    def _opt_weights(self):
        for i in range(self.iter):
            Xw = np.dot(self.x,self.w)
            XwY = Xw - self.y
            w_gradients = (2*(np.dot(self.x.T, XwY)))/self.instances
            self.w = self.w - (self.l_rate * w_gradients)
        final_ws = self.w
        return final_ws.ravel(), w_gradients

    def _coefficients(self):
        return self._opt_weights()[0][:-1]

    def _intercept(self):
        return self._opt_weights()[0][-1]

    def _gradients(self):
        return self._opt_weights()[1]

    def _predict(self, new_x):
        opt_w = self._opt_weights()[0].reshape(-1,1)
        new_x_ones = np.c_[new_x,np.ones((new_x.shape[0],1))]
        return new_x_ones.dot(opt_w)

    def _score(self, y_pred, y):
        error = 0
        for i in range(0,self.instances):
            YPi = y_pred[i,:].reshape(-1,1) #pred
            Yi = self.y[i,:] #true
            error += (YPi-Yi)**2
        return np.sqrt(error / self.instances)




##### STOCHASTIC-GRADIENT-DESCENT-REGRESSION:###################################
# -uses random training instances (fast)
# -higher bias (not as close to the minimum)
# -can jump out of local minima (due to random nature)
class reg_SGD(reg_BGD):
    def __init__(self,x,y,iter=5,l_rate=0.5, rand=42):
        self.x = np.c_[x,np.ones((x.shape[0],1))]
        self.y = y.reshape(-1,1)
        self.iter = iter
        self.l_rate = l_rate
        self.w = np.random.rand(self.x.shape[1],1)
        self.instances = len(self.x)
        self.rand = rand
        self._opt_weights_SGD()

    def _opt_weights_SGD(self):
        np.random.seed(self.rand)
        for epoch in range(0,self.iter):
            for i in range(self.instances):
                rand_i = np.random.randint(self.instances)
                Xi = self.x[rand_i:rand_i+1,:]
                Yi = self.y[rand_i:rand_i+1,:]
                Xiw = np.dot(Xi,self.w)
                XiwY = Xiw - Yi
                w_gradients = (2*(np.dot(Xi.T, XiwY)))
                sched = (epoch*self.instances) + i
                eta = self.l_rate*(sched + 50)**-1
                self.w = self.w - (eta * w_gradients)
        final_ws = self.w
        return final_ws.ravel(), w_gradients.round(decimals=4)

    def _coefficients(self):
        return self._opt_weights_SGD()[0][:-1]

    def _intercept(self):
        return self._opt_weights_SGD()[0][-1]

    def _gradients(self):
        return self._opt_weights_SGD()[1]

    def _predict(self, new_x):
        opt_w = self._opt_weights_SGD()[0].reshape(-1,1)
        new_x_ones = np.c_[new_x,np.ones((new_x.shape[0],1))]
        return new_x_ones.dot(opt_w)

    def _score(self, y_pred, y):
        error = 0
        y=y.reshape(-1,1)
        y_pred = y_pred.reshape(-1,1)
        print(y_pred.shape,y.shape)
        for i in range(0,self.instances):
            YPi = y_pred[i,:] #pred
            Yi = self.y[i,:] #true
            error += (YPi-Yi)**2
        return (error / self.instances)




##### RIDGE-REGRESSION:#########################################################
# in theory by manipulating alpha (and therefore the l2 penalty):
# -increases bias
# -reduces variance
class ridge_gd(reg_BGD):
    def __init__(self,x,y,iter=5,l_rate=0.5,alpha=0, rand=42):
        self.x = np.c_[x,np.ones((x.shape[0],1))]
        self.y = y.reshape(-1,1)
        self.iter = iter
        self.l_rate = l_rate
        self.w = np.random.rand(self.x.shape[1],1)
        self.instances = len(self.x)
        self.alpha = alpha
        self.rand = rand
        self._opt_weights_SGD()

    def _opt_weights_SGD(self):
        np.random.seed(self.rand)
        for epoch in range(0,self.iter):
            for i in range(self.instances):
                rand_i = np.random.randint(self.instances)
                Xi = self.x[rand_i:rand_i+1,:]
                Yi = self.y[rand_i:rand_i+1,:]
                Xiw = np.dot(Xi,self.w)
                XiwY = Xiw - Yi
                w_gradients = (2*(np.dot(Xi.T, XiwY))) + self.alpha*(self.w)
                sched = (epoch*self.instances) + i
                eta = self.l_rate*(sched + 50)**-1
                self.w = self.w - (eta * w_gradients)
        final_ws = self.w
        return final_ws.ravel(), w_gradients.round(decimals=4)

    def _coefficients(self):
        return self._opt_weights_SGD()[0][:-1]

    def _intercept(self):
        return self._opt_weights_SGD()[0][-1]

    def _gradients(self):
        return self._opt_weights_SGD()[1]

    def _predict(self, new_x):
        opt_w = self._opt_weights_SGD()[0].reshape(-1,1)
        new_x_ones = np.c_[new_x,np.ones((new_x.shape[0],1))]
        return new_x_ones.dot(opt_w)

    def _score(self, y_pred, y):
        error = 0
        y=y.reshape(-1,1)
        y_pred = y_pred.reshape(-1,1)
        print(y_pred.shape,y.shape)
        for i in range(0,self.instances):
            YPi = y_pred[i,:] #pred
            Yi = self.y[i,:] #true
            error += (YPi-Yi)**2
        return (error / self.instances)

#closed form solver:
class ridge_closed:
    def __init__(self,x,y,alpha=0):
        self.x = np.c_[x,np.ones((x.shape[0],1))]
        self.y = y.reshape(-1,1)
        self.alpha = np.array(alpha)

    def _calc(self):
        id = np.identity(self.x.shape[1])
        id[0,0] = 0
        w = np.dot(np.linalg.inv(self.x.T.dot(self.x) + self.alpha.dot(id)), self.x.T.dot(self.y))
        return w.ravel()




##### STANDARD-SCALER:##########################################################
class scaler(BaseEstimator,TransformerMixin):
    def __init__(self):
        return None
    def fit(self,x):
        return self
    def transform(self,x):
        mu = np.mean(x)
        sigma = np.std(x)
        z = (x - mu)/sigma
        return z
