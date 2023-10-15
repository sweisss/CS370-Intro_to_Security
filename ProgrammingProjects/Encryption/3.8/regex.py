import re

results = """
Collision detected on trial 24 with hash: f1e == f1e
Collision found in round 7 after 24 trials.
Collision detected on trial 379 with hash: 285 == 285
Collision found in round 8 after 379 trials.
Collision detected on trial 450 with hash: 3c8 == 3c8
Collision found in round 9 after 450 trials.
Collision detected on trial 620 with hash: 64e == 64e
Collision found in round 10 after 620 trials.
Collision detected on trial 197 with hash: 35a == 35a
Collision found in round 11 after 197 trials.
Collision detected on trial 773 with hash: 817 == 817
Collision found in round 13 after 773 trials.
Collision detected on trial 521 with hash: 2e6 == 2e6
Collision found in round 14 after 521 trials.
Collision detected on trial 71 with hash: 076 == 076
Collision found in round 18 after 71 trials.
Collision detected on trial 320 with hash: b17 == b17
Collision found in round 28 after 320 trials.
Collision detected on trial 643 with hash: b65 == b65
Collision found in round 31 after 643 trials.
Collision detected on trial 165 with hash: 27b == 27b
Collision found in round 34 after 165 trials.
Collision detected on trial 518 with hash: d3b == d3b
Collision found in round 35 after 518 trials.
Collision detected on trial 366 with hash: a02 == a02
Collision found in round 37 after 366 trials.
Collision detected on trial 345 with hash: 850 == 850
Collision found in round 38 after 345 trials.
Collision detected on trial 773 with hash: e5d == e5d
Collision found in round 39 after 773 trials.
Collision detected on trial 916 with hash: 310 == 310
Collision found in round 42 after 916 trials.
Collision detected on trial 158 with hash: c49 == c49
Collision found in round 43 after 158 trials.
Collision detected on trial 459 with hash: 4da == 4da
Collision found in round 45 after 459 trials.
Collision detected on trial 46 with hash: c95 == c95
Collision found in round 48 after 46 trials.
Collision detected on trial 488 with hash: 822 == 822
Collision found in round 49 after 488 trials.
Collision detected on trial 550 with hash: 110 == 110
Collision found in round 50 after 550 trials.
Collision detected on trial 933 with hash: b33 == b33
Collision found in round 55 after 933 trials.
Collision detected on trial 8 with hash: b60 == b60
Collision found in round 57 after 8 trials.
Collision detected on trial 973 with hash: 0e5 == 0e5
Collision found in round 65 after 973 trials.
Collision detected on trial 200 with hash: 3a5 == 3a5
Collision found in round 67 after 200 trials.
Collision detected on trial 5 with hash: 191 == 191
Collision found in round 69 after 5 trials.
Collision detected on trial 232 with hash: 4ff == 4ff
Collision found in round 71 after 232 trials.
Collision detected on trial 405 with hash: 5a0 == 5a0
Collision found in round 74 after 405 trials.
Collision detected on trial 446 with hash: e52 == e52
Collision found in round 81 after 446 trials.
Collision detected on trial 334 with hash: c0a == c0a
Collision found in round 91 after 334 trials.
Collision detected on trial 701 with hash: f85 == f85
Collision found in round 95 after 701 trials.
"""

# Use regular expressions to find lines with "Collision detected" and extract the trial number
collision_lines = re.findall(r'Collision detected on trial (\d+)', results)

# Convert the extracted trial numbers to integers and store them in a list
trials = [int(trial) for trial in collision_lines]

# Print the list of trials
print(trials)
print(len(trials))
print(sum(trials) / len(trials))
