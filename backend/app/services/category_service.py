from fastapi import HTTPException

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate


class CategoryService:

    @staticmethod
    async def create(category: CategoryCreate):
        print(" CategoryService.create() started")

        # Check duplicate category
        existing_category = await CategoryRepository.get_by_name(
            category.name
        )

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        # Create category object
        new_category = Category.create(
            name=category.name,
            description=category.description
        )

        # Save category
        category_id = await CategoryRepository.create(
            new_category
        )

        return {
            "message": "Category created successfully",
            "category_id": category_id
        }

    @staticmethod
    async def get_all():
        return await CategoryRepository.get_all()

    @staticmethod
    async def get_by_id(category_id: str):

        category = await CategoryRepository.get_by_id(
            category_id
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        return category
    @staticmethod
    async def update(
        category_id: str,
        category: CategoryCreate
    ):
        existing_category = await CategoryRepository.get_by_id(
            category_id
        )

        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        duplicate = await CategoryRepository.get_by_name(
            category.name
        )

        if (
            duplicate
            and str(duplicate["_id"]) != category_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        updated_category = {
            "name": category.name,
            "description": category.description
        }

        await CategoryRepository.update(
            category_id,
            updated_category
        )

        return {
            "message": "Category updated successfully"
        }

    @staticmethod
    async def delete(category_id: str):

        existing_category = await CategoryRepository.get_by_id(
            category_id
        )

        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        await CategoryRepository.delete(category_id)

        return {
            "message": "Category deleted successfully"
        }