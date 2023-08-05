#!/usr/bin/env python3

import click
import os
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

    def display(self, data):
        print()
        click.secho(data["word"].capitalize(), bold=True)

        for pos, defn in data["definitions"].items():
            click.echo("(" + click.style(pos, fg="yellow") + ") " + defn)

        print()

    def nuke(self):
        self.db.purge()

    def add_word(self, word):
        definitions = self.__get_definition(word)
        data = {
        "word": word,
        "definitions": definitions
        }

        assert isinstance(word, str)

        self.db.insert(data)

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
