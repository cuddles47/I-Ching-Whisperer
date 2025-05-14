import random
from typing import Dict, Any

from app.data.hexagrams import HEXAGRAMS, get_hexagram_by_number

class IChing:
    @staticmethod
    def cast_yarrow_stalks() -> int:
        """
        Simulates the traditional yarrow stalk method to generate a line.
        Returns 6, 7, 8, or 9 (corresponding to yin changing, yang, yin, or yang changing).
        """
        # Traditional yarrow stalk probabilities
        # 9 (old yang): 1/16
        # 8 (young yin): 7/16
        # 7 (young yang): 7/16
        # 6 (old yin): 1/16
        
        possibilities = [6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9]
        return random.choice(possibilities)

    @staticmethod
    def cast_coins() -> int:
        """
        Simulates the three-coin method to generate a line.
        Returns 6, 7, 8, or 9 (corresponding to yin changing, yang, yin, or yang changing).
        """
        # Three coins are tossed - heads (value 3) and tails (value 2)
        # The sum determines the line:
        # 9 (old yang, changing to yin): 3 tails = 6
        # 8 (young yin): 2 tails, 1 head = 7
        # 7 (young yang): 1 tail, 2 heads = 8
        # 6 (old yin, changing to yang): 3 heads = 9
        
        coins = [random.choice([2, 3]) for _ in range(3)]
        total = sum(coins)
        
        # Convert to traditional I Ching values (6, 7, 8, 9)
        if total == 6:  # 3 tails
            return 9  # old yang (changing)
        elif total == 7:  # 2 tails, 1 head
            return 8  # young yin
        elif total == 8:  # 1 tail, 2 heads
            return 7  # young yang
        else:  # total == 9, 3 heads
            return 6  # old yin (changing)

    @staticmethod
    def generate_hexagram(method: str = "coins") -> Dict[str, Any]:
        """
        Generates a random hexagram using either the coin or yarrow stalk method.
        Returns a dictionary with hexagram information.
        """
        # Cast six lines using specified method
        lines = []
        for _ in range(6):
            if method == "yarrow":
                line = IChing.cast_yarrow_stalks()
            else:  # default to coins
                line = IChing.cast_coins()
            lines.append(line)
        
        # Convert to hexagram number (1-64)
        # This is a simplified implementation
        # In a production system, you'd implement the full algorithm
        # to convert lines to trigrams and then to hexagram number
        hexagram_number = (sum(lines) % 64) + 1
        
        # Get hexagram information
        hexagram = get_hexagram_by_number(hexagram_number)
        if not hexagram:
            # If not found, default to first hexagram
            hexagram = HEXAGRAMS[0]
        
        return hexagram

    @staticmethod
    def cast_divination() -> Dict[str, Any]:
        """Perform a complete I Ching divination"""
        return IChing.generate_hexagram()
