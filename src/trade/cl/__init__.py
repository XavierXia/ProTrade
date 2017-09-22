# -*- coding: utf-8 -*-

__auther__ = @"XavierXia"

'''
可量化的部分:
1. 乘法原则下的技术面,比价关系,基本面;(72)
2. 均线系统;(72)
3. 短线5日线,中线5周线,5月线长线;(72)
4. 形态学就足以形成一套有效的操作系统;(72)
   第二买卖点可以用形态学来判断
5. 量化路径:分型--笔--线段--最小级别中枢--各级别中枢,走势类型
6. 其他技术理论:K线理论,波浪理论

有疑问的部分:
1. 没有特征序列的定义,那么线段里都要继续存在类似小级别转大级别的情况.

名词部分:
分型 parting: 顶分型 Top_type(简称T) 底分型 Bottom_type(简称B) N值表示此刻走势不为分型形态
方向: direction: 向上 up, 向下 down
走势形态: shape: 中继 relay 0  转折 turn 1
笔 stroke
线段 segment
中枢 maincenter
走势类型 trend_type
级别 level

例子数据:
1. data = pd.DataFrame(randn(7,4),index=pd.date_range('1/1/2017',periods=7),columns=list('ABCD'))
'''