import argparse

from gilded_rose import GildedRose, Item


def main():
    parser = argparse.ArgumentParser(description="Show the inventory over a few days.")
    parser.add_argument("days", type=int, nargs="?", default=2)
    args = parser.parse_args()
    if args.days < 0:
        parser.error("days must be zero or greater")

    items = [
        Item("+5 Dexterity Vest", 10, 20),
        Item("Aged Brie", 2, 0),
        Item("Elixir of the Mongoose", 5, 7),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),
        Item("Backstage passes to a TAFKAL80ETC concert", 5, 20),
        Item("Conjured Mana Cake", 1, 10),
    ]
    shop = GildedRose(items)

    for day in range(args.days + 1):
        print(f"-------- day {day} --------")
        print("name, sell_in, quality")
        for item in items:
            print(item)
        print()
        if day < args.days:
            shop.update_quality()


if __name__ == "__main__":
    main()
