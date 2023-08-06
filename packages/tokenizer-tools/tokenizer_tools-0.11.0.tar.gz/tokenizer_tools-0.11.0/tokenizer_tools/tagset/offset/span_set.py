import itertools

from tokenizer_tools.tagset.offset.span import Span


class SpanSet(list):
    @staticmethod
    def _are_separate(r: Span, s: Span) -> bool:
        # learned from https://stackoverflow.com/questions/27182137/check-if-two-lines-each-with-start-end-positions-overlap-in-python
        return r.end <= s.start or s.end <= r.start

    def check_overlap(self):
        comb = list(
            itertools.combinations(self, 2)
        )

        false_results = list(
            itertools.filterfalse(
                lambda x: self._are_separate(*x),
                comb
            )
        )

        if false_results:
            # raise AssertionError("spans are overlaped; total count: {} failed".format(false_results))
            return False

        return True

    def check_match(self, text):
        false_results = list(
            itertools.filterfalse(
                lambda x: x.check_match(text),
                self
            )
        )

        if false_results:
            # raise AssertionError("check match failed; total count: {} failed".format(false_results))
            return False

        return True


if __name__ == "__main__":
    # span_set = SpanSet()
    # span_set.append(Span(1, 2, 'entity'))
    # span_set.append(Span(2, 3, 'entity'))
    # span_set.check_overlap()

    span_set = SpanSet()
    span_set.append(Span(1, 2, 'entity'))
    span_set.append(Span(4, 6, 'entity'))
    span_set.check_overlap()


    # span_set = SpanSet()
    # span_set.append(Span(1, 4, 'entity'))
    # span_set.append(Span(2, 3, 'entity'))
    # span_set.check_overlap()



