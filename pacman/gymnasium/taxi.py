import gymnasium as gym
from optparse import OptionParser



if __name__ == '__main__':

    	
    env = gym.make("Taxi-v3", render_mode="human", is_raining=True, fickle_passenger=True)
    observation, info = env.reset()

    episode_over = False
    while not episode_over:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print(info)
        episode_over = terminated or truncated

env.close()