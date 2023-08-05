"""
Factor Analysis using Statistical Methods
The method is similar to principal components although, as the textbook points out, 
factor analysis is more elaborate.
In one sense, factor analysis is an inversion of principal components. 
"""

import math
import numpy as np
import scipy as sci
import scipy.stats as sstat
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import warnings
warnings.filterwarnings("ignore")

class FA_Tests():
    """
    Class that conducts FA tests. KMO and Bartlett's test of sphericity
    """
    def __init__(self, matrix = None):
        self.matrix = matrix
    
    def KMO(self, X, y = None):
        """
        The Kaiser-Meyer-Olkin Measure of Sampling Adequacy is a statistic that indicates the proportion of variance in 
        your variables that might be caused by underlying factors. 
        High values (close to 1.0) generally indicate that a factor analysis may be useful with your data. 
        If the value is less than 0.50, the results of the factor analysis probably won't be very useful.
        Returns a KMO Score value rounded off to the 4 decimal places
        """
        corr = X.corr().as_matrix() ## Correaltion matrix for the dataframe
        invcor = np.linalg.inv(corr) ## Inverse matrix
        d = np.linalg.inv(np.diag(np.sqrt(np.diag(invcor)))) ## Get the D 1/2 matrix
        antiimage = np.matmul(np.matmul(d, invcor), d) ## Get the anti-image matrix
        num = 0; den = 0

        ## Calculate the KMO using formula
        for rows in range(antiimage.shape[0]):
            for cols in range(antiimage.shape[1]):
                if rows != cols:
                    num += (corr[rows][cols] ** 2)
                    den += ((corr[rows][cols] ** 2) + (antiimage[rows][cols] ** 2))

        kmo = num / den
        return kmo.round(4)


    def BToS(self, X, y = None):
        """
        Bartlett's test of sphericity tests the hypothesis that your correlation matrix is an identity matrix, 
        which would indicate that your variables are unrelated and therefore unsuitable for structure detection. 
        Small values (less than 0.05) of the significance level indicate that a factor analysis may be useful with your data.
        """
        n = X.shape[0]
        p = X.shape[1]
        corr = X.corr()
        lhs = (n - 1) - (2 * p - 5) / 6 ## Formula of the first equation
        rhs = np.log(np.linalg.det(corr)) ## Formula of the second equation
        chi_square = -(lhs * rhs) ## Chi-Square value from this
        degree_of_freedom = (p ** 2 - p) / 2 ## Degrees of freedom
        k, p_val = sstat.bartlett(*X.as_matrix()[:, 0:10]) ## Test Statistics and P-Value of the test

        return chi_square.round(5), degree_of_freedom, k.round(5), p_val.round(10)

