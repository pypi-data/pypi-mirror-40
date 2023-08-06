import factory
from .models import Customer, Project
from djangoldp_account.factories import ChatConfigFactory
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker('company')
    address = factory.Faker('address')
    logo = factory.Faker('url')

@factory.django.mute_signals(post_save)
class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=250)
    number = factory.Faker('random_int', min=0)
    customer = factory.SubFactory(CustomerFactory)
    chatConfig = factory.SubFactory(ChatConfigFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.team.add(member)
