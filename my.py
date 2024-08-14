import matplotlib.pyplot as plt

length = [10,100,1000,10000,50000,100000,150000,200000]
time_taken = [0.000000,0.000001,0.00005,0.00155,1.00569,3.0090,4.8989,7.5678]

plt.figure(figsize=(10,6))
plt.plot(length,time_taken,marker='o',linestyle='-',color='b')
plt.xlabel('Array length')
plt.ylabel('Excecution time in seconds')
plt.grid(True)
plt.show()
