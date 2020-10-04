from monkeylearn import MonkeyLearn
 
ml = MonkeyLearn('1f8a83ad2bbb93b4074e4b9e6a2cf5d8acbfe7e4')
data = ["I love everything about @Zendesk!", "Theres a bug in the new integration"]
model_id = 'cl_pi3C7JiL'
result = ml.classifiers.classify(model_id, data)

print(result.body)