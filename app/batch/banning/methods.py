import pickle
from os.path import abspath, dirname, join

import ahocorasick
from sqlalchemy import select

from core.backend.postgres import SessionProvider
from core.entity import BannedWord
from core.exception import BannedWordException

model_path = join(dirname(abspath(__file__)), "ac.model")


def build_model():
    session = SessionProvider()
    banneds: list[BannedWord] = session.scalars(select(BannedWord).where(BannedWord.deleted == False))

    automaton = ahocorasick.Automaton()

    for banned in banneds:
        automaton.add_word(banned.word, (banned.id, banned.word))

    automaton.make_automaton()
    automaton.save(model_path, pickle.dumps)


def load_model():
    try:
        return ahocorasick.load(model_path, pickle.loads)
    except:
        return None


def validate(text: str, raise_exception=True):
    # io 성능이슈 생기면 메모리에 인스턴스화 고려
    A = load_model()

    if A is None:
        return True

    for idx, (id, value) in A.iter(text):
        if raise_exception:
            raise BannedWordException(f"""단어 '{value}'를 사용할 수 없습니다.""")
        else:
            return False

    return True
