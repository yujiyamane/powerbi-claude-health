# Prompt Engineering Log - Statewide Health BI Dashboard

This file records the actual prompts and responses when using Claude Code to build the Statewide Health KPI Dashboard.

---

## Session 1: Project Initialization and Requirements Definition
**Time**: 2026-05-12 09:00 - 09:30 (30 minutes)

### Prompt 1.1: Project Overview Description
```
I want to build a healthcare KPI dashboard for Statewide Health with the following requirements:

- 10 hospitals across 5 Local Health Districts
- Need bed occupancy rate, average length of stay, ED wait time, 4-hour rule compliance
- 2 years of data (FY2024-25, FY2025-26)
- Approximately 200,000 admission records
- Star schema design with performance focus

I want to create a dashboard that complies with Australian healthcare industry standards. Please proceed end-to-end from data generation to Power BI implementation.
```

**Claude Response Summary**:
- Statewide Health business understanding confirmation
- AIHW (Australian Institute of Health and Welfare) standard KPI compliance
- Star schema design proposal
- Data generation strategy planning
- 4-page dashboard configuration proposal

### Prompt 1.2: Data Model Detailed Design
```
Please detail the Star schema design, specifically:

1. Fact table (fact_admissions) granularity
2. Date dimension financial year handling
3. Patient dimension indigenous status and postcode distribution
4. Ward dimension bed capacity and LHD hierarchy

Also provide realistic dummy data generation methods that reflect Australian demographics and geographic distribution.
```

**Claude Response Summary**:
- Fact table grain: admission-level
- Date dimension: Financial year July-June support
- Patient distribution: NSW population demographics reflection
- Ward hierarchy: Hospital → LHD → NSW State structure
- Realistic data patterns: Seasonal variations, demographics distribution

---

## Session 2: Data Generation and Validation
**Time**: 2026-05-12 09:30 - 10:00 (30 minutes)

### Prompt 2.1: Python Data Generator Creation
```
Create generate_data.py with the following requirements:

- Australian-like data using faker + pandas
- Seasonal patterns (winter flu season, etc.)
- Realistic triage category distribution
- ED wait time distribution considering 4-hour rule
- Length of stay variation by ward type
- Realistic cost calculation

Execute to immediately output CSVs ready for Power BI import.
```

**Claude Response Summary**:
- Complete Python script generation (faker + numpy + pandas)
- NSW-specific pattern implementation
- Seasonal multiplier application
- Triage-based LOS distribution
- Cost modeling based on complexity
- 4 CSV file output (fact + 3 dimensions)

### Prompt 2.2: Data Quality Validation
```
Check the quality of generated data. Verify the following:

- Date range and financial year alignment
- Referential integrity (FK relationships)
- Business rule compliance (4-hour rule distribution, etc.)
- Outlier detection
- Missing value handling

I want to ensure data quality before loading into Power BI.
```

**Claude Response Summary**:
- Data validation script provision
- Integrity check logic
- Business rule validation
- Outlier analysis and handling
- CSV format optimization for Power BI

---

## Session 3: DAX Development and Performance Optimization
**Time**: 2026-05-12 10:00 - 11:00 (1 hour)

### Prompt 3.1: Core KPI Measures Creation
```
Create DAX measures for Power BI with the required KPIs:

1. Bed Occupancy Rate = patient days / available bed days
2. ALOS (Average Length of Stay) = total hours / admissions
3. ED Wait Time Median
4. 4-Hour Rule Compliance % (ED wait ≤ 240 min)
5. Cost per Admission
6. Time intelligence variants for all above

Apply performance optimization and best practices. Don't forget zero division protection with DIVIDE function.
```

**Claude Response Summary**:
- Performance-optimized DAX measures
- Proper DIVIDE usage for error handling
- Time intelligence patterns
- Variable usage for readability
- Filter context optimization

### Prompt 3.2: Advanced Analytics Measures
```
Create additional DAX measures:

- Bed occupancy alerts (>90% = red, >80% = amber)
- LHD ranking (based on 4-hour rule performance)
- Weekend vs weekday admission ratio
- Triage severity distribution
- Moving averages (7-day, 30-day)

Make them usable for visual conditional formatting.
```

**Claude Response Summary**:
- Conditional formatting measures
- Ranking functions (RANKX)
- Time-based analysis measures
- Alert logic implementation
- Color-coding for dashboard visuals

---

