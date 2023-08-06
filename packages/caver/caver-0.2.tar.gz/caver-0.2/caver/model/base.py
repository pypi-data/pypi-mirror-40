#!/usr/bin/env python
# encoding: utf-8

import os
import torch
import dill as pickle

class BaseModule(torch.nn.Module):
    """
    Base module for text classification.

    Inherit this if you want to implement your own model.
    """
    def __init__(self):
        super().__init__()
        self.labels = []
        self.vocab = {}


    def load(self, loaded_checkpoint, path):
        """ load model from file """
        # assert os.path.isfile(path)
        # self.load_state_dict(torch.load(path, map_location=lambda storage, loc: storage))
        # loaded_checkpoint = torch.load(os.path.join(path, "checkpoint_best.pt"), map_location=device)

        # self.model_type = loaded_checkpoint["model_type"]

        self.update_args(loaded_checkpoint["model_args"])
        self.load_state_dict(loaded_checkpoint["model_state_dict"])
        self.labels = pickle.load(open(os.path.join(path, "y_feature.p"), "rb"))
        self.TEXT= pickle.load(open(os.path.join(path, "TEXT.p"), "rb"))
        self.vocab = self.TEXT.vocab.stoi


    def save(self, path):
        """ save model to file """
        folder, _ = os.path.split(path)
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print('Folder: {} is created.'.format(folder))

        torch.save(self.state_dict(), path)
        print('[+] Model saved.')


    def get_args(self):
        return vars(self)


    def update_args(self, args):
        for arg, value in args.items():
            vars(self)[arg] = value


    def predict_label(self, batch_top_k_index):
        """
        lookup all the labels basedon own labels and top K index
        """
        batch_top_k_index = batch_top_k_index.data.cpu().numpy()
        labels = []
        for pred in batch_top_k_index:
            labels.append([self.labels[idx] for idx in pred])
        return labels
