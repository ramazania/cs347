encoding = '##1!2!3#44#5!6!7!8##'
encoding = encoding.replace('##','')
bins = encoding.split('#')

num_items = 0
for bin in bins:
    bin = bin.split('!')
    num_items += len(bin)
    
    

    
   
# total_size = 0
# for bin in encoding:
#     if '!' in bin:
#         bin = bin.split('!')
#         for num in bin:
#             total_size += int(num)
#     else:
#         total_size += int(bin)
    

# print(total_size)
print(len(bins))