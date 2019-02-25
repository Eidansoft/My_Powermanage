import unittest, requests

class TestStringMethods(unittest.TestCase):
    ip = 'localhost'
    port = '8080'

    def test_keepalive_method(self):
        r = requests.get('http://{}:{}/scripts/update.php'.format(self.ip, self.port), timeout=1)
        # test the response status
        self.assertTrue(r.status_code == 200,
                        "The status code {} was not expected".format(
                            r.status_code
                        )
        )
        # test the response contains the expected values
        self.assertTrue('status=0' in r.text)
        self.assertTrue('ka_time=' in r.text)
        self.assertTrue('allow=' in r.text)
        # test the response contains the expected headers
        self.assertTrue('Content-Type' in r.headers)
        self.assertTrue(
            r.headers['Content-Type'].lower() == 'text/plain; charset=utf-8',
            "The header[Content-Type] = {} is not valid".format(
                r.headers['Content-Type']
            )
        )


    def test_notification_method(self):
        index_code = '1234'
        payload = """<?xml version='1.0'?>
                   <notify>
                       <pmax_account>001234</pmax_account>
                       <index>{}</index>
                       <serial>052eeb</serial>
                       <time>1459463087</time>
                       <priority>2</priority>
                       <event id='81' type='Arm. Parcial'/>
                       <profile id='3' type='Open / Close'/>
                       <device id='3' type='Usuario'/>
                       <location id='1' type='admin'/>
                       <zone id='1'/>
                       <partition>1</partition>
                       <forward_automation>true</forward_automation>
                       <userlist>
                           <user name='admin' email='ownermailbox@hotmail.com' phone='555
                           666 777' is_sms='0' is_mms='0' is_email='1'/>
                           <user name='carmen' email='wifemailbox@gmail.com' phone='555 777
                           888' is_sms='0' is_mms='0' is_email='1'/>
                           <user name='juan' email='neigbourgmailbox@yahoo.com' phone='555
                           555 555' is_sms='0' is_mms='0' is_email='1'/>
                       </userlist>
                   </notify>""".format(index_code)

        r = requests.post('http://{}:{}/scripts/notify.php'.format(self.ip, self.port), data=payload, timeout=1)
        # test the response status
        self.assertTrue(r.status_code == 200)
        # test that the response does not contains php errors
        self.assertTrue('this will throw an Error in a future version of PHP' not in r.text)
        # test the response contains the expected values
        self.assertTrue('<index>{}</index>'.format(index_code) in r.text)
        # test the headers received are correct
        # print(r.headers)
        self.assertTrue(r.headers['Content-Type'] == 'text/xml;charset=UTF-8')


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
