# ai_spotibot_player
# AudioMIX
# audio/ai/modules/lightning_module.py

# This module defines a PyTorch Lightning module for training a simple feedforward neural network (LightningEQNet) to predict audio labels based on extracted features. The model consists of linear layers with ReLU activations and dropout for regularization. The training and validation steps compute the binary cross-entropy loss, and the optimizer used is Adam. The module is designed to be easily integrated into a PyTorch Lightning training loop for efficient training and validation.

import torch
import torch.nn as nn
import pytorch_lightning as pl

# Example usage:
# model = LightningEQNet(input_dim=100, num_classes=10)
class LightningEQNet(pl.LightningModule):
    def __init__(self, input_dim, num_classes, lr=1e-3):
        """
        A simple feedforward neural network for audio label prediction.
        """
        super().__init__()
        self.save_hyperparameters()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes),
            nn.Sigmoid()
        )
        self.loss_fn = nn.BCELoss()

    # Forward pass through the model.
    def forward(self, x):
        return self.model(x)

    # Training step for a batch of data.
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(y_hat, y)
        self.log("train_loss", loss)
        return loss

    # Validation step for a batch of data.
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(logits, y)
        self.log("val_loss", loss)

    # Optimizer configuration for training
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)
