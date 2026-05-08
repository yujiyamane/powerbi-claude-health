#!/usr/bin/env python3
"""
Statewide Health Healthcare KPI Dashboard - Dummy Data Generator

Generates realistic healthcare data following Australian health system patterns.
Creates CSV files for Power BI star schema: fact_admissions + dimension tables.

Target: 2 financial years (FY2024-25, FY2025-26), ~200k admission records
Structure: 10 hospitals across 5 LHDs, 40 wards total
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import os

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker('en_AU')
Faker.seed(42)

# Constants for Statewide Health system
NSW_LHDS = [
    'Sydney', 'South Eastern Sydney', 'South Western Sydney',
    'Western Sydney', 'Central Coast'
]

HOSPITALS = [
    ('Royal Prince Alfred Hospital', 'Sydney'),
    ('Liverpool Hospital', 'South Western Sydney'),
    ('Prince of Wales Hospital', 'South Eastern Sydney'),
    ('Westmead Hospital', 'Western Sydney'),
    ('Gosford Hospital', 'Central Coast'),
    ('St George Hospital', 'South Eastern Sydney'),
    ('Blacktown Hospital', 'Western Sydney'),
    ('Sutherland Hospital', 'South Eastern Sydney'),
    ('Campbelltown Hospital', 'South Western Sydney'),
    ('Royal North Shore Hospital', 'Sydney')
]

WARD_TYPES = [
    'Emergency Department', 'Intensive Care', 'Coronary Care', 'Medical Ward',
    'Surgical Ward', 'Orthopaedic Ward', 'Paediatric Ward', 'Maternity Ward'
]

TRIAGE_CATEGORIES = {
    1: 'Immediately Life-threatening',
    2: 'Imminently Life-threatening',
    3: 'Potentially Life-threatening',
    4: 'Potentially Serious',
    5: 'Less Urgent'
}

AGE_GROUPS = ['0-17', '18-34', '35-49', '50-64', '65-79', '80+']

def generate_dim_ward():
    """Generate ward dimension table."""
    wards = []
    ward_id = 1

    for hospital, lhd in HOSPITALS:
        # Each hospital has 4 wards (40 total across 10 hospitals)
        hospital_wards = random.sample(WARD_TYPES, 4)

        for ward_type in hospital_wards:
            bed_capacity = random.randint(20, 80) if ward_type != 'Intensive Care' else random.randint(8, 20)

            wards.append({
                'ward_id': ward_id,
                'ward_name': f"{ward_type} - {hospital[:15]}",
                'hospital': hospital,
                'lhd': lhd,
                'bed_capacity': bed_capacity
            })
            ward_id += 1

    return pd.DataFrame(wards)

def generate_dim_date():
    """Generate date dimension table for FY 2024-25 and 2025-26."""
    dates = []

    # FY starts July 1, ends June 30
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2026, 6, 30)

    current_date = start_date
    while current_date <= end_date:
        # Financial year calculation
        if current_date.month >= 7:
            fy = current_date.year + 1
        else:
            fy = current_date.year

        dates.append({
            'date_key': current_date.strftime('%Y%m%d'),
            'full_date': current_date,
            'year': current_date.year,
            'quarter': f"Q{(current_date.month-1)//3 + 1}",
            'month': current_date.month,
            'month_name': current_date.strftime('%B'),
            'week': current_date.isocalendar()[1],
            'day_of_week': current_date.strftime('%A'),
            'is_weekend': current_date.weekday() >= 5,
            'financial_year': f"FY{fy-1}-{str(fy)[-2:]}"
        })
        current_date += timedelta(days=1)

    return pd.DataFrame(dates)

def generate_dim_patient(num_patients=50000):
    """Generate patient dimension table."""
    patients = []

    # NSW postcodes by region for realistic distribution
    sydney_postcodes = range(2000, 2250)
    regional_postcodes = list(range(2250, 2260)) + list(range(2400, 2490)) + list(range(2800, 2900))

    for patient_id in range(1, num_patients + 1):
        # Age distribution based on NSW demographics
        age_group = np.random.choice(AGE_GROUPS, p=[0.18, 0.22, 0.18, 0.17, 0.15, 0.10])
        gender = np.random.choice(['Male', 'Female'], p=[0.49, 0.51])

        # Postcode based on population distribution
        if random.random() < 0.7:  # 70% in Greater Sydney
            postcode = random.choice(sydney_postcodes)
        else:
            postcode = random.choice(regional_postcodes)

        # Indigenous status based on NSW statistics (3.4%)
        indigenous_status = 'Yes' if random.random() < 0.034 else 'No'

        patients.append({
            'patient_id': patient_id,
            'age_group': age_group,
            'gender': gender,
            'postcode': postcode,
            'indigenous_status': indigenous_status
        })

    return pd.DataFrame(patients)

def generate_fact_admissions(dim_ward, dim_date, dim_patient, target_records=200000):
    """Generate admissions fact table."""
    admissions = []
    admission_id = 1

    # Get date range
    date_range = pd.to_datetime(dim_date['full_date'])
    min_date = date_range.min()
    max_date = date_range.max()

    # Seasonal patterns for admissions
    def get_seasonal_multiplier(date):
        month = date.month
        # Higher admissions in winter months (flu season)
        if month in [6, 7, 8]:  # Winter
            return 1.3
        elif month in [12, 1]:  # Holiday period - slightly higher
            return 1.1
        else:
            return 1.0

    # Generate admissions for each ward
    for _, ward in dim_ward.iterrows():
        # Calculate admissions per day based on ward type and capacity
        if 'Emergency' in ward['ward_name']:
            base_admissions_per_day = ward['bed_capacity'] * 0.8  # ED has high turnover
        elif 'Intensive Care' in ward['ward_name']:
            base_admissions_per_day = ward['bed_capacity'] * 0.3  # ICU has longer stays
        else:
            base_admissions_per_day = ward['bed_capacity'] * 0.5

        # Generate admissions across the date range
        current_date = min_date
        while current_date <= max_date and admission_id <= target_records:
            # Daily variation with seasonal adjustment
            seasonal_mult = get_seasonal_multiplier(current_date)
            daily_variation = np.random.normal(1.0, 0.2)
            daily_admissions = max(1, int(base_admissions_per_day * seasonal_mult * daily_variation))

            for _ in range(daily_admissions):
                if admission_id > target_records:
                    break

                admission_date = current_date + timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )

                # Triage category distribution
                if 'Emergency' in ward['ward_name']:
                    triage = np.random.choice([1,2,3,4,5], p=[0.02, 0.08, 0.25, 0.45, 0.20])
                else:
                    triage = np.random.choice([2,3,4], p=[0.1, 0.4, 0.5])  # Non-ED wards

                # Length of stay based on ward type and triage
                if 'Emergency' in ward['ward_name']:
                    if triage <= 2:
                        los_hours = max(1, np.random.exponential(8))  # 1-24 hours typically
                    else:
                        los_hours = max(0.5, np.random.exponential(4))  # 0.5-12 hours typically
                elif 'Intensive Care' in ward['ward_name']:
                    los_hours = max(24, np.random.exponential(120))  # 1-10 days typically
                else:
                    los_hours = max(12, np.random.exponential(72))   # 0.5-7 days typically

                discharge_date = admission_date + timedelta(hours=los_hours)

                # ED wait time (for emergency department only)
                if 'Emergency' in ward['ward_name']:
                    # 4-hour rule target - most under 240 minutes
                    if triage <= 2:
                        ed_wait = max(5, np.random.exponential(45))  # Urgent cases
                    else:
                        ed_wait = max(10, np.random.exponential(120))  # Less urgent
                else:
                    ed_wait = 0  # Non-ED wards

                # Cost based on complexity and LOS
                base_cost = {
                    'Emergency Department': 800,
                    'Intensive Care': 3500,
                    'Coronary Care': 2800,
                    'Surgical Ward': 2200,
                    'Medical Ward': 1500
                }.get(ward['ward_name'].split(' -')[0], 1800)

                cost = base_cost + (los_hours * 50) + random.randint(-200, 500)
                cost = max(100, cost)  # Minimum cost

                # Select random patient
                patient_id = random.choice(dim_patient['patient_id'])

                admissions.append({
                    'admission_id': admission_id,
                    'patient_id': patient_id,
                    'admission_date': admission_date,
                    'discharge_date': discharge_date,
                    'triage_category': triage,
                    'ward_id': ward['ward_id'],
                    'cost': round(cost, 2),
                    'los_hours': round(los_hours, 1),
                    'ed_wait_minutes': round(ed_wait, 0)
                })

                admission_id += 1

            current_date += timedelta(days=1)

    return pd.DataFrame(admissions)

def main():
    """Generate all CSV files for Power BI."""
    print("Statewide Health KPI Dashboard - Data Generation")
    print("=" * 50)

    # Generate dimension tables
    print("Generating dimension tables...")

    print("  * Ward dimension (40 wards across 10 hospitals)")
    dim_ward = generate_dim_ward()

    print("  * Date dimension (FY2024-25 to FY2025-26)")
    dim_date = generate_dim_date()

    print("  * Patient dimension (50,000 patients)")
    dim_patient = generate_dim_patient()

    # Generate fact table
    print("\nGenerating fact table...")
    print("  * Admissions fact (~200,000 records)")
    fact_admissions = generate_fact_admissions(dim_ward, dim_date, dim_patient)

    # Save to CSV
    print(f"\nSaving CSV files...")

    dim_ward.to_csv('dim_ward.csv', index=False)
    print(f"  [OK] dim_ward.csv ({len(dim_ward):,} rows)")

    dim_date.to_csv('dim_date.csv', index=False)
    print(f"  [OK] dim_date.csv ({len(dim_date):,} rows)")

    dim_patient.to_csv('dim_patient.csv', index=False)
    print(f"  [OK] dim_patient.csv ({len(dim_patient):,} rows)")

    fact_admissions.to_csv('fact_admissions.csv', index=False)
    print(f"  [OK] fact_admissions.csv ({len(fact_admissions):,} rows)")

    # Summary statistics
    print(f"\nData Summary:")
    print(f"  * Total admissions: {len(fact_admissions):,}")
    print(f"  * Date range: {fact_admissions['admission_date'].min()} to {fact_admissions['admission_date'].max()}")
    print(f"  * Average LOS: {fact_admissions['los_hours'].mean():.1f} hours")
    print(f"  * Average ED wait: {fact_admissions[fact_admissions['ed_wait_minutes'] > 0]['ed_wait_minutes'].mean():.0f} minutes")
    print(f"  * Average cost: ${fact_admissions['cost'].mean():,.0f}")

    print(f"\nData generation complete! Files saved in current directory")
    print("Ready to import into Power BI")

if __name__ == "__main__":
    main()