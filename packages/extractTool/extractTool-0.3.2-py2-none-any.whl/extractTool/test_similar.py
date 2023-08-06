import pytest
import math
import similar

"""
These tests check if the calucated similar score from two Bouding Boxes
is equal to our hand-calculted score
"""
#Germany - Poland
def test_answer():
    bbox1 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    bbox2 = [14.122971, 49.002048, 24.145782, 55.033695]
    assert similar.aehnlickeit(bbox1, bbox2) == 0.052537198756258265

# Muenster - Greven
def test_answer1():
    bbox1 = [7.473785, 51.840145, 7.774364, 52.060024]
    bbox2 = [7.5234, 52.0326, 7.7556, 52.152]
    assert similar.aehnlickeit(bbox1, bbox2) == 0.0006267747993827629

# Germany - Muenster
def test_answer2():
    bbox1 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    bbox2 = [7.5234, 52.0326, 7.7556, 52.152]
    assert similar.aehnlickeit(bbox1, bbox2) == 0.19316458780635867

# Germany - Mexico
def test_answer3():
    bbox1 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    bbox2 = [-118.6, 14.39, -86.49, 32.72]
    assert similar.aehnlickeit(bbox1, bbox2) == 0.6488100389180073

# Germany - Invalid input
def test_answer4():
    bbox1 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    bbox2 = ["abc"]
    assert similar.aehnlickeit(bbox1, bbox2) == None

# Germany - Germany
def test_answer5():
    bbox1 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    bbox2 = [5.8663155, 47.270111, 15.041932 , 55.099159]
    assert similar.aehnlickeit(bbox1, bbox2) == 0

# Invalid input - Invalid input
def test_answer6():
    bbox1 = ["cde"]
    bbox2 = ["abc"]
    assert similar.aehnlickeit(bbox1, bbox2) == None

"""
These tests check if the similarity score is multiplied wir 5/4
if the datatypes are not equal
"""
# equal
def test_answer7():
    input1 = "raster"
    input2 = "raster"
    assert similar.whatDataType(input1, input2, 0.6) == 0.6

# equal
def test_answer8():
    input1 = "vector"
    input2 = "vector"
    assert similar.whatDataType(input1, input2, 0.6) == 0.6

# not equal
def test_answer9():
    input1 = "vector"
    input2 = "raster"
    assert similar.whatDataType(input1, input2, 0.6) == 0.75

# not equal
def test_answer10():
    input1 = "raster"
    input2 = "vector"
    assert similar.whatDataType(input1, input2, 0.6) == 0.75

# sim score above 1
def test_answer11():
    input1 = "vector"
    input2 = "raster"
    assert similar.whatDataType(input1, input2, 0.9) == 1

# if 0
def test_answer12():
    input1 = "vector"
    input2 = "raster"
    assert similar.whatDataType(input1, input2, 0) == 0




