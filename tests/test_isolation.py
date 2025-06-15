import numpy as np
from sklearn.ensemble import IsolationForest

def test_anomaly_score_outlier():
    X = np.random.normal(0, 1, (100, 10))
    clf = IsolationForest(contamination=0.01)
    clf.fit(X)
    outlier = np.ones((1, 10)) * 10
    score = -clf.decision_function(outlier)[0]
    assert score > 0.8
