import unittest

from gilded_rose import GildedRose, Item


BRIE = "Aged Brie"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"


class GildedRoseTestCase(unittest.TestCase):
    def assert_update(self, name, sell_in, quality, expected_sell_in, expected_quality):
        item = Item(name, sell_in, quality)
        GildedRose([item]).update_quality()
        self.assertEqual((item.sell_in, item.quality),
                         (expected_sell_in, expected_quality))
        self.assertEqual(item.name, name)


class NormalItemTests(GildedRoseTestCase):
    def test_quality_and_sell_in_decrease_by_one(self):
        self.assert_update("+5 Dexterity Vest", 10, 20, 9, 19)

    def test_quality_decreases_twice_as_fast_on_sell_by_date(self):
        self.assert_update("+5 Dexterity Vest", 0, 20, -1, 18)

    def test_quality_decreases_twice_as_fast_after_sell_by_date(self):
        self.assert_update("+5 Dexterity Vest", -1, 20, -2, 18)

    def test_last_day_before_sell_by_date_has_normal_degradation(self):
        self.assert_update("+5 Dexterity Vest", 1, 20, 0, 19)

    def test_quality_never_becomes_negative(self):
        for sell_in in (5, 0, -5):
            for quality in (0, 1):
                with self.subTest(sell_in=sell_in, quality=quality):
                    self.assert_update("Elixir of the Mongoose", sell_in, quality,
                                       sell_in - 1, 0)

    def test_unknown_names_follow_normal_rules(self):
        for name in ("Aged Brie wheel", "Backstage passes", "Sulfuras replica",
                     "Conjuredly ordinary", "Potion of Conjured Mana"):
            with self.subTest(name=name):
                self.assert_update(name, 5, 20, 4, 19)


class AgedBrieTests(GildedRoseTestCase):
    def test_quality_increases_by_one(self):
        self.assert_update(BRIE, 2, 0, 1, 1)

    def test_quality_increases_by_two_on_sell_by_date(self):
        self.assert_update(BRIE, 0, 10, -1, 12)

    def test_quality_increases_by_two_after_sell_by_date(self):
        self.assert_update(BRIE, -1, 10, -2, 12)

    def test_last_day_before_sell_by_date_increases_quality_by_one(self):
        self.assert_update(BRIE, 1, 10, 0, 11)

    def test_quality_is_capped_at_fifty(self):
        for sell_in in (5, 0, -5):
            for quality in (49, 50):
                with self.subTest(sell_in=sell_in, quality=quality):
                    self.assert_update(BRIE, sell_in, quality, sell_in - 1, 50)


class BackstagePassTests(GildedRoseTestCase):
    def test_quality_increase_at_each_boundary(self):
        for sell_in, expected_quality in ((11, 21), (10, 22), (6, 22),
                                          (5, 23), (1, 23)):
            with self.subTest(sell_in=sell_in):
                self.assert_update(BACKSTAGE, sell_in, 20,
                                   sell_in - 1, expected_quality)

    def test_quality_drops_to_zero_on_concert_date(self):
        self.assert_update(BACKSTAGE, 0, 40, -1, 0)

    def test_quality_stays_zero_after_concert(self):
        self.assert_update(BACKSTAGE, -1, 0, -2, 0)

    def test_expired_pass_with_positive_quality_drops_to_zero(self):
        self.assert_update(BACKSTAGE, -2, 40, -3, 0)

    def test_quality_is_capped_at_fifty_in_every_day_band(self):
        cases = ((15, 48, 49), (15, 49, 50), (15, 50, 50),
                 (10, 48, 50), (10, 49, 50), (10, 50, 50),
                 (5, 48, 50), (5, 49, 50), (5, 50, 50))
        for sell_in, quality, expected_quality in cases:
            with self.subTest(sell_in=sell_in, quality=quality):
                self.assert_update(BACKSTAGE, sell_in, quality,
                                   sell_in - 1, expected_quality)

    def test_expired_pass_at_maximum_quality_drops_to_zero(self):
        self.assert_update(BACKSTAGE, 0, 50, -1, 0)


class ConjuredItemTests(GildedRoseTestCase):
    def test_quality_decreases_by_two(self):
        self.assert_update("Conjured Mana Cake", 3, 10, 2, 8)

    def test_quality_decreases_by_four_on_sell_by_date(self):
        self.assert_update("Conjured Mana Cake", 0, 10, -1, 6)

    def test_quality_decreases_by_four_after_sell_by_date(self):
        self.assert_update("Conjured Mana Cake", -1, 10, -2, 6)

    def test_last_day_before_sell_by_date_decreases_quality_by_two(self):
        self.assert_update("Conjured Mana Cake", 1, 10, 0, 8)

    def test_quality_never_becomes_negative_before_sell_by_date(self):
        for quality, expected_quality in ((0, 0), (1, 0), (2, 0), (3, 1)):
            with self.subTest(quality=quality):
                self.assert_update("Conjured Mana Cake", 3, quality,
                                   2, expected_quality)

    def test_quality_never_becomes_negative_after_sell_by_date(self):
        for quality in range(5):
            with self.subTest(quality=quality):
                self.assert_update("Conjured Mana Cake", 0, quality, -1, 0)

    def test_conjured_rule_applies_to_different_item_names(self):
        for name in ("Conjured Mana Cake", "Conjured Sword", "Conjured Potion"):
            with self.subTest(name=name):
                self.assert_update(name, 3, 10, 2, 8)

    def test_multiple_days_crossing_sell_by_date(self):
        item = Item("Conjured Mana Cake", 2, 10)
        shop = GildedRose([item])
        for expected in ((1, 8), (0, 6), (-1, 2), (-2, 0), (-3, 0)):
            shop.update_quality()
            self.assertEqual((item.sell_in, item.quality), expected)


class SulfurasTests(GildedRoseTestCase):
    def test_sell_in_and_quality_do_not_change(self):
        for sell_in in (10, 0, -10):
            with self.subTest(sell_in=sell_in):
                self.assert_update(SULFURAS, sell_in, 80, sell_in, 80)

    def test_sulfuras_does_not_change_over_multiple_days(self):
        item = Item(SULFURAS, -1, 80)
        shop = GildedRose([item])
        for _ in range(30):
            shop.update_quality()
        self.assertEqual((item.sell_in, item.quality), (-1, 80))


class InventoryTests(unittest.TestCase):
    def test_empty_inventory_can_be_updated(self):
        items = []
        shop = GildedRose(items)
        shop.update_quality()
        self.assertIs(shop.items, items)
        self.assertEqual(items, [])

    def test_updates_existing_items_in_the_original_list(self):
        items = [Item("+5 Dexterity Vest", 1, 10), Item(BRIE, 1, 10),
                 Item(BACKSTAGE, 1, 10), Item(SULFURAS, 1, 80),
                 Item("Conjured Mana Cake", 1, 10)]
        originals = list(items)
        shop = GildedRose(items)
        shop.update_quality()
        self.assertIs(shop.items, items)
        for actual, original in zip(items, originals):
            self.assertIs(actual, original)
        self.assertEqual([(item.sell_in, item.quality) for item in items],
                         [(0, 9), (0, 11), (0, 13), (1, 80), (0, 8)])

    def test_item_representation_is_unchanged(self):
        self.assertEqual(repr(Item("Elixir of the Mongoose", 5, 7)),
                         "Elixir of the Mongoose, 5, 7")


if __name__ == "__main__":
    unittest.main()
