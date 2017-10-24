use parking;

SELECT * FROM parking.mke_violations;

SELECT COUNT(Officer_Name) FROM parking.mke_violations;

SELECT OFFICER_DISTRICT,COUNT(*) as count FROM mke_violations GROUP BY OFFICER_DISTRICT ORDER BY count DESC;
SELECT VIODESCRIPTION,COUNT(*) as count FROM mke_violations GROUP BY VIODESCRIPTION ORDER BY count DESC;

select OFFICER_DISTRICT, 
CASE 
	WHEN OFFICER_DISTRICT < 200 THEN 'DISTRICTS'
	ELSE 'POSSIBLE ERRORS' 
END AS district_list, 
count(OFFICER_DISTRICT)  
FROM mke_violations 
group by district_list;

/*Create a randomized partition so that we don't have to query the whole dataset 
when we're just trying to refine our queries

count how many districts fall under district list

millions of night parking violations. 
Check the ticketing times
*/