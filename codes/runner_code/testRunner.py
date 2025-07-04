from Runner import Runner

runner = Runner("TestRunner")

runner.run_manylines(
"""
import(pythontoolsWin)

python {}:
    print('test')
    for i in range(10):
        print(i)
        print('test')

"""
)
