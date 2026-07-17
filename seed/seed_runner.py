import csv
from pathlib import Path

from sqlmodel import Session, SQLModel, select
from database import engine
from models.city import City, CityMetric

print("Starting Seeding")


def run_seed():
    print("Function Called")

    SQLModel.metadata.create_all(engine)

    csv_file = Path(__file__).parent / "cities_seed.csv"

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        print(reader.fieldnames)      # <-- IMPORTANT

        with Session(engine) as session:

            for row in reader:

                stmt = select(City).where(City.name == row["name"])
                city = session.exec(stmt).first()

                if city is None:
                    city = City(
                        name=row["name"],
                        state=row["state"],
                        population=int(row["population"])
                    )
                    session.add(city)
                    session.commit()
                    session.refresh(city)

                metric = CityMetric(
                    city_id=city.id,
                    year=int(row["year"]),
                    cost_of_living_index=float(row["cost_index"]),
                    air_quality_index=float(row["air_index"]),
                    safety_score=float(row["safety_score"]),
                    healthcare_score=float(row["health_score"])
                )

                session.add(metric)

            session.commit()

    print("Seed Complete")


if __name__ == "__main__":
    run_seed()