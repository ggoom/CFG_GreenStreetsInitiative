--the final table produced is called processed. The definition is below:

CREATE TABLE Public."processed" (
	Checked_In_Individuals__ID INTEGER,
	Home_Zip_Code VARCHAR,
	Work_Zip_Code VARCHAR,
	Carbon_Change Float,
	Carbon_Savings Float,
	Primary_Mode_Walk_Ride__Mode_id INTEGER,
	Secondary_Mode_Walk_Ride__Mode_id INTEGER,
	Primary_Mode_Normal__Mode_id INTEGER,
	Secondary_Mode_Normal__Mode_id INTEGER
);

--first step get personal information from checked_in_individuals
WITH
CHECKED_IN_INDIVIDUALS(
	Checked_In_Individuals__ID,
	Individual_home_zip_code,
	Individual_work_zip_code,
	Individual_carbon_change,
	Individual_carbon_savings
	
) AS (
	SELECT 
	id,
	substring(home_address from '\m(\d{5})\M'),
	substring(work_address from '\m(\d{5})\M'),	
	carbon_change,
	carbon_savings
	FROM survey_commuterSurvey
	WHERE survey_commuterSurvey.wr_day_month_id = 1 --we let month_id = 1
),

--get walk-ride day data from survey_leg
WALK_RIDE_DAY(
	Walk_Ride_Day__legID,
	Walk_Ride_Day__Duration,
	Walk_Ride_Day__Direction,
	Walk_Ride_Day__Day,
	Walk_Ride_Day__Checkin_id,
	Walk_Ride_Day__Mode_id
) AS (
	SELECT
	id,
	duration,
	direction,
	day,
	checkin_id,
	mode_id
	FROM survey_leg, CHECKED_IN_INDIVIDUALS
	WHERE survey_leg.checkin_id = Checked_In_Individuals__ID
	AND survey_leg.day = 'w'
	AND survey_leg.direction = 'tw'
),

--get normal day data from survey_leg
NORMAL_DAY(
	Normal_Day__legID,
	Normal_Day__Duration,
	Normal_Day__Direction,
	Normal_Day__Day,
	Normal_Day__Checkin_id,
	Normal_Day__Mode_id
) AS (
	SELECT
	id,
	duration,
	direction,
	day,
	checkin_id,
	mode_id
	FROM survey_leg, CHECKED_IN_INDIVIDUALS
	WHERE survey_leg.checkin_id = Checked_In_Individuals__ID
	AND survey_leg.day = 'n'
	AND survey_leg.direction = 'tw'
),

--multiply the duration by the correct speed to calculate the distance on walk-ride day
WALK_RIDE_DAY_DISTANCE(
	Walk_Ride_Day_Distance__Checkin_id,
	Walk_Ride_Day_Distance__Distance,
	Walk_Ride_Day_Distance__Mode_id
) AS (
	SELECT
	Walk_Ride_Day__Checkin_id,
	(Walk_Ride_Day__Duration * survey_mode.speed / 60),
	Walk_Ride_Day__Mode_id
	FROM WALK_RIDE_DAY, survey_mode
	WHERE survey_mode.id = Walk_Ride_Day__Mode_id
),

--multiply the duration by the correct speed to calculate the distance on normal day
NORMAL_DAY_DISTANCE(
	Normal_Day_Distance__Checkin_id,
	Normal_Day_Distance__Distance,
	Normal_Day_Distance__Mode_id
) AS (
	SELECT
	Normal_Day__Checkin_id,
	(Normal_Day__Duration * survey_mode.speed / 60),
	Normal_Day__Mode_id
	FROM NORMAL_DAY, survey_mode
	WHERE survey_mode.id = Normal_Day__Mode_id
),
--intermediate step to find the primary mode on walk-ride day
PRIMARY_MODE_WALK_RIDE_1(
	Primary_Mode_Walk_Ride__Checkin_id,	
	Primary_Mode_Walk_Ride__MAX
	
) AS (
	SELECT
	Walk_Ride_Day_Distance__Checkin_id,
	MAX(Walk_Ride_Day_Distance__Distance)
	FROM WALK_RIDE_DAY_DISTANCE
	GROUP BY Walk_Ride_Day_Distance__Checkin_id
),
--identify the primary mode on walk-ride day
PRIMARY_MODE_WALK_RIDE (
	Primary_Mode_Walk_Ride__Checkin_id,	
	Primary_Mode_Walk_Ride__Mode_id
) AS (
	SELECT
	Walk_Ride_Day_Distance__Checkin_id,
	Walk_Ride_Day_Distance__Mode_id
	FROM WALK_RIDE_DAY_DISTANCE, PRIMARY_MODE_WALK_RIDE_1
	WHERE WALK_RIDE_DAY_DISTANCE.Walk_Ride_Day_Distance__Distance = PRIMARY_MODE_WALK_RIDE_1.Primary_Mode_Walk_Ride__MAX	
	and WALK_RIDE_DAY_DISTANCE.Walk_Ride_Day_Distance__Checkin_id = PRIMARY_MODE_WALK_RIDE_1.Primary_Mode_Walk_Ride__Checkin_id
),

