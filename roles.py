# -*- coding: utf-8 -*-
import math
import random

#父类定义，定义了女武神共有的一些属性如下：
#命名比较随意，见谅
class role(object):
    #血量
    blood = 100
    #攻击力
    power = 0
    #防御力
    shield = 0
    #速度值 由极快-->一般-->极慢为 5-->3-->1
    speed = 0
    #姓名
    name0 = ''
    #沉默状态标识
    silent = False
    #攻击封禁状态标识
    block = False

    #构造函数
    def __init__(self, power, shield, speed, name0):
        self.power = power
        self.shield = shield
        self.speed = speed
        self.name0 = name0

    #基本的攻击和受击函数
    #攻击函数有一个参数，标明攻击的对象，，返回伤害值
    def attack(self, role):
        role.onAttack(self, self.power-role.shield)
        return self.power-role.shield
    #     #print('attacking!')

    #受击函数有三个参数，分别是攻击者，物理伤害值，元素伤害值(可缺省，缺省值为0)
    #受击函数返回自身受击后的血量
    def onAttack(self, role, dam, fire=0):
        self.blood = self.blood-dam-fire
        return self.blood
    #     #print('attacked')

#希儿子类
class xiEr(role):
    #属性初始化，charge是必杀技的计数器
    def __init__(self, num):
        super().__init__(23, 10, 5, '希儿')
        self.charge = 0

    def attack(self, role):
        #每次进攻，回合数加1，立即触发被动技能，
        # 随后判断当前是否被沉默，是否被封禁
        self.charge += 1
        #被动回血
        self.blood+=7
        if self.blood>100:
            self.blood=100
        #print('希儿回血+7')

        #状态判断
        if self.block:
            self.block = False
            return '0，行动被封锁'
            #如果被沉默，调用父类的攻击函数，即只进行普通攻击
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'

        dam0 = self.power-role.shield
        #每4个回合触发必杀技
        if self.charge % 4 == 0:
            dam0 = (100-role.shield)
            if random.randint(1,10000)>2500:
                dam0=0

        #计算好伤害值后，调用对方的onAttack函数进行伤害的结算，并便于触发对方的某些技能
        role.onAttack(self, dam0)
        if dam0:
            return dam0
        else:
            return '0,Miss!'

#丽塔子类
class liTa(role):
    #属性初始化
    def __init__(self, num):
        super().__init__(26, 8, 3, '丽塔')

    def attack(self, role):
        #没有被动技能，直接进行状态判断
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'
        
        dam0=role.blood-role.onAttack(self, self.power-role.shield)
        #回血技能
        if random.randint(1,10000)<=3000:
            self.blood+=dam0
            if self.blood>100:
                self.blood=100
            #print('丽塔回血+',dam0)
        #封禁对方攻击的技能
        if random.randint(1,10000)>8000:
            role.block=True
            #print('丽塔使用了岩石封')
        return self.power-role.shield

#罗莎莉亚子类
class rosalia(role):
    #属性初始化，charge为必杀技计数器，special为罗莎莉亚的特殊攻击倍率
    def __init__(self, num):
        super().__init__(30, 4, 4, '萝莎莉娅')
        self.charge = 0
        self.special = 1.0

    def attack(self, role):
        #计数器增加
        self.charge += 1
        #先进行伤害值的计算但并不进行攻击，因为倍率special接下来会发生变化
        #普通攻击伤害计算
        dam0 = (self.power-role.shield)*self.special
        #必杀技伤害计算
        if self.charge % 3 == 0:
            dam0 = (15-role.shield)*(self.special*10)
        #判断下回合的攻击倍率
        self.special = 1.0
        temp = random.randint(1, 10000)
        if temp <= 3000:
            self.special = 1.5
        if temp > 7000:
            self.special = 0.5

        #判定状态
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'

        #进行攻击，每三个回合自己的必杀技将对自己进行封锁
        if self.charge % 3 == 0:
            self.block = True
        role.onAttack(self, int(dam0))

        return int(dam0)

#姬子子类
class jiZi(role):
    #charge是必杀技蓄力完成的指示器，defence表示姬子阿姐血量低于40的防御状态
    def __init__(self, num):
        super().__init__(24, 10, 1, '姬子')
        self.charge = False
        self.defence = False

    def attack(self, role):
        #状态判定
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'
        
        #必杀技，两倍攻击力的元素伤害
        if self.charge == True:
            role.onAttack(self, 0, self.power*2)
            self.charge = False
            return self.power*2
        #必杀技的蓄力判定
        if (random.randint(1, 10000) < 3000):
            self.charge = True
            return 0
        #普通的攻击
        role.onAttack(self, self.power-role.shield)
        return self.power-role.shield

    def onAttack(self, role, dam, fire=0):
        self.blood = self.blood-dam-fire
        #血量低于40时进入防御状态，官方的战斗里攻击力加成似乎没有触发
        if self.blood < 40 and self.defence == False:
            self.defence = True
            self.power = self.power*1.5
            self.shield = self.shield*1.5
        return self.blood

