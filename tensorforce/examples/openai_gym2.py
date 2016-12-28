# Copyright 2016 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
OpenAI gym runner
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse
from six.moves import xrange

import numpy as np

from tensorforce.config import Config, create_config
from tensorforce.environments.runner import Runner
from tensorforce.environments.async_runner import AsyncRunner
from tensorforce.external.openai_gym import OpenAIGymEnvironment
from tensorforce.util.agent_util import create_agent, get_default_config
from tensorforce.util.wrapper_util import create_wrapper


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('gym_id', help="ID of the gym environment")
    parser.add_argument('-a', '--agent', default='DQNAgent')
    parser.add_argument('-c', '--agent-config', help="Agent configuration file",
                        default='examples/configs/dqn_agent.json')
    parser.add_argument('-n', '--network-config', help="Network configuration file",
                        default='examples/configs/dqn_network.json')
    parser.add_argument('-e', '--episodes', type=int, default=10000, help="Number of episodes")
    parser.add_argument('-t', '--max-timesteps', type=int, default=2000, help="Maximum number of timesteps per episode")
    parser.add_argument('-r', '--repeat-actions', type=int, default=4, help="???")
    parser.add_argument('-m', '--monitor', help="Save results to this file")
    args = parser.parse_args()

    environment = OpenAIGymEnvironment(args.gym_id)
    config = Config(environment)
    if args.agent_config:
        config.read_json(args.agent_config)
    if args.network_config:
        config.read_json(args.network_config)

    report_episodes = args.episodes / 10

    state_wrapper = None
    if config.state_wrapper:
        state_wrapper = create_wrapper(config.state_wrapper, config.state_wrapper_param)
        config.state_shape = state_wrapper.state_shape(config.state_shape)

    agent = create_agent(args.agent, config)

    def episode_finished(r):
        if r.episode % report_episodes == 0:
            print("Finished episode {ep} after ??? timesteps".format(ep=r.episode + 1, ts=None))
            print("Total reward: {}".format(r.episode_rewards[-1]))
            print("Average of last 500 rewards: {}".format(np.mean(r.episode_rewards[-500:])))
            print("Average of last 100 rewards: {}".format(np.mean(r.episode_rewards[-100:])))
        return True

    print("Starting {agent_type} for OpenAI Gym '{gym_id}'".format(agent_type=args.agent, gym_id=args.gym_id))
    if args.monitor:
        environment.gym.monitor.start(args.monitor)
        environment.gym.monitor.configure(video_callable=lambda count: False)  # count % 500 == 0)

    runner = AsyncRunner(vars(args), agent=agent, environment=environment, state_wrapper=state_wrapper)
    runner.run(episode_finished=episode_finished)

    if args.monitor:
        environment.gym.monitor.close()
    print("Learning finished. Total episodes: {ep}".format(ep=runner.episode))
    # TODO: Print results.


if __name__ == '__main__':
    main()