from sorter.core.sort import SorterConf, SorterFactory


def test_from_list(type_id, data, is_asc_order, top_n):
    '''
    Test case:
        data inputed from a given list object
    '''
    conf = SorterConf()
    conf.container = data
    if is_asc_order is not None:
        conf.is_asc_order = is_asc_order
    if top_n:
        conf.top_n = top_n
    sorter = SorterFactory.get_instance(type_id)
    sorter.set_conf(conf);
    sorter.sort()
    sorter.output()
    

def test_from_file(type_id, file_in, file_out, is_asc_order, top_n):
    '''
    Test case:
        data inputed from a given file
    '''
    conf = SorterConf()
    conf.is_data_in_file = True
    conf.file_in = file_in
    conf.file_out = file_out
    conf.f_converter = float
    if is_asc_order is not None:
        conf.is_asc_order = is_asc_order
    if top_n:
        conf.top_n = top_n
    sorter = SorterFactory.get_instance(type_id)
    sorter.set_conf(conf);
    sorter.sort()
    sorter.output()


if __name__ == '__main__':
    # test data from a given list
    type_id = 4
    data = [9, 1, 7, 7, 4, 0, 3, 8]
    test_from_list(type_id, data, True, 5)
    
    # test data from a given file
    type_id = 7
    is_asc_order = False
    top_n = 8
    file_in = r'C:\Users\thinkpad\Desktop\numbersIn.txt'
    file_out = r'C:\Users\thinkpad\Desktop\numbersOut.txt'
    test_from_file(type_id, file_in, file_out, is_asc_order, top_n)
