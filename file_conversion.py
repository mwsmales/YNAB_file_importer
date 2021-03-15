import settings
import functions
import datetime


def file_conversion_fn(input_file, output_file, bank_type):
    # OPEN, READ AND CLOSE FILE
    # open file to read
    f = open(input_file, 'r')

    # if filetype is Nationwide, discard first 4 rows
    if bank_type == 'nationwide':
        for i in range(0, 4):
            f.readline()

    # read in header row into header array
    if bank_type == 'first_direct' or bank_type == 'nationwide' :
        header = f.readline().strip().split(',')

    # read in data as strings into nxn array
    data_array = []
    for arr_t in f:
        data_array.append(arr_t.strip().split(','))

    # If Amex file then add headings
    if bank_type == 'amex':
        header = settings.amex_header[:]

    f.close()

    # get size of array
    num_rows = len(data_array)
    num_cols = len(data_array[0])

    # DATA CLEANING STEP 1: BASIC REFORMATTING
    # If Nationwide or Amex file type then clear additional '"' from each entry
    if bank_type == 'amex' or bank_type == 'nationwide':
        for i in range(0, num_rows):
            for j in range(0, num_cols):
                data_array[i][j] = data_array[i][j].strip('"')
        for i in range(0, num_cols):
            header[i] = header[i].strip('"')

    # If Nationwide then remove £ from inflow and outflow columns
    if bank_type == 'nationwide':
        for i in range(0, num_rows):
            data_array[i][3] = data_array[i][3].strip('£')
            data_array[i][4] = data_array[i][4].strip('£')

    # ADD / RENAME COLUMN HEADINGS
    # remap column headings depending on bank type
    if bank_type == 'first_direct':
        for i in range(0, num_cols):
            if header[i] in settings.fd_mapping.keys():
                header[i] = settings.fd_mapping[header[i]]
    elif bank_type == 'nationwide':
        for i in range(0, num_cols):
            if header[i] in settings.nw_mapping.keys():
                header[i] = settings.nw_mapping[header[i]]

    # Insert any missing columns with blank values
    if bank_type == 'first_direct' or bank_type == 'nationwide':
        header_to_insert = 'Memo'
        functions.insert_col(header, data_array, header_to_insert, num_rows)
        num_cols += 1
    elif bank_type == 'amex':
        header_to_insert = 'Inflow'
        functions.insert_col(header, data_array, header_to_insert, num_rows)
        num_cols += 1

    # DATA CLEANING STEP 2: CLEAN DATES
    # set up array to store transaction dates as datetime objects (rather than strings)
    trans_date = []
    # get index number for the 'Date' column
    date_col = functions.get_col_index(header, 'Date', num_cols)

    #rewrite date into standard format
    if bank_type == 'nationwide':
        for i in range(0, num_rows):
            date = datetime.datetime.strptime(data_array[i][date_col], '%d-%b-%y')
            trans_date.append(date)
            data_array[i][date_col] = date.strftime('%d-%m-%y')
    elif bank_type == 'first_direct' or bank_type == 'amex':
        for i in range(0, num_rows):
            date = datetime.datetime.strptime(data_array[i][date_col], '%d/%m/%Y')
            trans_date.append(date)
            data_array[i][date_col] = date.strftime('%d-%m-%y')

    # Delete any entries outside of date range
    # set starting and ending dates depending on file type
    if bank_type == 'first_direct':
        start_date = settings.fd_start_date
        end_date = settings.fd_end_date
    elif bank_type == 'amex':
        start_date = settings.amex_start_date
        end_date = settings.amex_end_date
    elif bank_type == 'nationwide':
        start_date = settings.nw_start_date
        end_date = settings.nw_end_date

    # loop through rows and if an entry is outside of the date range then delete it and reduce row_num
    i = 0
    while i < num_rows:
        if trans_date[i] < start_date or trans_date[i] > end_date:
            del data_array[i]
            del trans_date[i]
            num_rows -= 1
        else:
            i += 1

    # TODO: Once Amex file is working, change this to autodetect if any file headings are missing and add them if needed
    # TODO set up json file to save 'to' date from this export and next time import that as the 'from' date

    # Convert outflows to inflows and erase all values in outflows column
    if 'Outflow' in header:
        for i in range(0, num_cols):
            if header[i] == 'Outflow':
                outflow_col = i
            if header[i] == 'Inflow':
                inflow_col = i

        for i in range(0, num_rows):
            if data_array[i][outflow_col] == '':
                continue
            else:
                data_array[i][inflow_col] = str(- float(int(float(data_array[i][outflow_col]) * 100))/100)

        for i in range(0, num_rows):
            data_array[i][outflow_col] = ''

    # CONVERT GBP INFLOWS INTO CAD
    # Extract Inflow column as a list of integer values (in pennies)
    # Set up target array for the transactions
    transactions_gbp = []

    # Get index of column number we want to copy out
    col_to_copy = functions.get_col_index(header, 'Inflow', num_cols)

    # Copy the column in question
    for i in range(0, num_rows):
        value = float(data_array[i][col_to_copy])
        value = int(value * 100)
        transactions_gbp.append(value)

    # TODO: PRIORITY2 create array of exchange rates to use depending on the transaction date

    # Convert transactions to CAD (in cents)
    transactions_cad = [int(settings.gbp_cad * x) for x in transactions_gbp]

    # memos describing the conversion amount and rate
    memo = []
    for i in range(0, num_rows):
        memo.append("GBP" + str(transactions_gbp[i] / 100) + "@" + str(settings.gbp_cad))

    # write the memo list and updated CAD inflow list into the main data_table as string values for output to CSV
    # find the memo column index
    col_to_update = functions.get_col_index(header, 'Memo', num_cols)

    # overwrite the values in the memo column
    for i in range(0, num_rows):
        data_array[i][col_to_update] = memo[i]

    # find the inflow column index
    col_to_update = functions.get_col_index(header, 'Inflow', num_cols)

    # overwrite the values in the memo column
    for i in range(0, num_rows):
        data_array[i][col_to_update] = transactions_cad[i] / 100

    # WRITE THE DATA TO A CSV FILE
    import csv
    ofile = open(output_file, "w")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
    writer.writerow(header)
    for i in range(0, num_rows):
        writer.writerow(data_array[i])
    ofile.close()
