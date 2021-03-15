import datetime

# set conversion rate
gbp_cad = 1.72

# field mappings for different banks
fd_mapping = {'Description': 'Payee', 'Amount': 'Inflow'}
nw_mapping = {'Transactions':'Payee', 'Paid out': 'Outflow', 'Paid in': 'Inflow'}

# Amex header file
amex_header = ['Date', 'Description', 'Outflow', 'Payee', 'Memo', 'Not_used']

# Date ranges of interest
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 1, 31)
amex_start_date = start_date
amex_end_date = end_date
fd_start_date = start_date
fd_end_date = end_date
nw_start_date = start_date
nw_end_date = end_date
