/*test*/
/*test*/
/*prueba*/
/*prueba*/

SELECT * FROM tabla160;
SELECT * FROM tabla170;
SELECT * FROM tabla180;
SELECT * FROM tabla190;
SELECT * FROM tabla201;


{{ config(
    materialized='table',
    schema='marts'
) }}

WITH business_totals AS (
    SELECT
        b.business_group,
        COUNT(DISTINCT f.member_id) as total_members,
        COUNT(DISTINCT CASE WHEN f.category = 'Maternity Add-On' THEN f.member_id END) as maternity_members
    FROM {{ ref('fct_healthplan_amendments') }} f /*tabla 1*/
    JOIN {{ ref('dim_businesses') }} b ON b.id = f.business_id /*tabla 2*/
    WHERE
        f.is_active = true
    GROUP BY
        b.business_group
)

SELECT
    business_group,
    total_members,
    maternity_members,
    ROUND((maternity_members * 100.0 / NULLIF(total_members, 0)), 2) as maternity_coverage_percentage
FROM business_totals
