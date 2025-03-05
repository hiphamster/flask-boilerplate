from math import ceil

# def paginate(page=1, navs=3, pages=None):
def paginate(page, pages, navs=3):
    """page: page selected, navs: number of page links, pages: total pages"""

    if page < 1 or page > pages:
        return paginate(page=1, pages=pages, navs=navs)

    # page in range(1,navs)
    _paginate = {
        'page':page, 
        'min':1, 
        'max':navs,
        # 'page_range': range(1, navs)
    }

    if page >= navs:
        group = ceil(page/navs)

        # group = page // navs
        # if page % navs:
        #     group += 1

        _min = navs * (group - 1) + 1
        _max = navs * group
        if pages and _max > pages:
            _max = pages

        #FYI _max+1 because range upper bound is not inclusive
        # 'page_range': range(_min, _max+1)

        _paginate['min'] = _min
        _paginate['max'] = _max

    return _paginate



def _paginate(page=1, navs=3):
    """page: page selected, navs: number of page links"""
    # pages_group = list(range(1,navs+1)) + [0]
    # group_indexes = range(navs)
    # index_lookup = dict(zip(group_indexes, pages_group))
    if page < 1:
        return paginate(page=1, navs=navs)

    if page < navs:
                # page, group, index
        # return {'page':page, 'group': 1, 'index': page-1 , 'min':0, 'max':2}
        # return {'page':page, 'group': 1, 'index': index_lookup[page], 'min':1, 'max':navs}
        return {'page':page, 'group': 1, 'min':1, 'max':navs}
    else:
        group = page // navs
        if page % navs:
            group += 1
        _min = navs * (group - 1) + 1
        _max = navs * group
        _range = range(_min, _max+1)
        # return {'page':page, 'group': group, 'index': page % navs, 'min':_min, 'max':_max}
        return {'page':page, 'group': group, 'range': _range}




