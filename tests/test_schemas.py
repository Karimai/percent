from datetime import date, datetime, timedelta

from pytest import mark, raises

from config.config import Date_format
from schemas.schemas import ResidenceCreate, Status, UserCreate


def test_invalid_user_create():
    with raises(ValueError):
        UserCreate(
            username="test_user", email="invalid_email", date_of_birth="2020-0101"
        )


def test_invalid_residence_create_future_date():
    with raises(ValueError):
        ResidenceCreate(
            start_date=date.today() + timedelta(days=1),
            end_date="2022-01-01",
            status=Status.motherland,
            country="TestCountry",
            city="TestCity",
        )

    with raises(ValueError):
        ResidenceCreate(
            start_date=date.today() + timedelta(days=-1),
            end_date="now",
            status=Status.motherland,
            country="TestCountry",
            city="TestCity",
        )


@mark.parametrize(
    "start_date, end_date, status, country, city",
    [
        (
            date.today() + timedelta(days=-1),
            (date.today() + timedelta(days=-10)).strftime(Date_format),
            Status.motherland,
            "Test_empty_Country",
            "",
        ),
        (
            date.today() + timedelta(days=-1),
            (date.today() + timedelta(days=-10)).strftime(Date_format),
            Status.motherland,
            "",
            "Test_empty_City",
        ),
    ],
)
def test_invalid_city_country(start_date, end_date, status, country, city):
    with raises(ValueError):
        ResidenceCreate(
            start_date=start_date,
            end_date=end_date,
            status=status,
            country=country,
            city=city,
        )


@mark.parametrize(
    "username, email, password, date_of_birth",
    [
        ("test_user", "test@example.com", "test_password", None),
        ("user123", "user123@example.com", "secure123", "1990-01-01"),
    ],
)
def test_valid_user_create(username, email, password, date_of_birth):
    user = UserCreate(
        username=username, email=email, password=password, date_of_birth=date_of_birth
    )
    assert user.username == username
    assert user.email == email
    assert user.password == password
    if date_of_birth:
        assert (
            user.date_of_birth == datetime.strptime(date_of_birth, Date_format).date()
        )
    else:
        assert user.date_of_birth is None


@mark.parametrize(
    "start_date, end_date, status, country, city",
    [
        (date.today(), "2023-01-01", Status.motherland, "Test Country", "Test City"),
        (date(2022, 1, 1), "present", Status.travel, "Travel Country", "Travel City"),
    ],
)
def test_valid_residence_create(start_date, end_date, status, country, city):
    residence = ResidenceCreate(
        start_date=start_date,
        end_date=end_date,
        status=status,
        country=country,
        city=city,
    )
    assert residence.start_date == start_date
    if end_date == "present":
        assert residence.end_date == end_date
    else:
        assert residence.end_date == datetime.strptime(end_date, Date_format).date()
    assert residence.status == status
    assert residence.country == country
    assert residence.city == city
