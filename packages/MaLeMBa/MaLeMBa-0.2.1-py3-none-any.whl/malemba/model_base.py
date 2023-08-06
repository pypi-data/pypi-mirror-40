from abc import abstractmethod, ABCMeta
from copy import deepcopy
from collections import defaultdict, OrderedDict

import pandas as pd
from scipy.stats import fisher_exact, chi2_contingency


class ModelBase(metaclass=ABCMeta):

    @abstractmethod
    def fit(self, X, Y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    def validate(self, X_test, Y_test, labels_to_remove=None):
        tables_2x2 = defaultdict(lambda: defaultdict(int))
        test_pred = self.predict(X=X_test)
        labels = tuple(test_pred[0].keys())
        confusion_dict = OrderedDict()
        for label in labels:
            confusion_dict[label] = [0]*len(labels)
        confusion_matrix = pd.DataFrame.from_dict(data=confusion_dict, orient='index')
        confusion_matrix.columns = labels
        for i in range(len(test_pred)):
            not_TN = [Y_test[i]]
            prob_labels = get_prob_labels(test_pred[i], n_prob_states=1, max_d=0.1)
            if Y_test[i] in prob_labels:
                tables_2x2[Y_test[i]]["TP"] += 1
                confusion_matrix[Y_test[i]][Y_test[i]] += 1
            else:
                tables_2x2[Y_test[i]]["FN"] += 1
                tables_2x2[prob_labels[0]]["FP"] += 1
                confusion_matrix[prob_labels[0]][Y_test[i]] += 1
                not_TN.append(prob_labels[0])
            for label in test_pred[i]:
                if label not in not_TN:
                    tables_2x2[label]["TN"] += 1
        if type(labels_to_remove) in (list, tuple, set, frozenset):
            for label in labels_to_remove:
                del tables_2x2[label]
        tables_2x2_array = list()
        for label in tables_2x2.keys():
            tables_2x2_array.append([[tables_2x2[label]["TP"], tables_2x2[label]["FP"]],
                                     [tables_2x2[label]["FN"], tables_2x2[label]["TN"]]])
            tables_2x2[label]["Fisher_P-value"] = fisher_exact(tables_2x2_array[-1],
                                                               alternative='greater')[1]
            try:
                precision = float(tables_2x2[label]["TP"]) / float(tables_2x2[label]["TP"]+tables_2x2[label]["FP"])
                recall = float(tables_2x2[label]["TP"]) / float(tables_2x2[label]["TP"]+tables_2x2[label]["FN"])
                tables_2x2[label]["F1_score"] = 2.0 * (precision*recall) / (precision+recall)
            except ZeroDivisionError:
                tables_2x2[label]["F1_score"] = None
        tables_2x2["Chi-sq_P-value"] = chi2_contingency(tables_2x2_array)[1]
        return tables_2x2, confusion_matrix

    @classmethod
    def optimize_params(cls,
                        X,
                        Y,
                        X_test,
                        Y_test,
                        var_params_grid,
                        constant_params=None,
                        eval_labels=None):

        best_params = dict((param, var_params_grid[param].pop(0)) for param in var_params_grid)
        if constant_params is not None:
            best_params.update(constant_params)
        model_0 = cls(params=deepcopy(best_params))
        X_eval=deepcopy(model_0.str_to_factors(X=X))
        X_test=model_0.str_to_factors(X=X_test)
        str_features_f50 = model_0._str_features_f50
        model_0.fit(X=X_eval, Y=Y)
        confusion_matrix = model_0.validate(X_test=X_test, Y_test=Y_test)[1]
        if type(eval_labels) in (list, tuple, set, frozenset):
            best_score = sum(confusion_matrix[label][label] for label in eval_labels)
        else:
            best_score = sum(confusion_matrix[label][label] for label in confusion_matrix.columns)
        for param in var_params_grid:
            print("'%s' parameter optimization started" % str(param))
            curr_params = deepcopy(best_params)
            for param_v in var_params_grid[param]:
                curr_params[param] = param_v
                model = cls(params=deepcopy(curr_params))
                model._str_features_f50 = str_features_f50
                model.fit(X=X_eval, Y=Y)
                confusion_matrix = model.validate(X_test=X_test, Y_test=Y_test)[1]
                if type(eval_labels) in (list, tuple, set, frozenset):
                    score = sum(confusion_matrix[label][label] for label in eval_labels)
                else:
                    score = sum(confusion_matrix[label][label] for label in confusion_matrix.columns)
                if score > best_score:
                    best_score = score
                    best_params[param] = param_v
            print("'%s' parameter optimization finished - optimal value: %s" % (str(param),
                                                                                str(best_params[param])))
        return best_params, best_score

    @abstractmethod
    def dump(self, scheme_path, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def load(cls, scheme_path):
        pass

    @property
    @abstractmethod
    def features(self):
        pass

    @property
    @abstractmethod
    def labels(self):
        pass


def get_prob_labels(labels_scores, n_prob_states=1, max_d=0.1):
    prob_labels = [(None, 0)]*n_prob_states
    for label in labels_scores:
        for i in range(n_prob_states):
            if i > 0:
                if prob_labels[i-1][1]-labels_scores[label] > max_d:
                    break
            if prob_labels[i][0] is None:
                prob_labels[i] = (label, labels_scores[label])
                break
            elif labels_scores[label]-prob_labels[i][1] > 0:
                prob_labels.insert(i, (label, labels_scores[label]))
                break
    return list(filter(None, map(lambda l: l[0], prob_labels[:n_prob_states])))

