import arrow


def normal_data(data):
    utc = arrow.get(data)
    return utc.humanize(locale='ru')