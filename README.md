# Renaissance Periodization Workout Planner

## Use

Go to: [https://rpplan.streamlit.app/](https://rpplan.streamlit.app/)

## Disclaimer

I am not affiliated in any way to Renaissance Periodization.

## Overview

The [Renaissance Periodization (RP)](https://rpstrength.com/) Workout Planner is an application designed to help fitness enthusiasts and athletes create and manage their workout routines effectively. Drawing on the principles of Dr. Mike Israetel's training tips for hypertrophy, this planner allows users to benchmark their own workouts against RP's volume landmarks recommendations (MEV, MAV, MRV), and visualize their current scheduling in relation to established fitness metrics.

## Features

- Workout Customization: Users can input their exercises, sets, and target muscles, creating a tailored workout plan.
- Volume Landmark Tracking: Integrating Dr. Mike Israetel's MEV (Minimum Effective Volume) and MRV (Maximum Recoverable Volume) concepts, the app calculates and displays the percentage of these volume landmarks achieved per week.
- Dynamic Workout Addition: With the capability to add multiple workouts, users can plan and manage varied routines for different days.
- Interactive Data Visualization: the app visualizes workout data, allowing users to easily comprehend their training status (e.g., undertraining, productive, overtraining) based on their weekly volume.

## Sources

I got the [exercise list](exerciselist.txt) from <https://github.com/davejt/exercise/blob/master/data/exercises> with the following changes:

- Removed 5 entries with extra commas and mislabeled muscle groups (quadriceps when it could have been cardio), such as "bicycling, stationary, quadriceps". Added 5 corrected entries with "cardio" label, for example, "bicycling, cardio" and "running, cardio".

Affected Entries:

```
Bicycling, quadriceps # wrong target
Bicycling, stationary, quadriceps # 2 commas & wrong target
Running, treadmill, quadriceps
Rowing, stationary, quadriceps
Jogging-treadmill, quadriceps
```
