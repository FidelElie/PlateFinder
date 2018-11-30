import timeit

# x = timeit.timeit("import Test.test_file_converter")
x = timeit.timeit("import Test.CythonTest.test_file_converter")

print (x) 