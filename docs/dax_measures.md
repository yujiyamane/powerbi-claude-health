# DAX Measures - NSW Health KPI Dashboard

このドキュメントは、NSW Healthヘルスケア KPIダッシュボードで使用されるDAXメジャーの定義と説明を記載します。

## Core KPI Measures

### 1. 病床稼働率 (Bed Occupancy Rate)

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

**用途**: 病床リソースの使用効率を測定
**目標値**: 80-90% (NSW Health標準)

### 2. 平均在院日数 (Average Length of Stay - ALOS)

```dax
ALOS = 
AVERAGE(fact_admissions[los_hours]) / 24

ALOS (Days) = 
DIVIDE(
    SUM(fact_admissions[los_hours]),
    COUNT(fact_admissions[admission_id])
) / 24
```

**用途**: 治療効率と患者回転率の指標
**ベンチマーク**: 
- Emergency Department: < 0.5日
- Medical Ward: 3-5日
- Surgical Ward: 2-4日

### 3. ED待ち時間中央値 (ED Wait Time Median)

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

**用途**: 救急医療サービスの即応性評価
**目標**: < 240分 (4時間ルール)

### 4. 4時間ルール達成率 (4-Hour Rule Compliance)

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

**用途**: NSW Health 4時間ルール政策の達成度
**目標値**: ≥ 90%

### 5. 1入院当たりコスト (Cost per Admission)

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

**用途**: 医療サービスのコスト効率性評価

### 6. トリアージ別パフォーマンス

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

### 月別比較 (Month-over-Month)

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

### 年度累計 (Year-to-Date)

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

### 移動平均 (Moving Averages)

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

### 病床稼働率警告

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

### LHD (Local Health District) ランキング

```dax
LHD Rank by Performance = 
RANKX(
    ALL(dim_ward[lhd]),
    [4-Hour Rule Compliance],
    ,
    DESC
)
```

### 週末効果分析

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
    4  // Low utilisation
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

## 使用ガイド

### メジャー適用順序
1. **ベースメジャー**（Total Admissions, Total Cost等）を先に作成
2. **比率・平均系**メジャーを作成
3. **Time Intelligence**メジャーを追加
4. **Advanced Analytics**メジャーで拡張

### パフォーマンス最適化
- フィルタコンテキストを活用してメジャーを軽量化
- SUMMARIZE関数で大きなテーブルの集約を効率化
- VAR文でサブクエリを再利用

### テストケース
- 各メジャーに対して期待値との比較テスト実施
- DAX Studioでクエリプラン分析
- 大量データでのパフォーマンステスト実行