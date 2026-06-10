from pulp import *

x = LpVariable("x", lowBound=0, cat="Integer")
y = LpVariable("y", lowBound=0, cat="Integer")


prob = LpProblem("Simple_LP_Problem", LpMaximize)

prob += 2 * x + 3 * y, "Objective"
prob += x + 2 * y <= 2, "Constraint_1"
prob += 4 * x + 3 * y <= 12, "Constraint_2"

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Objective value =", value(prob.objective))