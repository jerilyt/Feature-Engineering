```{r}
library('smbinning')  #最优分箱
library('DMwR')  #检测离群值
library('xlsx')  

####################################################################################
df<-read.csv(readFilePath)
head(df)
names(df)

#smbinning(df, y, x, p = 0.05)
#df: 数据
#y： 二分类变量(0,1) 整型
#x：连续变量：至少满足10 个不同值，取值范围有限
#p：每个Bin记录数占比，默认5% (0.05) 范围0%-50%
#smbinning.plot, smbinning.sql,and smbinning.gen.

result1<-smbinning(df=df,x="acc_open_past_24mths",y="y",p=0.05)
smbinning.plot(result1,option="WoE",sub="acc_open_past_24mths")
r1 <- merge(result1$x,result1$ivtable)

result2<-smbinning(df=df,x="inq_last_12m",y="y",p=0.05)
smbinning.plot(result2,option="WoE",sub="inq_last_12m")
r2 <- merge(result2$x,result2$ivtable)

result3<-smbinning(df=df,x="bc_open_to_buy",y="y",p=0.05)
smbinning.plot(result3,option="WoE",sub="bc_open_to_buy")
r3 <- merge(result3$x,result3$ivtable)

result4<-smbinning(df=df,x="mths_since_rcnt_il",y="y",p=0.05)
smbinning.plot(result4,option="WoE",sub="mths_since_rcnt_il")
r4 <- merge(result4$x,result4$ivtable)

r_total <- rbind(r1,r2,r3,r4)
outFilePath <- "F:/TS/Lending_Club/04_output/03_r_smbining/r_best_binging.xlsx"
write.xlsx(r_total, outFilePath)  

####################################################################################
# Information Value for all variables in one step ---------------------------
smbinning.sumiv(df=df,y="y") # IV for eache variable

# Plot IV for all variables -------------------------------------------------
sumivt=smbinning.sumiv(df,y="y")
sumivt # Display table with IV by characteristic
par(mfrow=c(1,1))
smbinning.sumiv.plot(sumivt,cex=1) # Plot IV summary table
####################################################################################
```
