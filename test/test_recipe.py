from pathlib import Path
import allure
from pages.recipe_page import RecipesPage
from data.test_data import RECIPE


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ABS_IMAGE_PATH = str(PROJECT_ROOT / "assets" / RECIPE['image'])


@allure.title("Успешное добавление нового рецепта")
def test_create_recipe_success(authenticated_user):
    recipes_page = RecipesPage(authenticated_user)

    recipes_page.create_recipe(
        name=RECIPE["name"],
        ingredients=RECIPE["ingredients"],
        cooking_time=str(RECIPE["time"]),
        description=RECIPE["description"],
        image_file=ABS_IMAGE_PATH
    )

    assert recipes_page.wait_for_recipe_to_load(RECIPE['name']), f"Рецепт '{RECIPE['name']}' не отображается на странице"
