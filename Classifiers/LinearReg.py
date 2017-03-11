# logistic regression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from PatternsCollector import get_patterns_for_window_and_num, get_x_y_for_patterns
from sklearn.model_selection import KFold, cross_val_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn

cr = [10.0 ** i for i in range(-5, 2)]
i = 0
wrange = [1,2]
lrange = [10]
values = list()
legends = list()

for wnd in wrange:
    for l in lrange:
        scores = []
        patterns = get_patterns_for_window_and_num(wnd, l)
        X, y = get_x_y_for_patterns(patterns, 'buy')
        sc = StandardScaler()
        X_sc = sc.fit_transform(X)

        for c in cr:
            i = i+1
            kf = KFold(n_splits=5, shuffle=True, random_state=100)
            model = LogisticRegression(C=c, random_state=100)
            ms = cross_val_score(model, X_sc, y, cv=kf, scoring='roc_auc')
            scores.append(np.mean(ms))
            print 'Calculated {0}-{1}, C={2}, {3:.3f}%'.format(wnd, l, c, 100 * i/float((len(cr)*len(wrange)*len(lrange))))
        values.append(scores)
        legends.append('{0}-{1}'.format(wnd, l))

plt.xlabel('C value')
plt.ylabel('accuracy')
for v in values:
    plt.plot(cr, v)
plt.legend(legends)
plt.show()
