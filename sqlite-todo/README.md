## 🎁 Think of `Annotated` Like a Gift Box  

Imagine you are **sending a gift** to a friend. The gift (actual object) is inside a **box**, and you also attach a **label** to describe what's inside.

### **Without `Annotated` (just the gift)**  
```python
def give_gift(item: str):
    return f"Here is your {item}"
```
- You only know it's a string (item: str), but you don't know anything extra about it.

### **With `Annotated` (gift+label)**
```python
from typing import Annotated

def give_gift(item: Annotated[str, "This is a surprise gift"]):
    return f"Here is your {item}"
```
- Now, the string (str) has extra metadata ("This is a surprise gift").
- The function works the same, but the annotation adds more meaning.

## How This Applies to FastAPI
- In FastAPI, dependencies like Depends(get_db) inject values into your function.
- But with Annotated, you are also adding type information.

### **Without `Annotated`**  
```python
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todos).all()
```
- db is a Session, and FastAPI knows it comes from get_db().

### **Without `Annotated` (gift + label)**
```python
from typing import Annotated

db_dependency = Annotated[Session, Depends(get_db)]

def get_todos(db: db_dependency):
    return db.query(Todos).all()
```
- This clearly marks that db is a database session, and it must be injected.
