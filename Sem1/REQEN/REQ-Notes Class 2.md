# REQ-Notes Class 2

### Lessons from last time:

1. Kano Modell - 3 different Requirement categories:

   - Basic

   - Performance

   - Excitement

2. Brainstorming Paradox - Trying to find good ideas by brainstorming about how to worsen the feature

3. Wichtige Fragen bei Requirements:
   - Warum hast du dieses Requirement? - Requirements Rationale
   - Wie wichtig ist das Requirement? - Requirements Priority
   - Wie likely wird sich das Requirement verändern in der Zukunft? - Requirements Stability

### Notes

Kestner:

- System requirements (how the system should operate) 
- Requirement Specifications
- Assumptions

`As a < type of user >, I want < some goal > so that < some reason >`

### Exercise 1

**System Requirement:** "The system automatically notifies first responders if the user is buried by an avalanche"

Break it down into a requirements specification. Also document assumptions

**Requirements Specifications:**

Using the emergency button or voice control users can manually report avalanches which take priority over sensor data, and start an emergency call.

Using the camera and a motion sensor the system detects rapid drops in speed and being covered in snow, if the user doesn't respond to a prompt using eye-tracking, emergency services are contacted after 30 seconds.

Using a location sensor the goggles know in which country/skiing resort the user is in to know the proper emergency number for that location.

Using vitality sensors, the goggles decide whether the user is conscious and can decide on proper measures based on that, if user is conscious the goggles can let the user make the call, otherwise the goggles makes them autonomously.

**Assumptions:**

- Skiing Goggles
- Skiing Goggles stay on and functioning even after the avalanche
- Skiing Goggles have an emergency button for manual use, the same feature can also be accessed via voice control
- Camera and Motion Sensor functioning properly
- Eye-tracking capabilities
- System knows emergency contacts
- System has capabilities to make automated calls/emergence signal functionalities
- System can make the emergency calls autonomously without the users help

### Exercise 2

#### 	What are the domain objects of «EarlyBird»? 

​		Orders

​		Products

​		Deliveries

​		Customer

​		Address

#### 	What are the use cases for each domain object?

​	**Orders**

- New Order
- Delete Order
- View Order History
- Repeat Last Order

​	**Products**

- Select Product
- Create new Product
- Delete Product
- Edit Product
- Search Products

​	**Deliveries**

- 

​	**Customer**

- Change Address 
- Change Username
- Place Order
- Cancel Order
- Select Restaurant

​	**Address**

- Deliver Order



Requirements for a MVP of a Microblogging System (Twitter) 1 page max