#!/usr/bin/env python3

import click
import os
import random
import sys
import time
from tinydb import TinyDB, Query
from wiktionaryparser import WiktionaryParser

BASE_PATH = os.path.expanduser("~")
VOCAB_DB = os.path.join(BASE_PATH, "gre_vocab.json")

class Vocab:
    def __init__(self, debug=False):
        self.debug = debug
        os.system(f"touch {VOCAB_DB}")
        self.db = TinyDB(VOCAB_DB)
        self.parser = WiktionaryParser()

    def add(self, words):
        for word in words:
            self.add_word(word)

    def remove(self, words):
        for word in words:
            self.remove_word(word)

    def show(self):
        for doc in self.db.all():
            self.display(doc)

    def flash(self):
        doc = random.choice(self.db.all())
        self.display(doc, flash=True)

    def display(self, data, flash=False):
        print()
        click.secho(data["word"].capitalize(), bold=True)

        if flash:
            input("Press return key to show definition")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

        for pos, defn in data["definitions"].items():
            click.echo("(" + click.style(pos, fg="yellow") + ") " + defn)

        print()

    def export(self, path):
        data = self.db.all()
        data = map(lambda entry: entry["word"],
                   sorted(data, key=lambda entry: entry["word"]))

        with open(os.path.join(path, "vocab.txt"), "wt") as fp:
            for word in data:
                fp.write(word)
                fp.write("\n")


    def nuke(self):
        self.db.purge()

    def add_word(self, word):
        assert isinstance(word, str)

        word = word.lower()
        definitions = self.__get_definition(word)

        data = {
        "word": word,
        "definitions": definitions
        }

        self.db.insert(data)
        self.display(data)

    def __get_definition(self, word):
        response = self.parser.fetch(word)
        definitions = response[0]['definitions']
        data = dict()

        for entry in definitions:
            pos = entry['partOfSpeech']
            definition = entry['text'][1]

            data[pos] = definition

        return data

    def remove_word(self, word):
        assert isinstance(word, str)

        query = Query()
        result = self.db.get(query.word == word)

        try:
            doc_id = result.doc_id
            self.db.remove(doc_ids=[doc_id])
        except AttributeError as e:
            print(f"Error removing {word}")

    def get(self, word):
        assert isinstance(word, str)

        query = Query()
        results = self.db.search(query.word == word)

        if len(results) != 0:
            for doc in results:
                self.display(doc)