## Session 4: Dashboard Design and UX Optimization
**Time**: 2026-05-12 11:00 - 13:00 (2 hours)

### Prompt 4.1: Dashboard Layout Design
```
Design a 4-page dashboard configuration:

Page 1: Executive Summary (high-level overview)
Page 2: ED Performance (emergency department details)
Page 3: Ward & Bed Management (ward management)
Page 4: Cost Analysis (cost analysis)

Define visual placement, color palette, and filtering strategy for each page. Consider Statewide Health branding.
```

**Claude Response Summary**:
- Page-specific visual layouts
- NHS blue color palette adaptation for NSW
- Filter strategy per user persona
- Mobile-responsive considerations
- Navigation and user journey design

### Prompt 4.2: Performance Tuning
```
Power BI performance optimization methods for large dataset (200K records):

1. Model optimization (relationships, cardinality)
2. DAX query optimization
3. Visual-level performance
4. Import vs DirectQuery considerations
5. Incremental refresh settings

I want to ensure fast response in production environment.
```

**Claude Response Summary**:
- Model relationship optimization
- DAX performance best practices
- Visual selection criteria
- Memory usage optimization
- Incremental refresh configuration

---

## Session 5: Testing and Documentation
**Time**: 2026-05-12 13:00 - 13:30 (30 minutes)

### Prompt 5.1: Testing Strategy
```
Execute comprehensive dashboard testing:

1. Data accuracy validation
2. Performance benchmarking
3. User acceptance criteria check
4. Cross-browser/device compatibility
5. Accessibility compliance

Document the test plan and results.
```

**Claude Response Summary**:
- Systematic testing approach
- Performance benchmarks
- UAT criteria and results
- Accessibility checklist
- Test documentation template

### Prompt 5.2: Documentation Creation
```
Create the following documentation:

1. User guide (for end-users)
2. Technical documentation (for IT admin)
3. DAX measures reference
4. Deployment guide
5. Troubleshooting guide

Cover all information necessary for production support.
```

**Claude Response Summary**:
- Comprehensive documentation suite
- User training materials
- Technical reference guides
- Deployment procedures
- Support and maintenance guides

---

## Effective Prompt Strategies

### ✅ Success Patterns

#### 1. Context-Rich Prompts
```
Good: "Based on Statewide Health business understanding, design AIHW standard-compliant..."
Bad: "Create a healthcare dashboard"
```

#### 2. Specific Constraints
```
Good: "200K records, 4-hour rule, financial year July-June"
Bad: "Large data with high performance"
```

#### 3. Progressive Refinement
```
1st prompt: Overview and requirements
2nd prompt: Technical specifications
3rd prompt: Implementation details
```

#### 4. Quality Standards Specification
```
"Production-ready", "Industry compliance", "Performance-optimized"
```

### ❌ Patterns to Avoid

#### 1. Vague Requirements
```
❌ "Nice dashboard"
✅ "Executive summary page with 4 KPI cards and trend analysis"
```

#### 2. Everything at Once
```
❌ "Everything from data generation to deployment"
✅ Progressive execution by session division
```

#### 3. No Domain Knowledge Context
```
❌ "4-hour rule" only
✅ "ED 4-hour rule (NEAT target 90%+)"
```

---

## Learned Prompt Optimization

### Before vs After

#### Data Generation Request
**Before**:
```
Create dummy data
```

**After**:
```
Generate Statewide Health business-specific dummy data. Requirements:
- Reflect Australian population statistics
- Apply seasonal health patterns
- Realistic triage distribution
- 4-hour rule compliance varied by hospital
- Financial year structure (July-June)
Execute once for Power BI ready CSV output
```

#### DAX Development Request
**Before**:
```
Create DAX for KPIs
```

**After**:
```
Create performance-optimized DAX measures:
1. Statewide Health standard KPI compliance
2. Error handling with DIVIDE function
3. Time intelligence pattern application
4. Variable usage for readability
5. Filter context optimization
Ensure fast response in production environment with 200K records
```

### Improvements for Next Project

1. **Domain Expertise Declaration**: "Apply Australian healthcare industry expertise"
2. **Quality Gate Clarification**: "Production-ready", "Enterprise-grade"
3. **Progressive Validation**: Output quality confirmation at each phase
4. **Performance Baseline Setting**: Present specific numerical targets
5. **Compliance Requirements**: Regulatory and industry standard compliance requirements