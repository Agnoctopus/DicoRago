"""
Module for analysing korean text using khaiii.
"""

from typing import Optional

from khaiii.khaiii import KhaiiiWord

tag_meanings = {
    # Endings
    "EC": "Connecting ending",  # -고 (먹고)
    "EF": "Final ending",  # -요 (먹어요)
    "EP": "Pre-final ending",  # -으 (먹으세요)
    "ETM": "Modifier ending",  # -는 (먹는)
    "ETN": "Nominal ending",  # -기 (먹기)
    # Interjections
    "IC": "Interjection",  # 네 (네?)
    # Particles and Markers
    "JC": "Conjunctive particle",  # 하고 (사과하고)
    "JKB": "Adverbial case marker",  # 에서 (학교에서)
    "JKC": "Complement case marker",  # 에게 (선생님에게)
    "JKG": "Genitive case marker",  # 의 (철수의)
    "JKO": "Objective case marker",  # 를 (사과를)
    "JKQ": "Quotative particle",  # 랑 (사과랑)
    "JKS": "Subject case marker",  # 이 (철수가)
    "JKV": "Vocative particle",  # 야 (친구야)
    "JX": "Auxiliary particle",  # 도 (나도)
    # Adverbs and Determiners
    "MAG": "General adverb",  # 빨리
    "MAJ": "Conjunctive adverb",  # 그러므로
    "MM": "Determiner",  # 많은
    # Nouns
    "NNB": "Dependent noun",  # 것 (무엇인가의 것)
    "NNG": "Common noun",  # 사과
    "NNP": "Proper noun",  # 서울
    "NP": "Pronoun",  # 나
    "NR": "Numeral",  # 일
    # Symboles
    "SE": "Sentence-final ending symbol",  # !
    "SF": "Punctuation (period)",  # .
    "SH": "Chinese character",  # 漢
    "SL": "Foreign language",  # TV
    "SN": "Number",  # 123
    "SO": "Other symbol",  # %
    "SP": "Punctuation (comma)",  # ,
    "SS": "Punctuation (quotation)",  # “
    "SW": "Unknown word",  # ㅋㅋ
    "SWK": "Korean slang word",  # 대박
    # Verbs and Adjectives
    "VA": "Adjective verb",  # 예쁘
    "VCN": "Negative copula verb",  # 아닌
    "VCP": "Positive copula verb",  # 인
    "VV": "Action verb",  # 먹
    "VX": "Auxiliary verb",  # 있
    # Prefixes and Suffixes
    "XPN": "Noun prefix",  # 초
    "XR": "Verb Prefix",  # 조조용
    "XSA": "Adjective suffix",  # 롭
    "XSN": "Noun suffix",  # 들
    "XSV": "Verb suffix",  # 리
    # Others
    "ZN": "Unknown numeral",
    "ZV": "Unknown verb",
    "ZZ": "Unknown",
}


def get_vocabulary(word: KhaiiiWord) -> Optional[str]:
    """
    Derive a normalized vocabulary form from a KhaiiiWord.

    Args:
        word (KhaiiiWord): A word with morphological analysis.

    Returns:
        Optional[str]: The derived vocabulary form, or None.
    """

    # Get morphs
    morphs = word.morphs

    # No morph case
    if len(morphs) == 0:
        return None

    # Use the first morph to find the word
    morph = morphs[0]
    assert isinstance(morph.lex, str)

    # Returning vocabulary
    vocab = None

    # Interjections
    if morph.tag in ("IC"):
        # IC: Interjection: 네
        vocab = morph.lex
    # Nouns
    elif morph.tag in ("NNG", "NNB", "NP", "NNP"):
        # NNG: Common noun: 사과
        # NNB: Dependent noun: 것
        # NP: Pronoun: 그
        # NNP: Proper noun: 서울
        vocab = morph.lex
    elif morph.tag in ("NR"):
        # NR: Numeral: 하나
        vocab = None
    # Adverbs and Determiners
    elif morph.tag in ("MAG", "MAJ", "MM"):
        # MAG: General adverb: 빨리
        # MAJ: Conjunctive adverb: 그럼
        # MM: Determiner: 어떤
        vocab = morph.lex
    # Symboles
    elif morph.tag in ("SE", "SS"):
        # SE: Sentence-final ending symbol: ...
        # SS: Punctuation (quotation): ,
        word.morphs = word.morphs[1:]
        vocab = get_vocabulary(word)
    elif morph.tag in ("SN", "SL"):
        # SN: Number: 123
        # SL: Foreign language: TV
        vocab = None
    # Verbs
    elif morph.tag in ("VA", "VCN", "VCP", "VV", "VX"):
        # VA: Adjective verb: 예쁘 -> 예쁘다
        # VCN: Negative copula verb: 아니 -> 아니다
        # VCP: Positive copula verb: 이 -> 이다
        # VV: Action verb: 먹 -> 먹다
        # VX: Auxiliary verb: 있 -> 있다
        vocab = morph.lex + "다"
    # Prefixes and Suffixes
    elif morph.tag in ("XR"):
        # XR: Verb Prefix: 조조용/XR -> 조조용(V)다
        assert len(morphs) >= 2
        assert morphs[1].tag in ("XSA", "XSV")
        assert isinstance(morphs[1].lex, str)
        vocab = morph.lex + morphs[1].lex + "다"
    elif morph.tag in ("XPN"):
        # XR: Verb Prefix: 한/XPN -> 한(N)
        assert len(morphs) >= 2
        assert morphs[1].tag in ("NNG", "NNB")
        assert isinstance(morphs[1].lex, str)
        vocab = morph.lex + morphs[1].lex
    else:
        raise ValueError(f"Unhandled morphological tag encountered: {word}.")

    return vocab
