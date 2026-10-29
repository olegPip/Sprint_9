import allure
from pages.recipe_page import RecipesPage
from data.test_data import RECIPE


@allure.feature("Создание рецепта")
class TestCreateRecipe:
    @allure.title("Тест: успешное создание рецепта авторизованным пользователем")
    @allure.description(
        "1. Создать рецепт с ингредиентами и фото.\n"
        "2. Проверить отображение карточки и совпадение названия."
    )
    def test_create_recipe(self, authenticated_user):
        recipes_page = RecipesPage(authenticated_user)
        recipes_page.create_recipe(
            name=RECIPE["name"],
            ingredients=RECIPE["ingredients"],
            cooking_time=str(RECIPE["time"]),
            description=RECIPE["description"],
            image_file="omlet.jpg",
        )
        assert recipes_page.wait_for_recipe_to_load(RECIPE["name"])