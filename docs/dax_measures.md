# DAX Measures - NSW Health KPI Dashboard

This document provides definitions and explanations for DAX measures used in the NSW Health KPI Dashboard.

## Core KPI Measures

### 1. Bed Occupancy Rate

```dax
Bed Occupancy Rate = 
DIVIDE(
    [Total Patient Days],
    [Available Bed Days],
    0
)

Total Patient Days = 
SUMX(
    fact_admissions,
    fact_admissions[los_hours] / 24
)

Available Bed Days = 
SUMX(
    CROSSJOIN(
        VALUES(dim_date[full_date]),
        VALUES(dim_ward[ward_id])
    ),
    RELATED(dim_ward[bed_capacity])
)
```

**Purpose**: Measure bed resource utilization efficiency
**Target**: 80-90% (NSW Health standard)

### 2. Average Length of Stay (ALOS)

```dax
ALOS = 
AVERAGE(fact_admissions[los_hours]) / 24

ALOS (Days) = 
DIVIDE(
    SUM(fact_admissions[los_hours]),
    COUNT(fact_admissions[admission_id])
) / 24
```

**Purpose**: Treatment efficiency and patient turnover indicator
**Benchmarks**: 
- Emergency Department: < 0.5 days
- Medical Ward: 3-5 days
- Surgical Ward: 2-4 days

### 3. ED Wait Time Median

```dax
ED Wait Time Median = 
VAR EDWaitTimes = 
    FILTER(
        fact_admissions,
        fact_admissions[ed_wait_minutes] > 0
    )
RETURN
    MEDIAN(EDWaitTimes[ed_wait_minutes])

ED Wait Time (Hours) = 
    [ED Wait Time Median] / 60
```

**Purpose**: Emergency medical service responsiveness assessment
**Target**: < 240 minutes (4-hour rule)

### 4. 4-Hour Rule Compliance

```dax
4-Hour Rule Compliance = 
VAR EDAdmissions = 
    FILTER(
        fact_admissions,
        fact_admissions[ed_wait_minutes] > 0
    )
VAR ComplianceAdmissions = 
    FILTER(
        EDAdmissions,
        fact_admissions[ed_wait_minutes] <= 240
    )
RETURN
    DIVIDE(
        COUNTROWS(ComplianceAdmissions),
        COUNTROWS(EDAdmissions),
        0
    )

4-Hour Rule Compliance % = 
    [4-Hour Rule Compliance] * 100
```

**Purpose**: NSW Health 4-hour rule policy achievement
**Target**: ≥ 90%

### 5. Cost per Admission

```dax
Cost per Admission = 
DIVIDE(
    SUM(fact_admissions[cost]),
    COUNT(fact_admissions[admission_id]),
    0
)

Total Cost = 
SUM(fact_admissions[cost])

Total Admissions = 
COUNT(fact_admissions[admission_id])
```

**Purpose**: Healthcare service cost efficiency evaluation

### 6. Triage Performance

```dax
Triage 1-2 Admissions = 
CALCULATE(
    COUNT(fact_admissions[admission_id]),
    fact_admissions[triage_category] IN {1, 2}
)

Critical Cases % = 
DIVIDE(
    [Triage 1-2 Admissions],
    [Total Admissions],
    0
) * 100
```

## Time Intelligence Measures

### Month-over-Month Comparison

```dax
Previous Month ALOS = 
CALCULATE(
    [ALOS],
    DATEADD(dim_date[full_date], -1, MONTH)
)

ALOS MoM Change = 
[ALOS] - [Previous Month ALOS]

ALOS MoM Change % = 
DIVIDE(
    [ALOS MoM Change],
    [Previous Month ALOS],
    0
) * 100
```

### Year-to-Date

```dax
YTD Total Admissions = 
CALCULATE(
    [Total Admissions],
    DATESYTD(dim_date[full_date], "6/30")  // Financial year ends June 30
)

YTD Average ALOS = 
CALCULATE(
    [ALOS],
    DATESYTD(dim_date[full_date], "6/30")
)
```

### Moving Averages

```dax
7-Day Moving Avg Admissions = 
CALCULATE(
    AVERAGE(fact_admissions[daily_admissions]),
    DATESINPERIOD(
        dim_date[full_date],
        LASTDATE(dim_date[full_date]),
        -7,
        DAY
    )
)
```

## Advanced Analytics Measures

### Bed Occupancy Alert

```dax
Occupancy Alert = 
IF(
    [Bed Occupancy Rate] > 0.9,
    "🔴 Over Capacity",
    IF(
        [Bed Occupancy Rate] > 0.8,
        "🟡 High Occupancy",
        "🟢 Normal"
    )
)
```

### LHD (Local Health District) Ranking

```dax
LHD Rank by Performance = 
RANKX(
    ALL(dim_ward[lhd]),
    [4-Hour Rule Compliance],
    ,
    DESC
)
```

### Weekend Effect Analysis

```dax
Weekend Admissions = 
CALCULATE(
    [Total Admissions],
    dim_date[is_weekend] = TRUE
)

Weekend vs Weekday Ratio = 
DIVIDE(
    [Weekend Admissions] / 2,  // 2 days weekend
    ([Total Admissions] - [Weekend Admissions]) / 5,  // 5 days weekday
    0
)
```

## Conditional Formatting Measures

### KPI Status Indicators

```dax
Bed Occupancy Status = 
SWITCH(
    TRUE(),
    [Bed Occupancy Rate] >= 0.95, 1,  // Critical
    [Bed Occupancy Rate] >= 0.85, 2,  // Warning  
    [Bed Occupancy Rate] >= 0.70, 3,  // Good
    4  // Low utilization
)

ED Performance Status = 
IF(
    [4-Hour Rule Compliance] >= 0.9, 3,  // Target achieved
    IF(
        [4-Hour Rule Compliance] >= 0.8, 2,  // Below target
        1  // Critical
    )
)
```

## Implementation Guide

### Measure Application Order
1. **Base measures** (Total Admissions, Total Cost, etc.) first
2. **Ratio and average measures** second
3. **Time Intelligence** measures third
4. **Advanced Analytics** measures last

### Performance Optimization
- Leverage filter context to optimize measure performance
- Use SUMMARIZE function for efficient aggregation of large tables
- Reuse subqueries with VAR statements

### Testing Approach
- Implement expected value comparison tests for each measure
- Analyze query plans using DAX Studio
- Execute performance testing with large datasets