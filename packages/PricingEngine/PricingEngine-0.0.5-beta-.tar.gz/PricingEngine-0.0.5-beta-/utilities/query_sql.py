from utilities.constants import Constants


class QuerySql:
    sql_query = {
        Constants.SQL_APP_QUERY: """ select * from app_vehicle_information""",
        'sql_query': """select cfv.FileNum, cfv.Mileage, cfv.Color, cfv.AcquistionCost, cfa.AuctionSoldFor
                        as SalesPrice, cfa.AuctionDate as SoldOn, 
                        cfv.MMRAvgValue, av.Year, msmk.MakeName , msm.ModelName, mss.StyleName, msa.AddrZip
                        from cfgfileauction cfa
                        left join cfgfilevehicle cfv on cfv.FileNum = cfa.FileNum
                        left join appfile af on af.FileNum = cfa.FileNum
                        left join appvehicle av on av.VIN = af.CustRefNum
                        left join msmodel msm on msm.ModelId = av.ModelId
                        left join msmake msmk on msmk.MakeId = av.MakeId
                        left join msstyle mss on mss.StyleId = av.StyleId
                        left join cfgcustomerlocation ccl on ccl.clid = cfv.acquiredfromlocation
                        left join msaddress msa on msa.AddrId = ccl.AddrId
                        where cfa.AuctionStatus in (20,31,33,36,37,38,39,42)
                        and cfv.Mileage > 10000 and cfv.Mileage < 400000
                        and af.FileStatusId in (0,1,2)
                        and cfv.Mileage != cfv.AcquistionCost
                        and cfv.Color not like '%#%'
                        and cfv.MMRAvgValue is not null
                        and mss.StyleName != ''
                        and msa.AddrZip != ''
                        and cfv.AcquistionCost < 100000
                        UNION 
                        select cfv.FileNum,cfv.Mileage, cfv.Color, cfv.AcquistionCost, cfvrs.VehicleSoldFor as 
                        SalesPrice, cfvrs.VehicleSoldOn as SoldOn, 
                        cfv.MMRAvgValue, av.Year, msmk.MakeName , msm.ModelName, mss.StyleName, msa.AddrZip from 
                        cfgfilevehicleretailsale cfvrs
                        left join cfgfilevehicle cfv on cfv.fvID = cfvrs.fvID
                        left join appfile af on af.FileNum = cfv.FileNum
                        left join appvehicle av on av.VIN = af.CustRefNum
                        left join msmodel msm on msm.ModelId = av.ModelId
                        left join msmake msmk on msmk.MakeId = av.MakeId
                        left join msstyle mss on mss.StyleId = av.StyleId
                        left join cfgcustomerlocation ccl on ccl.clid = cfv.acquiredfromlocation
                        left join msaddress msa on msa.AddrId = ccl.AddrId
                        where af.FileStatusId in (0,1,2) 
                        and cfvrs.VehicleSoldFor > 300 and cfvrs.AuctionStatus = 31
                        and cfv.Mileage > 10000 and cfv.Mileage < 400000
                        and af.FileStatusId in (0,1,2)
                        and cfv.Mileage != cfv.AcquistionCost
                        and cfv.Color not like '%#%'
                        and cfv.MMRAvgValue is not null
                        and mss.StyleName != ''
                        and msa.AddrZip != ''
                        and cfv.AcquistionCost < 100000""",

        Constants.APP_HISTORY_QUERY: """insert into app_history(Platform, AlgoName, PredictedField, PredictedValue, MMRAvgValue,VIN, MakeName, ModelName, StyleName, Color, AddrZip, Mileage)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        Constants.APP_SUMMARY_QUERY: """insert into app_summary(Platform, Algorithms, Accuracy, CrossValidation, Remark) VALUES (%s, %s, %s, %s, %s)""",
        Constants.PREDICTION_RESULT_QUERY: """insert into prediction_result(Vehicle_ID, Framework, algorithm, Predicted_PARAM, Prediction_value) VALUES (%s,%s,%s,%s,%s)""",
    }
