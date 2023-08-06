import collections
import re


try:
    _input = raw_input  # Python2.7
except NameError:
    _input = input  # Python3.+


Preference = collections.namedtuple("Preference", ["name", "value"])


def get_preferences(preference_inputs, cmd_args):
    if cmd_args.yes:
        return {
            pref_input._name: pref_input.default() for pref_input in preference_inputs
        }

    preferences = [pref_input.get() for pref_input in preference_inputs]
    _print_overview(preferences)
    correct = _input("Is this correct? (yes) ").lower().strip() or "yes"
    if correct not in ("yes", "y"):
        print("")
        return get_preferences(preference_inputs, cmd_args)
    return {pref.name: pref for pref in preferences}


class PreferenceInput:
    def __init__(
        self,
        name,
        description,
        default_value,
        *,
        yes_or_no=False,
        regex=None,
        requirements=None
    ):
        self._name = name
        self._description = description
        self._default_value = default_value
        self._yes_or_no = yes_or_no
        self._regex = regex
        self._requirements = requirements

    def get(self):
        descr = self._description
        deflt = self._default_value
        value = _input("%s (%s) " % (descr, deflt)) or deflt
        if self._regex:
            match = re.match(self._regex, value)
            if not match or match.group(0) != value:
                if self._requirements:
                    print("Invalid input. %s" % self._requirements)
                else:
                    print("Invalid input.")
                print("")
                return self.get()
        if self._yes_or_no:
            value = value.lower() in ("yes", "y")
        return Preference(self._name, value)

    def default(self):
        return Preference(self._name, self._default_value)


def _print_overview(preferences):
    print("")
    print("Setup overview")
    print("--------------")
    sorted_by_name = list(preferences)
    sorted_by_name.sort(key=lambda pref: len(pref.name))
    longest_name_len = len(sorted_by_name[-1].name)
    for pref in preferences:
        len_dif = longest_name_len - len(pref.name)
        print("%s: %s%s" % (pref.name, (len_dif * " "), pref.value))
    print("")
