# Fractions Academy - High-Level Architecture & Design

Welcome to **Fractions Academy**, a Duolingo-inspired interactive, gamified learning experience designed to teach fractions in an engaging, bite-sized format. This document details the high-level architecture, UI wireframe/layout structure, and state management/data model for this feature.

---

## 1. High-Level Architecture & Component Breakdown

The Fractions section is built on a modular, event-driven architecture integrated directly with the main application. It is structured into distinct, reusable layers:

```
+-------------------------------------------------------------------------+
|                              Main UI Shell                              |
|           - Section Switcher (Space Game <-> Fractions Academy)          |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        Fractions Academy Module                         |
|   +-----------------------------------------------------------------+   |
|   |                      State / Progress Engine                    |   |
|   | - Level Progression System (Level 1 to 5)                       |   |
|   | - Session Stats: XP, Current Streak, Hearts, Progress bar       |   |
|   +-----------------------------------------------------------------+   |
|                                    |                                    |
|   +-----------------------------------------------------------------+   |
|   |                        Interactive Canvas                       |   |
|   | - Food-theme Vector Renderer (Pizza, Chocolate Cake, Cherry Pie)|   |
|   | - Slices & Toppings Renderer (Pepperonis, Sparkles, Cherries)   |   |
|   | - Interactive Click-to-Select / Highlight Slices Handler        |   |
|   +-----------------------------------------------------------------+   |
|                                    |                                    |
|   +-----------------------------------------------------------------+   |
|   |                     Gamified Exercise Engine                    |   |
|   | - Question Generators (Level 1-5 custom schemas)                |   |
|   | - Input Processors (Multiple-Choice, Tapping, Fill-in-the-Blank)|   |
|   | - Feedback Panel (Positive/Correction sound & animations)       |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

### Components:
1. **Section Switcher (UI Toggle):** A highly visible visual toggle at the top of the start screen allowing users to switch between the traditional "Numbers Space Voyage" and the new "Fractions Academy".
2. **Duolingo-style Visual Map:** A central hub showing 5 progression nodes (one for each level). Completed levels show filled stars/progress, current level is active and bouncing, while subsequent levels are locked.
3. **Interactive Food Renderer (Canvas-based):** A specialized 2D canvas drawing pipeline representing mathematical fractions using delicious, visually appealing shapes:
   - **Pizza:** Sliced with golden crust, red sauce, melted cheese, and pepperoni toppings.
   - **Chocolate Cake:** Rich dark brown slice partitions with sprinkles.
   - **Cherry Pie:** Flaky golden lattices and cherry fillings.
4. **Interactive Slice Selection Handler:** Detects clicks/touches on specific angular wedges of the pizza/cake/pie, updating highlighting states in real-time.
5. **Level Curricula Engine:** Orchestrates custom mini-games/lessons for:
   - *Level 1: Basic Recognition* (Multiple Choice matching visuals to fractions).
   - *Level 2: Building Fractions* (Click/tap slices to reach a target fraction).
   - *Level 3: Fraction Comparison* (Select the larger visual fraction side).
   - *Level 4: Equivalent Fractions* (Overlapping visual overlay toggles between $1/2$ and $2/4$, etc.).
   - *Level 5: Basic Operations* (Adding or subtracting wedges on a plate with shared denominators).
6. **Audio & Gamification Feedback:** Audio synthesizer using standard `AudioContext` to generate pleasant correct-answer major chords and instructive retry minor chords. Integrates with persistent XP, streak counts, and custom progress bars.

---

## 2. Suggested UI Wireframe & Layout

Below is the layout for the **Interactive Question Screen**, designed to match the clean, motivating UX of modern educational apps.

```
+-------------------------------------------------------------------------+
| [X] Close   |==========[ Progress Bar: 60% ]==========| ❤️ ❤️ ❤️ (Hearts) |
+-------------------------------------------------------------------------+
|                                                                         |
|   (🦉 Mascot Dialogue Bubble)                                           |
|   "היי! עזור לי לחתוך את הפיצה הזו כדי להגיע ל-3/8 מהשלם!"                  |
|                                                                         |
+-------------------------------------------------------------------------+
|                                                                         |
|                          [ Interactive Canvas ]                         |
|                                                                         |
|                                 (@@@)                                   |
|                               (@@@@@@@)     <-- Sliced food shape       |
|                                (@@@)            (e.g., Pizza or Pie)    |
|                                                                         |
|                          [ Click to Highlight ]                         |
|                                                                         |
+-------------------------------------------------------------------------+
|                                                                         |
|                    [ Dynamic Interactive Inputs ]                       |
|                                                                         |
|    [ Option A: 3/8 ]     [ Option B: 5/8 ]     [ Option C: 1/2 ]        |
|                                                                         |
|                           - OR -                                        |
|                                                                         |
|                     מונב (Numerator)   : [  3  ]                        |
|                     ----------------------------                        |
|                     מכנה (Denominator) : [  8  ]                        |
|                                                                         |
+-------------------------------------------------------------------------+
|                                                                         |
|                         [ לחיצה לבדיקת תשובה ]                          |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

