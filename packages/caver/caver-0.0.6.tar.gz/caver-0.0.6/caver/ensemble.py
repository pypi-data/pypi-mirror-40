import numpy as np
from scipy import stats
import torch
import torch.nn.functional as F

# from .classify import Caver


class Ensemble(object):
    """
    :param list models: each model should have the same label number

    For now, this only support soft voting methods.
    """
    def __init__(self, models):
        assert isinstance(models, list) and len(models) > 0
        # label_num = models[0].config.label_num

        self.models = models
        self.epsilon = 1e-8

        self.methods = {
            'avg': self.avg,
            'log': self.log,
            'hmean': self.hmean,
            'gmean': self.gmean,
        }


    def __str__(self):
        start = "====== ensemble summary =======\n"
        summary = "\n-------------\n".join([model.__str__() for model in self.models])
        return start+summary


    def avg(self, preds):
        return np.average(preds, axis=0)

    def log(self, preds):
        return np.exp(np.log(self.epsilon + preds).mean(axis=0))

    def hmean(self, preds):
        return stats.hmean(self.epsilon + preds)

    def gmean(self, preds):
        return stats.gmean(self.epsilon + preds)

    def predict(self, batch_sequence_text, vocab_dict, device="cpu", top_k=5, method='avg'):

        """
        :param str text: text
        :param str method: ['log', 'avg', 'hmean', 'gmean']
        """
        assert method in self.methods
        models_preds = [model._predict_text(batch_sequence_text, vocab_dict, device="cpu", top_k=5) for model in self.models]

        ensemble_batch_preds = torch.zeros(models_preds[0].shape)

        for preds in models_preds:
            # print(F.softmax(preds, dim=1))
            ensemble_batch_preds += F.softmax(preds, dim=1)
            # _softmax = F.softmax(preds, dim=1)
            # print(_softmax)

        ensemble_batch_preds /= len(self.models)
        # print(ensemble_res)

        batch_top_k_value, batch_top_k_index = torch.topk(torch.sigmoid(ensemble_batch_preds), k=top_k, dim=1)

        # return batch_top_k_index

        return batch_top_k_index

            # print(F.softmax(rr, dim=1))

        # preds = np.array([model._predict_text(batch_sequence_text, vocab_dict, device="cpu", top_k=5) for model in self.models])
        # print(preds.shape)
        # return self.methods.get(method)(preds)

    def get_top_label(self, text, method='log', top=5):
        """
        :param str text: text
        :param str method: ['log', 'avg', 'hmean', 'gmean']
        :param int top: top-n most possible labels
        """
        preds = self.predict(text, method)
        top_index = np.argsort(preds)[::-1]
        result = []
        result.append([self.models[0].index2label[i] for i in top_index[:top]])
        result.append([preds[i] for i in top_index[:top]])
        return result
