from scipy.misc import derivative as diff
import matplotlib.pyplot as plt

def beaut_plot():
    ''' To make plot more beautifull;
        code:
            plt.rcParams['figure.figsize'] = (12,12); 
            plt.box(on=False); 
            plt.axhline(); 
            plt.axvline(); 
            plt.grid(linestyle = '-.')'''
    plt.rcParams['figure.figsize'] = (12,12); 
    plt.box(on=False); 
    plt.axhline(); 
    plt.axvline(); 
    plt.grid(linestyle = '-.')
    pass 


def MNK(x,y):
    ''' Input two arrays x and y; y = b*x + c
        return b, c, d_b, d_b/b, d_c, d_c/c'''
    n = len(x); x_ser = sum(x)/n; y_ser = sum(y)/n
    D = sum([(x[i] - x_ser)**2 for i in range(n)])
    b = sum([(x[i] - x_ser)*y[i] for i in range(n)])/D
    c = y_ser - b*x_ser
    d_b = (sum([(y[i]-b*x[i]-c)**2 for i in range(n)])/(D*(n-2)))**0.5
    d_c = (1/n + x_ser**2/D)*(sum([(y[i]-b*x[i]-c)**2 for i in range(n)]))/(n-2)
    return b, c, d_b, d_b/b, d_c, d_c/c

def f_MNK(x,y):
    ''' BETA VERSION Input format: x,y\nx - n by m matrix (values of each variable in own LINE(!!!). Note, it should be 2-d array. If you have only 1-d, print double \ny - n by 1 matrix one LINE(!!!)\nOutput format: b0 (free member), b1, b2, ... , bn '''
    x = np.array([[60,50,75]]).T
    y = np.array([10,7,12])
    x = np.hstack((np.ones((x.shape[0],1)), x))
    b = np.linalg.inv(x.T.dot(x)).dot(x.T).dot(y)
    print(b)

def partial_derivative(func, var=0, point=[]):
    ''' Don\'t forget to import: \tfrom scipy.misc import derivative as diff\n \t\t\t\timport matplotlib.pyplot as plt

        1) You need to create function that returns formula of variable, you want to derivative;
        function takes arguments - variables which will be performed differentiation

        Example: def f(T1_sr, T2_sr, phi1_sr, phi2_sr): # to find velocity; 
                     return (2*np.pi*M/(m*l))*(phi1_sr*T1_sr+phi2_sr*T2_sr)*(R2**2-R1**2)/(T2_sr**2-T1_sr**2)
        2) Structure: Input:
                        1. function (see "1)"), 
                        2. number of variable by that funktion depends 
                            In the example above T1_sr = 0; T2_sr = 1; phi1_sr = 2; phi2_sr = 3 

                        3. values that will use in differentiated function
                            Example: values = [T1_sr, T2_sr, phi1_sr, phi2_sr]

        Example of calling function:
         dfT1, dfT2, dfphi1, dfphi2 = [i for i in [partial_derivative(f, j, values) for j in range(4)]]'''
    args = point[:]
    def wraps(x):
        args[var] = x
        return func(*args)
    return diff(wraps, point[var], dx = 1e-6)


def random_error(array, t_stud):
    ''' Input array (list type), t_stud (float type);
        return error, mean'''
    len_ = len(array)
    mean = sum(array) / len_
    error = t_stud*((sum([(array[i]-mean)**2 for i in range(len_)])/(len_*(len_-1)))**0.5)
    return error

