def get_lazy_enumerator(client, get_first_page, item_parser=None, next_link_parser=None):
    """
    Returns api results as "lazy" collection.
    Makes api requests for new parts of data on demand only.
    :type client: bandwidth.catapult.Client
    :param client: catapult client
    :type get_first_page: types.FunctionType
    :param get_first_page: function which returns contane of first part (page) of data

    :rtype: types.GeneratorType
    :returns: lazy collection
    """
    get_data = get_first_page
    while True:
        _items, response, _ = get_data()
        next_page_url = ''

        if item_parser: items = item_parser(_items)
        else: items = _items

        for item in items:
            yield item

        if next_link_parser:
            links = [next_link_parser(_items)]
        else:
            links = response.headers.get('link', '').split(',')

        for link in links:
            values = link.split(';')
            if len(values) == 2 and values[1].strip() == 'rel="next"':
                next_page_url = values[0].replace('<', ' ').replace('>', ' ').strip()
                break

        if len(next_page_url) == 0:
            break

        def get_data():
            return client._make_request('get', next_page_url)
