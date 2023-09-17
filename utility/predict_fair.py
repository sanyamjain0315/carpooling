import pickle
filename="my_model.pickle"
loaded_model = pickle.load(open(filename, "rb"))

def predict_fare(car_type, fuel_type, distance_traveled):
    if fuel_type!='electric':
        
        model_input=[]
        if car_type=='suv':
            model_input.extend([1,0])
        else:
            model_input.extend([0,1])
            
        if fuel_type=='diesel':
            model_input.extend([1,0,95])
        else:
            model_input.extend([0,1,107])

        model_input.append(distance_traveled)

        if car_type == 'suv':
            if fuel_type == 'diesel':
                model_input.append(12) 
            else:
                model_input.append(10) 
        else:
            if fuel_type == 'diesel':
                model_input.append(15) 
            else:
                model_input.append(12)
                
        print(model_input)
        fare = loaded_model.predict([model_input])
        return fare[0]
    else:
        return 2.5*distance_traveled

# car_type = "sedan"
# fuel_type = "petrol"
# distance_traveled = 15

# predicted_fare = predict_fare(car_type, fuel_type, distance_traveled)
# print(f"The predicted fare is: {predicted_fare}")