#符华子类
class fuHua(role):
    #charge是上仙的必杀技计数器
    #defence表示进入锁血状态
    def __init__(self, num):
        super().__init__(27, 8, 5, '符华')
        self.charge = 0
        self.defence = False

    def attack(self, role):
        #计数器+1，状态判定
        self.charge += 1
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'

        #每3个回合触发必杀技，随机10-30元素伤害
        if self.charge % 3 == 0:
            temp = random.randint(10, 30)
            role.onAttack(self, 0, temp)
            return temp
        #普通攻击
        role.onAttack(self, self.power-role.shield)
        return self.power-role.shield

    def onAttack(self, role, dam, fire=0):
        #锁血状态下免疫元素伤害
        if self.defence:
            self.blood = self.blood-dam
            return self.blood
        #普通的受击判定
        self.blood = self.blood-dam-fire
        #受到致命伤害时开始锁血
        if self.blood < 1 and self.defence == False:
            self.defence = True
            self.blood = 1
        return self.blood


#卡莲子类
class kaLian(role):
    #defence表示卡莲的减伤状态剩余几个回合
    def __init__(self, num):
        super().__init__(26, 6, 5, '卡莲')
        self.defence = 0

    def attack(self, role):
        #如果处于减伤状态，每过一回合denfence-1，当其为0时，将对方的攻击力归还
        if self.defence:
            self.defence-=1
            if self.defence==0:
                role.power+=15

        #状态判定
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'
        #5%可能直接胜利
        if random.randint(1, 10000) <= 500:
            role.blood = 0
            return
        #30%概率触发技能，对方攻击力减15
        if random.randint(1, 10000) <= 3000:
            self.defence = 2
            role.power-=15
        role.onAttack(self, self.power-role.shield)
        return self.power-role.shield


#琪亚娜子类
class qiYaNa(role):
    #琪亚娜被动血量为120，charge为必杀技计数器
    def __init__(self, num):
        super().__init__(23, 11, 2, '琪亚娜')
        self.blood = 120
        self.charge = 0

    def attack(self, role):
        #回合数增加，状态判定
        self.charge += 1
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return super().attack(role)
        #正常攻击
        dam0 = self.power-role.shield
        #每三回合触发必杀攻击
        if (self.charge % 3 == 0):
            dam0 = (12-role.shield)*8
        role.onAttack(self, dam0)
        return dam0

#芽衣姐姐的子类
class yaYi(role):
    def __init__(self, num):
        super().__init__(26, 6, 3, '芽衣')

    def attack(self, role):
        #状态判定
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return str(super().attack(self, role))+',沉默'

        #一般状态下附加5点元素伤害
        dam0 = self.power-role.shield
        fire0 = 5
        #触发必杀技时，附加20点元素伤害，将对方沉默
        if random.randint(0, 10000) < 3000:
            fire0 = 20
            role.silent = True
        role.onAttack(self, dam0, fire0)
        return dam0+fire0

#魔法少女的子类
class teriri(role):
    #charge是必杀技计数器
    def __init__(self, num):
        super().__init__(24, 8, 2, '德丽莎')
        self.charge = 1

    def attack(self, role):
        #计数器增加，状态判定
        self.charge += 1
        if self.block:
            self.block = False
            return '0，行动被封锁'
        if self.silent:
            self.silent = False
            return super().attack(role)

        #普通攻击伤害计算
        dam0 = self.power-role.shield
        fire0 = 0
        #每两个回合触发必杀技，造成4次随机的元素伤害
        if self.charge % 2 == 0:
            a = random.randint(1, 16)
            b = random.randint(1, 16)
            c = random.randint(1, 16)
            d = random.randint(1, 16)
            #print('随机数序列',a,b,c,d)
            fire0 = a+b+c+d
            role.onAttack(self, 0, fire0)
            return fire0
        role.onAttack(self, dam0, fire0)
        return dam0+fire0

    def onAttack(self, role, dam, fire=0):
        self.blood = self.blood-dam-int(0.5*fire)
        return self.blood
