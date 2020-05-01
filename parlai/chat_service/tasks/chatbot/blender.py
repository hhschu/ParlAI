#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# py parlai/chat_service/tasks/overworld_demo/run.py --debug --verbose

from parlai.core.worlds import World
from parlai.chat_service.services.messenger.worlds import OnboardWorld
from parlai.core.agents import create_agent_from_shared


class OnboardWorld(OnboardWorld):
    @staticmethod
    def generate_world(opt, agents):
        return OnboardWorld(opt=opt, agent=agents[0])

    def parley(self):
        self.episodeDone = True


class TaskWorld(World):
    MAX_AGENTS = 1

    def __init__(self, opt, agent, bot):
        self.agent = agent
        self.episodeDone = False
        self.model = bot

    @staticmethod
    def generate_world(opt, agents):
        if opt['models'] is None:
            raise RuntimeError("Model must be specified")
        return TaskWorld(
            opt,
            agents[0],
            create_agent_from_shared(opt['shared_bot_params']['blender']),
        )

    @staticmethod
    def assign_roles(agents):
        agents[0].disp_id = 'ChatbotAgent'

    def parley(self):
        a = self.agent.act()
        if a is not None:
            if '[DONE]' in a['text']:
                self.episodeDone = True
            else:
                self.model.observe(a)
                response = self.model.act()
                self.agent.observe(response)

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown()


class Overworld(World):
    def __init__(self, opt, agent):
        self.agent = agent
        self.opt = opt
        self.episodeDone = False

    @staticmethod
    def generate_world(opt, agents):
        return Overworld(opt, agents[0])

    @staticmethod
    def assign_roles(agents):
        for a in agents:
            a.disp_id = 'Agent'

    def episode_done(self):
        return self.episodeDone

    def parley(self):
        self.episodeDone = True
        return 'default'
