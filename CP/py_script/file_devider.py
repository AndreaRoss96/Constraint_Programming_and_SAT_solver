index=0
finish = 0
index_paper = 0
finish_paper = 0

output_file = open(r"CP\\output_rot.txt", 'r')
lines = output_file.readlines()

file_payload = []

for line in lines :
    #print(line)
    if line.find('> ') != -1 :
        start_name_index = line.find('>')
        end_name_index = line.find('.dzn')
        file_name = line[start_name_index+2:end_name_index]
        print("******************************************************" + file_name)
    elif line.find("----------") == 0 :
        # write file 
        #  reset varaibles
        print(">>>>>>>>>>>>>" + file_name)
        [print(f) for f in file_payload]

        final_file = open(file_name + '-out.txt', 'w')
        [final_file.write(f) for f in file_payload]
        final_file.close()
        file_payload = []
    elif line == "=====UNKNOWN=====\n" or line == "Stopped.\n" or line.find("Finished") == 0:
        # print("continue")
        continue
    else :
        #print("<<<<<<<<<<" + line.replace("\n", "")) 
        file_payload.append(line)
    



# while index < len(a):
#     index = a.find('>', index)
#     if index == -1:
#         break
#     finish = a.find('.dzn', finish)
#     paper_name = a[index+2:finish]
#     index += 2
#     finish+=5
    
#     index_paper = a.find(time_, index_paper)
#     finish_paper = a.find('s', index_paper+len(time_))
    
#     time_sum = a[index+len(time_):finish+1]
#     index += len(time_)
#     finish += 4
    
#     if time_sum == "16m 41s":
#         time_sum = "- - "
    
#     print(paper + " & " + time_sum + "\\\\")