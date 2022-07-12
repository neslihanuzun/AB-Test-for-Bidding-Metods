import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#!pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_excel("ab_testing.xlsx")
df.describe().T

df.head()

ab_testing_file = "ab_testing.xlsx"
control_group_df = pd.read_excel((r"C:\Users\lenovo\Desktop\vbo-ml\hafta4\ÖDEVLER\ab_testing\ab_testing.xlsx"), sheet_name="Control Group", keep_default_na=True)
test_group_df = pd.read_excel((r"C:\Users\lenovo\Desktop\vbo-ml\hafta4\ÖDEVLER\ab_testing\ab_testing.xlsx"), sheet_name="Test Group", keep_default_na=True)

control_group_df.describe().T

#              count         mean         std         min         25%  \
#Impression 40.00000 101711.44907 20302.15786 45475.94296 85726.69035
#Click      40.00000   5100.65737  1329.98550  2189.75316  4124.30413
#Purchase   40.00000    550.89406   134.10820   267.02894   470.09553
#Earning    40.00000   1908.56830   302.91778  1253.98952  1685.84720
#                   50%          75%          max
#Impression 99790.70108 115212.81654 147539.33633
#Click       5001.22060   5923.80360   7959.12507

test_group_df.describe().T
#              count         mean         std         min          25%  \
#Impression 40.00000 120512.41176 18807.44871 79033.83492 112691.97077
#Click      40.00000   3967.54976   923.09507  1836.62986   3376.81902
#Purchase   40.00000    582.10610   161.15251   311.62952    444.62683
#Earning    40.00000   2514.89073   282.73085  1939.61124   2280.53743
#                    50%          75%          max
#Impression 119291.30077 132050.57893 158605.92048
#Click        3931.35980   4660.49791   6019.69508
#Purchase      551.35573    699.86236    889.91046
#Earning      2544.66611   2761.54540   3171.48971

control_and_test = pd.concat([control_group_df, test_group_df], axis=1)

#2

#Hipotezin Tanımlanması
# H0 : M1 = M2 Kontrol ve Test verisi arasında istatistiksel olarak anlamlı bir farklılık yoktur.
# H1 : M1!= M2 Kontrol ve Test verisi arasında istatistiksel olarak anlamlı bir farklılık vardır.

control_and_test.head()
control_and_test.columns = ["c_Impression", "c_Click", "c_Purchase", "c_Earning", "t_Impression", "t_Click", "t_Purchase", "t_Earning"]

control_and_test["c_Purchase"].mean()
#Out[45]: 550.8940587702316

control_and_test["t_Purchase"].mean()
#Out[46]: 582.1060966484675

# Normallik Varsayımı

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(control_and_test["c_Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 0.9773, p-value = 0.5891 , Normal dağılım varsayımı sağlanmaktadır.

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


test_stat, pvalue = shapiro(control_and_test["t_Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 0.9589, p-value = 0.1541 Normal dağılım varsayımı sağlanmaktadır.

# Varyans Homojenligi Varsayımı

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene((control_and_test["c_Purchase"]), (control_and_test["t_Purchase"]))
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 2.6393, p-value = 0.1083 , Varyanslar Homojendir

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = ttest_ind((control_and_test["c_Purchase"]), (control_and_test["t_Purchase"]),
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = -0.9416, p-value = 0.3493, H0 : M1 = M2 Kontrol ve Test verisi arasında istatistiksel olarak anlamlı bir farklılık yoktur.

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ. h0=h1



#bağımsız iki örneklem t testi (parametrik test) kullandım. Sebebi varyans homojenliği ve normallik varsayımı koşullarının sağlanmasıdır.
#Kontrol ve test grupları arasında %95 güven aralığı içerisinde ve %5 hata payı ile istatistiksel olarak anlamlı bir farklılık yoktur.
#Oratalamada oluşan farklılıklar tesadüfidir.
#Maximum Bidding ve Average Bidding yöntemlerinden en düşük maliyetli olan yöntemin kullanılması önerilmektedir.