from collections import defaultdict
import re
from typing import Any, Dict


def process_bylines(entry_list) -> Dict[str, Any]:
    bylines = defaultdict(lambda: {"articles": [], "count": 0})

    regex_single_byline = r"B([yY]) (\w+) (\w+)"
    regex_double_byline = r"B([yY]) (\w+) (\w+) AND (\w+) (\w+)"
    regex_triple_byline = r"B([yY]) (\w+) (\w+), (\w+) (\w+) AND (\w+) (\w+)"

    for entry in entry_list:
        try:
            entry["author"]
        except KeyError:
            continue
        match_three = re.match(regex_triple_byline, entry["author"])
        if match_three is None:
            match_two = re.match(regex_double_byline, entry["author"])
            if match_two is None:
                match_one = re.match(regex_single_byline, entry["author"])
                if match_one is None:
                    print("Nothing found for: " + entry["author"])
                    pass
                elif match_one.group(2) + " " + match_one.group(3) == "STAFF REPORTS":
                    pass
                else:
                    key_string = f"{match_one.group(2)} {match_one.group(3)}"
                    bylines[key_string]["articles"].append(entry["title"])
                    bylines[key_string]["count"] = bylines[key_string]["count"] + 1
            else:
                key_string = f"{match_two.group(2)} {match_two.group(3)}"
                bylines[key_string]["articles"].append(entry["title"])
                bylines[key_string]["count"] = bylines[key_string]["count"] + 1

                key_string = f"{match_two.group(4)} {match_two.group(5)}"
                bylines[key_string]["articles"].append(entry["title"])
                bylines[key_string]["count"] = bylines[key_string]["count"] + 1
        else:
            key_string = f"{match_three.group(2)} {match_three.group(3)}"
            bylines[key_string]["articles"].append(entry["title"])
            bylines[key_string]["count"] = bylines[key_string]["count"] + 1

            key_string = f"{match_three.group(4)} {match_three.group(5)}"
            bylines[key_string]["articles"].append(entry["title"])
            bylines[key_string]["count"] = bylines[key_string]["count"] + 1

            key_string = f"{match_three.group(6)} {match_three.group(7)}"
            bylines[key_string]["articles"].append(entry["title"])
            bylines[key_string]["count"] = bylines[key_string]["count"] + 1

    return bylines
