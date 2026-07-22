from sqlmodel import Session, select
from models.city import City, CityMetric


def calculate_budget(city_name: str, salary: float, family: int, session: Session):

    city = session.exec(
        select(City).where(City.name == city_name)
    ).first()

    if not city:
        return None

    metric = session.exec(
        select(CityMetric).where(CityMetric.city_id == city.id)
    ).first()

    if not metric:
        return None

    # Cost factor using cost of living index
    cost_factor = metric.cost_of_living_index / 100

    rent = salary * (0.04 + cost_factor * 0.01)

    food = family * 5000

    transport = 3000 + (family - 1) * 500

    utilities = 2500 + family * 400

    total = rent + food + transport + utilities

    remaining = salary - total

    if remaining >= salary * 0.30:
        verdict = (
            f"Excellent! Your monthly salary of ₹{salary:,.0f} is more than enough to live comfortably in {city.name}. "
            f"After covering your estimated monthly expenses, you can still save around ₹{remaining:,.0f} every month."
        )

    elif remaining >= salary * 0.15:
        verdict = (
            f"Comfortable! Your income is sufficient to manage your living expenses in {city.name}. "
            f"You are expected to save approximately ₹{remaining:,.0f} each month while maintaining a comfortable lifestyle."
        )

    elif remaining > 0:
        verdict = (
            f"Manageable. Your salary is just enough to cover your monthly expenses in {city.name}. "
            f"You may save only around ₹{remaining:,.0f} per month, so careful budgeting is recommended."
        )

    else:
        verdict = (
            f"Not Affordable. Your estimated monthly expenses exceed your salary by ₹{abs(remaining):,.0f}. "
            "Consider increasing your income, reducing expenses, or choosing a city with a lower cost of living."
        )

    return {
        "city": city.name,
        "salary": salary,
        "rent": round(rent, 2),
        "food": round(food, 2),
        "transport": round(transport, 2),
        "utilities": round(utilities, 2),
        "remaining": round(remaining, 2),
        "verdict": verdict
    }