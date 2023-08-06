﻿# coding=UTF-8
from __future__ import print_function, unicode_literals
import six
from six.moves import range, zip
from math import isnan
import numpy as np
import time
import gc
import psutil

if six.PY2:
    import unittest2 as unittest
else:
    import unittest

import sjts

try:
    from blist import blist
except ImportError:
    blist = None


class SJTSTests(unittest.TestCase):
    def test_simple(self):
        encoded = sjts.encode({'success': False})
        self.assertEqual(encoded, b'SJTS\x11\x00\x00\x00{"success":false}')

    def test_simpleException1(self):
        with self.assertRaises(sjts.ParseException):
            sjts.encode(True)

    def test_simpleException3(self):
        with self.assertRaises(sjts.ParseException):
            sjts.encode({'success': False, 'series': []})

    def test_big(self):
        obj = {'success': False, 'big_value': [{'abcdef': 12345.67890}] * 10000}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodeResponses(self):
        obj = {'success': True, 'series': [1, 2]}
        encoded = sjts.encode(obj)
        self.assertEqual(encoded, b'SJTS\x1b\x00\x00\x00{"series":2,"success":true}\x01\x00\x00\x001\x01\x00\x00\x002')
        self.assertEqual(sjts.decode(encoded), obj)

    def test_encodeBigReponse(self):
        obj = {'success': True, 'series': [{'big_value': [{'abcdef': 12345.67890}] * 10000}]}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodePoint(self):
        obj = {'success': True, 'series': [{'points': [(1, 1234.5678)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(encoded[39:-22], b'{"points":1}\x10\x00')
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodePointAsList(self):
        obj = {'success': True, 'series': [{'points': [[1, 1234.5678]]}]}
        objTuple = {'success': True, 'series': [{'points': [(1, 1234.5678)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(objTuple, sjts.decode(encoded))

    def test_encodePoints2(self):
        obj = {'success': True, 'series': [{'points': [(1, 1234.5678), (2, 33.2)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(encoded[39:-34], b'{"points":2}\x1c\x00')
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodePoints2Backward(self):
        obj = {'success': True, 'series': [{'points': [(2, 1234.5678), (1, 33.2)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(encoded[39:-34], b'{"points":2}\x1c\x00')
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodeDecode(self):
        obj = {'success': True, 'series': [{'points': [(a, 12.345) for a in range(100)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_encodeDecodeSkippedPonts(self):
        obj = {'success': True,
               'series': [{'points': [(1, 1234.5678), (2, 33.2), (10, 123.445), (20, 323.33), (50, 323.1)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_emptyPoints(self):
        obj = {'success': True, 'series': [{'points': []}]}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_emptyPointWithInteger(self):
        obj = {'success': True, 'series': [{'points': [[1, 2]]}]}
        objFloat = {'success': True, 'series': [{'points': [(1, 2.0)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(objFloat, sjts.decode(encoded))

    def test_emptyPointWithFloat(self):
        obj = {'success': True, 'series': [{'points': [[1.2345, 2.0]]}]}
        objFloat = {'success': True, 'series': [{'points': [(1, 2.0)]}]}
        encoded = sjts.encode(obj)
        self.assertEqual(objFloat, sjts.decode(encoded))

    def test_malloc_memory_corruption(self):
        obj = {'series': [
            {'series_id': u'G_LA_43\\Output\\Ammonia',
             'points': [(1293840000000, 0.132), (1325376000000, 0.0), (1356998400000, 0.0), (1388534400000, 0.0),
                        (1420070400000, 0.132), (1451606400000, 0.132), (1483228800000, 0.132), (1514764800000, 0.132),
                        (1546300800000, 0.132), (1577836800000, 0.132), (1609459200000, 0.132), (1640995200000, 0.132),
                        (1672531200000, 0.132), (1704067200000, 0.132), (1735689600000, 0.132),
                        (1767225600000, 0.132)]},
            {'series_id': u'Gasification\\gasification_plants\\G_NA_72'},
            {'series_id': u'Gasification\\gasification_plant_series\\G_AS_997\\Input\\Natural Gas',
             'points': [(1293840000000, 36.358), (1325376000000, 36.358), (1356998400000, 36.358),
                        (1388534400000, 36.358), (1420070400000, 36.358), (1451606400000, 36.358),
                        (1483228800000, 36.358), (1514764800000, 36.358), (1546300800000, 36.358),
                        (1577836800000, 36.358), (1609459200000, 36.358), (1640995200000, 36.358),
                        (1672531200000, 36.358), (1704067200000, 36.358), (1735689600000, 36.358),
                        (1767225600000, 36.358)]}
        ], 'success': True}
        encoded = sjts.encode(obj)
        self.assertEqual(obj, sjts.decode(encoded))

    def test_series_jobs(self):
        series = {'points': [(1, 1, 4), (2, 2, 5), (4, 3, 6), (10, 1, 1)]}
        decode_data = sjts.dumps_series(series, True, False)
        self.assertEqual(series, sjts.loads_series(decode_data))

    def test_series_timestamps(self):
        series = {'points': [(1, 1, 4), (2, 2, 5), (4, 3, 6), (10, 1, 1)]}
        decode_data = sjts.dumps_series(series, False, True)
        # loads_series returns the same what dump_series got as parameter
        self.assertEqual(series, sjts.loads_series(decode_data))

    def test_series_job_timestamps(self):
        series = {'points': [(1, 1, 4, 10), (2, 2, 5, 11), (4, 3, 6, 12), (10, 1, 1, 14)]}
        decode_data = sjts.dumps_series(series, True, True)
        self.assertEqual(series, sjts.loads_series(decode_data))

    def test_with_sjts_key(self):
        with self.assertRaises(sjts.ParseException):
            sjts.encode({'success': True, 'sjts': {}})

    def test_with_sjts_key2(self):
        with self.assertRaises(sjts.ParseException):
            sjts.dumps_series({'success': True, 'sjts': {}})

    def test_crash_regression(self):
        series = {'points': [(1, 1,), (2, 2), (4, 3), (10, 1,)]}
        sjts.dumps_series(series)

    def test_job_timestamps(self):
        series = {'success': True,
                  'series': [{'points': [(1, 1, 4, 10), (2, 2, 5, 11), (4, 3, 6, 12), (10, 1, 1, 14)]}]}
        decode_data = sjts.dumps(series, True, True)
        self.assertEqual(series, sjts.loads(decode_data))

    def test_numpy(self):
        points = [(1, 2), (3, 4), (5, 6)]

        def obj(points): return {'success': True, 'series': [{'points': points}]}

        decode_data = sjts.dumps(obj(np.array(points, np.dtype('i8,f8'))))
        self.assertEqual(obj(points), sjts.loads(decode_data))

    def test_numpy_jobs_timestamps(self):
        points = [(1, 2, 7, 8), (3, 4, 9, 10), (5, 6, 11, 12)]

        def obj(points): return {'success': True, 'series': [{'points': points}]}

        decode_data = sjts.dumps(obj(np.array(points, np.dtype('i8,f8,i4,u8'))), True, True)
        self.assertEqual(obj(points), sjts.loads(decode_data))

    def test_numpy_jobs(self):
        points = [(1, 2, 7), (3, 4, 9), (5, 6, 11)]

        def obj(points): return {'success': True, 'series': [{'points': points}]}

        decode_data = sjts.dumps(obj(np.array(points, np.dtype('i8,f8,i4'))), True)
        self.assertEqual(obj(points), sjts.loads(decode_data))

    def test_numpy_timestamps(self):
        points = [(1, 2, 7), (3, 4, 9), (5, 6, 11)]

        def obj(points): return {'success': True, 'series': [{'points': points}]}

        decode_data = sjts.dumps(obj(np.array(points, np.dtype('i8,f8,u8'))), False, True)
        self.assertEqual(obj(points), sjts.loads(decode_data))

    def test_numpy_series(self):
        points = [(1, 2), (3, 4), (5, 6)]
        obj = {'success': True, 'series': [{'points': points}]}
        decode_data = sjts.dumps_series({'points': np.array(points, np.dtype('i8,f8'))})
        self.assertEqual(points, sjts.loads_series(decode_data)['points'])

    def test_numpy_loads(self):
        obj = {'success': True, 'series': [{'points': np.array([(1, 2), (3, 4), (5, 6)], np.dtype('i8,f8'))}]}
        decode_data = sjts.dumps(obj)
        obj2 = sjts.loads(decode_data, True)

        def to_list(obj): obj['series'][0]['points'] = [(f[0], f[1]) for f in obj['series'][0]['points']]

        to_list(obj)
        to_list(obj2)
        self.assertEqual(obj, obj2)

    def test_numpy_loads_series(self):
        points = np.array([(1, 2), (3, 4), (5, 6)], np.dtype('i8,f8'))
        obj = {'points': points}
        decode_data = sjts.dumps_series({'points': points})
        obj2 = sjts.loads_series(decode_data, True)

        def to_list(obj): obj['points'] = [(f[0], f[1]) for f in obj['points']]

        to_list(obj)
        to_list(obj2)
        self.assertEqual(obj, obj2)

    def test_without_success(self):
        try:
            encoded = sjts.encode({})
        except sjts.ParseException:
            self.fail("should encode without success key!")

    def test_nan(self):
        decode_data = sjts.dumps_series({'points': [(1, float('nan'))]})
        obj = sjts.loads_series(decode_data)
        self.assertTrue(isnan(obj['points'][0][1]))

    def test_none(self):
        decode_data = sjts.dumps_series({'points': [(1, None)]})
        obj = sjts.loads_series(decode_data)
        self.assertTrue(isnan(obj['points'][0][1]))

    def test_numpy_types(self):
        series = {'points': [(1, 1234.5678, 2, 3)]}
        decode_data = sjts.dumps_series(series)
        res = sjts.loads_series(decode_data, use_numpy = True)
        self.assertEqual(res['points'].tolist(), [(1, 1234.5678,)])
        self.assertItemsEqual(['dates', 'values'], res["points"].dtype.fields.keys())

    def test_numpy_types_jobs(self):
        series = {'points': [(1, 1234.5678, 2)]}
        decode_data = sjts.dumps_series(series, True)
        res = sjts.loads_series(decode_data, use_numpy = True)
        self.assertEqual(res['points'].tolist(), [(1, 1234.5678, 2)])
        self.assertItemsEqual(['jobs', 'dates', 'values'], res["points"].dtype.fields.keys())

    def test_numpy_types_timestamps(self):
        series = {'points': [(1, 1234.5678, 3)]}
        decode_data = sjts.dumps_series(series, False, True)
        res = sjts.loads_series(decode_data, use_numpy = True)
        self.assertEqual(res['points'].tolist(), [(1, 1234.5678, 3)])
        self.assertItemsEqual(['dates', 'values', 'ts'], res["points"].dtype.fields.keys())

    def test_numpy_types_jobs_timestamps(self):
        series = {'points': [(1, 1234.5678, 2, 3)]}
        decode_data = sjts.dumps_series(series, True, True)
        res = sjts.loads_series(decode_data, use_numpy = True)
        self.assertEqual(res['points'].tolist(), [(1, 1234.5678, 2, 3)])
        self.assertItemsEqual(['jobs', 'dates', 'values', 'ts'], res["points"].dtype.fields.keys())

class TestMemoryLeaks(unittest.TestCase):
    def test_sjts_dumps_with_small_numpy_arrays(self):
        pts1_data = [(i, 1., 1, 1) for i in xrange(100)]
        pts2_data = [(i + 1000, 1., 1, 1) for i in xrange(100)]

        _s = time.time()
        init_usage = psutil.Process().memory_info().rss
        iterations = 0
        while (time.time() - _s) < 60:
            sjts.dumps({
                'success': True,
                'series': [
                    {
                        'series_id': '1', 'points': pts1_data,
                    },
                    {
                        'series_id': '2', 'points': pts2_data
                    }
                ]
            })
            iterations += 1
        gc.collect()
        end_usage = psutil.Process().memory_info().rss

        self.assertLess(float(end_usage) / float(init_usage) - 1, 0.9,
                        'process mem rss grew from {:.2f}mb to {:.2f}mb ({:.2f}%)'
                        ' after {} iterations'.format(init_usage / 1024. / 1024,
                                                      end_usage / 1024. / 1024.,
                                                      (float(end_usage) / float(init_usage) - 1) * 100.,
                                                      iterations))

    def test_sjts_loads_and_use_numpy(self):
        points = [[i, i] for i in xrange(200000)]
        data = sjts.dumps({
            'success': True,
            'series': [{
                'series_id': 'test',
                'points': points
            }]
        })
        _s = time.time()
        init_usage = psutil.Process().memory_info().rss
        iterations = 0
        while (time.time() - _s) < 60:
            sjts.loads(data, use_numpy=True)
        gc.collect()
        end_usage = psutil.Process().memory_info().rss

        self.assertLess(float(end_usage) / float(init_usage) - 1, 0.9,
                        'process mem rss grew from {:.2f}mb to {:.2f}mb ({:.2f}%)'
                        ' after {} iterations'.format(init_usage / 1024. / 1024,
                                                      end_usage / 1024. / 1024.,
                                                      (float(end_usage) / float(init_usage) - 1) * 100.,
                                                      iterations))

    def test_sjts_dumps_with_large_numpy_arrays(self):
        points = np.array([[i, i] for i in xrange(200000)])
        _s = time.time()
        init_usage = psutil.Process().memory_info().rss
        iterations = 0
        while (time.time() - _s) < 60:
            sjts.dumps({
                'success': True,
                'series': [{
                    'series_id': 'test',
                    'points': points
                }]
            })
        gc.collect()
        end_usage = psutil.Process().memory_info().rss

        self.assertLess(float(end_usage) / float(init_usage) - 1, 0.9,
                        'process mem rss grew from {:.2f}mb to {:.2f}mb ({:.2f}%)'
                        ' after {} iterations'.format(init_usage / 1024. / 1024,
                                                      end_usage / 1024. / 1024.,
                                                      (float(end_usage) / float(init_usage) - 1) * 100.,
                                                      iterations))

    def test_sjts_dumps_if_unpack_args_used(self):
        _s = time.time()
        init_usage = psutil.Process().memory_info().rss
        iterations = 0
        body = {"points_desc": False, "request_id": "7SzrCMgVTqTBmuN", "scroll_id": "NfwvgKL2zt",
                "series": [{"series_id": "test_memleak\\384"}, {"series_id": "test_memleak\\323"},
                           {"series_id": "test_memleak\\395"}, {"series_id": "test_memleak\\356"},
                           {"series_id": "test_memleak\\393"}, {"series_id": "test_memleak\\337"},
                           {"series_id": "test_memleak\\304"}, {"series_id": "test_memleak\\315"},
                           {"series_id": "test_memleak\\299"}, {"series_id": "test_memleak\\367"},
                           {"series_id": "test_memleak\\328"}, {"series_id": "test_memleak\\377"},
                           {"series_id": "test_memleak\\331"}, {"series_id": "test_memleak\\378"}, ],
                "success": True,
                "total": 397}

        while (time.time() - _s) < 60:
            ser_args = [False, False]
            sjts.dumps(body, *ser_args)
        gc.collect()
        end_usage = psutil.Process().memory_info().rss

        self.assertLess(float(end_usage) / float(init_usage) - 1, 0.9,
                        'process mem rss grew from {:.2f}mb to {:.2f}mb ({:.2f}%)'
                        ' after {} iterations'.format(init_usage / 1024. / 1024,
                                                      end_usage / 1024. / 1024.,
                                                      (float(end_usage) / float(init_usage) - 1) * 100.,
                                                      iterations))


if __name__ == "__main__":
    unittest.main()

"""
# Use this to look for memory leaks
if __name__ == '__main__':
    from guppy import hpy
    hp = hpy()
    hp.setrelheap()
    while True:
        try:
            unittest.main()
        except SystemExit:
            pass
        heap = hp.heapu()
        print(heap)
"""
