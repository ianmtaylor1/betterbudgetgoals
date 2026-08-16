from dataclasses import dataclass
from .month import YearMonth

# I know you shouldn't use floats for currency. This is a proof of concept.

@dataclass
class ImmediateGoal:
    """
    Templates that tell you exactly how much to put in the category this month, 
    with the implied expectation that it will be spent this month.
    Examples:
    * Simple type
    * Periodic type
    * Percent type
    * Schedule type (with 'full')
    * Average type
    * Copy type
    """
    amount: float
    category: str
    name: str = ""

@dataclass
class GradualGoal:
    """
    Templates that steadily contribute for a large future expense within a category,
    with the implied expectation that it only matters whether that much money
    is in that category by the goal month.
    Examples:
    * By type
    * Schedule type (without 'full')
    """
    month: YearMonth
    amount: float
    category: str
    name: str = ""
    spend: float = 0.0

@dataclass
class CategoryLimit:
    """
    Represents a limit placed on a category's balance due to an 'up to' clause.
    """
    amount: float
    category: str
    name: str = ""

@dataclass
class RemainderGoal:
    """
    Remainder type templates, since they are run separately in their own pass.
    """
    weight: int
    category: str
    name: str = ""

def gradual_contribution_amounts(
        gradual_goals: list[GradualGoal], 
        current_month: YearMonth, 
        category_amounts: dict[str, float]) -> tuple[dict[str,float], dict[str,float]]:
    """Calculate the contribution amount for each category based for gradual goals.
    Uses the "rubber band"/"shadow cast" method to calculate the contribution amounts."""
    if any(goal.month < current_month for goal in gradual_goals):
        raise ValueError("Gradual goals must be for future months.")
    cumulative_total = 0.0 # Running total of goal amounts (minus balances)
    max_per_month = None # Current monthly contribution required
    cat_contrib = {} # Current contributions by category (sum should equal max_per_month)
    name_contrib = {} # Contributions by goal name (sum should equal max_per_month)
    seen_categories = set() # Categories with a goal already tracked
    # Go through the gradual goals sorted by month
    for g in sorted(gradual_goals, key=lambda x: x.month):
        # Add to running cumulative total, minus the amount already spent
        cumulative_total += g.amount - g.spend
        # If this is the first time seeing this category, subtract its current balance.
        if g.category not in seen_categories:
            cumulative_total -= category_amounts.get(g.category, 0.0)
            seen_categories.add(g.category)
        # What is the new monthly contribution required to meet this timeline?
        new_per_month = cumulative_total / (g.month - current_month + 1)
        # If this goal requires additional contributions, add them to its category
        if (max_per_month is None) or (new_per_month > max_per_month):
            delta = new_per_month - (0.0 if max_per_month is None else max_per_month)
            cat_contrib[g.category] = cat_contrib.get(g.category, 0.0) + delta
            name_contrib[g.name] = name_contrib.get(g.name, 0.0) + delta
            max_per_month = new_per_month
    return cat_contrib, name_contrib

def contribution_amounts(
        gradual_goals: list[GradualGoal], 
        immediate_goals: list[ImmediateGoal], 
        current_month: int, 
        category_amounts: dict[str, float],
        category_limits: list[CategoryLimit]) -> tuple[dict[str,float], dict[str,float]]:
    # Calculate gradual goals, then add on immediate goals.
    cat_contrib, name_contrib = gradual_contribution_amounts(gradual_goals, current_month, category_amounts)
    for g in immediate_goals:
        cat_contrib[g.category] = cat_contrib.get(g.category, 0.0) + g.amount
        name_contrib[g.name] = name_contrib.get(g.name, 0.0) + g.amount
    # Finally, limit to category limits
    for l in category_limits:
        if l.amount < category_amounts.get(l.category,0.0) + cat_contrib.get(l.category,0.0):
            adjustment = l.amount - (category_amounts.get(l.category,0.0) + cat_contrib.get(l.category,0.0))
            cat_contrib[l.category] = cat_contrib.get(l.category, 0.0) + adjustment
            name_contrib[l.name] = name_contrib.get(l.name, 0.0) + adjustment
    return cat_contrib, name_contrib


if __name__ == "__main__":
    # TODO: set up test example with all same category for sanity test
    gradual_goals = [
        GradualGoal(YearMonth(2026,7), 300, "A"),
        GradualGoal(YearMonth(2026,8), 400, "A"),
        GradualGoal(YearMonth(2026,10), 100, "A")
    ]
    current_month = YearMonth(2026,4)
    current_amounts = {"A":100}
    print(gradual_contribution_amounts(gradual_goals, current_month, current_amounts))
    # TODO: set up test example with all different categories
    gradual_goals = [
        GradualGoal(YearMonth(2026,7), 300, "A"),
        GradualGoal(YearMonth(2026,8), 400, "A"),
        GradualGoal(YearMonth(2026,10), 100, "A")
    ]
    current_month = YearMonth(2026,4)
    current_amounts = {"A":50, "B":50}
    print(gradual_contribution_amounts(gradual_goals, current_month, current_amounts))
    # TODO: run test examples over time to see how contributions change.