--intermediate step to find the secondary mode on walk-ride day
SECONDARY_MODE_WALK_RIDE_1(
	Secondary_Mode_Walk_Ride__Checkin_id,	
	Secondary_Mode_Walk_Ride__MAX
) AS (
	SELECT
	Walk_Ride_Day_Distance__Checkin_id,
	MAX(Walk_Ride_Day_Distance__Distance)
	Walk_Ride_Day_Distance__Mode_id
	FROM WALK_RIDE_DAY_DISTANCE
	WHERE Walk_Ride_Day_Distance__Distance < (SELECT MAX(Walk_Ride_Day_Distance__Distance) FROM WALK_RIDE_DAY_DISTANCE)
	GROUP BY Walk_Ride_Day_Distance__Checkin_id
),
--find the secondary mode on walk-ride day
SECONDARY_MODE_WALK_RIDE (
	Secondary_Mode_Walk_Ride__Checkin_id,	
	Secondary_Mode_Walk_Ride__Mode_id
) AS (
	SELECT
	Walk_Ride_Day_Distance__Checkin_id,
	Walk_Ride_Day_Distance__Mode_id
	FROM WALK_RIDE_DAY_DISTANCE, SECONDARY_MODE_WALK_RIDE_1
	WHERE WALK_RIDE_DAY_DISTANCE.Walk_Ride_Day_Distance__Distance = SECONDARY_MODE_WALK_RIDE_1.Secondary_Mode_Walk_Ride__MAX	
	and WALK_RIDE_DAY_DISTANCE.Walk_Ride_Day_Distance__Checkin_id = SECONDARY_MODE_WALK_RIDE_1.Secondary_Mode_Walk_Ride__Checkin_id
),

--intermediate step to find the primary mode on normal day
PRIMARY_MODE_NORMAL_1(
	Primary_Mode_Normal__Checkin_id,	
	Primary_Mode_Normal__MAX
) AS (
	SELECT
	Normal_Day_Distance__Checkin_id,
	MAX(Normal_Day_Distance__Distance)
	Normal_Day_Distance__Mode_id
	FROM NORMAL_DAY_DISTANCE
	GROUP BY Normal_Day_Distance__Checkin_id
),

--find the primary mode on normal day

PRIMARY_MODE_NORMAL (
	Primary_Mode_Normal__Checkin_id,	
	Primary_Mode_Normal__Mode_id
) AS (
	SELECT
	Normal_Day_Distance__Checkin_id,
	Normal_Day_Distance__Mode_id
	FROM NORMAL_DAY_DISTANCE, PRIMARY_MODE_NORMAL_1
	WHERE NORMAL_DAY_DISTANCE.Normal_Day_Distance__Distance = PRIMARY_MODE_NORMAL_1.Primary_Mode_Normal__MAX	
	and NORMAL_DAY_DISTANCE.Normal_Day_Distance__Checkin_id = PRIMARY_MODE_NORMAL_1.Primary_Mode_Normal__Checkin_id
),

--intermediate step to find the secondary mode on normal day

SECONDARY_MODE_NORMAL_1(
	Secondary_Mode_Normal__Checkin_id,	
	Secondary_Mode_Normal__MAX
) AS (
	SELECT
	Normal_Day_Distance__Checkin_id,
	MAX(Normal_Day_Distance__Distance)
	Normal_Day_Distance__Mode_id
	FROM NORMAL_DAY_DISTANCE
	WHERE Normal_Day_Distance__Distance < (SELECT MAX(Normal_Day_Distance__Distance) FROM NORMAL_DAY_DISTANCE)
	GROUP BY Normal_Day_Distance__Checkin_id
),

--find the secondary mode on normal day

SECONDARY_MODE_NORMAL (
	Secondary_Mode_Normal__Checkin_id,	
	Secondary_Mode_Normal__Mode_id
) AS (
	SELECT
	Normal_Day_Distance__Checkin_id,
	Normal_Day_Distance__Mode_id
	FROM NORMAL_DAY_DISTANCE, SECONDARY_MODE_NORMAL_1
	WHERE NORMAL_DAY_DISTANCE.Normal_Day_Distance__Distance = SECONDARY_MODE_NORMAL_1.Secondary_Mode_Normal__MAX	
	and NORMAL_DAY_DISTANCE.Normal_Day_Distance__Checkin_id = SECONDARY_MODE_NORMAL_1.Secondary_Mode_Normal__Checkin_id
)

--insert the result into our newly created table processed
INSERT INTO Public."processed"
(
Checked_In_Individuals__ID,
Home_Zip_Code,
Work_Zip_Code,
Carbon_change,
Carbon_savings,
Primary_Mode_Walk_Ride__Mode_id,
Secondary_Mode_Walk_Ride__Mode_id,
Primary_Mode_Normal__Mode_id,
Secondary_Mode_Normal__Mode_id
)

SELECT 
Checked_In_Individuals__ID,
Individual_home_zip_code,
Individual_work_zip_code,
Individual_carbon_change,
Individual_carbon_savings,
Primary_Mode_Walk_Ride__Mode_id,
Secondary_Mode_Walk_Ride__Mode_id,
Primary_Mode_Normal__Mode_id,
Secondary_Mode_Normal__Mode_id

FROM
CHECKED_IN_INDIVIDUALS,
PRIMARY_MODE_WALK_RIDE,
SECONDARY_MODE_WALK_RIDE,
PRIMARY_MODE_NORMAL,
SECONDARY_MODE_NORMAL

--To ensure ID matches across the board for each value
WHERE Checked_In_Individuals__ID = Primary_Mode_Walk_Ride__Checkin_id 
and Checked_In_Individuals__ID = Secondary_Mode_Walk_Ride__Checkin_id
and Checked_In_Individuals__ID = Primary_Mode_Normal__Checkin_id
and Checked_In_Individuals__ID = Secondary_Mode_Normal__Checkin_id;
