from pydantic import UUID4, BaseModel


class OrderItem(BaseModel):
    product_id: UUID4
    quantity: int
