import csirtgsdk.utils as utils
import arrow
import logging
import base64
import binascii
from pprint import pprint
import hashlib
from six import string_types
import os.path


class Indicator(object):
    """
    Represents an Indicator object
    """
    def __init__(self, client, args):
        """
        :param client: csirtgsdk.client.Client object
        :param args: dict https://github.com/csirtgadgets/csirtgsdk/wiki/API#indicators
        :return: Indicator object

        Example:
            Indicator(cli, {
                'indicator': 'example.org',
                'tags': 'botnet',
                'lasttime': '2015-01-01T00:00:59Z',
                'comment': 'example comment',
                'attachment': '/tmp/malware.zip'
            }).create()
        """
        self.logger = logging.getLogger(__name__)
        self.client = client

        required = set(['user', 'feed'])

        if args is None or len(required - set(args.keys())) > 0:
            raise Exception("invalid arguments. missing: {}"
                            .format(required-set(args.keys())))

        self.args = utils.Map(args)

        if self.args.tags and isinstance(self.args.tags, string_types):
            self.args.tags = self.args.tags.split(',')
        
        if self.args.firsttime:
            self.args.firsttime = arrow.get(self.args.firsttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if self.args.lasttime:
            self.args.lasttime = arrow.get(self.args.lasttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def show(self, user, feed, id):
        """
        Show a specific indicator by id

        :param user: feed username
        :param feed: feed name
        :param id: indicator endpoint id [INT]
        :return: dict

        Example:
            ret = Indicator.show('csirtgadgets','port-scanners', '1234')
        """
        uri = '/users/{}/feeds/{}/indicators/{}'.format(user, feed, id)
        return self.client.get(uri)

    def _file_to_attachment(self, blob, filename=None):
        """

        :param blob: a local file path or base64 encoded blob
        :param filename: file path
        :return: dict of base64 encoded filestring, with orig filename
        """

        if os.path.isfile(blob):
            filename = blob
            with open(blob, encoding="ISO-8859-1") as f:
                data = f.read()
        else:
            if filename is None:
                raise RuntimeError('missing filename')
            try:
                data = base64.b64decode(blob)
            except TypeError:
                raise RuntimeError('attachment must be base64 encoded')

        md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
        sha1 = hashlib.sha1(data.encode('utf-8')).hexdigest()
        sha256 = hashlib.sha256(data.encode('utf-8')).hexdigest()
        sha512 = hashlib.sha512(data.encode('utf-8')).hexdigest()
        data = base64.b64encode(data.encode('utf-8'))

        return {
            'data': data.decode("utf-8"),
            'filename': filename,
            'sha1': sha1,
            'md5': md5,
            'sha256': sha256,
            'sha512': sha512
        }

    def comments(self, user, feed, id):
        """
        Return comments for a specific indicator id

        :param user: feed username
        :param feed: feed name
        :param id: indicator id [INT]
        :return: list

        Example:
            ret = Indicator.comments('csirtgadgets','port-scanners', '1234')
        """
        uri = '/users/{}/feeds/{}/indicators/{}/comments'.format(user, feed, id)
        return self.client.get(uri)

    def create(self):
        """
        Submit action on the Indicator object

        :return: Indicator Object
        """
        uri = '/users/{0}/feeds/{1}/indicators'.format(self.args.user, self.args.feed)

        data = {
            "indicator": {
                "indicator": self.args.indicator,
                "tags": self.args.tags,
                "description": self.args.description,
                "portlist": self.args.portlist,
                "protocol": self.args.protocol,
                'firsttime': self.args.firsttime,
                'lasttime': self.args.lasttime,
                'portlist_src': self.args.portlist_src,
                'content': self.args.content,
                'provider': self.args.provider,
            },
            "comment": self.args.comment
        }

        if self.args.attachment:
            attachment = self._file_to_attachment(self.args.attachment, filename=self.args.attachment_name)
            data['attachment'] = {
                'data': attachment['data'],
                'filename': attachment['filename']
            }

        if not data['indicator'].get('indicator'):
            data['indicator']['indicator'] = attachment['sha1']

        if not data['indicator'].get('indicator'):
            raise Exception('Missing indicator')

        return self.client.post(uri, data)

    submit = create

    def create_bulk(self, indicators, user, feed):
        from .constants import API_VERSION
        if API_VERSION == '1':
            print("create_bulk currently un-avail with APIv1")
            raise SystemExit

        """
        Submit action against the IndicatorBulk endpoint

        :param indicators: list of Indicator Objects
        :param user: feed username
        :param feed: feed name
        :return: list of Indicator Objects submitted

        from csirtgsdk.client import Client
        from csirtgsdk.indicator import Indicator

        remote = 'https://csirtg.io/api'
        token = ''
        verify_ssl = True

        i = {
            'indicator': 'example.com',
            'feed': 'test',
            'user': 'admin',
            'comment': 'this is a test',
        }

        data = []

        cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

        for x in range(0, 5):
            data.append(
                Indicator(cli, i)
            )

        ret = cli.submit_bulk(data, 'csirtgadgets', 'test-feed')
        """

        uri = '/users/{0}/feeds/{1}/indicators_bulk'.format(user, feed)

        data = {
            'indicators': [
                {
                    'indicator': i.args.indicator,
                    'feed_id': i.args.feed,
                    'tag_list': i.args.tags,
                    "description": i.args.description,
                    "portlist": i.args.portlist,
                    "protocol": i.args.protocol,
                    'firsttime': i.args.firsttime,
                    'lasttime': i.args.lasttime,
                    'portlist_src': i.args.portlist_src,
                    'comment': {
                        'content': i.args.comment
                    },
                    'content': i.args.content,
                    'provider': i.args.provider,
                } for i in indicators
                ]
        }
        return self.client._post(uri, data)

    submit_bulk = create_bulk
