from BeadworkDesigner.BeadworkModel import BeadworkModel, BeadworkTransposeModel

# TODO: create test for BeadworkModel init with data

def test_BeadworkModel_init_nodata():
    testModel = BeadworkModel()

    # TEST FOR NOT EMPTY
    assert(len(testModel._data) != 0)
    assert(len(testModel._data[0]) != 0)

    # TEST FOR WHITE DEFAULT WHEN NOT DEBUG
    assert(data == "#FFFFFF" for row in testModel._data for data in row)

    # TEST FOR RANDOM COLOR DEFAULT WHEN DEBUG
    testModel = BeadworkModel(debug=True)
    assert(data != "#FFFFFF" for row in testModel._data for data in row)