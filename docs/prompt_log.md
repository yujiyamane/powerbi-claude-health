# Prompt Engineering Log - NSW Health BI Dashboard

このファイルは、Claude Codeを使用してNSW Health KPIダッシュボードを構築した際の実際のプロンプトと応答を記録します。

---

## Session 1: プロジェクト初期化と要件定義
**Time**: 2026-05-12 09:00 - 09:30 (30分)

### Prompt 1.1: プロジェクト概要説明
```
NSW Healthのヘルスケア KPI ダッシュボードを構築したい。以下の要件：

- 10病院、5つのLocal Health District
- 病床稼働率、平均在院日数、ED待ち時間、4時間ルール達成率が必要
- 2年分のデータ（FY2024-25, FY2025-26）
- 約20万件の入院レコード
- Star schema設計でパフォーマンス重視

オーストラリアの医療業界標準に準拠したダッシュボードを作りたい。データ生成からPower BI実装まで、一気通貫で進めて。
```

**Claude Response Summary**:
- NSW Health業務理解確認
- AIHW (Australian Institute of Health and Welfare) 標準KPI準拠
- Star schema設計提案
- データ生成戦略立案
- 4ページダッシュボード構成提案

### Prompt 1.2: データモデル詳細化
```
Star schemaの設計を詳細化して。特に：

1. Fact table (fact_admissions) の粒度
2. Date dimensionでfinancial year handling
3. Patient dimension でindigenous statusとpostcode distribution
4. Ward dimension でbed capacityとLHD hierarchy

オーストラリアの人口統計と地理的分布を反映したリアルなダミーデータ生成方法も教えて。
```

**Claude Response Summary**:
- Fact table grain: 入院単位（admission-level）
- Date dimension: Financial year July-June対応
- Patient distribution: NSW population demographics反映
- Ward hierarchy: Hospital → LHD → NSW State structure
- Realistic data patterns: Seasonal variations, demographics分布

---

## Session 2: データ生成と検証
**Time**: 2026-05-12 09:30 - 10:00 (30分)

### Prompt 2.1: Python data generator作成
```
generate_data.pyを作成して。要件：

- faker + pandasでオーストラリアっぽいデータ
- Seasonal patterns（冬のflu season等）
- Triage category distribution現実的に
- ED wait time 4-hour ruleを意識した分布
- Length of stay ward typeによって変動
- Cost calculationもrealistic

実行したら即座にPower BIで使えるCSVが出力されるようにして。
```

**Claude Response Summary**:
- 完全なPython script生成（faker + numpy + pandas）
- NSW-specific patterns実装
- Seasonal multipliers適用
- Triage-based LOS distribution
- Cost modeling based on complexity
- 4つのCSVファイル出力（fact + 3 dimensions）

### Prompt 2.2: データ品質検証
```
生成されたデータの品質をチェックして。以下を確認：

- Date rangeとfinancial year alignment
- Referential integrity (FK relationships)
- Business rule compliance (4-hour rule distribution等)
- Outlier detection
- Missing value handling

Power BIでの読み込み前にdata qualityを保証したい。
```

**Claude Response Summary**:
- Data validation script提供
- Integrity check logic
- Business rule validation
- Outlier analysis and handling
- CSV format optimization for Power BI

---

## Session 3: DAX開発とパフォーマンス最適化
**Time**: 2026-05-12 10:00 - 11:00 (1時間)

### Prompt 3.1: Core KPI measures作成
```
Power BI用のDAX measureを作成して。必要なKPI：

1. Bed Occupancy Rate = patient days / available bed days
2. ALOS (Average Length of Stay) = total hours / admissions
3. ED Wait Time Median
4. 4-Hour Rule Compliance % (ED wait ≤ 240 min)
5. Cost per Admission
6. Time intelligence variants for all above

Performance最適化とbest practiceを適用して。DIVIDE関数でzero division対策も忘れずに。
```

**Claude Response Summary**:
- Performance-optimized DAX measures
- Proper DIVIDE usage for error handling
- Time intelligence patterns
- Variable usage for readability
- Filter context optimization

### Prompt 3.2: Advanced analytics measures
```
追加のDAX measureも作って：

- 病床稼働率アラート (>90% = red, >80% = amber)
- LHDランキング (4-hour rule performanceベース)
- Weekend vs weekday admission ratio
- Triage severity distribution
- Moving averages (7-day, 30-day)

Visual conditional formattingにも使えるようにして。
```

**Claude Response Summary**:
- Conditional formatting measures
- Ranking functions (RANKX)
- Time-based analysis measures
- Alert logic implementation
- Color-coding for dashboard visuals

