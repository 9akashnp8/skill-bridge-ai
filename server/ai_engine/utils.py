from langchain.schema.runnable import Runnable

from .main import question_gen_chain, gen_validate_chain


def get_chain(validate: bool) -> Runnable:
    if validate:
        return gen_validate_chain
    return question_gen_chain
