# Copyright 2017 reinforce.io. All Rights Reserved.
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

from tensorforce.core.explorations import Exploration


class EpsilonAnneal(Exploration):
    """
    Annealing epsilon parameter based on ratio of current timestep to total timesteps.
    """

    def __init__(self, epsilon=1.0, epsilon_final=0.1, epsilon_timesteps=10000):
        self.epsilon = epsilon
        self.epsilon_final = epsilon_final
        self.epsilon_timesteps = epsilon_timesteps

    def __call__(self, episode=0, timestep=0):
        # TODO: Trim by length of `first_update`, removing steps with no learning.
        offset = 0 # self.first_update
        self.epsilon = min(1.0, max(
            self.epsilon_final,
            1.0 - (timestep - offset) / (self.epsilon_timesteps - offset)
        ))

        return self.epsilon
