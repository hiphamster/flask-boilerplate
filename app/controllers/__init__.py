

def paginate(page=1, navs=3):
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
        # return {'page':page, 'group': group, 'index': page % navs, 'min':_min, 'max':_max}
        return {'page':page, 'group': group, 'min':_min, 'max':_max}


def _paginate(pages,window,start=0):
    end = pages
    # print(f'pages: {list(range(1,pages+1))}')
    # pages_iter = iter(range(0,pages,window))
    pages_iter = iter(range(start,end,window))

    slide = next(pages_iter, -1)
    # print(f'slide: {slide}')

    show_pages = list()

    while slide >= 0:
        start = slide
        end = slide + window
        if end > pages:
            end = pages

        page_slice = list(range(1, 1 + pages)[start:end])
        if len(list(page_slice)) < window:
            window = len(list(page_slice))

        # print(f'window: {window}')

        # for i in range(window):
            # print(f'start,end: {start,end}, i => {i}')
            # print(f'pages_slice: {page_slice}\n')
            # show_pages.append((page_slice, i))

        show_pages.append(page_slice)
        slide = next(pages_iter, -1)

    return show_pages


