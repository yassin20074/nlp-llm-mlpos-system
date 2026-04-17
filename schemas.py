from pydantic import BaseModel

'''Create a schema to receive the input text in the backend'''
class TextData(BaseModel):
    text: str 
