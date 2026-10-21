import unittest

from gilded_rose import GildedRose, Item
from tests.fixtures.gilded_rose_original import GildedRose as OriginalGildedRose
from tests.fixtures.gilded_rose_original import Item as OriginalItem


class LegacyBehaviorTests(unittest.TestCase):
    def test_existing_items_match_original_for_twenty_days(self):
        names = ("+5 Dexterity Vest", "Aged Brie",
                 "Backstage passes to a TAFKAL80ETC concert",
                 "Sulfuras, Hand of Ragnaros")
        for name in names:
            qualities = (80,) if name == "Sulfuras, Hand of Ragnaros" else range(51)
            for sell_in in range(-2, 16):
                for quality in qualities:
                    with self.subTest(name=name, sell_in=sell_in, quality=quality):
                        item = Item(name, sell_in, quality)
                        original = OriginalItem(name, sell_in, quality)
                        shop = GildedRose([item])
                        original_shop = OriginalGildedRose([original])
                        for day in range(1, 21):
                            shop.update_quality()
                            original_shop.update_quality()
                            self.assertEqual(
                                (item.name, item.sell_in, item.quality),
                                (original.name, original.sell_in, original.quality),
                                f"Different result on day {day}",
                            )


if __name__ == "__main__":
    unittest.main()
