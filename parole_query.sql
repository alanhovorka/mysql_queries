show databases;
create database parole;
show databases;
use parole;
show tables;

create table parole_1201_data (
	doc_number varchar(256), name varchar(256), 
	event_date varchar(256), event_type varchar(256), 
    hearing_type varchar(256), final_action varchar(256));

create table parole_1208_data (
	doc_number varchar(256), name varchar(256), 
	event_date date, event_type varchar(256), 
    hearing_type varchar(256), final_action varchar(256));

/*
create table parole_1201_to_join_data (
	doc_number varchar(256), name varchar(256), 
	event_date date, event_type varchar(256), hearing_type varchar(256), 
    final_action varchar(256), 
    reason_decision_1 varchar(2000), reason_decision_2 varchar(2000),
    reason_decision_3 varchar(2000), reason_decision_4 varchar(2000),
    reason_decision_5 varchar(2000));
*/
show tables;   
/*
drop table parole_1201_data; 
drop table parole_1201_to_join_data;
*/
LOAD DATA LOCAL INFILE 'C:\\Users\\ahovorka\\Downloads\\parole\\1201_data.csv'
	into table parole_1201_data 
    fields terminated by ',' 
    optionally enclosed by '"'
    lines TERMINATED BY '\r\n' 
    ignore 1 lines
    (doc_number, name, @event_date, event_type, hearing_type, final_action)
    set event_date = STR_TO_DATE(@event_date, '%m/%d/%Y');

LOAD DATA LOCAL INFILE 'C:\\Users\\ahovorka\\Downloads\\parole\\1208_data.csv'
	into table parole_1208_data
    fields terminated by ',' 
    optionally enclosed by '"'
    lines TERMINATED BY '\r\n' 
    ignore 1 lines
    (doc_number, name, @event_date, event_type, hearing_type, final_action)
    set event_date = STR_TO_DATE(@event_date, '%m/%d/%Y');
    
/*LOAD DATA LOCAL INFILE 'C:\\Users\\ahovorka\\Downloads\\parole\\1201_to_join_data_reasons_2011-2016.csv'
	into table parole_1201_to_join_data 
    fields terminated by ',' 
    optionally enclosed by '"'
    lines TERMINATED BY '\r\n' 
    ignore 1 lines
    (doc_number, name, @event_date, event_type, final_action, 
    hearing_type, reason_decision_1, 
    reason_decision_2, reason_decision_3, 
    reason_decision_4, reason_decision_5)
    set event_date = STR_TO_DATE(@event_date, '%m/%d/%Y');*/
show warnings;

alter table parole_1208_data change final_action 1208_final_action varchar(256);
alter table parole_1201_data change final_action 1201_final_action varchar(256);
alter table parole_1201_data change doc_number doc_number_1201 varchar(256);
alter table parole_1201_data change name name_1201 varchar(256);
alter table parole_1201_data change event_date event_date_1201 varchar(256);
alter table parole_1201_data change event_type event_type_1201 varchar(256);
alter table parole_1201_data change hearing_type hearing_type_1201 varchar(256);


SELECT COUNT(DISTINCT final_action) FROM parole.parole_1208_data;

SELECT COUNT(final_action) FROM parole.parole_1208_data;

/*List the different distinct values and their frequency*/
SELECT 1201_final_action,COUNT(*) as count FROM parole_1201_data GROUP BY 1201_final_action ORDER BY count DESC;
SELECT 1208_final_action,COUNT(*) as count FROM parole_1208_data GROUP BY 1208_final_action ORDER BY count DESC;

/*
1208 grant list
*/
SELECT CASE
  WHEN 1208_final_action = 'Parole Grant' THEN 'parole grants'
  WHEN 1208_final_action = 'Grant Parole' THEN 'parole grants'
  WHEN 1208_final_action = 'Parole Grant to TIS' THEN 'parole grants'
  WHEN 1208_final_action = 'Compassionate Release Parole G' THEN 'parole grants'
  ELSE 'other, non-grants'
END AS final_action_list, Count(doc_number)
FROM  parole_1208_data
group by final_action_list;

/*
1201 grant list
*/

SELECT CASE
  WHEN 1201_final_action = 'Parole Grant' THEN 'parole grants'
  WHEN 1201_final_action = 'Grant Parole' THEN 'parole grants'
  WHEN 1201_final_action = 'Parole Grant to TIS' THEN 'parole grants'
  WHEN 1201_final_action = 'Compassionate Release Parole G' THEN 'parole grants'
  ELSE 'other, non-grants'
END AS final_action_list, Count(doc_number)
FROM  parole_1201_data
group by final_action_list;

create table grant_list_1208 
select * from parole_1208_data where 1208_final_action = 'Parole Grant'
    union
select * from parole_1208_data where 1208_final_action = 'Grant Parole'
	union
select * from parole_1208_data where 1208_final_action = 'Parole Grant to TIS' 
	union
select * from parole_1208_data where 1208_final_action = 'Compassionate Release Parole G';
    
create table grant_list_1201 
select * from parole_1201_data where 1201_final_action = 'Parole Grant'
    union
select * from parole_1201_data where 1201_final_action = 'Grant Parole'
	union
select * from parole_1201_data where 1201_final_action = 'Parole Grant to TIS' 
	union
select * from parole_1201_data where 1201_final_action = 'Compassionate Release Parole G';
    
    
create table 1208_with_1201	select * 
	from parole_1201_data a left join grant_list_1208 b
    on a.doc_number_1201 = b.doc_number;   

create table 1208_with_1201	select * 
	from grant_list_1201 a left join grant_list_1208 b
    on a.doc_number_1201 = b.doc_number;

create table 1208_without_1201	select * 
	from grant_list_1208 a left join parole_1201_data  b
    on a.doc_number = b.doc_number_1201;   
    
drop table 1208_without_1201;




select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a left join parole_1201_data b
    on a.doc_number = b.doc_number_1201
    where a.1208_final_action like '%Parole Grant%'
    and a.event_date != b.event_date_1201; 
    
    /*count each unique DOC numbers in each dataset*/
    
    count distinct doc_number from parole_1208_data
    parole_1201_data 
    
    /*did anybody get parole recommended from the board that didn't eventually get it approved, 
    what exactly is in the 1208 and what is in the 1201
    Would someone's doc number change*/


