#!/usr/bin/env python


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def combine_hosts_names(hosts, names):
    result = []
    for i in range(len(names)):
        result.append(merge_two_dicts(hosts[i], names[i]))
    return result


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'combine_hosts_names': combine_hosts_names
        }
