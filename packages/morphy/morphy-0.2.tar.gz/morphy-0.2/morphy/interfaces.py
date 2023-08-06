"""
Representation of texts processed after NLP
--------------------------------------------

This module defines main text containers, which represent common information about item of selected level
"""

from typing import List, Dict, Union, Iterator, NamedTuple

from .errors import MorphyError


class Document:
    """ Main text container. Uses `morphy.MultiLang` class for text processing: sentence segmenting,
    tokenization, NER and noun phrases extraction.

    Attributes
    ----------
    text: Input text

    """

    _sentences = None
    _tokens = None
    _noun_phrases = None
    _ner = None

    def __init__(self, text: str):
        self.text = text

    def init_proc(self, proc):
        """
        Parameters
        ----------
        proc: :class:`~morphy.MultiLang`
        """

        doc = proc.parse_doc(self.text)

        class AttribCall(NamedTuple):
            func: callable
            args: List

            def execute(self, *args):
                return self.func(*(args or self.args))

        self._sentences = AttribCall(proc.extract_sentences, [self.text])
        self._tokens = AttribCall(proc.extract_tokens, [self.text, doc])
        self._noun_phrases = AttribCall(proc.extract_noun_phrases, [self.text, doc])
        self._ner = AttribCall(proc.extract_named_entities, [self.text, doc])

    @property
    def sentences(self) -> List['Sentence']:
        """ Segments input text into sentences, marks invalid sentences """

        if not self._sentences or not hasattr(self._sentences, 'execute'):
            raise MorphyError('Language processor was not found')

        res = list()
        for sent in self._sentences.execute():
            sent.parent = self
            res.append(sent)
        return res

    @property
    def tokens(self) -> List['Token']:
        """ Tokenize input text, marks tokens that passed filtering """

        if not self._tokens or not hasattr(self._tokens, 'execute'):
            raise MorphyError('Language processor was not found')

        res = list()
        for token in self._tokens.execute():
            token.parent = self
            res.append(token)
        return res

    @property
    def noun_phrases(self) -> List['Token']:
        """ Extracts noun phrases from input text """

        if not self._noun_phrases or not hasattr(self._noun_phrases, 'execute'):
            raise MorphyError('Language processor was not found')

        res = list()
        for token in self._noun_phrases.execute():
            token.parent = self
            res.append(token)
        return res

    @property
    def ner(self) -> List['Token']:
        """ NER for input text """

        if not self._ner or not hasattr(self._ner, 'execute'):
            raise MorphyError('Language processor was not found')

        res = list()
        for token in self._ner.execute():
            token.parent = self
            res.append(token)
        return res

    def dump(self) -> Dict:
        """ Saves `Document` content into json format """

        return {
            'text': self.text,
            'sentences': [s.dump() for s in self.sentences] if self.sentences else [],
            'tokens': [t.dump() for t in self.tokens] if self.tokens else [],
            'noun_phrases': [t.dump() for t in self.noun_phrases] if self.noun_phrases else [],
            'ner': [t.dump() for t in self.ner] if self.ner else []
        }

    @classmethod
    def load(cls, data: Dict) -> 'Document':
        """ Loads `Document` class object from json """

        doc = cls(data['text'])

        class AttribCache(NamedTuple):
            attrib: List

            def execute(self, *args):
                if args:
                    raise MorphyError('No tokens were found. Try to initialize doc with `MultiLang` class instance')
                return self.attrib

        doc._sentences = AttribCache([Sentence.load(s) for s in data['sentences']] if data['sentences'] else None)
        doc._tokens = AttribCache([Token.load(t) for t in data['tokens']] if data['tokens'] else None)
        doc._noun_phrases = AttribCache([Token.load(t) for t in data['noun_phrases']] if data['noun_phrases'] else None)
        doc._ner = AttribCache([Token.load(t) for t in data['ner']] if data['ner'] else None)
        return doc


class Sentence:
    """ Is used when task requires sentence structured text.

    Attributes
    ----------
    matches: If True, current sentence passed filtering at sentence segmentation stage

    Examples
    --------
    >>> sent = Sentence('This is a small test sentence')
    """

    _tokens = None

    def __init__(self, text: str):
        self.text = text

        self.parent = None  # type: Document
        self.matches = False

    def __repr__(self):
        return '[%s] %s' % ('+' if self.matches else '-', ' '.join(self.text.split()))

    def __iter__(self) -> Union[Iterator, None]:
        return iter(self.tokens) if self.tokens else None

    @property
    def tokens(self) -> List['Token']:
        """ Extracts  """

        if self._tokens:
            return self._tokens

        if self.parent:
            self._tokens = list()
            for token in self.parent._tokens.execute(self.text):
                token.parent = self
                self._tokens.append(token)

        return self._tokens

    @tokens.setter
    def tokens(self, tokens: List['Token']):
        self._tokens = tokens

    def dump(self) -> Dict:
        return {'text': self.text, 'tokens': [t.dump() for t in self.tokens] if self.tokens else [],
                'matches': self.matches}

    @classmethod
    def load(cls, data: Dict) -> 'Sentence':
        sent = cls(data['text'])
        sent.matches = data['matches']
        tokens = list()
        if data['tokens']:
            for t in data['tokens']:
                token = Token.load(t)
                token.parent = sent
                tokens.append(token)
        sent.tokens = tokens
        return sent


class Token:
    """ Container for token (word, entity or phrase) metadata.

    Attributes
    ----------
    text: Original word form from input text
    lemma: Normal word form
    tag: Word POS tag or category (for entity and phrase)
    is_stop: If True, token belongs to so called `stop words`
    """

    def __init__(self, text: str, lemma: str = '', tag: str = '', is_stop: bool = False):
        self.text = text
        self.lemma = lemma
        self.tag = tag
        self.is_stop = is_stop

        self.parent = None  # type: Union[Document, Sentence]
        self.matches = False

    def __repr__(self):
        return '[%s] %s -> %s (%s)' % ('+' if self.matches else '-', self.text, self.lemma, self.tag)

    def dump(self) -> Dict:
        return {'text': self.text, 'lemma': self.lemma, 'tag': self.tag, 'is_stop': self.is_stop,
                'matches': self.matches}

    @classmethod
    def load(cls, data: Dict) -> 'Token':
        res = cls(**{k: v for k, v in data.items() if k != 'matches'})
        res.matches = data['matches']
        return res
