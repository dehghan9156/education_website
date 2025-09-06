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
        categories = {            
            "Technology":{
                "Programming and Development":["Web Development","Mobile Apps","Artificial Intelligence","Data Science"],
                "Hardware and Gadgets":["Smartphones","Laptops and Computers","Smart Home Devices"],
                "Software and Applications":["Operating Systems","Productivity Tools","Gaming Software"]
            },
            "Health and Fitness":{
                "Exercise and Workout":["Gym Training","Yoga and Meditation","Cardio Exercises"],
                "Nutrition and Diet":["Healthy Recipes","Weight Management","Supplements"],
                "Mental Health":["Stress Management","Sleep Health","Mindfulness"]
            },
            "Tourism and Travel":{
                "Destinations":["Domestic Travel","International Travel","Adventure Tourism"],
                "Travel Planning":["Budget Travel","Luxury Travel","Family Vacations"],
                "Travel Tips":["Packing Guides","Travel Safety","Cultural Etiquette"]
            }}
        lst_cat =[]
        for main_cats,subcats in categories.items():
            # سطح اول 
            category,_=Category.objects.get_or_create(name=main_cats)
            for sub_cat,topics in subcats.items():
                # سطح دوم
                sub_category,_=Category.objects.get_or_create(name=sub_cat,parent=category)
                for topic in topics:
                    # سطح سوم
                    topic_cat,_ = Category.objects.get_or_create(name=topic,parent=sub_category)
                    lst_cat.append(topic_cat)
            for cat in lst_cat:
                for _ in range(6):
                    Post.objects.create(
                        title = self.fake.name(),
                        image = self.get_random_posts_image(),
                        category = cat,

                    )