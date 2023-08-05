import boundio as bio
from boundio.item_codes import SKIP_ITEM, ITEM_CODE, END_IO, CLOSE_STREAM
from boundio.asynchronous.tasks import task_list

def test_itemcodes():
    assert isinstance(SKIP_ITEM,ITEM_CODE) and str(SKIP_ITEM) == ''
    assert isinstance(CLOSE_STREAM(''),ITEM_CODE)
    assert str( CLOSE_STREAM('TEST_STRING') ) == 'TEST_STRING'
    assert isinstance(END_IO, CLOSE_STREAM) and str(END_IO) == ''

def test_task_list():
    @bio.task()
    async def my_func():
        pass
    assert len(task_list.tasks) == 1
    assert my_func in task_list.get_functions()
    bio.clear_tasks()
    assert len(task_list.tasks) == 0
    assert my_func not in task_list.get_functions()
