import sys

args = sys.argv   # args[1] = xyzfile, args[2] = POSCARfile

def get_sort_element(file1):
    from collections import Counter, OrderedDict
    with open(file1,'r') as f_xyz:
        fr = f_xyz.readlines()[2:]       #xyzファイルで座標は3行目から始まるので。
        line_list = [ l.split() for l in fr ]
        e_list = [ l.split()[0] for l in fr ]      #eは元素名だけが並び続けるリスト #yusuke e_list = [ l[0] for l in line_list] と書けるぽい？

        class OrderedCounter(Counter, OrderedDict):  #Counter that remembers the order elements are first encountered #yusuke メソッドの中にclassがあるのはイマイチなのでは。目的が分からないからいまいち断言できないが、もっとclassを使わずにシンプルにかけそうな雰囲気は感じる。

            def __repr__(self):
                return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

            def __reduce__(self):
                return self.__class__, (OrderedDict(self),)

        e_name = [ w for w,n in OrderedCounter(e_list).items() ]
        e_number = [ str(n) for w,n in OrderedCounter(e_list).items() ] #yusuke ここで同じ対象について二度ループするのはできるだけ避けて欲しい気はする
        sorted_list = [ l[1:] for l in sorted(line_list, key=lambda e: e_name.index(e[0])) ]
    return(e_name, e_number, sorted_list)

#yusuke ここの3つの変数は配列番号を指定しているのが少しイマイチかも。 e_name,e_number,sorted_list = get_sort_element(args[1])かな。それと使用するのはもっと下なので、もう少し使う所の近くで変数は宣言した方が読みやすい
e_name = get_sort_element(args[1])[0]
e_number = get_sort_element(args[1])[1]
sorted_list = get_sort_element(args[1])[2]

def get_lattice_length(POSCARfile):
    with open(POSCARfile,'r') as f_poscar:
        fr_pos = f_poscar.readlines()
        lattice_length = [ float(a.split()[i]) for i,a in enumerate(fr_pos[2:5]) ]
    return(lattice_length)

lattice_length = get_lattice_length(args[2]) #yusuke 俺はメソッドの宣言部分とそれ以外を分けたいので、上はmethod宣言だけにして変数を使うのは一番下にまとめるタイプ。

def get_direct(Cartesian_list,lattice_length):
    #yusuke ここのネストは浅くした方がよい
                directs = []
                for l in Cartesian_list:
                    direct = []
                    for i, a in enumerate(l):
                        xyz = float(a)/lattice_length[i]         #セルの長さでxyzファイルのそれぞれの値を割りDirect座標に変換
                        if xyz == -0.0:                          #出力ファイルのの表示をきれいに見せたいので-0.0は0.0に直す
                            xyz = 0.0
                        direct.append('%03.16f' % xyz)           #小数点の前は3桁まで、小数点以下は16桁まで0埋め
                    directs.append(direct)
                return(directs)

directs = get_direct(sorted_list, lattice_length)

with open('POSCAR_test2','w') as f2: #yusuke 変数名でマジックナンバーはできるだけ避けた方がデバッグがしやすいよ
    with open(args[2],'r') as f_poscar:
        fr_pos = f_poscar.readlines()
        for l in fr_pos[:5]:
            f2.write(l)          #copy 1~5
        names = "   "+"   ".join(e_name)+"\n"
        f2.write(names)
        numbers = "   "+"   ".join(e_number)+"\n"
        f2.write(numbers)
        f2.write('Selective dynamics'+'\n'+'Direct'+"\n")
        for direct in directs:
            f2.write("   "+"   ".join(direct)+"   T   T   T"+"\n")

#yusuke コマンドライン引数はそのままだとマジックナンバーを使用することになるので、スクリプトの初めに変数に入れるのがおすすめ。
