"""Validates that the selected character conforms to Lightbringer creation rules gives X many scenarios of
character progression."""
__author__ = 'Josiah Seaman'

from ExaltedCharacter import ExaltedCharacter
from Glossary import ability_list, attribute_list, social, physical, mental, dexterity


def validate_lightbringer(character):
    assert isinstance(character, ExaltedCharacter)

    """Attributes"""
    """Physical, mental and social at a 5"""
    """ Set Dexterity to 5."""
    assert character[dexterity] == 5
    """Choose one Social and one Mental attribute to be rated at 5."""
    for category in [social, mental]:
        assert max([character[att] for att in category] ) >= 5

    """Distribute 6 points in your primary category, 4 in your secondary, 2 in your tertiary."""
    attr_totals = [sum([character[att] for att in category]) for category in (physical, mental, social)]
    attr_totals.sort()
    assert attr_totals[2] >= 2+5+6
    assert attr_totals[1] >= 2+5+4
    assert attr_totals[0] >= 2+5+2
