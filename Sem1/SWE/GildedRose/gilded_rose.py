# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue

            if item.name == "Aged Brie":
                self._update_brie(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self._update_backstage_pass(item)
            else:
                daily_loss = 2 if item.name.startswith("Conjured ") else 1
                self._update_degrading_item(item, daily_loss)

            # Use the starting sell_in value for today's update.
            item.sell_in -= 1

    def _update_brie(self, item):
        increase = 2 if item.sell_in <= 0 else 1
        item.quality = min(50, item.quality + increase)

    def _update_backstage_pass(self, item):
        if item.sell_in <= 0:
            item.quality = 0
            return

        if item.sell_in <= 5:
            increase = 3
        elif item.sell_in <= 10:
            increase = 2
        else:
            increase = 1
        item.quality = min(50, item.quality + increase)

    def _update_degrading_item(self, item, daily_loss):
        if item.sell_in <= 0:
            daily_loss *= 2
        item.quality = max(0, item.quality - daily_loss)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
