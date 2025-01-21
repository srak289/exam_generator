# SPDX-FileCopyrightText: © 2025 Spencer Rak
# SPDX-License-Identifier: MIT
import argparse
import datetime
import logging
import mako
import random
import yaml

from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Answer:
    value: str
    name: str = None
    id: int = None

@dataclass
class Question:
    id: int = None
    text: str = None
    answer: Answer = None
    #references: str = None

    @classmethod
    def from_json(cls, data) -> "Question":
        """Build `cls` from "type" value in `data`
            Looks up `cls` in `globals()` after performing transform
            e.g.
                type: multi-choice -> globals()["MultiChoice"]
        """
        clsname = "".join(map(str.title, data.pop("type").split("-")))

        options = []
        for a in data.pop("options"):
            logger.debug(f"Constructing Answer from {a}")
            #options.append(Answer(a))

        logger.debug(f"Instantiating class {clsname}")
        kls = globals()[clsname](options=options, answer=answer, **data)
        return kls
    
    def __post_init__(self):
        # handle options init
        # handle answer init
        if self.text == None:
            raise ValueError(f"{self} `text` property cannot be `None`")
        if self.answer == None:
            raise ValueError(f"{self} `answer` property cannot be `None`")
        pass

@dataclass
class FillBlank(Question):
    pass

@dataclass
class MultiChoice(Question):
    options: [str] = field(default_factory=lambda: list())

@dataclass
class SelectAll(Question):
    options: [str] = field(default_factory=lambda: list())
    answer: [Answer] = field(default_factory=lambda: list())

@dataclass
class Exam:
    title: str
    date: str
    instructor: str
    questions: [Question] = field(default_factory=lambda: list())

    _prepare: bool = field(init=False, default=False)

    def add_question(self, q: Question):
        self.questions.append(q)

    def _prepare(self):
        if self._prepared:
            return

    def render(self):
        pass

@dataclass
class AnswerKey:
    title: str
    instructor: str
    exam: Exam

def run(args):
    data = yaml.safe_load(open("question.yaml").read())

    e = Exam(
        title = data["title"],
        date = str(datetime.date.today()),
        instructor = data["instructor"],
    )

    if args.D >= 2:
        logger.warning("Triggering pre-model breakpoint")
        breakpoint()

    # any question assigned an id will appear at that position
    # two questions sharing an id will raise an error
    # questions without id will be randomized

    # any question with options specified as unordered list
    # will have order randomized

    # any question with options specified as ordered elements
    # will appear as-is

    for q in data["questions"]:
        e.add_question(
            Question.from_json(q)
        )

    logger.debug("Finished building model")

    if args.D >= 1:
        logger.warning("Triggering pre-render breakpoint")
        breakpoint()

    # we should dump the final set of yaml as well after it's finished being randomized / built

def main():
    ap = argparse.ArgumentParser(
        prog="ExamGenerator",
        description="Generate randomized exams from .yaml files",
        epilog="Authored by Spencer Rak",
    )
    ap.add_argument("-f", "--file", help="The file to load (.yaml)")
    ap.add_argument("-D", help="Trigger a breakpoint, more `D`s will trigger the breakpoint earlier", action="count")
    ap.add_argument("-v", help="Increase verbosity, more `v`s will increase verbosity", action="count")
    args = ap.parse_args()

    if not args.v:
        args.v = 0

    # TODO add verbosity scaling

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(message)s",
    )

    logger.debug(f"Received args {args}")
    logger.info("Startup complete")

    if not args.D:
        args.D = 0

    if args.D >= 3:
        logger.warning("Triggering pre-run breakpoint")
        breakpoint()

    run(args)

if __name__ == "__main__":
    main()
