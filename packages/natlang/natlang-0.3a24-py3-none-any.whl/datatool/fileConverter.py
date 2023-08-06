# -*- coding: utf-8 -*-
# Python version: 2
#
# Jetic's file converter tool for NLP datasets
# Simon Fraser University
# Jetic Gu
#
# This module contains functions for loading and converting
# datasets in multiple formats.
#
import os
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import jieba


def procXML(filename, jieba=False):
    result = []
    tree = ET.parse(filename)
    root = tree.getroot()

    for post in root:
        for su in post:
            result.append([su.text])
        result.append('')
    return result


def procXMLCN(filename):
    result = []
    tree = ET.parse(filename)
    root = tree.getroot()

    for post in root:
        for su in post:
            result.append(jieba.lcut(su.text))
        result.append('')
    return result


def rawIntoSegForms(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        result.append(jieba.lcut(line))
    return result


def pennTreeIntoTags(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        sentence = []
        procLine = line
        for ch in ('(', ')', '[', ']'):
            procLine = procLine.replace(ch, ' ')
        procLine = procLine.split()
        for i in range(len(procLine)):
            if procLine[i].isdigit():
                sentence.append(procLine[i - 1])
                print "Missing elements!"
        # sentence = [entry for entry in sentence if entry != "-NONE-"]
        result.append(sentence)
    return result


def pennTreeNoWords(fileName, linesToLoad=sys.maxint):
    from tree import Node, loadPennTree, lexicaliseNode
    w2int = {"<UNK>": "XX"}
    t2int = {"<UNK>": "XX"}
    result = []
    fileName = os.path.expanduser(fileName)
    content = loadPennTree(fileName, linesToLoad)
    for node in content:
        sentence = lexicaliseNode(node, w2int, t2int).export()
        result.append((sentence, ))
    return result


def tokenIntoForms(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        sentence = []
        procLine = line.split()
        for i in range(len(procLine)):
            sentence.append(procLine[i - 1].split(";")[-1])
        # sentence = [entry for entry in sentence if entry != "*"]
        sentence = [entry for entry in sentence]
        result.append(sentence)
    return result


def sgmIntoText(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.replace('>', '<').split("<")
               for line in open(fileName)][:linesToLoad]
    content = [[line[2]] for line in content if line[-2] == '/seg']
    return content


def removeEmptyLines(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.split() for line in open(fileName) if line.strip() != ""][
        :linesToLoad]
    return content


def rawIntoForms(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        sentence = []
        procLine = line.split()
        for i in range(len(procLine)):
            sentence.append(procLine[i].split(";")[-1])
        # sentence = [entry for entry in sentence if entry != "*"]
        sentence = [entry for entry in sentence]
        result.append(sentence)
    return result


def alignmentToList(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        result.append(line.split())
    return result


def pennTreeSplitIntoPennTree(fileName, linesToLoad=sys.maxint):
    result = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        result += line.replace("(", " ( ").replace(")", " ) ").split()
    results = []
    counter = 0
    for element in result:
        if counter == 0:
            results.append([])
            if element != "(":
                results[-1].append("(")
                counter += 1
                element = element[1:]
        results[-1].append(element)
        for char in element:
            if char == "(":
                counter += 1
            if char == ")":
                counter -= 1
    if counter != 0:
        raise RuntimeError
    return results


def armSplitIntoARMAndText(fileName, linesToLoad=sys.maxint):
    result = []
    text = []
    fileName = os.path.expanduser(fileName)
    content = [line.strip() for line in open(fileName)][:linesToLoad]
    for line in content:
        if len(line) != 0 and line[0] == "#":
            if line[:8] == "# ::snt ":
                text.append(line[8:])
            continue
        result += line.replace("(", " ( ").replace(")", " ) ").split()
    results = []
    counter = 0
    for element in result:
        if counter == 0:
            results.append([])
            if element != "(":
                results[-1].append("(")
                counter += 1
                element = element[1:]
        results[-1].append(element)
        for char in element:
            if char == "(":
                counter += 1
            if char == ")":
                counter -= 1
    if counter != 0:
        raise RuntimeError
    return results, text


def convertFiles(filePattern, converter, output="o.pos"):
    """
    This function first scans the files matching the filePattern, then run each
    of them through the converter, the writes the results to output file(s).
    The output can be a list/tuple of str or simpe an str(single file).
    The converter's output can be a list (single output file) or a tuple of
    lists (multiple output files).
    Each converter's entry (a single line in each output file) can be either a
    list (which will be joined by space) or an str (one line, no "\n" at the
    end).
    """
    if isinstance(output, list) or isinstance(output, tuple):
        numFiles = len(output)
    else:
        numFiles = 1
        output = [output, ]
    result = [[] for item in output]
    import glob
    for name in glob.glob(os.path.expanduser(filePattern)):
        if os.path.isfile(name):
            print name
            converterOutput = converter(name)
            if not isinstance(converterOutput, tuple):
                converterOutput = (converterOutput, )
            if len(converterOutput) != numFiles:
                print len(converterOutput), type(entry)
                raise RuntimeError("Incorrect return entry length")
            for i in range(len(output)):
                result[i] += converterOutput[i]

    file = [open(os.path.expanduser(outputFile), "w") for outputFile in output]
    for i in range(numFiles):
        for sentence in result[i]:
            if isinstance(sentence, str):
                file[i].write(sentence)
            else:
                file[i].write(" ".join(sentence))
            file[i].write("\n")
    for f in file:
        f.close()
    return


def ASPECtoBitext(path, file1out, file2out, linesToLoad=sys.maxint, pos=3):
    path = os.path.expanduser(path)
    bitext = list(open(path))[:linesToLoad]
    bitext = [entry.strip().split(" ||| ")[pos:] for entry in bitext]
    with open(os.path.expanduser(file1out), "w") as f1:
        with open(os.path.expanduser(file2out), "w") as f2:
            for entry in bitext:
                f1.write(entry[0])
                f2.write(entry[1])
                f1.write("\n")
                f2.write("\n")
    return


def alignedRawText(file1, file2, file1out, file2out, linesToLoad=sys.maxint):
    path1 = os.path.expanduser(file1)
    path2 = os.path.expanduser(file2)
    bitext = list(zip(open(path1), open(path2)))[:linesToLoad]
    for i in range(len(bitext)):
        f, e = bitext[i]
        if f.strip() == "" or e.strip() == "":
            bitext[i] = None
    bitext = [entry for entry in bitext if entry is not None]
    with open(os.path.expanduser(file1out), "w") as f1:
        with open(os.path.expanduser(file2out), "w") as f2:
            for f, e in bitext:
                f1.write(f)
                f2.write(e)
    return


def alignedTextTree(textFile, treeFile, treeOut, linesToLoad=sys.maxint):
    path1 = os.path.expanduser(textFile)
    path2 = os.path.expanduser(treeFile)

    text = list(open(path1))[:linesToLoad]
    tree = list(open(path2))[:linesToLoad]

    for i in range(len(text)):
        if text[i].strip() == "":
            tree.insert(i, "\n")

    with open(os.path.expanduser(treeOut), "w") as f1:
        for f in tree:
            f1.write(f)
    return


if __name__ == '__main__':
    """convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/train.de-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/train.de-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/train.cs-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/train.cs-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/train.ru-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/train.ru-en.tree.en")

    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/dev.de-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/dev.de-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/dev.cs-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/dev.cs-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/dev.ru-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/dev.ru-en.tree.en")

    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/test.de-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/test.de-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/test.cs-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/test.cs-en.tree.en")
    convertFiles(
        "/Users/jetic/Daten/align-data/eriguchi/test.ru-en.rawtree.en",
        pennTreeSplitIntoPennTree,
        "/Users/jetic/Daten/align-data/eriguchi/test.ru-en.tree.en")"""

    """alignedRawText(
        "~/Daten/align-data/eriguchi/train.de-en.tok.en",
        "~/Daten/align-data/eriguchi/train.de-en.tok.de",
        "~/Daten/align-data/eriguchi/train.de-en.clean.en",
        "~/Daten/align-data/eriguchi/train.de-en.clean.de")

    alignedRawText(
        "~/Daten/align-data/eriguchi/train.cs-en.tok.en",
        "~/Daten/align-data/eriguchi/train.cs-en.tok.cs",
        "~/Daten/align-data/eriguchi/train.cs-en.clean.en",
        "~/Daten/align-data/eriguchi/train.cs-en.clean.cs")

    alignedRawText(
        "~/Daten/align-data/eriguchi/train.ru-en.tok.en",
        "~/Daten/align-data/eriguchi/train.ru-en.tok.ru",
        "~/Daten/align-data/eriguchi/train.ru-en.clean.en",
        "~/Daten/align-data/eriguchi/train.ru-en.clean.ru")"""
    """ASPECtoBitext(
        "/Volumes/Schwarzbox/Sink/mark18/ASPEC/ASPEC-JE/train/train-1.txt",
        "train.raw.jp", "train.raw.en", 100000)

    ASPECtoBitext(
        "/Volumes/Schwarzbox/Sink/mark18/ASPEC/ASPEC-JE/dev/dev.txt",
        "dev.raw.jp", "dev.raw.en", 100000, 2)

    ASPECtoBitext(
        "/Volumes/Schwarzbox/Sink/mark18/ASPEC/ASPEC-JE/test/test.txt",
        "test.raw.jp", "test.raw.en", 100000, 2)

    convertFiles("/Users/jetic/Daten/semantic-data/amr_2.0/raw/data/amrs/split/training/amr-release-2.0-amrs-training-cctv.txt",
        armSplitIntoARMAndText,
        ("output.amr", "output.txt"))
    """
