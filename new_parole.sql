show databases;
use parole;
show tables;

/*List the different distinct values and their frequency*/
SELECT 1201_final_action,COUNT(*) as count FROM parole_1201_data GROUP BY 1201_final_action ORDER BY count DESC;
SELECT 1208_final_action,COUNT(*) as count FROM parole_1208_data GROUP BY 1208_final_action ORDER BY count DESC;

SELECT name,COUNT(*) as count FROM parole_1208_data GROUP BY name ORDER BY count DESC;
SELECT name,COUNT(*) as count FROM parole_1208_data where 1208_final_action like '%Parole%' GROUP BY name ORDER BY count DESC;
SELECT name_1201,COUNT(*) as count FROM parole_1201_data GROUP BY name_1201 ORDER BY count DESC;
SELECT name_1201,COUNT(*) as count FROM parole_1201_data where 1201_final_action like '%Parole%' GROUP BY name_1201 ORDER BY count DESC;

/*Johnson received to parole grants*/
select * from parole_1201_data where name_1201 like 'JOHNSON, CHRISTOPHER';

/*Looking at actions taken by parole chair Returns 500 records with a number of parole grants*/
select * from parole_1208_data where event_type like 'Parole Chair Only Review Held';

SELECT doc_number,COUNT(*) as count FROM parole_1208_data GROUP BY doc_number ORDER BY count DESC;

select parole_1208_data from parole_1208_data where name = 'JOHNSON, MICHAEL';

/*
1208 grant list, summary stats
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
1201 grant list summary list
*/

SELECT CASE
  WHEN 1201_final_action = 'Parole Grant' THEN 'parole grants'
  WHEN 1201_final_action = 'Grant Parole' THEN 'parole grants'
  WHEN 1201_final_action = 'Parole Grant to TIS' THEN 'parole grants'
  WHEN 1201_final_action = 'Compassionate Release Parole G' THEN 'parole grants'
  ELSE 'other, non-grants'
END AS final_action_list, Count(doc_number_1201)
FROM  parole_1201_data
group by final_action_list;

/*Queries that select just the parole grant terms*/
select * from parole_1208_data where 1208_final_action = 'Parole Grant'
    union
select * from parole_1208_data where 1208_final_action = 'Grant Parole'
	union
select * from parole_1208_data where 1208_final_action = 'Parole Grant to TIS' 
	union
select * from parole_1208_data where 1208_final_action = 'Compassionate Release Parole G';

select * from parole_1201_data where 1201_final_action = 'Parole Grant'
    union
select * from parole_1201_data where 1201_final_action = 'Grant Parole'
	union
select * from parole_1201_data where 1201_final_action = 'Parole Grant to TIS' 
	union
select * from parole_1201_data where 1201_final_action = 'Compassionate Release Parole G';




select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a left join parole_1201_data b
    on a.doc_number = b.doc_number_1201
    where a.1208_final_action like '%Parole Grant%'
    and a.event_date != b.event_date_1201; 
    
    /*count each unique DOC numbers in each dataset*/
    
    count distinct doc_number from parole_1208_data
    parole_1201_data 
    
    /*Working hypothesis is that everyone that got it recommended got it approved
    Let's try to disprove that:
    list of parole grants in 1208 and then left join on 1201 data or maybe select all from 1201 where doc_ = 1208.doc
    
    Do prisoners get new DOC numbers after they're released?
    
    did anybody get parole recommended from the board that didn't eventually get it approved    
    
    what exactly is in the 1208 and what is in the 1201
    
    of those that have 1208 parole grant, who don't have 1201.    
    
    What do the 1208 and 1201 joins look like. Are the data essentially the same?
    
    Check to see if it's all within the same time period. 
    
    Who are the couple hundred in the 1201 that don't have a 1208?    

    We need to know which terms are relevant
    
    If someone comes out for one crime and goes back in for another, do they have new doc numbers?
   
   Select but without duplicates:
   
   Would someone's doc number change
   
   Ask Gina what these other actions are they non-grants? What does a release me?
   
   Would there be any action in the 1208 that would lead to no 1201?
   
   How soon would a 1201 be created?
   
   Something we noticed is that people who do get parole board recomendation get a 1201 xxxxxx
   Is it possible that they don't record a 1201 if they don't approve the board's decision? 
   Maybe we're looking for people that don't show up on the 1201 list when they have parole grant from 1208
   Could be rubber stamping going on or looking at the files before the hearing to predetermine who they'll parole*/

/*    list of parole grants in 1208 and then left join on 1201 data or maybe select all from 1201 where doc_ = 1208.doc
*/
select * where doc_number_1201 = 
	(select * from parole_1208_data where 1208_final_action = 'Parole Grant'
		union
	select * from parole_1208_data where 1208_final_action = 'Grant Parole'
		union
	select * from parole_1208_data where 1208_final_action = 'Parole Grant to TIS' 
		union
	select * from parole_1208_data where 1208_final_action = 'Compassionate Release Parole G');


/*Just a regular, unfiltered left join, try filtering out the deferments */

select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a left join parole_1201_data b
    on a.doc_number = b.doc_number_1201; 

/*right join instead*/

select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a right join parole_1201_data b
    on a.doc_number = b.doc_number_1201; 
    
/*Filtered for deferments (left and right joins), 
looks like a decision on if they got parole would happen the same day as their hearing*/
select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a left join parole_1201_data b
    on a.doc_number = b.doc_number_1201
	where a.1208_final_action not like '%Defer%'; 
    
select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a right join parole_1201_data b
    on a.doc_number = b.doc_number_1201
	where a.1208_final_action not like '%Defer%'; 

/*Filter for parole with right and left join*/    
select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a left join parole_1201_data b
    on a.doc_number = b.doc_number_1201
	where a.1208_final_action like '%Parole%';
    
select a.doc_number, a.name, a.1208_final_action, a.event_date, a.hearing_type, 
	b.doc_number_1201, b.name_1201, b.1201_final_action, b.event_date_1201, b.hearing_type_1201
	from parole_1208_data a right join parole_1201_data b
    on a.doc_number = b.doc_number_1201
	where a.event_date = b.event_date_1201;  