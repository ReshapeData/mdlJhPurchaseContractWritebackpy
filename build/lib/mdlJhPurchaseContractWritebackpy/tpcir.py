#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyrda.dbms.rds import RdClient
def sql_update(token):
    '''
    采购合同反写
    :param token: ERP数据库token
    :return:
    '''

    app3 = RdClient(token=token)

    sql="""
    --采购合同-应付单-付款申请单-付款单 F_fk_amount
    --采购合同-付款申请单-付款单 F_fk_amount
    update x set x.F_fk_amount=y.FPAYAMOUNTFOR 
    from T_PUR_CONTRACT x 
    inner join(
    select 
    sum(FPAYAMOUNTFOR) as FPAYAMOUNTFOR,
    FBILLNO 
    from rds_vw_fkamount_result 
    group by FBILLNO) y
    on y.FBILLNO=x.FBillNO
    
    --采购合同-应付单-付款申请单-付款单 付款单号 F_fk_no
    --采购合同-付款申请单-付款单  付款单号 fk_no F_fk_no
    
    update x set x.F_fk_no=y.FBILLNO_YF from T_PUR_CONTRACT x
    inner join (
    SELECT
        a.FBILLNO,
        FBILLNO_YF = (STUFF((SELECT ',' + FBILLNO_YF FROM rds_vw_fkno_result WHERE FBILLNO = a.FBILLNO FOR xml path('')),1,1,''))
    FROM rds_vw_fkno_result a
    GROUP by a.FBILLNO) y
    on x.FBILLNO=y.FBILLNO
    
    
    --采购合同-付款申请单-付款单  最新付款日期  F_fk_date
    --采购合同-应付单-付款申请单-付款单 最新付款日期 F_fk_date
    
    update up set up.F_fk_date=up2.FDATE from T_PUR_CONTRACT up
    inner join (
    select x.FBILLNO,y.FDATE from T_PUR_CONTRACT x
    inner join (
    select a.FBillNO,a.FDate from 
    (select ROW_NUMBER() over(partition by FBillNO order by FDate desc) as t,FBillNO,FDATE
    from rds_vw_fkdate_result ) a
    where a.t=1
    ) y
    on x.FBILLNO=y.FBILLNO) up2
    on up.FBILLNO=up2.FBILLNO
    
    
    
    --采购合同-应付单 不含税金额 fp_money F_fp_money、税额（发票号逗号隔开）fp_taxmoney F_fp_taxmoney 价税合计 fp_amount F_fp_amount
    update x set x.F_fp_amount=y.FALLAMOUNT,x.F_fp_taxmoney=y.FTAXAMOUNT,x.F_fp_money=y.FNOTAXAMOUNT from T_PUR_CONTRACT x
    inner join  (
    select sum(b.FALLAMOUNT) as FALLAMOUNT,sum(b.FTAXAMOUNT) as FTAXAMOUNT,sum(b.FNOTAXAMOUNT) as FNOTAXAMOUNT,b.FSOURCEBILLNO,b.FSOURCETYPE from T_AP_PAYABLE a
    inner join T_AP_PAYABLEENTRY b
    on a.FID=b.FID
    inner join T_AP_PAYABLEFIN c
    on c.FID=a.FID
    group by b.FSOURCEBILLNO,b.FSOURCETYPE,a.FDOCUMENTSTATUS
    having b.FSOURCETYPE='PUR_Contract'and a.FDOCUMENTSTATUS='C') y
    on x.FBILLNO=y.FSOURCEBILLNO
    
    --采购合同-应付单 发票
    
    update x set x.F_fp_no=y.F_KD_TEXT01 from T_PUR_CONTRACT x
    inner join
    (SELECT
        a.FBILLNO,
        F_KD_TEXT01 = (STUFF((SELECT ',' + F_KD_TEXT01 FROM rds_result_fp WHERE FBILLNO = a.FBILLNO FOR xml path('')),1,1,''))
    FROM rds_result_fp a
    GROUP by a.FBILLNO) y
    on x.FBILLNO=y.FBILLNO
    
    
    --fk_proportion F_fk_proportion  累计付款占比
    update z set z.F_fk_proportion=res.proportion from T_PUR_CONTRACT z
    inner join(
    select a.FBillNO,(b.FPAYAMOUNTFOR/a.FALLAMOUNT)*100 as proportion from rds_pur_contract_amount a
    inner join rds_vw_proportion_result b
    on a.FBillNO=b.FBillNO) res
    on res.FBillNO=z.FBillNO
    """

    app3.update(sql)

    return True