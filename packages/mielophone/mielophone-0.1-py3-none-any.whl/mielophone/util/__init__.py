# -*- coding: utf-8 -*-
# romiq.kh@gmail.com, 2018-2019

import os
import sys
import base64
import hashlib 

def pack_file(f, filename = None, encoding = "base85", hash = "sha1"):
    "Pack file data to json-compatible dictionary"
    
    if hash == "sha1":
        ho = hashlib.sha1()
    elif hash is None:
        ho = None
    else:
        raise Exception("Unsupported hash %r" % hash)
    
    if isinstance(f, bytes):
        # in-memory bytes
        fdata = f
    else:
        fdata = f.read()
    
    if encoding == "base64":
        fdata = base64.b64encode(fdata).decode("latin-1")
    elif encoding == "base85":
        fdata = base64.b85encode(fdata).decode("latin-1")
    else:
        raise Exception("Unsupported data encoding %r" % encoding)
        
    fobj = {
        "data": fdata,
        "filename": filename,
        "encoding": encoding
        }

    filehash = None
    if hash:
        fobj["hash"] = hash
        ho.update(f)
        fobj["digest"] = ho.hexdigest()
        
    return fobj
    
def extract_file(packed):
    "Extract file data from packed dictionary. Returns tuple (data, filename)"
    
    filename = packed.get("filename")
    fdata = packed.get("data")
    if fdata is None:
        raise Exception("No file data")
    
    encoding = packed.get("encoding") or "base85"
    if encoding == "base64":
        fdata = base64.b64decode(fdata)
    elif encoding == "base85":
        fdata = base64.b85decode(fdata)
    else:
        raise Exception("Unsupported data encoding %r" % encoding)
    
    hash = packed.get("hash")
    if hash == "sha1":
        ho = hashlib.sha1()
        ho.update(fdata)
        if ho.hexdigest() != packed.get("digest"):
            raise Exception("Hash digest mismatch")
    
    return (fdata, filename)
    