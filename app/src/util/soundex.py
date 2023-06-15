import re

consonant = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
vowel = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
final_consonant = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]
pairs = {
    "ㅏ": "ㅑ",
    "ㅑ": "ㅏ",
    "ㅓ": "ㅕ",
    "ㅕ": "ㅓ",
    "ㅗ": "ㅛ",
    "ㅛ": "ㅗ",
    "ㅜ": "ㅠ",
    "ㅠ": "ㅜ",
}

oral_consonant = ["ㄱ", "ㄷ", "ㄹ", "ㅂ", "ㅅ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅎ"]
nasal_consonant = ["ㅁ", "ㄴ", "ㅇ"]
liquid_consonant = ["ㄹ"]


exceptions = ["ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅗ"]


def jamo_split(char):
    base = ord(char) - ord("가")
    c = base // 588
    v = (base - 588 * c) // 28
    f_c = base - 588 * c - 28 * v
    return [consonant[c], vowel[v], final_consonant[f_c]]


def jamo_merge(jamo_list):
    if jamo_list[1:] == ["", ""]:
        return jamo_list[0]
    c, v, f_c = [_list.index(j) for _list, j in zip([consonant, vowel, final_consonant], jamo_list)]
    return chr(f_c + 588 * c + 28 * v + ord("가"))


def palatalization(fc, nc):
    palatal = {"ㄷ": "ㅈ", "ㅌ": "ㅊ"}
    if (fc[-1] in palatal) and nc[:-1] == ["ㅇ", "ㅣ"]:
        nc[0] = palatal[fc[-1]]
        fc[-1] = " "
    return fc, nc


def liquidization(fc, nc):
    liquid_set = {"ㄴㄹ": "ㄹㄹ", "ㄹㄴ": "ㄹㄹ", "ㄾㄴ": "ㄹㄹ"}
    exception_set = {"ㄴㄹㅕㄱ": "ㄴㄴ"}

    if fc[-1] + "".join(nc) in exception_set:
        fc[-1], nc[0] = exception_set[fc[-1] + "".join(nc)]
        return fc, nc
    else:
        if fc[-1] + nc[0] in liquid_set:
            fc[-1], nc[0] = liquid_set[fc[-1] + nc[0]]
        return fc, nc


def nasalization(fc, nc):
    nasalization_set = {
        "ㅂㅁ": "ㅁㅁ",
        "ㄷㄴ": "ㄴㄴ",
        "ㄱㅁ": "ㅇㅁ",
        "ㄱㄴ": "ㅇㄴ",
        "ㅇㄹ": "ㅇㄴ",
        "ㅁㄹ": "ㅁㄴ",
        "ㄲㄴ": "ㅇㄴ",
        "ㅂㄹ": "ㅁㄴ",
        "ㄱㄹ": "ㅇㄴ",
        "ㅊㄹ": "ㄴㄴ",
        "ㄺㄴ": "ㅇㄴ",
        "ㅍㄴ": "ㅁㄴ",
    }
    fc_c = fc[-1] + nc[0]
    if fc_c in nasalization_set:
        fc[-1], nc[0] = nasalization_set[fc_c]
    return fc, nc


def soundex(content):
    uncased = [jamo_split(ch) if re.match("[가-힣]", ch) else [ch, "", ""] for ch in content]

    for i in range(len(uncased) - 1):
        uncased[i], uncased[i + 1] = palatalization(uncased[i], uncased[i + 1])
        uncased[i], uncased[i + 1] = liquidization(uncased[i], uncased[i + 1])
        uncased[i], uncased[i + 1] = nasalization(uncased[i], uncased[i + 1])

    content = "".join([jamo_merge(unc) for unc in uncased])
    return content
