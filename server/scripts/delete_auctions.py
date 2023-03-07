# setup Django for standalone use
# also set DJANGO_SETTINGS_MODULE='dj_wfl.settings' in ~/.bashrc
import django
django.setup()

import datetime as dt
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl' to PYTHONPATH
from wfl.utils import QueryManager

# add '/home/ec2-user/environment/wow-free-lunch/server' to PYTHONPATH


def main():
    
    # delete data 3 days old or older
    DATE_THRESHOLD = 3
    
    qm = QueryManager()
    
    # delete data more than 3 days old except for the 1st of each month
    date = (dt.datetime.now() 
        - dt.timedelta(days=DATE_THRESHOLD)).strftime('%Y-%m-%d')
    print('Deleting auctions up to and including {}'.format(date))
    
    sql = '''
        DELETE
        FROM auction 
        WHERE update_date <= %s
            AND DAY(update_date) > 1;
    '''
    params = [date]
    res = qm.query(sql, params, row_count=True)
    print('Deleted {} rows'.format(res))
    
    # OPTIMIZE table to reclaim space
    
    sql = 'OPTIMIZE TABLE auction;'
    res = qm.query(sql)
    print('Optimized auction table')

if __name__ == "__main__":
    main()