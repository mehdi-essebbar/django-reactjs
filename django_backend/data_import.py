from mongoengine import connect, register_connection
from mongoengine import fields, Document

class Shops(Document):
    meta = {
        'db_alias': 'shops',
        'collection': 'shops'
    }
    
    name = fields.StringField()
    picture = fields.URLField()
    email = fields.EmailField()
    city = fields.StringField()
    location = fields.PointField()
    
    def __str__(self):
        return self.name

class Shop(Document):
    meta = {
        'db_alias': 'test_local',
        #'collection': 'shop'
    }
    
    name = fields.StringField()
    picture = fields.URLField()
    email = fields.EmailField()
    city = fields.StringField()
    location = fields.PointField()
    
    def __str__(self):
        return self.name
        
host = "mongodb://admin:azerty@cluster0-shard-00-00-uaelv.mongodb.net:27017,cluster0-shard-00-01-uaelv.mongodb.net:27017,cluster0-shard-00-02-uaelv.mongodb.net:27017/?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

host_local = "127.0.0.1:27017"

connect(db="shops", alias="shops", host=host)
#register_connection(name="test", alias="test", host=host)
register_connection(name="test", alias="test_local", host=host_local)


for shop in Shops.objects.all():
    new_shop =Shop(name=shop.name, picture=shop.picture, email=shop.email, city=shop.city, location=shop.location)
    new_shop.save()

print (Shop.objects.all().count())
#shop = Shops(name='test_name', picture="http://www.example.com", email="my_email@gmail.com", city="Rbat")
#shop.save()