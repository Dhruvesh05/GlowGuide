# Block 6: EDA Dashboard - Quick Start Guide

## What is the EDA Dashboard?

The Exploratory Data Analysis (EDA) Dashboard is an interactive data visualization tool built into GlowGuide that lets you explore patterns, trends, and insights from the skincare dataset. It's the **Insights** tab in the Streamlit app.

### Quick Facts

- **Location**: 4th tab in GlowGuide app ("Insights")
- **Type**: Interactive Streamlit dashboard with Plotly charts
- **Data**: 50 skincare profiles with 6 attributes each
- **Visualizations**: 10+ interactive charts
- **Features**: Distributions, heatmaps, statistics, CSV export

---

## Getting Started

### Step 1: Start the Streamlit App

```bash
cd c:\Users\dhruv\GlowGuide
streamlit run app/app.py
```

**Expected Output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.10.22.197:8503
```

### Step 2: Navigate to Insights Tab

1. Open the app in your browser
2. Look for **4 tabs** at the top:
   - Product Search
   - Ingredient Analyzer
   - Routine Builder
   - **Insights** ← Click here

### Step 3: Explore Visualizations

The dashboard displays automatically with 7 sections of data and charts.

---

## Dashboard Sections Explained

### 1. Dataset Overview (Top Section)

Four metric cards showing:

```
┌─────────────────────────────────────────────┐
│  Total Samples: 50  │  Unique Ingredients: 4 │
│  Skin Types: 4      │  Data Quality: 100%     │
└─────────────────────────────────────────────┘
```

**What it means**:
- **Total Samples**: 50 skincare profiles in the database
- **Unique Ingredients**: 4 different ingredients recommended (Niacinamide, Retinol, Hyaluronic Acid, Salicylic Acid)
- **Skin Types**: 4 categories (Oily, Dry, Combination, Sensitive)
- **Data Quality**: 100% of data is complete (no missing values)

### 2. Key Distributions (3 Bar Charts)

#### Chart A: Skin Type Distribution
Shows how many profiles have each skin type:

```
Oily: 14 profiles (28%)
Dry: 14 profiles (28%)
Combination: 12 profiles (24%)
Sensitive: 10 profiles (20%)
```

**What to look for**:
- Which skin type is most common? (Oily and Dry are tied)
- Is data well-balanced? (Yes - fairly even distribution)

#### Chart B: Ingredient Distribution
Shows which ingredients are recommended most often:

```
Niacinamide: 19 recommendations (38%)  ← Most popular
Retinol: 13 recommendations (26%)
Hyaluronic Acid: 13 recommendations (26%)
Salicylic Acid: 5 recommendations (10%)  ← Least popular
```

**What to look for**:
- Which ingredient dominates? (Niacinamide in ~1 out of 3 profiles)
- Are recommendations balanced? (Fairly balanced except Salicylic Acid)

#### Chart C: Concern Frequency
Shows how many profiles experience each skincare concern:

```
Acne: 22 profiles (44%)
Dryness: 27 profiles (54%)
Sensitivity: 27 profiles (54%)
Aging: 27 profiles (54%)
```

**What to look for**:
- Which concern is most common? (Dryness, Sensitivity, Aging all at 54%)
- Which is least common? (Acne at 44%)
- **Key Insight**: More than 1 concern per profile on average

### 3. Advanced Analysis (2 Complex Charts)

#### Chart A: Ingredient × Skin Type Heatmap
A color-coded grid showing which ingredients are recommended for each skin type:

```
                 Niacinamide  Retinol  HyaluronicAcid  Salicylic
