import matplotlib.pyplot as plt
from math import sqrt


def calc_LOF(x,h1,h2,distance):
    a=0
    if ( x>0):
        a=(float(h2)-float(h1))/(float(distance)-0)
    b=h1
    LOF=a*x+b
    return LOF

#def plot_fresnel(distance, freq):
    #index=list(range(0,(int(distance*100))))
    #step=[float(i)/100 for i in index]
    
    #data=[]
    #data2=[]
    #for n in range(1,5):
        #for x in step:
            #y_temp=calc_LOF(
            ##data.append(calc_fresnell_radius(n,freq,x,distance-x))
            ##data2.append(-calc_fresnell_radius(n,freq,x,distance-x))
        #plt.plot(step,data,"brown")
        #plt.plot(step,data2,"brown")
        #data=[]
        #data2=[]
    ##plt.plot([0,distance], [0,0])
   ## plt.plot(step,data,"brown",
     ##        step, data2)
    #plt.ylabel('Fresnell curves')
    #plt.show()


def plot_fresnel2(h1,h2,distance, freq):
    index=list(range(0,(int(distance*100))))
    step=[float(i)/100 for i in index]
    
    data=[]
    data2=[]
    for n in range(1,5):
        for x in step:
            y_temp=calc_LOF(x,h1,h2,distance)
            d1=sqrt((x-0)*(x-0)+(y_temp-h1)*(y_temp-h1))
            d2=sqrt((distance-x)*(distance-x)+(h2-y_temp)*(h2-y_temp))
            fresnel_radius=calc_fresnell_radius(n,freq,d1,d2)
            data.append(y_temp+fresnel_radius)
            data2.append(y_temp-fresnel_radius)
            #data.append(calc_fresnell_radius(n,freq,x,distance-x))
            #data2.append(-calc_fresnell_radius(n,freq,x,distance-x))
        plt.plot(step,data,"brown")
        plt.plot(step,data2,"brown")
        data=[]
        data2=[]
    plt.plot([0,distance], [0,0], "red")
    plt.ylabel('Fresnell curves')
    plt.show()


def plot_fresnel_check_needed_clearance(h1,h2,distance, freq,wall_x_pos):
    index=list(range(0,(int(distance*100))))
    step=[float(i)/100 for i in index]
    
    data=[]
    data2=[]
    max_height_wall=0;
    for n in range(1,5):
        for x in step:
            y_temp=calc_LOF(x,h1,h2,distance)
            d1=sqrt((x-0)*(x-0)+(y_temp-h1)*(y_temp-h1))
            d2=sqrt((distance-x)*(distance-x)+(h2-y_temp)*(h2-y_temp))
            fresnel_radius=calc_fresnell_radius(n,freq,d1,d2)
            data.append(y_temp+fresnel_radius)
            data2.append(y_temp-fresnel_radius)
            if x==wall_x_pos and n==1:
                max_height_wall=y_temp-(fresnel_radius*0.6)
                print "The maximum allowed height of the wall is: "
                print max_height_wall
            #data.append(calc_fresnell_radius(n,freq,x,distance-x))
            #data2.append(-calc_fresnell_radius(n,freq,x,distance-x))
        plt.plot(step,data,"brown")
        plt.plot(step,data2,"brown")
        data=[]
        data2=[]
    plt.plot([0,distance], [0,0], "red")
    
    plt.plot([wall_x_pos,wall_x_pos], [0,max_height_wall], "red")
    
    plt.ylabel('Fresnell curves')
    plt.show()

def calc_fresnell_radius(n,freq,d1,d2):
    lampda=300000000/freq
    return sqrt((n*lampda*(d1*d2))/(d1+d2))


#plot_fresnel2(0.5,50.0,400.0,2400000000.0)

plot_fresnel_check_needed_clearance(0.5,50.0,200.0,433000000.0,30.0)
