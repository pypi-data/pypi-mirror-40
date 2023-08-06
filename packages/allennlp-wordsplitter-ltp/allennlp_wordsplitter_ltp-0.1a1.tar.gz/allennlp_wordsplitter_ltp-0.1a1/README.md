# allennlp_wordsplitter_ltpnlp

Add a [LTP][] `WordSplitter` into [AllenNLP][]'s tokenizers.

## config

```js
{
  "dataset_reader": {

    // ... ...

    "tokenizer": {
      "word_splitter": {
        "type": "ltp_remote",
        "url": "http://10.1.1.174:12345/ltp"
      }
    },

    // ... ...

  },

  // ... ...

}
```

## CLI

```sh
allennlp train --include-package allennlp_wordsplitter_ltp -s /your/output/dir /your/training/config/file
```

------
[AllenNLP]: https://allennlp.org/
[LTP]: https://github.com/HIT-SCIR/ltp
