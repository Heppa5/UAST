
import matplotlib.pyplot as plt


from datetime import datetime

def read_get_time(filename):
    f=open(filename)
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split('\t')[4])
    f.close
    
    return result

def read_get_voltage(filename):
    f=open(filename)
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split('\t')[11])
    f.close
    
    return result

def calc_soc(voltage):
    a=(1-0)/(4.15-3.19)
    b=1-a*4.15
    SOC=a*voltage+b
    
    return SOC


voltage=read_get_voltage("log-2016-01-14.txt")

index=list(range(0,len(voltage)))
SOC=[(float(i)/4215) for i in index]


# Have chosen a simple linear equation to describe the relationship
print calc_soc(3.19)
print calc_soc(4.15)
print calc_soc(3.7)

plt.plot(voltage,list(reversed(SOC)),"o")
plt.plot([3.19,4.15], [0, 1], 'k-', lw=2)
plt.ylabel('SOC')
plt.xlabel('Voltage')
plt.show()

#time2=[datetime.strptime(x, '%hr%min%sec') for x in time]
#time2=[datetime.strptime(x, '%H%M%S.%f') for x in time]
#plt.plot(time2,voltage, "o")
#plt.plot(voltage,time2)
#plt.show()
