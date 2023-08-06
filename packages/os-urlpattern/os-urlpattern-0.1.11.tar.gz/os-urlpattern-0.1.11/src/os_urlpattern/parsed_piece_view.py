"""ParsedPieceView and subclass implementation.
"""
from __future__ import unicode_literals

from .definition import DIGIT_AND_ASCII_RULE_SET, BasePatternRule
from .parse_utils import ParsedPiece, fuzzy_join, mix
from .utils import pick


class ParsedPieceView(object):
    """The base class of parsed piece view.

    View object is a wrapper of parsed piece, which have individual
    view, parsed_piece and parsed_pieces propertys are based on the
    raw parsed piece.

    """
    __slots__ = ('parsed_piece', '_parsed_pieces', '_view')

    def __init__(self, parsed_piece):
        self.parsed_piece = parsed_piece
        self._parsed_pieces = None
        self._view = None

    def __eq__(self, o):
        if not isinstance(o, ParsedPieceView):
            return False
        return self.view == o.view

    def __hash__(self):
        return hash(self.view)

    @property
    def view(self):
        if self._view is None:
            self._view = fuzzy_join(self.parsed_pieces)
        return self._view

    @property
    def parsed_pieces(self):
        if self._parsed_pieces:
            return self._parsed_pieces

        self._parsed_pieces = [ParsedPiece((piece,), (rule,)) for piece, rule in zip(
            self.parsed_piece.pieces, self.parsed_piece.rules)]
        return self._parsed_pieces


class PieceView(ParsedPieceView):

    def __init__(self, parsed_piece):
        super(PieceView, self).__init__(parsed_piece)
        self._view = self.parsed_piece.piece


class LengthView(ParsedPieceView):

    def __init__(self, parsed_piece):
        super(LengthView, self).__init__(parsed_piece)
        self._view = self.parsed_piece.piece_length


class MultiView(ParsedPieceView):
    pass


class MixedView(ParsedPieceView):

    @property
    def parsed_pieces(self):
        if self._parsed_pieces:
            return self._parsed_pieces

        if len(self.parsed_piece.rules) <= 1:
            self._parsed_pieces = [self.parsed_piece]
        else:
            mixed_pieces, mixed_rules = mix(
                self.parsed_piece.pieces, self.parsed_piece.rules)

            self._parsed_pieces = [ParsedPiece(
                (piece,), (rule,)) for piece, rule in zip(mixed_pieces, mixed_rules)]
        return self._parsed_pieces


class LastDotSplitFuzzyView(ParsedPieceView):

    @property
    def parsed_pieces(self):
        if self._parsed_pieces:
            return self._parsed_pieces
        rules = self.parsed_piece.rules
        dot_idx = None
        part_num = len(rules)
        for idx, rule in enumerate(reversed(rules)):
            if idx > 2:
                break
            if rule == BasePatternRule.DOT:
                dot_idx = part_num - idx - 1
                break
        self._parsed_pieces = [ParsedPiece((self.parsed_piece.piece,),
                                           (self.parsed_piece.fuzzy_rule,))]
        if dot_idx is not None:
            skip = False
            for rule in self.parsed_piece.rules[dot_idx + 1:]:
                if rule not in DIGIT_AND_ASCII_RULE_SET:
                    skip = True
                    break
            if not skip:
                pieces = []
                rules = []
                pieces.append(''.join(self.parsed_piece.pieces[0:dot_idx]))
                pieces.append(self.parsed_piece.pieces[dot_idx])
                rules.append(
                    ''.join(sorted(set(self.parsed_piece.rules[0:dot_idx]))))
                rules.append(self.parsed_piece.rules[dot_idx])
                mixed_pieces, mixed_rules = mix(
                    self.parsed_piece.pieces[dot_idx + 1:],
                    self.parsed_piece.rules[dot_idx + 1:])
                pieces.extend(mixed_pieces)
                rules.extend(mixed_rules)
                self._parsed_pieces = [ParsedPiece(
                    (piece,), (rule,)) for piece, rule in zip(pieces, rules)]
        return self._parsed_pieces


class FuzzyView(ParsedPieceView):

    def __init__(self, parsed_piece):
        super(FuzzyView, self).__init__(parsed_piece)
        self._view = self.parsed_piece.fuzzy_rule

    @property
    def parsed_pieces(self):
        if self._parsed_pieces:
            return self._parsed_pieces
        self._parsed_pieces = [ParsedPiece((self.parsed_piece.piece,),
                                           (self.parsed_piece.fuzzy_rule,))]
        return self._parsed_pieces


def view_cls_from_pattern(pattern, is_last_path=False):
    """Get ParsedPieceView class from pattern.

    ParsedPieceView type can be deduced from the pattern.

    Args:
        pattern (Pattern): The Pattern object.
        is_last_path (bool, optional): Defaults to False. Whether the pattern
            is at the last path position.

    Returns:
        class: The class of ParsedPieceView.
    """
    view_cls = PieceView
    pattern_units = pattern.pattern_units
    if len(pattern_units) == 1:
        pattern_unit = pattern_units[0]
        if not pattern_unit.is_literal():
            if pattern_unit.num < 0:
                view_cls = FuzzyView
            else:
                view_cls = LengthView
    else:
        for pattern_unit in pattern_units:
            if not pattern_unit.is_literal():
                if len(pattern_unit.rules) > 1:
                    view_cls = MixedView
                    break
                else:
                    view_cls = MultiView
        if is_last_path \
                and len(pattern_units) == 3 \
                and view_cls != PieceView \
                and len(pattern_units[1].rules) == 1 \
                and pick(pattern_units[1].rules) == BasePatternRule.DOT \
                and not (set(pattern_units[-1].rules) - DIGIT_AND_ASCII_RULE_SET):
            view_cls = LastDotSplitFuzzyView

    return view_cls
