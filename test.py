import subprocess
import re


def _parse_esn_data():
    """Parse out the esn id data from the big chunk of dicts we got from
       parsing the JSOn-ish data from the netflix homepage
    Parameters
    ----------
    netflix_page_data : :obj:`list` of :obj:`dict`
        List of all the JSON-ish data that has been
        extracted from the Netflix homepage
        see: extract_inline_netflix_page_data
    Returns
    -------
        :obj:`str` of :obj:`str
        ESN, something like: NFCDCH-MC-D7D6F54LOPY8J416T72MQXX3RD20ME
    """
    # we generate an esn from device strings for android
    try:
        # manufacturer = subprocess.check_output(
        #     ['/system/bin/getprop', 'ro.product.manufacturer']).decode('utf-8')
        manufacturer = 'Google'
        # model = subprocess.check_output(
        #     ['/system/bin/getprop', 'ro.product.model']
        # ).decode('utf-8').strip(' \t\n\r')
        model = 'Pixel'.strip(' \t\n\r')

        if manufacturer:
            # esn = 'NFANDROID1-PRV-' if subprocess.check_output(
            #     ['/system/bin/getprop', 'ro.build.characteristics']
            # ).decode('utf-8').strip(' \t\n\r') != 'tv' else 'NFANDROID2-PRV-'

            esn = 'NFANDROID1-PRV-'

            # esn = 'nosdcard'.strip(' \t\n\r') != 'tv' else 'NFANDROID2-PRV-'
            # input = subprocess.check_output(
            #     ['/system/bin/getprop', 'ro.nrdp.modelgroup']
            # ).decode('utf-8').strip(' \t\n\r')
            input = None
            if not input:
                if model:
                    esn += model.replace(' ', '').upper() + '-'
                else:
                    esn += 'T-L3-'
            else:
                esn += input + '-'
            esn += '{:=<5.5}'.format(manufacturer.strip(' \t\n\r').upper())
            esn += model.replace(' ', '=').upper()
            esn = re.sub(r'[^A-Za-z0-9=-]', '=', esn)
            print('Android generated ESN:' + esn)
            # self.nx_common.log(msg='Android generated ESN:' + esn)
            return esn
    except OSError as e:
        print(e)
        print('Ignoring exception for non Android devices')

    # values are accessible via dict (sloppy parsing successfull)
    # if type(netflix_page_data) == dict:
    #     return netflix_page_data.get('esn', '')
    return ''


import pymsl
user_auth_data = {
     'scheme': 'EMAIL_PASSWORD',
     'authdata': {
         'email': 'chinmaympatel5000@gmail.com',
         'password': '4bhaiBIDI'
     }
}
client = pymsl.MslClient(user_auth_data)
a = client.load_manifest(80092521)
print(a)
# {'version': 2, ...