class FA():
    """
    Class that calculates Factor Analysis.
    """
    def __init__(self, mat = None):
        self.matrix = mat

    def Eigens(self, X):
        """
        Return the eigen values and a dataframe of eigen vectors for the correlation dataframe
        """
        self.eval_corr, self.evect_corr = np.linalg.eig(X.corr())
        idx_corr = self.eval_corr.argsort()[::-1]
        self.eval_corr = self.eval_corr[idx_corr]
        self.evect_corr = self.evect_corr[:, idx_corr]
        
        return self.eval_corr.round(5), self.evect_corr.round(5).T

    def VarperComp(self):
        """
        Returns a dataframe containing the components and it's amount of explained variance and cumulative dist
        """
        exp = self.eval_corr * 100 / np.sum(self.eval_corr)
        accsum = np.cumsum(exp)
        self.pcnum = list(range(0, len(self.eval_corr)))
        data = np.array([self.pcnum, self.eval_corr, exp, accsum])
        self.varpercomp = pd.DataFrame(data.T, columns = ["PC", "EigenValues", "% of Var", "Cumulative %"])

        return self.varpercomp

    def _PrintScreePlot(self):
        """
        Prints the scree-plot of the distribution of variance across prinicpal components
        """
        plt.figure(figsize = [15.0, 7.0])
        eachexp = self.varpercomp.iloc[:, 2]
        sns.lineplot(self.pcnum, eachexp, label = "% of variance explained")
        plt.xlabel("Number of principal components")
        plt.ylabel("% of variance")
        plt.title("% of variance per principal component", fontsize =  15)
        plt.legend()
        plt.show()

    def loadings(self, n_components = None):
        """
        Returns the loading matrix of the specified number of principal components.
        If not specified retuns for all the components whose Eigen value greater than 1
        """
        n = 0
        for i in self.eval_corr:
            if i >= 1:
                n += 1
        if n_components == None:
            evec_corr3 = self.evect_corr[:, :n]
            eval_corr3 = self.eval_corr[:n]
            self.loadings = evec_corr3 * np.sqrt(eval_corr3) ## Loading matrices
            index  = ["PC"+str(i) for i in range(n)]
            loading_df = pd.DataFrame(self.loadings.T, index = index)
        else:
            evec_corr3 = self.evect_corr[:, :n_components]
            eval_corr3 = self.eval_corr[:n_components]
            self.loadings = evec_corr3 * np.sqrt(eval_corr3) ## Loading matrices
            index  = ["PC"+str(i) for i in range(n_components)]
            loading_df = pd.DataFrame(self.loadings.T, index = index)

        return loading_df.T

    def pcscores(self, X, columns = None):
        """
        Returns the principal component scores which can used for FA
        """
        n = 0
        for i in self.eval_corr:
            if i >= 1:
                n += 1
        if columns == None:
            evec_corr3 = self.evect_corr[:, :n]
            eval_corr3 = self.eval_corr[:n]
            loadings = evec_corr3 * np.sqrt(eval_corr3) ## Loading matrices
            pcscorecoeff = np.linalg.inv(X.corr()).dot(loadings)
            index  = ["PC"+str(i) for i in range(n)]
            pcscorecoeff_df = pd.DataFrame(pcscorecoeff, columns = index)
        else:
            evec_corr3 = self.evect_corr[:, :columns]
            eval_corr3 = self.eval_corr[:columns]
            loadings = evec_corr3 * np.sqrt(eval_corr3) ## Loading matrices
            pcscorecoeff = np.linalg.inv(X.corr()).dot(self.loadings[:columns])
            self.index  = ["PC"+str(i) for i in range(columns)]
            pcscorecoeff_df = pd.DataFrame(pcscorecoeff, columns = self.index)
        
        return pcscorecoeff_df

    def varimaxr(self, loadings, normalize = True, max_iter = 500, tolerance = 1e-5):
        df = loadings.copy()
        column_names = df.index.values
        index_names = df.columns.values
        n_rows, n_cols = df.shape
        if n_cols < 2:
            return df
        X = df.values
        if normalize:
            normalized_mtx = df.apply(lambda x: np.sqrt(sum(x**2)),
                                      axis=1).values
            X = (X.T / normalized_mtx).T
        rotation_mtx = np.eye(n_cols)

        d = 0
        for _ in range(max_iter):
            old_d = d
            basis = np.dot(X, rotation_mtx)
            transformed = np.dot(X.T, basis**3 - (1.0 / n_rows) *
                                 np.dot(basis, np.diag(np.diag(np.dot(basis.T, basis)))))
            U, S, V = np.linalg.svd(transformed)
            rotation_mtx = np.dot(U, V)
            d = np.sum(S)
            if old_d != 0 and d / old_d < 1 + tolerance:
                break

        X = np.dot(X, rotation_mtx)

        if normalize:
            X = X.T * normalized_mtx
        else:
            X = X.T
        loadings = pd.DataFrame(X, columns=column_names, index=index_names).T

        def flip_sign(vec):
            for i in range(vec.shape[1]):
                if(vec[:, i].sum() < 0):
                    vec[:, i] = -1 * vec[:, i]
            return vec

        rloadnpmat = loadings.as_matrix()
        rloadingflip = flip_sign(rloadnpmat)

        def matx(mat):
            rpe = mat ** 2
            rpesum = np.sum(rpe, axis = 0)
            ind = rpesum.argsort()
            rr = mat[:, ind]
            return rr
        
        index  = ["PC"+str(i) for i in range(loadings.shape[1])]
        varmaxrotmat = pd.DataFrame(matx(rloadingflip), columns = index)
        
        return varmaxrotmat