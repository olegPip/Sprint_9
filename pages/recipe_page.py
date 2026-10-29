
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.recipes_page_locators import RecipesPageLocators
from config.urls import URLS
from pathlib import Path
import random
import allure


class RecipesPage(BasePage):
    TAG_LOCATORS = [
        RecipesPageLocators.TAG_BREAKFAST,
        RecipesPageLocators.TAG_LUNCH,
        RecipesPageLocators.TAG_DINNER,
    ]

    @allure.step("Открыть страницу создания рецепта")
    def open_create_recipe_page(self):
        self.open(URLS.CREATE_RECIPE)

    @allure.step("Ввести название рецепта: {name}")
    def enter_recipe_name(self, name):
        self.input_text(RecipesPageLocators.NAME_RECIPE, name)

    @allure.step("Выбрать тег")
    def select_random_tag(self):
        random_tag = random.choice(self.TAG_LOCATORS)
        self.click(random_tag)

    @allure.step("Добавить ингредиент: {name}, количество: {qnt}")
    def add_ingredient(self, name, qnt):
        from selenium.webdriver.common.keys import Keys
        import time

        # 1. Ждем поле ввода, кликаем и очищаем его
        input_field = self.wait.until(
            EC.element_to_be_clickable(RecipesPageLocators.INGREDIENT_NAME)
        )
        input_field.click()
        input_field.clear()
        time.sleep(0.3)

        # 2. Вводим имя ингредиента (например, 'банан')
        input_field.send_keys(name)

        # 3. Принудительно вызываем событие фильтрации во фронтенде
        input_field.send_keys(Keys.SPACE)
        time.sleep(0.1)
        input_field.send_keys(Keys.BACKSPACE)

        # 4. Даем списку раскрыться
        time.sleep(1.0)

        # 5. Ищем подсказку
        suggestion_locator = RecipesPageLocators.choosing_an_ingredient(name)
        suggestion = self.wait.until(
            EC.presence_of_element_located(suggestion_locator),
            message=f"Не найдено предложения для ингредиента {name}"
        )

        # 6. Кликаем через JavaScript (это сработает, даже если элемент перекрыт или невидим для обычного клика)
        self.driver.execute_script("arguments[0].click();", suggestion)
        time.sleep(0.3)

        # 7. Заполняем количество
        quantity_field = self.find_visible_element(RecipesPageLocators.QUANTITY_INGREDIENT)
        quantity_field.click()
        quantity_field.clear()
        quantity_field.send_keys(str(qnt))
        time.sleep(0.2)

        # 8. Фиксируем ингредиент
        self.click(RecipesPageLocators.ADD_INGREDIENT)
        time.sleep(0.5)

    def add_ingredients(self, ingredients: list[dict]):
        for item in ingredients:
            self.add_ingredient(item["name"], item["qnt"])

    @allure.step("Ввести время приготовления: {time}")
    def enter_cooking_time(self, time):
        self.input_text(RecipesPageLocators.COOKING_TIME, time)

    @allure.step("Ввести описание рецепта: {text}")
    def enter_description(self, text):
        self.input_text(RecipesPageLocators.RECIPE_DESCRIPTION, text)

    @allure.step("Загрузить изображение: {file_name}")
    def upload_image(self, file_name):
        from selenium.webdriver.remote.file_detector import LocalFileDetector  # Импортируем детектор

        file_path = Path(__file__).parent.parent / "assets" / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_name} не найден по пути {file_path}")

        # Говорим драйверу, что файл нужно загрузить с локальной машины в контейнер
        self.driver.file_detector = LocalFileDetector()

        file_input = self.find_element(RecipesPageLocators.IMAGE_INPUT)
        file_input.send_keys(str(file_path.resolve()))

    @allure.step("Нажать кнопку 'Создать рецепт'")
    def click_create_recipe_button(self):
        self.click(RecipesPageLocators.CREATE_RECIPE_BTN)

    @allure.step("Создать рецепт: {name}")
    def create_recipe(
        self, name, ingredients, cooking_time, description, image_file="omlet.jpg"
    ):
        self.open_create_recipe_page()
        self.enter_recipe_name(name)
        self.select_random_tag()
        self.add_ingredients(ingredients)
        self.enter_cooking_time(cooking_time)
        self.enter_description(description)
        self.upload_image(image_file)
        self.click_create_recipe_button()

    @allure.step("Проверить, что рецепт с названием '{expected_title}' отображается")
    def wait_for_recipe_to_load(self, expected_title: str, timeout: int = 15) -> bool:
        try:
            self.wait.until(
                lambda d: self.find_visible_element(
                    RecipesPageLocators.RECIPE_TITLE
                ).text.strip()
                == expected_title,
                message=f"Не найден рецепт с названием '{expected_title}' за {timeout} секунд",
            )
            return True
        except Exception:
            return False