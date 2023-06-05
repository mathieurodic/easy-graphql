from django.contrib.auth import get_user_model
from django.db.models import Sum

import easy_graphql_server

from .models import BankAccount, DailyOccupation, House, Person


class ExposedPersonSameAsBirthdate(easy_graphql_server.CustomField):
    name = "same_as_birth_date"
    format = easy_graphql_server.Model("person").fields.birth_date

    @staticmethod
    def read_one(instance, authenticated_user, graphql_selection):
        return instance.birth_date

    @staticmethod
    def create_one(instance, authenticated_user, value):
        instance.birth_date = value

    update_one = create_one


class ExposedPerson(easy_graphql_server.ExposedModel):
    orm_model = Person
    name = "person"
    plural_name = "people"
    can_expose = (
        "id",
        "username",
        "first_name",
        "last_name",
        "birth_date",
        "houses",
        "home",
        "daily_occupations",
        "gender",
    )
    can_read = (
        "updates_count",
        "creation_data",
    )
    custom_fields = [ExposedPersonSameAsBirthdate]


class ExposedMe(easy_graphql_server.ExposedQuery):
    name = "me"
    require_authenticated_user = True
    pass_authenticated_user = True
    output_format = (
        easy_graphql_server.Model("person").output_format
        + {"is_superuser": bool, "is_staff": bool}
        - ("houses", "home", "daily_occupations")
    )

    @staticmethod
    def method(authenticated_user):
        return authenticated_user


class ExposedHouseTenantsOccupations(easy_graphql_server.CustomField):
    name = "tenants_occupations"
    format = {
        "total_hours_per_day": int,
        "occupations": easy_graphql_server.Model("dailyoccupation").fields.occupation,
    }

    @staticmethod
    def read_one(instance, authenticated_user, graphql_selection):
        return [
            {
                "occupation": occupation["occupation"],
                "hours_per_day": occupation["total_hours_per_day"],
            }
            for occupation in DailyOccupation.objects.filter(
                person__home__id=instance.id
            )
            .values("occupation")
            .annotate(
                total_hours_per_day=Sum("hours_per_day"),
            )
            .order_by("occupation")
        ]


class ExposedHouse(easy_graphql_server.ExposedModel):
    orm_model = House
    name = "house"
    custom_fields = [ExposedHouseTenantsOccupations]


class ExposedDailyOccupation(easy_graphql_server.ExposedModel):
    orm_model = DailyOccupation
    name = "daily_occupation"
    only_when_child_of = Person


class ExposedBankAccount(easy_graphql_server.ExposedModel):
    orm_model = BankAccount
    name = "bank_account"
    require_authenticated_user = True


schema = easy_graphql_server.Schema(debug=True, restrict_models_queried_fields=True)
schema.expose(ExposedPerson)
schema.expose(ExposedMe)
schema.expose(ExposedHouse)
schema.expose(ExposedDailyOccupation)
schema.expose(ExposedBankAccount)