## 3. Sample State Management Logic & Data Model

Every question/exercise within a level is represented by a strictly typed JSON schema. This ensures extensibility, making it easy to create new micro-lessons statically or dynamically.

### Sample Exercise JSON Data Model:

```json
{
  "id": "frac_lev2_ex3",
  "level": 2,
  "theme": "pizza",
  "type": "slice_tap",
  "questionHebrew": "הדגש 3 מתוך 8 פרוסות כדי ליצור את השבר 3/8",
  "data": {
    "targetNumerator": 3,
    "denominator": 8,
    "initialSelectedSlices": []
  },
  "hints": [
    "ספור את סך כל הפרוסות בפיצה (זה המכנה - 8).",
    "לחץ על 3 פרוסות כדי לצבוע אותן בצהוב טעים!"
  ],
  "validation": {
    "type": "exact_slices_count",
    "value": 3
  }
}
```

### Curricular Question Model Examples:

#### Level 1 (Recognition - Multiple Choice)
```json
{
  "id": "frac_lev1_ex1",
  "level": 1,
  "theme": "cake",
  "type": "multiple_choice",
  "questionHebrew": "איזה שבר מייצג החלק המודגש בעוגת השוקולד?",
  "data": {
    "denominator": 4,
    "highlightedSlices": 1,
    "options": ["1/4", "2/4", "3/4", "1/2"],
    "correctAnswer": "1/4"
  }
}
```

#### Level 3 (Comparison)
```json
{
  "id": "frac_lev3_ex1",
  "level": 3,
  "theme": "pie",
  "type": "comparison",
  "questionHebrew": "איזה שבר גדול יותר?",
  "data": {
    "fractionA": { "numerator": 1, "denominator": 2 },
    "fractionB": { "numerator": 1, "denominator": 4 },
    "correctAnswer": "A"
  }
}
```

#### Level 4 (Equivalent Fractions)
```json
{
  "id": "frac_lev4_ex1",
  "level": 4,
  "theme": "pizza",
  "type": "equivalent_match",
  "questionHebrew": "השלם את השבר השקול: 1/2 שווה ל-? מתוך 4",
  "data": {
    "visualNumerator": 1,
    "visualDenominator": 2,
    "targetDenominator": 4,
    "correctAnswer": 2
  }
}
```

#### Level 5 (Basic Operations)
```json
{
  "id": "frac_lev5_ex1",
  "level": 5,
  "theme": "pizza",
  "type": "operation",
  "questionHebrew": "חיבור פרוסות: 1/4 + 2/4 = ?",
  "data": {
    "op": "add",
    "fractionA": { "numerator": 1, "denominator": 4 },
    "fractionB": { "numerator": 2, "denominator": 4 },
    "options": ["3/4", "2/4", "1/4", "4/4"],
    "correctAnswer": "3/4"
  }
}
```
