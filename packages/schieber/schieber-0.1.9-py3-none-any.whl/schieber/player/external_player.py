import logging
from multiprocessing import Condition

from schieber.player.challenge_player.challenge_player import ChallengePlayer

from schieber.player.base_player import BasePlayer
from schieber.trumpf import Trumpf

logger = logging.getLogger(__name__)


class ExternalPlayer(ChallengePlayer):
    """
    The RL player in the gym environment wants to initiate control by
        invoking the step() function. This step function sends an action, lets the environment simulate and then
        receives an observation back from the environment.
    In this schieber environment the control is initiated by the Game and not by the player. This is why we need this
        architecture with this external player. The external player blocks when its choose_card() method is called and
        sends the current state received by the Game as an observation to the rl player from gym who connects via a
        websocket. Then the rl agent selects an action and sends it back to this external player. The external player
        submits this action as the chosen card to the Game. The Game simulates the game and this process starts over.
        With the help of this architecture we can use the benefits of the standardized gym environments with many
        rl methods which are already implemented (openai baselines: https://github.com/openai/baselines).
    """

    def __init__(self, name='unknown', seed=None, trumps='all'):
        super().__init__(name, seed, trumps)
        self.action_received = Condition()
        self.observation_received = Condition()

        self.action = {}
        self.observation = {}

    def choose_card(self, state=None):
        """
        Chooses the card and verifies if the chosen card is allowed to be played in the current game state.
        :param state:
        :return:
        """
        # if self.at_last_stich():
        #    allowed = yield self.cards[0]
        # else:
        self.observation_received.acquire()
        self.observation = self.build_observation(state, self.cards)
        logger.debug(f"choose_card received observation: {self.observation}")
        self.observation_received.notify_all()  # notify all threads to be sure
        self.observation_received.release()

        self.action_received.acquire()
        received = self.action_received.wait()
        if not received:
            logger.debug("Timeout occurred. action_received condition has not been notified.")
        logger.debug(f"choose_card received action: {self.action}")
        allowed_cards = self.allowed_cards(state=state)
        chosen_card = allowed_cards[0]  # set chosen_card to the first allowed card in case anything goes south
        chosen_card = self.set_chosen_card(allowed_cards, chosen_card)
        self.action_received.release()

        allowed = yield chosen_card

        if allowed:
            yield None

    @staticmethod
    def build_observation(state, cards):
        observation = state
        observation["cards"] = cards
        return observation

    def set_chosen_card(self, allowed_cards, chosen_card):
        """
        Sets the chosen card based on the action of the RL player.
        :param allowed_cards:
        :param chosen_card:
        :return:
        """
        if self.action is not None:
            if self.action in allowed_cards:
                logger.info(f"Successfully chose the card: {self.action}")
                chosen_card = self.action
            else:
                logger.error(f"{self.action} is not a valid card! Choosing the first allowed card now.")
        else:
            logger.debug("chosen card is None")
        return chosen_card

    def get_observation(self):
        """
        Gets the observation obtained by the game
        :return:
        """
        self.observation_received.acquire()
        received = self.observation_received.wait(0.01)
        if not received:
            print("Timeout occurred. observation_received condition has not been notified.")
        observation = self.observation
        logger.debug(f"get_observation {observation}")
        self.observation_received.release()
        return observation

    def set_action(self, action):
        """
        Sets the action chosen by the RL player
        :param action:
        :return:
        """
        if self.hand_empty():
            logger.error("set_action: There are no cards on my hand, so I cannot choose any card!")
        self.action_received.acquire()
        self.action = action
        logger.debug(f"set_action: {self.action}")
        self.action_received.notify_all()  # notify all threads to be sure
        self.action_received.release()

    def before_first_stich(self):
        """
        Checks if the player has already played any cards in this game
        :return:
        """
        return len(self.cards) == 9

    def at_last_stich(self):
        """
        Checks if the player is at the last stich where there is no choice anymore
        :return:
        """
        return len(self.cards) == 1

    def hand_empty(self):
        """
        Checks if the hand is empty or if there are any cards left.
        :return:
        """
        return len(self.cards) == 0
