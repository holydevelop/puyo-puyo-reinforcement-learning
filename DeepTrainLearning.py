#<---------------- M O D E L O   D E E P   Q   L E A R N I N G ----------------->
# Importacion de librerias necesarias para el modelo Deep Q Learning
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
#<-------- F I N   D E L   M O D E L O   D E E P   Q   L E A R N I N G ---------->


#<------ M E M O R I A   D E   E X P E R I E N C I A   P A R A   R E P L A Y ------>
#Importacion de libreria con estructura de datos para la memoria de experiencia
from collections import deque 
#Importacion de libreria random para la memoria
import random
#<-- F I N   D E   M E M O R I A   D E   E X P E R I E N C I A   P A R A   R E P L A Y -->

#Importacion de libreria para valores aleatorios de Deep Q Learning ( sampleAction )
import numpy as np

#Define memory for experience replay
class ReplayMemory():
    def __init__(self, maxlen):
        self.memory = deque([], maxlen=maxlen )

    def append(self, transition):
        self.memory.append(transition)

    def sample(self, sample_size):
        return random.sample(self.memory, sample_size)

    def __len__(self):
        return len(self.memory)

# Creacion del modelo para Deep Q Learning y modificar el input_dim
class DeepQNetworkModel(nn.Module):
    def __init__(self, input_dim, output_dim=5):
        self.c = input_dim[0]
        self.model = nn.Squential(
            nn.Conv2d(in_channels=self.c, out_channels=32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, output_dim)
        )

    def forward(self, x):
        return self.model(x)

class DeepQLearning:
    # Hyperparameters (adjustable)
    learning_rate_a = 0.001         # learning rate (alpha)
    discount_factor_g = 0.9         # discount rate (gamma)    
    network_sync_rate = 10          # number of steps the agent takes before syncing the policy and target network
    replay_memory_size = 1000       # size of replay memory
    mini_batch_size = 32            # size of the training data set sampled from the replay memory

    # Neural Network
    loss_fn = nn.MSELoss()          # NN Loss function. MSE=Mean Squared Error can be swapped to something else.
    optimizer = None                # NN Optimizer. Initialize later.
    max_epochs = 100
    act_epoch = 0

    def sampleAction(self):
        return np.random.randint(0, 22)