# Internet Programming Exam - Doctor Who Episodes Explorer

**Duration:** 2 hours  
**Tools Allowed:** Any online resources, including AI assistants (ChatGPT, Claude, etc.)

## Important Notice to Students

This exam tests your ability to build working software using modern tools and techniques. **Using AI assistants is encouraged and expected** as part of professional development practice.

### Grading Philosophy

- ✅ **Basic functionality (60-70 points):** Display and basic interaction
- ✅ **Robust handling (75-89 points):** Edge cases, error handling, polish
- ✅ **Advanced features (90-100 points):** Extra functionality and optimization

⚠️ **Critical:** Your code must work with the provided test data, which includes edge cases. Code that crashes, has obvious bugs, or fails to handle data variations will lose points.

### Tips for Success

1. **Test frequently** - Don't just assume it works
2. **Check the console** for errors and warnings
3. **Try different inputs** - Filter by different values, sort different columns
4. **Read your code** - Make sure you understand what it does
5. **Handle edge cases** - Not all data is perfect

## Assignment Overview

Build a website that allows users to explore Doctor Who episodes with sorting, filtering, and display capabilities. The Doctor Who series has been running for over 50 years with multiple actors playing the Doctor across different eras.

## Data Source

The data is available at:
```
https://raw.githubusercontent.com/sweko/internet-programming-adefinater/refs/heads/main/data/doctor-who-episodes.json
```

### Data Format

The API returns an object with an `episodes` array:

```javascript
{
  "episodes": [
    {
      "rank": 1,
      "title": "Blink",
      "series": 3,
      "era": "Modern",
      "broadcast_date": "2007-06-09",
      "director": "Hettie MacDonald",
      "writer": "Steven Moffat",
      "plot": "Sally Sparrow receives a mysterious message...",
      "doctor": {
        "actor": "David Tennant",
        "incarnation": "Tenth Doctor"
      },
      "companion": {
        "actor": "Freema Agyeman",
        "character": "Martha Jones"
      },
      "cast": [
        {
          "actor": "Carey Mulligan",
          "character": "Sally Sparrow"
        },
        {
          "actor": "Michael Obiora",
          "character": "Billy Shipton"
        }
      ]
    }
  ]
}
```

**Note:** Some episodes may have missing or varied data (see Edge Cases section).

---

## Requirements

### Tier 1: Basic Requirements (60 points)

These are the minimum requirements for a passing grade.

#### 1. Data Loading (15 points)
- Load episode data from the provided API endpoint
- Display a loading indicator while fetching data
- Show an error message if loading fails

#### 2. Episode Display (20 points)
Display episodes in a table with the following columns:
- **Rank:** The episode's rank number
- **Title:** Episode title
- **Series:** Series number
- **Era:** Classic, Modern, or Recent
- **Year:** Broadcast year (extract from `broadcast_date`)
- **Director:** Director name
- **Writer:** Writer name
- **Doctor:** Actor name and incarnation (format: "David Tennant (Tenth Doctor)")
- **Companion:** Actor and character (format: "Freema Agyeman (Martha Jones)")
- **Cast:** Number of additional cast members

#### 3. Basic Sorting (15 points)
- Clicking a column header should sort by that column
- First click: ascending order
- Second click: descending order
- Indicate sort direction with an arrow (↑ or ↓)
- **Note:** Era should sort in order: Classic, Modern, Recent

#### 4. Basic Filtering (10 points)
- Filter by episode name (partial match, case-insensitive)
- Filter updates the display in real-time or on button click

---

### Tier 2: Robust Implementation (25 points)

These demonstrate understanding and attention to detail.

#### 5. Edge Case Handling (15 points)

Your code must gracefully handle the following real-world data issues:

**Missing Companions (5 points)**
- Some episodes have no companion (`companion` is `null` or missing)
- Display should show "No companion" or similar, not crash or show "undefined"

**Empty Cast Arrays (3 points)**
- Some episodes have `cast: []`
- Should display "0" or handle gracefully, not cause errors

**Multiple Writers (4 points)**
- Some episodes have writers like "Steven Moffat & Mark Gatiss"
- Should display correctly and sort properly

**Special Characters in Names (3 points)**
- Titles may contain apostrophes, quotes, or slashes
- Example: "The Doctor's Wife" or "Bad Wolf / The Parting of the Ways"
- Must display correctly without breaking

#### 6. Multiple Filter Support (5 points)
- Filter by Era (dropdown: All, Classic, Modern, Recent)
- Filters work together (name AND era)

