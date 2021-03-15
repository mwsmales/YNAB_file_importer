import file_conversion
import settings

# import and convert FirstDirect file
file_conversion.file_conversion_fn('C:/Users/micha/Downloads/02022020_1684.CSV', 'C:/Users/micha/Downloads/fd.CSV',
                                   'first_direct')

# Import and convert Amex file
#file_conversion.file_conversion_fn('C:/Users/micha/Downloads/ofx.CSV', 'C:/Users/micha/Downloads/Amex.CSV', 'amex')

# Import and convert Nationwide file
#file_conversion.file_conversion_fn('C:/Users/micha/Downloads/Statement Download 2019-Feb-19 5-55-02.csv',
#                                   'C:/Users/micha/Downloads/Nationwide.CSV', 'nationwide')
