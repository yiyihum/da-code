import numpy as np
import pandas as pd
from sqlalchemy import create_engine
male={}
for i in range(0,7):
    x2='players'
    y2=16 + i
    male[y2] =pd.read_csv('../' + x2 + '_' + str(y2) + '.csv', low_memory=False)
female={}
for i in range(0,7):
    z2 = 'female'
    x2='players'
    y2=16 + i              
    female[y2] =pd.read_csv('../' + z2 + '_' +x2+'_'+str(y2) + '.csv', low_memory=False)
engine = create_engine('sqlite://', echo=False)

female[16].to_sql("female_fifa_16", con =engine) ##  fifa 16 dataset for female
female[17].to_sql("female_fifa_17", con =engine) ##  fifa 17 dataset for female
female[18].to_sql("female_fifa_18", con =engine) ##  fifa 18 dataset for female
female[19].to_sql("female_fifa_19", con =engine) ##  fifa 19 dataset for female
female[20].to_sql("female_fifa_20", con =engine) ##  fifa 20 dataset for female
female[21].to_sql("female_fifa_21", con =engine) ##  fifa 21 dataset for female
female[22].to_sql("female_fifa_22", con =engine) ##  fifa 22 dataset for female

male[16].to_sql("male_fifa_16", con =engine) ##  fifa 16 dataset for male
male[17].to_sql("male_fifa_17", con =engine) ##  fifa 17 dataset for male
male[18].to_sql("male_fifa_18", con =engine) ##  fifa 18 dataset for male
male[19].to_sql("male_fifa_19", con =engine) ##  fifa 19 dataset for male
male[20].to_sql("male_fifa_20", con =engine) ##  fifa 20 dataset for male
male[21].to_sql("male_fifa_21", con =engine) ##  fifa 21 dataset for male
male[22].to_sql("male_fifa_22", con =engine) ##  fifa 22 dataset for male

