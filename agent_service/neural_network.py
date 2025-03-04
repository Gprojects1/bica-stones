class NeuralNetwork:
    def choose_stone(self, move_data: dict[int, tuple[bool, list[int]]]) -> int:
        for stone, (is_available, _) in move_data.items():
            if is_available:
                return stone
        raise ValueError("No available stones")