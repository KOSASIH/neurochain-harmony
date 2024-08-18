import pulp
import numpy as np
from scipy.optimize import linprog

class ResourceOptimizationModel:
    def __init__(self, resources: List[str], demands: List[float], capacities: List[float]):
        self.resources = resources
        self.demands = demands
        self.capacities = capacities
        self.model = pulp.LpProblem(name="resource_optimization", sense=pulp.LpMaximize)

    def add_variables(self) -> None:
        self.variables = pulp.LpVariable.dicts("Resource", self.resources, lowBound=0, cat=pulp.LpInteger)

    def add_objective(self) -> None:
        self.model += pulp.lpSum([self.variables[r] for r in self.resources])

    def add_constraints(self) -> None:
        for i, demand in enumerate(self.demands):
            self.model += pulp.lpSum([self.variables[r] for r in self.resources]) >= demand
        for i, capacity in enumerate(self.capacities):
            self.model += pulp.lpSum([self.variables[r] for r in self.resources]) <= capacity

    def solve(self) -> None:
        self.model.solve()
        print("Status:", pulp.LpStatus[self.model.status])
        for v in self.model.variables():
            print(v.name, "=", v.varValue)

    def solve_scipy(self) -> None:
        A_ub = np.array([[1] * len(self.resources)] * len(self.capacities))
        b_ub = np.array(self.capacities)
        A_eq = np.array([[1] * len(self.resources)] * len(self.demands))
        b_eq = np.array(self.demands)
        bounds = [(0, None)] * len(self.resources)
        res = linprog(c=-np.ones(len(self.resources)), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        print("Status:", res.success)
        print("Optimal solution:", res.x)
