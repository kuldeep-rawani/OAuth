from models import *
import datetime

def store(modelName, values):
	return modelName.objects.create(**values)

def filter_attribute(modelName, filterKeys):
	return modelName.objects.filter(**filterKeys)

def filter_by_attribute(modelName, filterKeys):
    return modelName.objects.get(**filterKeys)

def update(modelName, filterKeys, updatedWith):
	updateWith.update({'updated_at':datetime.datetime.now()})
	return modelName.objects.update(**values)

def delete(modelName, filterKeys):
	return modelName.objects.filter(**filterKeys).delete()

def fetch_all(modelName):
	return modelName.objects.all()			