text_file_path = '/workspace/my_tacotron2/filelists/vctk_valid_docker.txt'
text_file_path2 = '/workspace/my_tacotron2/filelists/vctk_valid_docker.txt'

with open(text_file_path,'r',encoding='utf-8') as f:
    #lines = f.readlines()
    lines = f.readlines()

sort_dict = {}
for idx in range(len(lines)):
    lines[idx] = lines[idx].strip()
    temp = lines[idx].split('|')

    # if 'p225' in lines[idx]:
    #     lines[idx]+='|0|0|0'
    # if 'p226' in lines[idx]:
    #     lines[idx]+='|0|1|1'
    # if 'p227' in lines[idx]:
    #     lines[idx]+='|0|2|1'
    # if 'p228' in lines[idx]:
    #     lines[idx]+='|0|3|0'
    # if 'p229' in lines[idx]:
    #     lines[idx]+='|0|4|0'
    # if 'p230' in lines[idx]:
    #     lines[idx]+='|0|5|0'
    # if 'p231' in lines[idx]:
    #     lines[idx]+='|0|6|0'
    # if 'p232' in lines[idx]:
    #     lines[idx]+='|0|7|1'
    # if 'p243' in lines[idx]:
    #     lines[idx]+='|0|8|1'
    # if 'p254' in lines[idx]:
    #     lines[idx]+='|0|9|1'

    # num = temp[0].split('/')
    # sort_dict[int(num[-1][-11:-4])] = lines[idx]

    # if 'FHGA0' in lines[idx]:
    #     temp = lines[idx].split(' ')
    #     temp[0] = '/workspace/data/skt_db/2020/small/FHGA0/wav_48000/' + temp[0] +'.wav'
    # else:
    #     lines[idx-1] += lines[idx]
    #     continue
    #temp[0] = '/workspace/disk/data/kaist-audio-book/wav/'+ temp[0]
    lines[idx] = lines[idx].replace('/workspace/disk/data/data/','/workspace/disk/data/')
    # lines[idx] = lines[idx].replace('/txt/','/wav48/')
    # lines[idx] = lines[idx].replace('.txt','.wav')
    # lines[idx] = lines[idx].replace('/man2/','/man2_22050/')
    # lines[idx] = lines[idx].replace('/man3/','/man3_22050/')
    # lines[idx] = lines[idx].replace('/man4/','/man4_22050/')
    # lines[idx] = lines[idx].replace('/man5/','/man5_22050/')
    # lines[idx] = lines[idx].replace('/man6/','/man6_22050/')
    # lines[idx] = lines[idx].replace('/woman1/','/woman1_22050/')
    # lines[idx] = lines[idx].replace('/woman2/','/woman2_22050/')
    # lines[idx] = lines[idx].replace('/woman3/','/woman3_22050/')
    # lines[idx] = lines[idx].replace('/woman4/','/woman4_22050/')
    # lines[idx] = lines[idx].replace('/woman5/','/woman5_22050/')
    # lines[idx] = lines[idx].replace('/woman6/','/woman6_22050/')
    

    #lines[idx] = lines[idx].replace('')

    #temp[0] = '/workspace/data/skt_db/2020/large/FPHJ0/wav_48000/' + temp[0].split('/')[-1] +'.wav'

    # if 'raw' in temp[0]:
    #     temp[0] = temp[0].replace('raw','wav')

    #lines[idx] = '|'.join(temp)
    # lines[idx] = temp[0] + '|'

# print(len(sort_dict))
# d1 = sorted(sort_dict.items())
# d2 = dict(d1)
# sort_dict = d2

with open(text_file_path2,'w',encoding='utf-8') as f:
   for idx in range(len(lines)):
        # if '/man1_22050/' in lines[idx]:
        #     f.write(lines[idx])
        #     f.write('\n')
        # if '/woman1_22050/' in lines[idx]:
        #     f.write(lines[idx])
        #     f.write('\n')
        f.write(lines[idx])
        f.write('\n')

# with open(text_file_path2,'w',encoding='utf-8') as f:
#    for key in sort_dict.keys():
#         # if '/man1_22050/' in lines[idx]:
#         #     f.write(lines[idx])
#         #     f.write('\n')
#         # if '/woman1_22050/' in lines[idx]:
#         #     f.write(lines[idx])
#         #     f.write('\n')
#         f.write(sort_dict[key])
#         f.write('\n')