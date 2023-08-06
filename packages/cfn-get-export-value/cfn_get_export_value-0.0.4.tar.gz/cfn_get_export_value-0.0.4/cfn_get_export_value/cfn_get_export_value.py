import boto3


def get_export_value(name, client=None, session=None):
    def _get_export_value(name, next_token):
        resp = _list_exports(next_token=next_token, client=client, session=session)

        exports = resp['Exports']
        export = next((export for export in exports if export['Name'] == name), None)

        if export:
            return export['Value']

        next_token = resp['NextToken'] if 'NextToken' in resp else None
        if not export and next_token:
            return _get_export_value(name, next_token=next_token)

        # at this point, no export is found and next_token==None
        raise ExportNotFoundError(name=name)

    return _get_export_value(name, next_token=None)


def _list_exports(next_token=None, client=None, session=None):
    """
    Cloudformation facade, for easier mocking during unit testing
    """
    if client and session:
        raise ValueError('Cannot specify both client and session')

    if session:
        cf = session.client('cloudformation')
    elif client:
        cf = client
    else:
        cf = boto3.client('cloudformation')

    if next_token:
        return cf.list_exports(NextToken=next_token)
    else:
        return cf.list_exports()


class ExportNotFoundError(Exception):
    def __init__(self, name):
        super(ExportNotFoundError, self).__init__(
            'Name: {name} not found in exports'.format(name=name))
