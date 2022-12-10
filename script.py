from collections import OrderedDict
def main():

    def write_chunk(part, lines):
        with open('datas//data_part_'+ str(part) +'.csv', 'w', encoding="utf-8-sig") as f_out:
            f_out.write(header)
            f_out.writelines(lines)
            f_out.close()
    datas=OrderedDict()
    with open('vacancies_by_year.csv', 'r', encoding="utf-8-sig") as f:
        header = f.readline()
        for line in f:
            data=line.split(",")[-1][0:4]
            if(data in datas):
                datas[data].append(line)
            else:
                datas[data]=[line]

        for data in datas:  
            write_chunk(data,datas[data])
                


if __name__ == '__main__':
    main()
