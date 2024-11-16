from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.core.security import get_username_from_token
from app.models.models import User, Cart, CartItem, Product
from app.schemas.carts import CartCreate, CartUpdate
from app.utils.responses import ResponseHandler
from sqlalchemy.exc import SQLAlchemyError


class CartService:
    @staticmethod
    async def get_user_by_token(token: str, db: AsyncSession) -> User:
        """
        Utility to fetch the active user from the token.
        """
        username = await get_username_from_token(token)
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalars().first()
        if not user:
            raise ValueError(f"User with username '{username}' not found.")
        return user

    @staticmethod
    async def get_all_carts(
            token: str,
            db: AsyncSession,
            page: int = 1,
            limit: int = 10,
    ):
        try:
            user = await CartService.get_user_by_token(token, db)

            # Fetch paginated carts for the user
            result = await db.execute(
                select(Cart)
                .filter(Cart.user_id == user.id)
                .offset((page - 1) * limit)
                .limit(limit)
            )
            carts = result.scalars().all()

            message = f"Retrieved {len(carts)} carts for page {page} with limit {limit}."
            return ResponseHandler.success(message, carts)
        except SQLAlchemyError as e:
            return ResponseHandler.server_error(f"Database error: {str(e)}")

    @staticmethod
    async def create_cart(token: str, db: AsyncSession, cart: CartCreate):
        try:
            user = await CartService.get_user_by_token(token, db)
            cart_dict = cart.model_dump()
            cart_items_data = cart_dict.pop("cart_items", [])

            cart_items = []
            total_amount = 0
            for item_data in cart_items_data:
                product_id = item_data["product_id"]
                quantity = item_data["quantity"]

                # Validate product existence
                result = await db.execute(select(Product).filter(Product.id == product_id))
                product = result.scalars().first()
                if not product:
                    return ResponseHandler.not_found_error("Product", product_id)

                # Calculate subtotal
                subtotal = product.price * quantity * (1 - (product.discount_percentage / 100))
                total_amount += subtotal

                cart_items.append(CartItem(product_id=product_id, quantity=quantity, subtotal=subtotal))

            # Create cart
            cart_db = Cart(cart_items=cart_items, user_id=user.id, total_amount=total_amount, **cart_dict)
            db.add(cart_db)
            await db.commit()
            await db.refresh(cart_db)

            return ResponseHandler.create_success("cart", cart_db.id, cart_db)
        except SQLAlchemyError as e:
            await db.rollback()
            return ResponseHandler.server_error(f"Database error: {str(e)}")

    @staticmethod
    async def get_cart(token: str, db: AsyncSession, cart_id: int):
        try:
            user = await CartService.get_user_by_token(token, db)

            # Fetch cart
            result = await db.execute(
                select(Cart).filter(Cart.id == cart_id, Cart.user_id == user.id)
            )
            cart = result.scalars().first()
            if not cart:
                return ResponseHandler.not_found_error("Cart", cart_id)

            return ResponseHandler.get_single_success("cart", cart_id, cart)
        except SQLAlchemyError as e:
            return ResponseHandler.server_error(f"Database error: {str(e)}")

    @staticmethod
    async def update_cart(token: str, db: AsyncSession, cart_id: int, cart: CartUpdate):
        try:
            user = await CartService.get_user_by_token(token, db)

            # Fetch the cart to update
            result = await db.execute(
                select(Cart).filter(Cart.id == cart_id, Cart.user_id == user.id)
            )
            db_cart = result.scalars().first()
            if not db_cart:
                return ResponseHandler.not_found_error("Cart", cart_id)

            # Clear existing cart items
            await db.execute(
                select(CartItem).filter(CartItem.cart_id == db_cart.id).delete()
            )

            # Add updated items
            total_amount = 0
            for item in cart.cart_items:
                product_id = item.product_id
                quantity = item.quantity

                # Validate product existence
                result = await db.execute(select(Product).filter(Product.id == product_id))
                product = result.scalars().first()
                if not product:
                    return ResponseHandler.not_found_error("Product", product_id)

                # Calculate subtotal
                subtotal = product.price * quantity * (1 - (product.discount_percentage / 100))
                total_amount += subtotal

                db.add(CartItem(cart_id=db_cart.id, product_id=product_id, quantity=quantity, subtotal=subtotal))

            db_cart.total_amount = total_amount
            await db.commit()
            await db.refresh(db_cart)

            return ResponseHandler.update_success("cart", db_cart.id, db_cart)
        except SQLAlchemyError as e:
            await db.rollback()
            return ResponseHandler.server_error(f"Database error: {str(e)}")

    @staticmethod
    async def delete_cart(token: str, db: AsyncSession, cart_id: int):
        try:
            user = await CartService.get_user_by_token(token, db)

            # Fetch cart with related cart items
            result = await db.execute(
                select(Cart)
                .options(joinedload(Cart.cart_items))
                .filter(Cart.id == cart_id, Cart.user_id == user.id)
            )
            db_cart = result.scalars().first()
            if not db_cart:
                return ResponseHandler.not_found_error("Cart", cart_id)

            # Delete cart and its items
            for cart_item in db_cart.cart_items:
                await db.delete(cart_item)
            await db.delete(db_cart)
            await db.commit()

            return ResponseHandler.delete_success("cart", cart_id, db_cart)
        except SQLAlchemyError as e:
            await db.rollback()
            return ResponseHandler.server_error(f"Database error: {str(e)}")
