from stable_baselines3 import PPO
import os
from files.modoIA.fnaf2_gym_RL import FNAF2Env
import time
import wandb


class PPOTrainer:
    def __init__(self, env, model_name, total_timesteps=10000, verbose=1):
        self.env = env
        self.model_name = model_name
        self.total_timesteps = total_timesteps
        self.verbose = verbose

    def train_model(self):
        models_dir = f"models/{self.model_name}/"
        logdir = f"logs/{self.model_name}/"

        conf_dict = {"Model": "v19",
                     "Machine": "Main",
                     "policy": "MultiInputPolicy",
                     "model_save_name": self.model_name}

        wandb.init(
            project=f'FNAF2RL',
            entity="sentdex",
            config=conf_dict,
            sync_tensorboard=True,
            save_code=True
        )

        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        model = PPO('MultiInputPolicy', self.env, verbose=self.verbose, tensorboard_log=logdir)

        iters = 0
        while True:
            print("On iteration: ", iters)
            iters += 1
            model.learn(total_timesteps=self.total_timesteps, reset_num_timesteps=False, tb_log_name=f"PPO")
            model.save(f"{models_dir}/{self.total_timesteps * iters}")