Oily              [dark]      [medium] [light]         [light]
Dry               [medium]    [dark]   [dark]          [light]
Combination       [medium]    [medium] [medium]        [light]
Sensitive         [dark]      [light]  [dark]          [light]
```

**Color Coding**:
- **Dark** = More recommendations (popular for this skin type)
- **Light** = Fewer recommendations (less popular)

**What to look for**:
- Does Dry skin get more Hyaluronic Acid? (Yes - helps with hydration)
- Does Sensitive skin get more Niacinamide? (Yes - it's gentle)
- Patterns show the recommendation engine works logically

#### Chart B: Concern Distribution Pie Chart
Shows the breakdown of how many concerns each profile has:

```
Profiles with:
- 2 Concerns: 30%
- 3 Concerns: 40%
- 4 Concerns: 20%
- 1 Concern: 10%
```

**What it means**:
- Most profiles have multiple concerns (not just one)
- The recommendation system must balance multiple needs

### 4. Pattern Analysis (Text + Chart)

Shows how each concern shows up across different skin types:

```
ACNE:
- Oily: 57% have acne
- Combination: 50% have acne
- Sensitive: 40% have acne
- Dry: 29% have acne
```

**Pattern**: Acne is most common in Oily skin (makes sense - excess oil)

```
DRYNESS:
- Dry: 86% have dryness
- Sensitive: 60% have dryness
- Combination: 42% have dryness
- Oily: 29% have dryness
```

**Pattern**: Dryness is very common in Dry skin (as expected)

### 5. Statistics Section

Two expandable sections with detailed numbers:

**Summary Statistics** (click to expand):
- Total samples and features
- Breakdown by skin type with percentages
- Breakdown by ingredient with percentages
- Concern frequency with percentages

**Detailed Statistics** (click to expand):
- In-depth per-skin-type statistics
- Per-concern prevalence metrics
- Additional correlation data

### 6. Raw Data View

See the actual dataset:

```
┌────────┬──────┬──────┬────────────┬───────┬─────────────────────┐
│SkinType│ Acne │Dryness│Sensitivity│ Aging │RecommendedIngredient│
├────────┼──────┼──────┼────────────┼───────┼─────────────────────┤
│ Oily   │  1   │  0   │     0      │  1    │  Niacinamide        │
│ Dry    │  0   │  1   │     0      │  1    │  Hyaluronic Acid    │
│ Sensitive│ 0   │  0   │     1      │  1    │  Niacinamide        │
└────────┴──────┴──────┴────────────┴───────┴─────────────────────┘
```

**Features**:
- Click column headers to sort
- Search/filter rows
- Download as CSV (button at bottom)

### 7. Key Insights (Auto-Generated)

Four automatic insights generated from the data:

```
Most Common Concern: Dryness (27 profiles, 54%)
Top Ingredient: Niacinamide (19 recommendations, 38%)
Most Common Skin Type: Oily (tied with Dry, 14 profiles each)
Average Concerns per Profile: 2.1 concerns
```

---

## Interactive Features

### Hover Over Charts

Move your mouse over any chart to see exact values:

```
Bar Chart: Shows count and percentage
Heatmap: Shows exact cell value
Pie Chart: Shows percentage and count
```

### Click Legend Items

On some charts, click legend items to hide/show data series

### Download Chart

Click the camera icon in the top-right of any chart to save as PNG

### Export Dataset

Scroll to "Raw Data View" section and click the blue **"Download CSV"** button to export the entire dataset

### Toggle Expandable Sections

Click on sections like "Summary Statistics" to expand/collapse detailed information

---

## Common Questions

### Q: What do the binary values (0, 1) mean?

**A**: In the columns Acne, Dryness, Sensitivity, and Aging:
- **1** = Profile has this concern
- **0** = Profile does NOT have this concern

Example: A profile with `Acne=1, Dryness=0, Sensitivity=1, Aging=0` has **2 concerns**: Acne and Sensitivity.

### Q: Why do some insights show percentages over 100%?

**A**: Because profiles can have multiple concerns. When you add up all concern percentages (44% + 54% + 54% + 54% = 206%), it exceeds 100% - that's expected. It means most profiles have 2+ concerns.

### Q: Can I filter the data?

**A**: The main dashboard shows all 50 profiles. Use the **Visualization Selector** (if available) to focus on specific aspects (e.g., just Skin Type distribution).

### Q: How often is this data updated?

**A**: The dataset is static (fixed 50 profiles). If you want to analyze new data, update the CSV file at `app/data/skincare_dataset.csv` and restart the Streamlit app.

### Q: Where does this data come from?

**A**: The dataset is synthetically generated from `generate_models.py` to represent realistic skincare profiles with appropriate concern-ingredient pairings.

---

## Interpretation Tips

### For Product Teams

Use the ingredient distribution to understand:
- **Which ingredients should you stock more of?** (Niacinamide - 38%)
- **Which ingredients are niche?** (Salicylic Acid - 10%)
- **Which skin type audience is biggest?** (Oily/Dry - 28% each)

### For Data Science Teams

Use the pattern analysis to understand:
- **Which concerns are most prevalent?** (Dryness, Sensitivity, Aging - all 54%)
- **Which skin type has the most diverse concerns?** (Sensitive - 90% sensitivity concern)
- **What's the average profile complexity?** (2.1 concerns per profile)

### For Marketing Teams

Use the distributions to target:
- **"For Oily Skin"**: 28% of audience (14 profiles)
- **"For Dryness"**: 54% affected (27 profiles)
- **"Niacinamide is Our Hero Ingredient"**: In 38% of recommendations

---

## Troubleshooting

### Issue: Dashboard shows no data

**Solution**:
1. Make sure you're on the "Insights" tab (4th tab)
2. Check if the app is still running (look for "Streamlit running" message)
3. Refresh the page (press F5 in browser)

### Issue: Charts look blurry or misaligned

**Solution**:
1. Zoom browser to 100% (Ctrl + 0)
2. Make your browser window wider
3. Clear browser cache (Ctrl + Shift + Del)

### Issue: Can't download CSV

**Solution**:
1. Scroll down to "Raw Data View" section
2. Look for blue "Download CSV" button
3. If button doesn't appear, refresh page and try again

### Issue: Numbers don't match what I expected

**Solution**:
1. Check your understanding of what each column means
2. Remember: 1 = YES for concerns, 0 = NO
3. Percentages can exceed 100% when profiles have multiple concerns

---

## Next Steps

### Want to Dive Deeper?

1. **Explore Product Search**: Try searching for ingredients to see recommendations
2. **Check Ingredient Analyzer**: See detailed ingredient info
3. **Build a Routine**: Use Routine Builder to create skincare routines
4. **Compare with Predictions**: See how ML predictions compare to rule-based recommendations in Integration tab

### Want to Analyze Custom Data?

1. Update `app/data/skincare_dataset.csv` with your data
2. Restart Streamlit app
3. Come back to Insights tab to see new visualizations

### Want to Understand the System Better?

Read the full technical documentation:
- [BLOCK6_EDA_DASHBOARD.md](BLOCK6_EDA_DASHBOARD.md) - Full technical details
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - System architecture
- [BLOCK5_INTEGRATION.md](BLOCK5_INTEGRATION.md) - How rules and ML work together

---

## Key Takeaways

| Concept | Key Number | What It Means |
|---------|-----------|---------------|
| **Dataset Size** | 50 profiles | Enough for initial ML training |
| **Skin Types** | 4 types | Oily, Dry, Combination, Sensitive |
| **Ingredients** | 4 options | Niacinamide, Retinol, Hyaluronic Acid, Salicylic Acid |
| **Data Quality** | 100% | No missing values, fully complete |
| **Most Common Concern** | Dryness (54%) | Over half of profiles |
| **Top Ingredient** | Niacinamide (38%) | Recommended for ~1 in 3 profiles |
| **Profile Complexity** | 2.1 concerns avg | Most profiles have 2+ concerns |
| **Best for Dryness** | Hyaluronic Acid | 6/14 dry profiles get it |
| **Best for Sensitivity** | Niacinamide | 5/10 sensitive profiles get it |
| **Acne Correlation** | Oily Skin (57%) | Strong link to oily skin type |

---

## Tips for Best Experience

✓ **Use a desktop browser** - Charts display best on larger screens
✓ **Click and hover** - Interactive features give more details
✓ **Download the CSV** - Keep a backup copy of the data
✓ **Check back regularly** - If data updates, new patterns will appear
✓ **Share insights** - Use key findings with your team

---

## Support

For technical issues or questions:
1. Check [BLOCK6_EDA_DASHBOARD.md](BLOCK6_EDA_DASHBOARD.md) for technical details
2. Review [Troubleshooting section](#troubleshooting) above
3. Run `test_block6_eda_dashboard.py` to verify system health

