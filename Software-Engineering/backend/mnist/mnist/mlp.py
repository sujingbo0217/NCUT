# -*- coding = utf-8 -*-
# @Time : 2023/6/4 5:23 PM
# @Author : Jingbo Su
# @File : mlp.py
# @Software : PyCharm

import torch.nn as nn
import torch.nn.functional as F


class MLP(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()

        self.input_fc = nn.Linear(input_dim, 250)
        self.hidden_fc = nn.Linear(250, 100)
        self.output_fc = nn.Linear(100, output_dim)

    def forward(self, x):
        # x = [batch_size, height, width]
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)

        # x = [batch_size, height*width]
        H1 = F.relu(self.input_fc(x))

        # x = [batch_size, 250]
        H2 = F.relu(self.hidden_fc(H1))

        # x = [batch_size, 100]
        y_hat = self.output_fc(H2)

        return y_hat, H2
