from abc import ABC, abstractmethod
from enum import Enum


class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class LibraryItem(ABC):
    def __init__(self, title):
        self.title = title
        self._status = ItemStatus.AVAILABLE

    @property
    def status(self):
        return self._status

    @abstractmethod
    def loan_period(self):
        pass

    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError("Item is not available")
        self._status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError("Item is not checked out")
        self._status = ItemStatus.AVAILABLE

    def mark_lost(self):
        if self._status == ItemStatus.LOST:
            raise ValueError("Item is already lost")
        self._status = ItemStatus.LOST

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __str__(self):
        return f"{self.title} ({self.__class__.__name__}) — {self.status.value.title()}"

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r})"

    @staticmethod
    def validate_isbn(isbn):
        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) != 13 or not isbn.isdigit():
            return False

        total = 0

        for i, digit in enumerate(isbn):
            if i % 2 == 0:
                total += int(digit)
            else:
                total += int(digit) * 3

        return total % 10 == 0


class Book(LibraryItem):
    def __init__(self, title, author, isbn):
        super().__init__(title)
        self.author = author
        self.isbn = isbn

    def loan_period(self):
        return 21


class DVD(LibraryItem):
    def __init__(self, title, director):
        super().__init__(title)
        self.director = director

    def loan_period(self):
        return 5


class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title)
        self.issue = issue

    def loan_period(self):
        return 14


class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def checkout(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError("Item not found")

        item.checkout()

    def return_item(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError("Item not found")

        item.return_item()

    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item

        return None

    def list_available(self):
        return [
            item for item in self.items
            if item.status == ItemStatus.AVAILABLE
        ]


class Database:
    def __init__(self, filename="database.txt"):
        self.filename = filename

    def save(self, items):
        with open(self.filename, "w") as file:
            for item in items:
                if isinstance(item, Book):
                    line = (
                        f"type=Book|title={item.title}|author={item.author}|"
                        f"isbn={item.isbn}|status={item.status.value}"
                    )

                elif isinstance(item, DVD):
                    line = (
                        f"type=DVD|title={item.title}|director={item.director}|"
                        f"status={item.status.value}"
                    )

                elif isinstance(item, Magazine):
                    line = (
                        f"type=Magazine|title={item.title}|issue={item.issue}|"
                        f"status={item.status.value}"
                    )

                file.write(line + "\n")

    def load(self):
        items = []

        try:
            with open(self.filename, "r") as file:
                for line in file:
                    data = {}

                    for part in line.strip().split("|"):
                        key, value = part.split("=", 1)
                        data[key] = value

                    item = LibraryItem.from_dict(data)
                    items.append(item)

        except FileNotFoundError:
            pass

        return items


def from_dict(data):
    item_type = data["type"]

    if item_type == "Book":
        item = Book(data["title"], data["author"], data["isbn"])

    elif item_type == "DVD":
        item = DVD(data["title"], data["director"])

    elif item_type == "Magazine":
        item = Magazine(data["title"], data["issue"])

    else:
        raise ValueError("Unknown item type")

    item._status = ItemStatus[data["status"]]

    return item


LibraryItem.from_dict = classmethod(lambda cls, data: from_dict(data))