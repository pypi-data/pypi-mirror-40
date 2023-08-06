import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List

import requests
from allennlp.data.tokenizers.token import Token
from allennlp.data.tokenizers.word_splitter import WordSplitter
from overrides import overrides

try:
    import pyltp
except ImportError:
    pyltp = None
    logging.getLogger(__name__).warning(
        'Can NOT import module `pyltp`. `LtpEmbeddedWordSplitter` DISABLED!'
    )


__all__ = ['LtpRemoteWordSplitter', 'LtpEmbeddedWordSplitter']


@WordSplitter.register('ltp_remote')
class LtpRemoteWordSplitter(WordSplitter):
    """
    A ``WordSplitter`` that uses LTP's tokenizer.
    It calls ``ltp_server``'s Web API.
    """

    def __init__(self,
                 url: str = 'http://localhost:12345/ltp',
                 max_workers: int = None
                 ):
        """
        Parameters
        ----------
        url : str, optional
            HTTP URL of `ltp_server` to call it's Web API (the default is 'http://localhost:12345/ltp')

        max_workers: int, optional
            The maximum number of threads that can be used to query LTP web server.
        """
        self._url = url
        self._max_workers = max_workers

    @overrides
    def split_words(self, sentence: str) -> List[Token]:
        return [Token(t) for t in self._segment(sentence)]

    @overrides
    def batch_split_words(self, sentences: List[str]) -> List[List[Token]]:
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            return [Token(ret_val) for ret_val in executor.map(
                lambda s: [t for t in self._segment(s)],
                sentences
            )]

    def _segment(self, s: str)-> List[str]:
        # pylint: disable=invalid-name
        segments = []
        r = requests.post(
            self._url,
            data={'s': s, 'x': 'n', 't': 'ws'}
        )
        r.raise_for_status()
        ltp_result = r.json()
        for sent in ltp_result[0]:
            for word_dict in sent:
                word = word_dict['cont'].strip()
                if word:
                    segments.append(word)
        return segments


@WordSplitter.register('ltp_embedded')
class LtpEmbeddedWordSplitter(WordSplitter):
    """
    A ``WordSplitter`` that uses LTP's tokenizer.
    It loads ``ltp`` module into memory.
    """

    def __init__(self,
                 model: str
                 ):
        """
        Parameters
        ----------
        model : str
            model file path
        """
        if pyltp:
            self._segmentor = pyltp.Segmentor()
            self._segmentor.load(model)
        else:
            raise NotImplementedError(
                'Can NOT import module `pyltp`. `LtpEmbeddedWordSplitter` DISABLED!'
            )

    def __del__(self):
        self._segmentor.release()

    @overrides
    def split_words(self, sentence: str) -> List[Token]:
        result = []
        result = self._segmentor.segment(sentence)
        return list(result)
