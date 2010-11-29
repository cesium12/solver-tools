from solvertools.puzzle_array import PuzzleArray, Header
from solvertools.util import get_datafile

def test_csv():
    puz = PuzzleArray.from_csv(get_datafile('test/test.csv'))
    assert isinstance(puz, PuzzleArray)
    assert isinstance(puz[0,0], Header)
    assert isinstance(puz[0,1], Header)
    assert list(puz[1:7,0]) == list('123456')
    assert puz[1,1] == 'UP'
    assert len(puz[2,1]) == 3
