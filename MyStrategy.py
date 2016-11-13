from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World


class MyStrategy:
    def __init__(self):
        self.perception = Perception();
        self.position = Position();
        self.decision = Decision();

    def move(self, me: Wizard, world: World, game: Game, move: Move):
        self.perception.update(me, world, game);
        self.position.update(move, self.perception);
        self.decision.update(me, move, game);

class Perception:
    def update(self, me: Wizard, world: World, game: Game):
        self.me = me;
        self.world = world;
        self.game = game;
        self.allied_minions = [];

    def get_allied_minions(self):
        if (len(self.allied_minions) > 0):
            return self.allied_minions;
        self.allied_minions = []
        for minion in self.world.minions:
            if minion.faction == self.me.faction:
                self.allied_minions.append((self.me.get_distance_to_unit(minion), minion))
        return sorted(self.allied_minions, key=lambda m: m[0])


class Position:
    def update(self, move, perception):
        self.move = move;
        self.perception = perception;
        self.follower();

    def follower(self):
        minions = self.perception.get_allied_minions();
        if (len(minions) < 1):
            return;
        target = minions[0];
        if (len(target) < 2):
            return;
        self.move.turn = self.perception.me.get_angle_to_unit(target[1]);
        self.move.speed = self.perception.game.wizard_forward_speed
        self.move.strafe_speed = self.perception.game.wizard_strafe_speed


class Decision:
    def update(self, me, move, game):
        self.me = me;
        self.move = move;
        self.game = game;
        move.action = ActionType.MAGIC_MISSILE
