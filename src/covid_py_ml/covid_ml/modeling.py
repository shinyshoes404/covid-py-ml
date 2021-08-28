from ml_config.ml_config import MlConfig
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class DataModeler:
    def __init__(self):
        self.poly_degree = MlConfig.poly_degree
    
    def model_train(self,X,y):

        # if we have a polynomial degree greater than 1, transform X before fitting the model
        if self.poly_degree > 1:
            poly = PolynomialFeatures(degree=self.poly_degree)
            x_train = poly.fit_transform(X)
        
        # otherwise, we are just doing multiple linear regression, no transform necessary
        else:
            x_train = X

        # instantiate our linear regression model
        self.model = LinearRegression()
        self.model.fit(x_train, y)
        self.model_score = self.model.score(x_train, y)

    
        