-- Insert example process flow 2 with rule
INSERT INTO process_flows (id,name,description,rule_content) VALUES (2,'Example Process Flow 2',NOW(),'// some_rule.mvel

if (condition) {
    // Do something
}
');

-- Insert example process flow with rule
INSERT INTO process_flows (id,name,description,rule_content) VALUES (CURRENT_TIMESTAMP,'Example Process Flow','This is an example process flow.','// second_rule.mvel

// Define a map with some initial values
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 90);
scores.put("Bob", 85);
scores.put("Charlie", 88);

// Calculate the average score
int totalScore = 0;
for (Integer score : scores.values()) {
    totalScore += score;
}
double averageScore = totalScore / scores.size();

// Print the average score
System.out.println("Average Score: " + averageScore);

// Check if any score is below a threshold
int threshold = 80;
boolean belowThreshold = false;
for (Integer score : scores.values()) {
    if (score < threshold) {
        belowThreshold = true;
        break;
    }
}

// Print if any score is below the threshold
if (belowThreshold) {
    System.out.println("Some scores are below the threshold of " + threshold);
} else {
    System.out.println("All scores are above the threshold of " + threshold);
}');

-- Insert example task 1 with rule
INSERT INTO tasks (task_id,task_name,task_description,task_rule) VALUES (1,'Maker Task Example 1','A long description about the task','[thisValue >= thatValue]');

-- Insert example task 2 with rule
INSERT INTO tasks (task_id,task_name,task_description,task_rule) VALUES (2,'Checker Task Example 1','A long description about the task','[thisValue >= thatValue]');

