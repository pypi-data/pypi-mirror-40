# Copyright 2016 Google Inc.
# Copyright 2017 Yelp
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import bz2
from hashlib import md5

from mrjob.fs.gcs import GCSFilesystem
from mrjob.fs.gcs import _CAT_CHUNK_SIZE

from tests.compress import gzip_compress
from tests.mock_google import MockGoogleTestCase


class CatTestCase(MockGoogleTestCase):

    def setUp(self):
        super(CatTestCase, self).setUp()
        self.fs = GCSFilesystem()

    def test_cat_uncompressed(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'foo\nfoo\n'
        })

        self.assertEqual(
            b''.join(self.fs._cat_file('gs://walrus/data/foo')),
            b'foo\nfoo\n')

    def test_cat_bz2(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo.bz2': bz2.compress(b'foo\n' * 1000)
        })

        self.assertEqual(
            b''.join(self.fs._cat_file('gs://walrus/data/foo.bz2')),
            b'foo\n' * 1000)

    def test_cat_gz(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo.gz': gzip_compress(b'foo\n' * 10000)
        })

        self.assertEqual(
            b''.join(self.fs._cat_file('gs://walrus/data/foo.gz')),
            b'foo\n' * 10000)

    def test_chunks_file(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'foo\nfoo\n' * 10000
        })

        self.assertGreater(
            len(list(self.fs._cat_file('gs://walrus/data/foo'))),
            1)

    def test_chunk_boundary(self):
        # trying to read from end of file raises an exception, which we catch
        data = b'a' * _CAT_CHUNK_SIZE + b'b' * _CAT_CHUNK_SIZE

        self.put_gcs_multi({
            'gs://walrus/data/foo': data,
        })

        self.assertEqual(
            list(self.fs._cat_file('gs://walrus/data/foo')),
            [b'a' * _CAT_CHUNK_SIZE, b'b' * _CAT_CHUNK_SIZE])


class GCSFSTestCase(MockGoogleTestCase):

    def setUp(self):
        super(GCSFSTestCase, self).setUp()
        self.fs = GCSFilesystem()

    def test_ls_blob(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b''
        })

        self.assertEqual(list(self.fs.ls('gs://walrus/data/foo')),
                         ['gs://walrus/data/foo'])

    def test_ls_missing(self):
        self.assertEqual(list(self.fs.ls('gs://nope/not/here')), [])

    def test_ls_ignores_dirs(self):
        # Dataproc (i.e. Hadoop) will create empty blobs whose names end
        # in '/'
        self.put_gcs_multi({
            'gs://walrus/data/foo/': b'',
            'gs://walrus/data/foo/bar': b'baz',
        })

        self.assertEqual(list(self.fs.ls('gs://walrus/data')),
                         ['gs://walrus/data/foo/bar'])

    def test_ls_recursively(self):
        self.put_gcs_multi({
            'gs://walrus/data/bar': b'',
            'gs://walrus/data/bar/baz': b'',
            'gs://walrus/data/foo': b'',
            'gs://walrus/qux': b'',
        })

        uris = [
            'gs://walrus/data/bar',
            'gs://walrus/data/bar/baz',
            'gs://walrus/data/foo',
            'gs://walrus/qux',
        ]

        self.assertEqual(set(self.fs.ls('gs://walrus/')), set(uris))
        self.assertEqual(set(self.fs.ls('gs://walrus/*')), set(uris))

        self.assertEqual(set(self.fs.ls('gs://walrus/data')), set(uris[:-1]))
        self.assertEqual(set(self.fs.ls('gs://walrus/data/')), set(uris[:-1]))
        self.assertEqual(set(self.fs.ls('gs://walrus/data/*')), set(uris[:-1]))

    def test_ls_globs(self):
        self.put_gcs_multi({
            'gs://w/a': b'',
            'gs://w/a/b': b'',
            'gs://w/ab': b'',
            'gs://w/b': b'',
        })

        self.assertEqual(set(self.fs.ls('gs://w/')),
                         set(['gs://w/a', 'gs://w/a/b',
                              'gs://w/ab', 'gs://w/b']))
        self.assertEqual(set(self.fs.ls('gs://w/*')),
                         set(['gs://w/a', 'gs://w/a/b',
                              'gs://w/ab', 'gs://w/b']))
        self.assertEqual(list(self.fs.ls('gs://w/*/')),
                         ['gs://w/a/b'])
        self.assertEqual(list(self.fs.ls('gs://w/*/*')),
                         ['gs://w/a/b'])
        self.assertEqual(list(self.fs.ls('gs://w/a?')),
                         ['gs://w/ab'])
        # * can match /
        self.assertEqual(set(self.fs.ls('gs://w/a*')),
                         set(['gs://w/a', 'gs://w/a/b', 'gs://w/ab']))
        self.assertEqual(set(self.fs.ls('gs://w/*b')),
                         set(['gs://w/a/b', 'gs://w/ab', 'gs://w/b']))

    def test_du(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'abcde',
            'gs://walrus/data/bar/baz': b'fgh'
        })

        self.assertEqual(self.fs.du('gs://walrus/'), 8)
        self.assertEqual(self.fs.du('gs://walrus/data/foo'), 5)
        self.assertEqual(self.fs.du('gs://walrus/data/bar/baz'), 3)

    def test_exists(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'abcd'
        })
        self.assertEqual(self.fs.exists('gs://walrus/data/foo'), True)
        self.assertEqual(self.fs.exists('gs://walrus/data/bar'), False)

    def test_md5sum(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'abcd'
        })

        self.assertEqual(self.fs.md5sum('gs://walrus/data/foo'),
                         md5(b'abcd').hexdigest())

    def test_md5sum_of_missing_blob(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'abcd'
        })

        self.assertRaises(IOError, self.fs.md5sum, 'gs://walrus/data/bar')

    def test_rm(self):
        self.put_gcs_multi({
            'gs://walrus/foo': b''
        })

        self.assertEqual(self.fs.exists('gs://walrus/foo'), True)
        self.fs.rm('gs://walrus/foo')
        self.assertEqual(self.fs.exists('gs://walrus/foo'), False)

    def test_rm_dir(self):
        self.put_gcs_multi({
            'gs://walrus/data/foo': b'',
            'gs://walrus/data/bar/baz': b'',
        })

        self.assertEqual(self.fs.exists('gs://walrus/data/foo'), True)
        self.assertEqual(self.fs.exists('gs://walrus/data/bar/baz'), True)
        self.fs.rm('gs://walrus/data')
        self.assertEqual(self.fs.exists('gs://walrus/data/foo'), False)
        self.assertEqual(self.fs.exists('gs://walrus/data/bar/baz'), False)
