import random


class LadderGame:
    def __init__(self, num_verticals=8, num_vertical_slots=30, num_steps=15):
        self.num_verticals = num_verticals
        self.num_vertical_slots = num_vertical_slots
        self.num_steps = num_steps
        self.verticals = []

        self.create_ladder()

    def create_ladder(self):
        for i in range(self.num_verticals):
            vertical = {
                'number': i + 1,
                'is_first': i == 0,
                'is_last': i == (self.num_verticals - 1),
                'slots': [None for _ in range(self.num_vertical_slots)],
                'value': None
            }
            self.verticals.append(vertical)

        self.create_steps()

    def create_steps(self):
        num_added_steps = 0
        while num_added_steps < self.num_steps:
            vertical_index = random.randint(0, self.num_verticals - 1)
            # Leave the last slot None
            slot_index = random.randint(0, self.num_vertical_slots - 2)

            if self.add_step(vertical_index, slot_index):
                num_added_steps += 1

    def add_step(self, vertical_index, slot_index):
        if vertical_index >= self.num_verticals:
            raise IndexError

        vertical = self.verticals[vertical_index]
        if vertical['is_last']:
            return False

        if vertical['slots'][slot_index] is not None:
            return False

        right_vertical = self.verticals[vertical_index + 1]
        if right_vertical['slots'][slot_index] is not None:
            return False

        vertical['slots'][slot_index] = {
            'direction': 'right',
            'vertical': right_vertical,
            'slot_index': slot_index
        }
        right_vertical['slots'][slot_index] = {
            'direction': 'left',
            'vertical': vertical,
            'slot_index': slot_index
        }

        return True

    def set_value(self, v_number, value):
        if 0 < v_number <= self.num_verticals:
            self.verticals[v_number - 1]['value'] = value
        else:
            raise IndexError

    def get_value_for_vertical(self, v_number):
        current_vertical = self.verticals[v_number - 1]
        current_slot = 0
        while current_slot < self.num_vertical_slots:
            if current_vertical['slots'][current_slot] is not None:
                current_vertical = current_vertical['slots'][current_slot]['vertical']
            current_slot += 1

        return current_vertical['value']


if __name__ == '__main__':
    result = [0 for _ in range(8)]

    for g in range(1000):
        game = LadderGame(num_verticals=8, num_vertical_slots=30, num_steps=15)
        game.set_value(4, 'Star')
        for i in range(8):
            value = game.get_value_for_vertical(i + 1)
            if value == 'Star':
                result[i] = result[i] + 1
                break
