# import mylib
# myfunction(id,"this is a sentence")
import os
import json

#private函数集：
def get_description(idcode,description):
    with open('intact_reactions.json', 'r') as load_s:
        description_sentence=""
        lines_json = load_s.readlines()

        if_find = False  # flag初始化为false
        for line in lines_json:

            # print(line)
            intact_item = json.loads(line)
            intact_id = intact_item['intact_id']

            if  intact_id == idcode:
                if_find = True #已经找到
                description_sentence = intact_item['description']  # 得到description
                # print(description_sentence)
                description.append(description_sentence)
                return True

        # 对于在intact.json中没有找到的idcode
        if if_find == False:
            print('%s未找到' % (idcode))
            return False


#public函数集:

#description()返回一个idcode对应的description
#input:str idcode
#return:str description
def description(idcode):
    description=[]
    assert get_description(idcode,description)
    return description[0]


#same()判断idcode和sentence是否对应同一个event，返回True/False
#input:str idcode,str sentence
#output:bool True/False
def same(idcode,sentence):
    sentence1 = description(idcode)
    sentence2=sentence.strip("\"")
    # print(sentence2)

    #调用模型判断
    a = os.popen('th ./load_model2.lua -task snli ' + '-sent1 \"' + sentence1 + '\" -sent2 \"' + sentence2 + '\"')
    #将结果打印出来，返回给用户一个值t/f
    lines = a.readlines()
    result=""
    for line in lines: # 注意：明天要改这个same为特殊标记，确保不出现：如sssssame
        if line[:4]=="diff" or line[:4]=="same":
            result=line
        # result = lines[-1]
    # print(result)
    #判断
    # assert result[:4] == "diff" or result[:4] == "same"
    if (result[:4] == "diff"):
        # print("Different Event : \n" + sentence1 + "\n" + sentence2)
        return False
    elif (result[:4] == "same"):
        # print("Same Event : \n" + sentence1 + "\n" + sentence2)
        return True
    else:
        print("wrong!")
        # print(lines)

#主函数测试：

if __name__ == '__main__':
    # samemeaning("Cancer between BCL2L2 and Bid, and the interaction type is physical association","tBID displace in a pattern that replicates the pattern in Figure 2D from BCL-w by sensitizer BH3 peptides.")

    # idcode = "EBI-2638578"
    # sentence1 = description(idcode) #获得idcode对应的sentence
    # # print(sentence1)
    # print(same(idcode,"Immunoblot analysis of the applied, flowthrough, and bound samples revealed that PP4C and PP4R1 co-purified on microcystin-Sepharose (Fig. 7)."))

    a=open('source-part.txt','r')
    lines_t=a.readlines()
    cnt=0
    N=0
    for line_t in lines_t:

        # print(N)
        N=N+1
        first_comm=line_t.index(',')
        second_comm=line_t.index(',',first_comm+1)
        idcode_t=line_t[first_comm+1:second_comm]
        sentence_t=line_t[second_comm+1:-1]

        if(print(same(idcode_t,sentence_t))):
            cnt=cnt+1
    accuracy=cnt/N
    print(accuracy)