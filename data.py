import pandas as pd

data = {
    'Dish': ['Salad', 'Pasta', 'Pizza'],
    'Ingredients': [
        ['Lettuce', 'Tomato', 'Cucumber', 'Olive Oil'],
        ['Pasta', 'Tomato Sauce', 'Cheese'],
        ['Dough', 'Tomato Sauce', 'Cheese', 'Pepperoni']
    ],
    'Image': [
        'C:/IT/bot_grocery_shopping/images/salad.jpg',
        'C:/IT/bot_grocery_shopping/images/pasta.jpg',
        'C:/IT/bot_grocery_shopping/images/pizza.jpg'
    ]
}

df = pd.DataFrame(data)
