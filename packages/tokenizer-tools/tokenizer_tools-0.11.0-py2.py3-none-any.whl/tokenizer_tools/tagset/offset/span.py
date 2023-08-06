class Span(object):
    def __init__(self, start, end, entity, value=None, normal_value=None):
        if start < 0:
            raise AssertionError("start index should greater or equal than zero")
        if end <= start:
            raise AssertionError("end is smaller than or equal to start")
        if not entity:
            raise AssertionError("'{}' is not a legal entity".format(entity))

        self.start = start
        self.end = end
        self.entity = entity
        self.value = value
        self.normal_value = normal_value

    def check_match(self, text):
        if self.end > len(text):
            raise AssertionError("end index should less or equal than lenght of text")

        if self.value is None:  # no value provide so skip match test
            return True

        matched_text = text[self.start: self.end]

        if matched_text != self.value:
            return False

        return True

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            self.__class__.__name__, self.start, self.end, self.entity
        )


if __name__ == "__main__":
    span = Span(0, 9, 'entity')
    print(repr(span))
    assert repr(span) == "Span(0, 9, 'entity')"

    # span = Span(0, 0, 'entity')
    #
    # span = Span(1, 0, 'entity')
