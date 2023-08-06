"""Tabular, frontend-representation of financeager period."""
from . import DEFAULT_TABLE
from .entries import BaseEntry, CategoryEntry


class Model(object):
    """Holds Entries in hierarchical order. First-level children are
    CategoryEntries, second-level children are BaseEntries. Generator methods
    are provided to iterate over these."""

    CATEGORY_ENTRY_SORT_KEY = "value"

    def __init__(self, name=None, categories=None):
        self.name = name or "Model"
        self.categories = categories or []

    @classmethod
    def from_elements(cls, elements, name=None):
        """Create model from list of element dictionaries"""
        model = cls(name=name)
        for element in elements:
            category = element.pop("category", None)
            model.add_entry(BaseEntry(**element), category_name=category)
        return model

    def __str__(self):
        """Format model (incl. name and header)."""
        result = ["{1:^{0}}".format(CategoryEntry.TOTAL_LENGTH, self.name)]

        header_line = "{3:{0}} {4:{1}} {5:{2}}".format(
            CategoryEntry.NAME_LENGTH, BaseEntry.VALUE_LENGTH,
            BaseEntry.DATE_LENGTH, *[k.capitalize() for k in
                                     BaseEntry.ITEM_TYPES])
        if BaseEntry.SHOW_EID:
            header_line += " " + "ID".ljust(BaseEntry.EID_LENGTH)
        result.append(header_line)

        sort_key = lambda e: getattr(e, Model.CATEGORY_ENTRY_SORT_KEY)
        for category in sorted(self.categories, key=sort_key):
            result.append(str(category))

        return '\n'.join(result)

    def add_entry(self, entry, category_name=None):
        """Add a Category- or BaseEntry to the model.
        Category names are unique, i.e. a CategoryEntry is discarded if one
        with identical name (case INsensitive) already exists.
        When adding a BaseEntry, the parent CategoryEntry is created if it does
        not exist. If no category is specified, the BaseEntry is added to the
        default category. The CategoryEntry's value is updated.

        :raises: TypeError if neither CategoryEntry nor BaseEntry given
        """

        if category_name is None:
            category_name = CategoryEntry.DEFAULT_NAME

        if isinstance(entry, CategoryEntry):
            if entry.name not in self.category_entry_names:
                self.categories.append(entry)
        elif isinstance(entry, BaseEntry):
            self.add_entry(CategoryEntry(name=category_name))
            category_item = self.find_category_entry(category_name)
            category_item.append(entry)
        else:
            raise TypeError("Invalid entry type: {}".format(entry))

    def category_fields(self, field_type):
        """Generator iterating over the field specified by `field_type` of the
        first-level children (CategoryEntries) of the model.

        :param field_type: 'name' or 'value'

        raises: KeyError if `field_type` not found.
        yields: str or float
        """
        for category_entry in self.categories:
            yield getattr(category_entry, field_type)

    def base_entry_fields(self, field_type):
        """Generator iterating over the field specified by `field_type` of the
        second-level children (BaseEntries) of the model.

        :param field_type: 'name', 'value' or 'date'

        raises: KeyError if `field_type` not found.
        yields: str, float or datetime.date
        """
        for category_entry in self.categories:
            for base_entry in category_entry.entries:
                yield getattr(base_entry, field_type)

    @property
    def category_entry_names(self):
        """Convenience generator method yielding category names."""
        for category_name in self.category_fields("name"):
            yield category_name

    def find_category_entry(self, category_name):
        """Find CategoryEntry by given `category_name` or return None if not
        found. The search is case insensitive."""

        category_name = category_name.lower()
        for category_entry in self.categories:
            if category_entry.name == category_name:
                return category_entry
        return None

    def category_sum(self, category_name):
        """Return total value of category named `category_name`."""
        category_entry = self.find_category_entry(category_name)
        if category_entry is not None:
            return category_entry.value
        return 0.0

    def total_value(self):
        """Return total value of the model."""
        result = 0.0
        for value in self.category_fields("value"):
            result += value
        return result


def prettify(elements, stacked_layout=False):
    """Sort the given elements (type acc. to Period._search_all_tables) by
    positive and negative value and return pretty string build from the
    corresponding Models.

    :param stacked_layout: If True, models are displayed one by one
    """

    earnings = []
    expenses = []

    def _sort(eid, element):
        # Copying avoids modifying the original element. Flattening is in order
        # to distinguish recurrent entries (they have the same element ID which
        # thus can't be used as dict key)
        flat_element = element.copy()
        flat_element["eid"] = eid
        if flat_element["value"] > 0:
            earnings.append(flat_element)
        else:
            expenses.append(flat_element)

    # process standard elements
    for eid, element in elements[DEFAULT_TABLE].items():
        _sort(eid, element)

    # process recurrent elements, i.e. for each eid iterate list
    for eid, recurrent_elements in elements["recurrent"].items():
        for element in recurrent_elements:
            _sort(eid, element)

    if not earnings and not expenses:
        return ""

    model_earnings = Model.from_elements(earnings, name="Earnings")
    model_expenses = Model.from_elements(expenses, name="Expenses")

    if stacked_layout:
        return "{}\n\n{}\n\n{}".format(
                str(model_earnings),
                CategoryEntry.TOTAL_LENGTH * "-",
                str(model_expenses)
                )
    else:
        result = []
        models = [model_earnings, model_expenses]
        models_str = [str(m).splitlines() for m in models]
        for row in zip(*models_str):
            result.append(" | ".join(row))
        earnings_size = len(models_str[0])
        expenses_size = len(models_str[1])
        diff = earnings_size - expenses_size
        if diff > 0:
            for row in models_str[0][expenses_size:]:
                result.append(row + " | ")
        else:
            for row in models_str[1][earnings_size:]:
                result.append(CategoryEntry.TOTAL_LENGTH * " " + " | " + row)
        # add 3 to take central separator " | " into account
        result.append((2 * CategoryEntry.TOTAL_LENGTH + 3) * "=")

        # add total value of earnings and expenses as final line
        total_values = []
        for m in models:
            total_entry = CategoryEntry(name="TOTAL")
            total_entry.value = m.total_value()
            total_values.append(str(total_entry))
        result.append(" | ".join(total_values))

        return '\n'.join(result)
