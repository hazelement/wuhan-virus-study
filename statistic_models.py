
import numpy as np

si_model = lambda t, N, I, R: N*I/(I+(N-I)*np.exp(-R*t))
si_model_expression = lambda N, I, R: r"$\frac{" + f"{N*I:.2f}" + "}{"+ f"{I:.2f}" + "+(" + f"{N-I:.2f}" + ")*exp(-" + f"{R:.2f}" + "*t)}$"
