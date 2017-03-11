# gradient boosting
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from PatternsCollector import get_patterns_for_window_and_num, get_x_y_for_patterns
import seaborn

nums = [10, 20, 40, 80, 160, 320]
i = 0
wrange = [2]
lrange = [10]
values = list()
legends = list()

for wnd in wrange:
    for l in lrange:
        scores = []
        patterns = get_patterns_for_window_and_num(wnd, l)
        X, y = get_x_y_for_patterns(patterns, 'buy')

        for n in nums:
            i = i+1
            kf = KFold(n_splits=5, shuffle=True, random_state=100)
            model = GradientBoostingClassifier(n_estimators=n, random_state=100)
            ms = cross_val_score(model, X, y, cv=kf, scoring='roc_auc')
            scores.append(np.mean(ms))
            print 'Calculated {0}-{1}, num={2}, {3:.3f}%'.format(wnd, l, n, 100 * i/float((len(nums)*len(wrange)*len(lrange))))
        values.append(scores)
        legends.append('{0}-{1}'.format(wnd, l))

plt.xlabel('estimators count')
plt.ylabel('accuracy')
for v in values:
    plt.plot(nums, v)
plt.legend(legends)
plt.show()
