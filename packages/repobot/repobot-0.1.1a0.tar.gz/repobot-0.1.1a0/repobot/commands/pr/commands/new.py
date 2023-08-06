from .base import Base

from repobot.commands.utils import set_token

class New(Base):

    def run(self):
        print('running the pr')
