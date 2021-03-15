# Define a function to insert a column
def insert_col(header, data_array, header_to_insert, num_rows):
    col_to_follow = len(header)

    header.insert(col_to_follow + 1, header_to_insert)

    # Next, insert the blank column into the data_array
    for i in range(0, num_rows):
        data_array[i].insert(col_to_follow + 1, '')


# function to delete a column
def delete_col(header, data_array, header_to_delete, num_cols, num_rows):
    if 'Balance' in header:
        for i in range(0, num_cols):
            if header[i] == header_to_delete:
                col_to_delete = i

        del header[col_to_delete]

        for i in range(0, num_rows):
            del data_array[i][col_to_delete]

    else:
        print('Error, value does not exist in array')
        quit()


# define a function to find a keyword in the header
def get_col_index(header, keyword, num_cols):
    for i in range(0, num_cols):
        if header[i] == keyword:
            return i