#### 7. Enhanced Sorting (5 points)
- All displayed columns are sortable
- Sort indicator clearly shows current sort column and direction
- Companion and Doctor columns sort by actor name

---

### Tier 3: Advanced Features (15 points)

Choose **at least 2** of the following to demonstrate deeper understanding:

#### Option A: Additional Filters (5 points)
Add filters for:
- Doctor (dropdown populated from data)
- Companion (dropdown populated from data)

#### Option B: Cast Details (5 points)
When showing cast count, make it interactive:
- Click the number to show full cast list
- Display as "Actor (Character)" for each member
- Or show cast in a tooltip on hover

#### Option C: Broadcast Decade (5 points)
- Add a "Decade" column
- Extract decade from broadcast_date
- Format as "1960s", "1970s", "2000s", etc.
- Make it sortable

#### Option D: Plot Preview (5 points)
- Add a "Plot" column
- Show first 50 characters of plot
- Don't cut words in half
- End with "..." if truncated
- Click to expand full plot (optional bonus)

#### Option E: Data Validation (5 points)
- Check for data quality issues on load
- Log warnings to console for:
  - Missing required fields
  - Future broadcast dates
  - Negative or zero rank
  - Invalid era values
- Display count of validation warnings

#### Option F: Performance Optimization (5 points)
- Implement efficient sorting (don't re-sort on every render)
- Use event delegation for table clicks
- Debounce filter inputs
- Add comment explaining your optimization strategy

#### Option G: Keyboard Navigation (5 points)
- Support keyboard shortcuts:
  - Tab through filters
  - Enter to apply filters
  - Arrow keys to change sort (when focused on headers)
- Must work without mouse

#### Option H: Your Choice (5 points)
- Implement a creative feature you think would be useful
- Add a comment explaining what it does and why

---

## Edge Cases in Test Data

⚠️ **Important:** The test data intentionally includes edge cases. Your code must handle:

- Episodes with `null` companions
- Episodes with empty `cast` arrays
- Writers with multiple names (e.g., "Name1 & Name2")
- Titles with special characters (`'`, `"`, `/`)
- Varying broadcast date formats (some may differ)

**Code that crashes on edge cases will lose significant points.**

---

## Submission Requirements

1. Complete the code in your assigned student folder
2. Your submission should include:
   - `index.html`
   - `script.js`
   - `styles.css`
3. Your code must be your own work (even if assisted by AI)
4. Test your code before submitting

---

## Evaluation Criteria

| Category | Points | Description |
|----------|--------|-------------|
| Data Loading | 15 | Correctly fetches and handles API data |
| Display | 20 | Shows all required information correctly |
| Basic Sorting | 15 | Implements sorting with direction indicators |
| Basic Filtering | 10 | Name filter works correctly |
| Edge Cases | 15 | Handles missing data, special characters gracefully |
| Multiple Filters | 5 | Era filter + combination logic |
| Enhanced Sorting | 5 | All columns sortable with proper logic |
| Advanced Features | 15 | At least 2 advanced features implemented |
| **Total** | **100** | |

---

## Technical Notes

### Era Sorting Order
When sorting by Era, use this order:
1. Classic (first)
2. Modern
3. Recent (last)

### Date Handling
- Extract year from `broadcast_date` (format: "YYYY-MM-DD")
- For decade: extract year and format as "1960s", "1970s", etc.

### Filter Behavior
- Name filter: case-insensitive, partial match (contains)
- Dropdown filters: exact match
- Multiple filters: AND logic (all must match)

### Sorting Behavior
- Default sort: by rank (ascending)
- Click header: toggle between ascending/descending
- Only one column sorted at a time

---

## Recommended Approach

1. **Start simple:** Get basic display working first
2. **Test early:** Check for errors in console frequently  
3. **Handle edge cases:** Add null checks and validations
4. **Add features incrementally:** Don't try to do everything at once
5. **Use AI effectively:** Ask for explanations, not just code
6. **Understand your code:** Be able to explain what each part does

---

## Academic Integrity

- You may use any online resources including AI assistants
- Your final code must be your own submission
- You must understand all code you submit
- Identical submissions will be flagged for review

---

## Getting Help During Exam

- Raise your hand if you have questions about requirements
- Check the console for error messages
- Test with different filter/sort combinations
- Read the error messages - they often tell you what's wrong

---

**Good luck! Remember: Working code that handles edge cases beats fancy features that crash.**
