import os
import time
from datetime import datetime
import socket
import torch
import matplotlib.pyplot as plt
import sys
from torch.utils.tensorboard import SummaryWriter

class Logger(object):
    def __init__(self, directory, write, save_freq = 10):
        self.parent_dir = directory
        self.write = write
        self.dir = ""
        self.fig_index = 0
        self.model_index = 0
        self.save_freq = save_freq
        if self.write:
            self.boardWriter = SummaryWriter()
            current_time = datetime.now().strftime('%b%d_%H-%M-%S')
            self.dir = os.path.join(self.parent_dir, current_time + '_' + socket.gethostname())
            self.log(f"Logs from {self.dir}\n{' '.join(sys.argv)}\n")

    def add_loss_board(self, loss, step):
        if self.write:
            self.boardWriter.add_scalar('Loss', loss, step)

    def add_distances_board(self, start_dists, info, episode):
        if self.write:
            agent_diffs = { f"Agent {i}" : start_dists[i]-info['distError_'+str(i)] for i in range(len(start_dists))}
            final_distances = { f"Agent {i}" : info['distError_'+str(i)] for i in range(len(start_dists))}
            self.boardWriter.add_scalars('Distance difference', agent_diffs, episode)
            self.boardWriter.add_scalars('Distance final', final_distances, episode)

    def plot_res(self, losses, distances):
        if len(losses) == 0 or not self.write:
            return

        fig, axs = plt.subplots(2)
        axs[0].plot(list(range(len(losses))), losses, color='orange')
        axs[0].set_xlabel("Steps")
        axs[0].set_ylabel("Loss")
        axs[0].set_title("Training")
        axs[0].set_yscale('log')
        for dist in distances:
            axs[1].plot(list(range(len(dist))), dist)
        axs[1].set_xlabel("Steps")
        axs[1].set_ylabel("Distance change")
        axs[1].set_title("Training")

        if self.fig_index > 0:
            os.remove(os.path.join(self.dir, f"res{self.fig_index-1}.png"))
        fig.savefig(os.path.join(self.dir, f"res{self.fig_index}.png"))
        self.boardWriter.add_figure(f"res{self.fig_index}", fig)
        self.fig_index+=1

    def log(self, message):
        print(str(message))
        if self.write:
            self.boardWriter.add_text("log", str(message))
            with open(os.path.join(self.dir, "logs.txt"), "a") as logs:
                logs.write(str(message) + "\n")

    def save_model(self, state_dict):
        if not self.write:
            return
        if self.model_index > 0 and self.model_index % self.save_freq != 1:
                os.remove(os.path.join(self.dir, f"dqn{self.model_index-1}.pt"))
        torch.save(state_dict, os.path.join(self.dir, f"dqn{self.model_index}.pt"))
        self.model_index+=1
