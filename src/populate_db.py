from engine.db import DB


def populate(db: DB):
    db.add({
        "category": "Cleaning",
        "name": "Detergent",
        "description": "Laundry detergent, 2L bottle",
        "price": 50
    })

    db.add({
        "category": "Food",
        "name": "Rice",
        "description": "White rice, 1kg",
        "price": 35
    })

    db.add({
        "category": "Food",
        "name": "Beans",
        "description": "Black beans, 500g",
        "price": 28
    })

    db.add({
        "category": "Hygiene",
        "name": "Toothpaste",
        "description": "Mint flavored, 120g",
        "price": 15
    })

    db.add({
        "category": "Hygiene",
        "name": "Shampoo",
        "description": "Anti-dandruff, 400ml",
        "price": 40
    })

    db.add({
        "category": "Cleaning",
        "name": "Floor Cleaner",
        "description": "Pine scent, 1L",
        "price": 30
    })

    db.add({
        "category": "Food",
        "name": "Milk",
        "description": "UHT Milk, 1L",
        "price": 25
    })
