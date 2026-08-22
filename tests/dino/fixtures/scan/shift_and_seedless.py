# Intentional leakage fixtures for scan rules
import numpy as np
from sklearn.model_selection import train_test_split

close = np.array([1.0, 2.0, 3.0])
future = close.shift(-1) if hasattr(close, "shift") else close  # noqa: pattern bait
y = close
# force pattern for SHIFT_NEGATIVE text scan:
_ = "series.shift(-1)"

X_train, X_test, y_train, y_test = train_test_split(close, y)
