def add_anchor(string):
    return "<a href='#'>" + string + "</a>"


def add_enable_anchor(enabled):
    if enabled is True:
        return 'Enabled | <a href=\'#\'>Disable</a>'
    else:
        return 'Disabled | <a href=\'#\'>Enable</a>'


def add_multiple_anchor(string_list):
    str_list = string_list.split(',')
    out_string = ''
    for index, string in enumerate(str_list):
        out_string += '<a href=\'#\'>' + string + '</a>'
        if (index + 1) < len(str_list):
            out_string += ' | '

    return out_string


def handle_uploaded_file(f):
    print 'Storing file : ' + f.name
    print 'Content-Type : ' + f.content_type
    with open('D:/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
