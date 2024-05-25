from rest_framework import serializers
from work.models import User,Taskmodel



class Registration(serializers.ModelSerializer):

    class Meta:

        model= User

        fields=['id','username','password','email','first_name','last_name']

        read_only_fields=['id']

    
    def create(self,validated_data):        #method ovverriding is happening here cuz we have invoked create() method from parent class(ModelSerializer) to child class(Registration)
        return User.objects.create_user(**validated_data)




class Todoserializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Taskmodel

        fields='__all__'

        read_only_fields=['id','created_data','user','completed']