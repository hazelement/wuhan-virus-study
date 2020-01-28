
import numpy as np


si_model = lambda t, N, I, R: N*I/(I+(N-I)*np.exp(-R*t))