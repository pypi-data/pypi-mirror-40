#!/usr/bin/env python
# encoding: utf-8

import torchtext


class AnutshellBaseField(torchtext.data.Field):
    def __init__(self, **kwargs):
        kwargs["sequential"] = True
        kwargs["tokenize"] = lambda x: x.split()
        kwargs["lower"] = True
        kwargs["batch_first"] = True
        super(AnutshellBaseField, self).__init__(**kwargs)

    def build_vocab(self, args):
        super(AnutshellBaseField, self).build_vocab(args["Dataset"])


class AnutshellSourceField(AnutshellBaseField):
    def __init__(self, **kwargs):
        kwargs["eos_token"]  = "<eos>"
        super(AnutshellSourceField, self).__init__(**kwargs)


class AnutshellTargetField(AnutshellBaseField):
    """
    Wrapper of original torchtext data Field
    """
    def __init__(self, **kwargs):
        kwargs["eos_token"] = "<eos>"
        kwargs["init_token"] = "<sos>"

        super(AnutshellTargetField, self).__init__(**kwargs)

