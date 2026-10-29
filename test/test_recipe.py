import os
from pathlib import Path
import allure
from pages.recipe_page import RecipesPage

RECIPE = {
    'name': 'Омлет',
    'tags': [0],
'ingredients': [
    {'name': 'яйца', 'qnt': 2},
    {'name': 'молоко', 'qnt': 50},
    {'name': 'сливочное масло', 'qnt': 10}
],
'time': 15,
'description': 'Яйца разбиваем в миску, добавляем молоко и соль по вкусу. Взбиваем смесь. Растапливаем сливочное масло на сковороде, выливаем яичную смесь и готовим на слабом огне 5-7 минут до готовности.',
'image': 'image1.jpg'
}

class TestCreateRecipe:

    @allure.title("Тест: успешное создание рецепта авторизованным пользователем")
    @allure.description(
        "1. Создать рецепт с ингредиентами и фото.\n"
        "2. Проверить отображение карточки и совпадение названия."
    )
    def test_create_recipe(self, authenticated_user):  # <-- Внутри класса self ОБЯЗАТЕЛЕН
        recipes_page = RecipesPage(authenticated_user)

        # Находим корень проекта (Sprint_9) независимо от окружения
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent

        # Вычисляем железный путь к картинке
        if (project_root / "assets" / "image1.jpg").exists():
            abs_image_path = str(project_root / "assets" / "image1.jpg")
        elif (project_root / "image1.jpg").exists():
            abs_image_path = str(project_root / "image1.jpg")
        else:
            abs_image_path = str(current_dir / "image1.jpg")

        recipes_page.create_recipe(
            name=RECIPE["name"],
            ingredients=RECIPE["ingredients"],
            cooking_time=str(RECIPE["time"]),
            description=RECIPE["description"],
            image_file=abs_image_path,
        )
        assert recipes_page.wait_for_recipe_to_load(RECIPE["name"])