sql='''
with raw_data as (
Select *,'female' as gender,2016 as year from female_fifa_16
union 
Select *, 'male'as gender,2016 as year from male_fifa_16
union
Select *,'female' as gender,2017 as year from female_fifa_17
union 
Select *, 'male'as gender,2017 as year from male_fifa_17
union
Select *,'female' as gender,2018 as year from female_fifa_18
union 
Select *, 'male'as gender,2018 as year from male_fifa_18
union
Select *,'female' as gender,2019 as year from female_fifa_19
union 
Select *, 'male'as gender,2019 as year from male_fifa_19
union
Select *,'female' as gender,2020 as year from female_fifa_20
union 
Select *, 'male'as gender,2020 as year from male_fifa_20
union
Select *,'female' as gender,2021 as year from female_fifa_21
union 
Select *, 'male'as gender,2021 as year from male_fifa_21
union
Select *,'female' as gender,2022 as year from female_fifa_22
union 
Select *, 'male'as gender,2022 as year from male_fifa_22
),

player_full_position AS(
select *,
case  
when player_position like '%LCM%' then 'Left center midfield'
when player_position like '%CAM%' then 'Central Attacking Midfielder'
when player_position like '%CB%' then 'Centre-back'
when player_position like '%CDM%' then 'Central Defensive Midfielder'
when player_position like '%CF%' then 'Central Forward'
when player_position like '%CM%' then 'Central Midfielder'
when player_position like '%GK%' then 'Goal Keeper'
when player_position like '%LAM%' then 'Left Attacking Midfielder'
when player_position like '%LB%' then 'Full-back (Left-back)'
when player_position like '%LCB%' then 'Left Centre-back'
when player_position like '%LCM%' then 'Left Central Midfielder'
when player_position like '%LDM%' then 'Left Defensive Midfielder'
when player_position like '%LF%' then 'Left Forward'
when player_position like '%LM%' then 'Wide Midfielder(Left Midfielder)'
when player_position like '%LS%' then 'Long snapper'
when player_position like '%LW%' then 'Left Winger'
when player_position like '%LWB%' then 'Left wing back'
when player_position like '%RAM%' then 'Right Attacking Midfielder'
when player_position like '%RB%' then 'Full-back (Right-back)'
when player_position like '%RCB%' then 'Right Centre-back'
when player_position like '%RCM%' then 'Right Central Midfielder'
when player_position like '%RDM%' then 'Right Defensive Midfielder'
when player_position like '%RES%' then 'reserve team'
when player_position like '%RF%' then 'Right Forward'
when player_position like '%RM%' then 'Wide Midfielder(Right Midfielder)'
when player_position like '%RS%' then 'Right Safety'
when player_position like '%RW%' then 'Right Winger'
when player_position like '%RWB%' then 'Right Wing Back'
when player_position like '%ST%' then 'Striker'
when player_position like '%SUB%' then 'Substitute'
else 'None' 
end as player_position_full_form
from
(
select
sofifa_id,
case when nation_position is null then club_position else nation_position end as player_position
from raw_data
group by 1
)),
 
 
raw_data2 AS (
select r.sofifa_id AS Sofifa_id ,
r.short_name,
p.player_position,
p.player_position_full_form,
r.gender,
r.year,
r.pace,
r.shooting,
r.passing,
r.dribbling,
r.defending,
r.physic,
r.attacking_crossing,
r.attacking_finishing,
r.attacking_heading_accuracy,
r.attacking_short_passing,
r.attacking_volleys,
r.skill_dribbling,
r.skill_curve,
r.skill_fk_accuracy,
r.skill_long_passing,
r.skill_ball_control,
r.movement_acceleration,
r.movement_sprint_speed,
r.movement_agility,
r.movement_reactions,
r.movement_balance,
r.power_shot_power,
r.power_jumping,
r.power_stamina,
r.power_strength,
r.power_long_shots,
r.mentality_aggression,
r.mentality_interceptions,
r.mentality_positioning,
r.mentality_vision,
r.mentality_penalties,
r.mentality_composure,
r.defending_marking_awareness,
r.defending_standing_tackle,
r.defending_sliding_tackle,
r.goalkeeping_diving,
r.goalkeeping_handling,
r.goalkeeping_kicking,
r.goalkeeping_positioning,
r.goalkeeping_reflexes,
r.goalkeeping_speed
from raw_data r inner join player_full_position p
on r.sofifa_id = p.sofifa_id
),

raw_data3 AS (

select
sofifa_id,
short_name,
gender,
year,
player_position_full_form,
case 
when player_position_full_form like '%Goal Keeper%'
then (
nullif(goalkeeping_diving,0) +
nullif(goalkeeping_handling,0) +
nullif(goalkeeping_kicking,0) +
nullif(goalkeeping_positioning,0) +
nullif(goalkeeping_reflexes,0) +
nullif(goalkeeping_speed,0)
)

when player_position_full_form like '%Defensive%'
then (
nullif(defending,0) +
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) +
nullif(defending_sliding_tackle,0) 
)

when player_position_full_form like '%Midfield%' and player_position_full_form not like '%Defensive%'
then (
nullif(movement_acceleration,0) +
nullif(movement_sprint_speed,0) +
nullif(movement_agility,0) +
nullif(movement_reactions,0) +
nullif(movement_balance,0) + 
nullif(shooting,0) +
nullif(passing,0) +
nullif(dribbling,0)

)

when player_position_full_form like '%Striker%'
then (
nullif(pace,0) +
nullif(shooting,0) +
nullif(passing,0) +
nullif(dribbling,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_stamina,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)

)

when player_position_full_form like '%Foward%'
then (
nullif(pace,0) +
nullif(shooting,0) +
nullif(passing,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)

)

when player_position_full_form like '%Winger%'
then (
nullif(pace,0) +
nullif(dribbling,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_stamina,0)+
nullif(power_strength,0)

)

when player_position_full_form like '%Snapper%'
then (
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)
)

when upper(player_position_full_form) like '%BACK%'
then (
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) +
nullif(defending_sliding_tackle,0) 
)

when player_position_full_form like '%Safety%'
then (
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) 
)

when player_position_full_form like '%Substitute%' or player_position_full_form like '%reserve team%'
then (
 60*7
)

else 0 end as role_level_score,

case 
when player_position_full_form like '%Goal Keeper%'
then ((
nullif(goalkeeping_diving,0) +
nullif(goalkeeping_handling,0) +
nullif(goalkeeping_kicking,0) +
nullif(goalkeeping_positioning,0) +
nullif(goalkeeping_reflexes,0) +
nullif(goalkeeping_speed,0)
)/600)*100

when player_position_full_form like '%Defensive%'
then ((
nullif(defending,0) +
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) +
nullif(defending_sliding_tackle,0) 
)/400)*100

when player_position_full_form like '%Midfield%' and player_position_full_form not like '%Defensive%'
then ((
nullif(movement_acceleration,0) +
nullif(movement_sprint_speed,0) +
nullif(movement_agility,0) +
nullif(movement_reactions,0) +
nullif(movement_balance,0) + 
nullif(shooting,0) +
nullif(passing,0) +
nullif(dribbling,0)

)/800)*100

when player_position_full_form like '%Striker%'
then ((
nullif(pace,0) +
nullif(shooting,0) +
nullif(passing,0) +
nullif(dribbling,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_stamina,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)

)/1200)*100

when player_position_full_form like '%Foward%'
then ((
nullif(pace,0) +
nullif(shooting,0) +
nullif(passing,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)

)/1000)*100

when player_position_full_form like '%Winger%'
then ((
nullif(pace,0) +
nullif(dribbling,0) +
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_stamina,0)+
nullif(power_strength,0)

)/800)*100

when player_position_full_form like '%Snapper%'
then ((
nullif(attacking_finishing,0) +
nullif(attacking_heading_accuracy,0) +
nullif(attacking_short_passing,0) +
nullif(attacking_volleys,0)+
nullif(power_jumping,0)+
nullif(power_strength,0)+
nullif(power_long_shots,0)
)/700)*100

when upper(player_position_full_form) like '%BACK%'
then ((
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) +
nullif(defending_sliding_tackle,0) 
)/300)*100

when player_position_full_form like '%Safety%'
then ((
nullif(defending_marking_awareness,0) +
nullif(defending_standing_tackle,0) 
)/200)*100

when player_position_full_form like '%Substitute%' or player_position_full_form like '%reserve team%'
then (
 60*7
)
else 0 end AS role_level_percentage
from raw_data2
where player_position_full_form != 'Substitute'
group by 1,2,3,4)


select *
from raw_data3
''';

    
df_sql = pd.read_sql_query(sql,con=engine)
df_sql.iloc[:20, :].to_csv('./result.csv', index=False)