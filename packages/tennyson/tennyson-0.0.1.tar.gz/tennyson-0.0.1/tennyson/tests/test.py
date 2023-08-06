#!/usr/bin/env python3
import unittest, os, tempfile

from tennyson import *

class TestPrinting(unittest.TestCase):

    def test_logger(self):
        log = mklog()
        self.assertEqual(log.name, __file__)
        log = mklog('asdf')
        self.assertEqual(log.name,'asdf')

    def test_timestamps_run(self):
        date_stamp()
        datetime_stamp()
        datetime_zone_stamp()


    def test_atomic_write(self):
        pass
    

class TestEmail(unittest.TestCase):

    def test_email(self):
        if os.environ.get('TEST_SEND_EMAILS', False):
            send_email_exn(recipients=['tennysontaylorbardwell@gmail.com'],
                           subject='Test 1/3', text='Test 1/3')
            alert_exn(message='Test 2/3', subject='Test 2/3')
            try:
                raise RuntimeError('Test 3/3')
            except Exception as e:
                error_email_exn(e)


class TestSafty(unittest.TestCase):

    def test_atomic_write(self):
        with tempfile.TemporaryDirectory() as dir_:
            a = os.path.join(dir_, 'a')
            b = os.path.join(dir_, 'b')

            with open_atomic(a, 'w') as fp:
                fp.write('abc')
            with open(a) as fp:
                self.assertEqual(fp.read(), 'abc')

            try:
                with open_atomic(b, 'w') as fp:
                    fp.write('abc')
                    raise RuntimeError()
            except RuntimeError:
                self.assertFalse(os.path.isfile(b))
            
            try:
                with open_atomic(a, 'w') as fp:
                    fp.write('xyz')
                    raise RuntimeError()
            except RuntimeError:
                with open(a) as fp:
                    self.assertEqual(fp.read(), 'abc')

    # def test_time_limit(self):
    #     time_limit()
    #     try:
    #         pass
    #     except TimeoutException:
    #         pass
        

class TestCommon(unittest.TestCase):

    def test_mkdir_p(self):
        with tempfile.TemporaryDirectory() as dir_:
            d = os.path.join(dir_, 'a', 'b', 'c', 'd')
            self.assertFalse(os.path.isdir(d))
            mkdir_p(d)
            self.assertTrue(os.path.isdir(d))

    def test_json(self):
        with tempfile.TemporaryDirectory() as dir_:
            f = os.path.join(dir_, 'a.json')
            o = ['a', 'b']
            j_dump(o, f)
            self.assertEqual(j_load(f), o)


class TestConfigAndSecrets(unittest.TestCase):

    def test_get_config(self):
        self.assertEqual(type(get_config()), dict)

    def test_get_settings(self):
        self.assertEqual(type(get_secrets()), dict)

if __name__ == '__main__':
    unittest.main()
