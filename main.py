import gradient_descent as gd
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

np.set_printoptions(suppress=True)

##### TEST-REGRESSION-DATA:
xs,ys = make_regression(n_samples=1000,n_features=10,
                        n_informative=8,noise = 50, n_targets=1,random_state=12)
x_train, x_test, y_train, y_test = train_test_split(xs,ys,test_size=0.33,random_state=12)


##### SCALER:-------------------------------------------------------------------
sc = gd.scaler()
scaled = sc.fit_transform(x_train)
scaled_t = sc.fit_transform(x_test)

##### BATCH-GD: ----------------------------------------------------------------
clf1 = gd.reg_BGD(scaled,y_train,1000,0.01)

# train + score:
y_pred1 = clf1._predict(scaled)
print("BatchGD train:", mean_squared_error(y_pred1,y_train))
# test + score:
yt_pred1 = clf1._predict(scaled_t)
print("BatchGD test:", mean_squared_error(yt_pred1,y_test))


##### STOCHASTIC-GD: -----------------------------------------------------------
clf2 = gd.reg_SGD(scaled,y_train,iter=10,l_rate=0.5, rand=42)

# train + score:
y_pred2 = clf2._predict(scaled)
print("StochasticGD train:", mean_squared_error(y_pred2,y_train))

# test + score:
yt_pred2 = clf2._predict(scaled_t)
print("StochasticGD test:", mean_squared_error(yt_pred2,y_test))

print(clf2._coefficients())

##### RIDGE-GD: ----------------------------------------------------------------
clf3 = gd.ridge_gd(scaled,y_train,iter= 10, l_rate=0.5, alpha=0.01, rand=42)

# train + score:
y_pred3 = clf3._predict(scaled)
print("Ridge train:", mean_squared_error(y_pred3,y_train))

# test + score:
yt_pred3 = clf3._predict(scaled_t)
print("Ridge test:",mean_squared_error(yt_pred3,y_test))

print(clf3._coefficients())

##### RIDGE-CLOSED: ------------------------------------------------------------
clf4 = gd.ridge_closed(scaled,y_train,alpha=0.1)
print(clf4._calc())

##### PLOTS: -------------------------------------------------------------------
def visualisation_2D():
    plt.plot(x_train, y_train, "r.")

    line_x = np.linspace(-3,3,100)
    clf1_ys = clf1._predict(line_x)
    clf2_ys = clf2._predict(line_x)
    clf3_ys = clf3._predict(line_x)

    plt.plot(line_x,clf1_ys, "o-", label="BGD")
    plt.plot(line_x,clf2_ys, "b-", label="SGD")
    plt.plot(line_x,clf3_ys,"g-", label="SGD penalised (l1 or l2)")
    plt.legend()
    plt.show()
#visualisation_2D()