---

## Session 4: ダッシュボード設計とUX最適化
**Time**: 2026-05-12 11:00 - 13:00 (2時間)

### Prompt 4.1: Dashboard layout設計
```
4ページのダッシュボード構成を設計して：

Page 1: Executive Summary (高レベル overview)
Page 2: ED Performance (救急部門詳細)
Page 3: Ward & Bed Management (病棟管理)
Page 4: Cost Analysis (コスト分析)

各ページのvisual配置、color palette、filtering strategyを定義して。NSW Health brandingも考慮して。
```

**Claude Response Summary**:
- Page-specific visual layouts
- NHS blue color palette adaptation for NSW
- Filter strategy per user persona
- Mobile-responsive considerations
- Navigation and user journey design

### Prompt 4.2: Performance tuning
```
Large dataset (200K records) でのPower BI performance最適化方法：

1. Model optimization (relationships, cardinality)
2. DAX query optimization
3. Visual-level performance
4. Import vs DirectQuery considerations
5. Incremental refresh設定

Production environmentでも fast responseを保証したい。
```

**Claude Response Summary**:
- Model relationship optimization
- DAX performance best practices
- Visual selection criteria
- Memory usage optimization
- Incremental refresh configuration

---

## Session 5: テストとドキュメント化
**Time**: 2026-05-12 13:00 - 13:30 (30分)

### Prompt 5.1: Testing strategy
```
ダッシュボードのcomprehensive testingを実行して：

1. Data accuracy validation
2. Performance benchmarking
3. User acceptance criteria check
4. Cross-browser/device compatibility
5. Accessibility compliance

Test planとresultsをドキュメント化して。
```

**Claude Response Summary**:
- Systematic testing approach
- Performance benchmarks
- UAT criteria and results
- Accessibility checklist
- Test documentation template

### Prompt 5.2: Documentation作成
```
以下のドキュメントを作成して：

1. User guide (end-user向け)
2. Technical documentation (IT admin向け)
3. DAX measures reference
4. Deployment guide
5. Troubleshooting guide

Production supportに必要な情報を網羅して。
```

**Claude Response Summary**:
- Comprehensive documentation suite
- User training materials
- Technical reference guides
- Deployment procedures
- Support and maintenance guides

---

## 効果的だったプロンプト戦略

### ✅ 成功パターン

#### 1. Context-Rich Prompts
```
良い例: "NSW Health の業務理解を前提に、AIHW標準準拠の..."
悪い例: "ヘルスケアダッシュボードを作って"
```

#### 2. 具体的な制約条件
```
良い例: "200K records, 4-hour rule, financial year July-June"
悪い例: "大量データで高パフォーマンス"
```

#### 3. 段階的詳細化
```
1st prompt: Overview and requirements
2nd prompt: Technical specifications
3rd prompt: Implementation details
```

#### 4. 品質基準明示
```
"Production-ready", "Industry compliance", "Performance-optimized"
```

### ❌ 避けるべきパターン

#### 1. 曖昧な要件
```
❌ "いい感じのダッシュボード"
✅ "Executive summary page with 4 KPI cards and trend analysis"
```

#### 2. 一度に全てを要求
```
❌ "データ生成からデプロイまで全部"
✅ Session分割で段階的実行
```

#### 3. ドメイン知識を前提としない
```
❌ "4-hour rule"だけ
✅ "ED 4-hour rule (NEAT target 90%+)"
```

---

## 学習したプロンプト最適化

### Before vs After

#### データ生成要求
**Before**:
```
ダミーデータを作成して
```

**After**:
```
NSW Health業務に特化したダミーデータ生成。要件：
- オーストラリア人口統計反映
- Seasonal health patterns適用
- Triage distribution現実的に
- 4-hour rule compliance varied by hospital
- Financial year structure (July-June)
実行一発でPower BI ready CSVs出力
```

#### DAX開発要求
**Before**:
```
KPIのDAXを作って
```

**After**:
```
Performance-optimized DAX measures作成：
1. NSW Health標準KPI準拠
2. DIVIDE関数でエラー処理
3. Time intelligence patterns適用
4. Variable活用で可読性確保
5. Filter context最適化
Production環境200K recordsでfast response保証
```

### 次プロジェクト用改善点

1. **Domain expertise前提表明**: "オーストラリア医療業界の専門知識適用"
2. **Quality gate明確化**: "Production-ready", "Enterprise-grade"
3. **段階的validation**: 各フェーズでoutput品質確認
4. **Performance baseline設定**: 具体的数値目標提示
5. **Compliance requirement**: 法規制・業界標準への準拠要求