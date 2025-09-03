from ...models import Post,Category
from faker import Faker
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

        
    def get_random_posts_image(self):
        # RANDOM_USER_API_URL = "https://randomuser.me/api/portraits/men/"
        random_number = self.fake.random.randint(1, 100)  # ایجاد یک عدد تصادفی برای انتخاب تصویر
        # return image_url
        return f"https://placehold.co/250x250?text=Product+{random_number}"

    def handle(self, *args, **kwargs):
        categories = [
            "تکنولوژی",
            "سلامت و تناسب اندام",
            "گردشگری و سفر",
            "غذا و آشپزی",
            "آموزش و تحصیل",
            "سبک زندگی",
            "فرهنگ و هنر",
            "ورزش و بدنسازی",
            "اقتصاد و کسب‌وکار",
            "روانشناسی و خودیاری"
        ]
        for name in categories:
            category,_=Category.objects.get_or_create(name=name)
            for _ in range(6):
                Post.objects.create(
                    title = self.fake.name(),
                    image = self.get_random_posts_image(),
                    category = category,

                )