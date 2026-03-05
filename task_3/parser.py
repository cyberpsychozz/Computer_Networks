import csv

from playwright.sync_api import sync_playwright

login = ""
password = ""
city = "Москва"
vacancy = "Data science"
page_to_parse = 4

def save_to_csv(data):
    keys = data[0].keys() if data else []
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print("Данные сохранены в results.csv")

def register(page, login, password):
    page.goto("https://hh.ru/account/login?role=applicant&backurl=%2F&hhtmFrom=main")
    page.click('button[data-qa="submit-button"]')
    page.fill('input[data-qa="magritte-phone-input-national-number-input"]', login)
    page.click('button[data-qa="expand-login-by-password"]')
    page.fill('input[data-qa="applicant-login-input-password"]', password)
    page.click('button[data-qa="submit-button"]')

def set_search_parameters(page, city, vacancy):
    #vacancies params
    page.click('button[data-qa="geoSwitcher-button"]')
    page.fill('input[data-qa="geo-switcher-search"]', city)
    page.locator('[data-qa="cell-text-content"]:has-text("Москва")').first.click()
    page.fill('input[data-qa="search-input"]', vacancy)
    page.keyboard.press("Enter")

def parse_vacancies(page, page_to_parse):
    #parsing 
    results = []
    for pg in range(page_to_parse):
        page.wait_for_load_state("networkidle")

        items = page.query_selector_all('div[data-qa="vacancy-serp__vacancy"]')

        for item in items:
            vacancy_el = item.query_selector('[data-qa="serp-item__title"]')
            vacancy_name = vacancy_el.inner_text().strip() if vacancy_el else "N/A"

            company_el = item.query_selector('[data-qa="vacancy-serp__vacancy-employer"]')
            company_name = company_el.inner_text().strip() if company_el else "N/A"
            
            salary_el = item.query_selector('.compensation-labels--vwum2s12fQUurc2J span')
            salary = salary_el.inner_text().strip() if salary_el else "N/A"

            experience_el = item.query_selector('div[class*="magritte-tag__label"] span')
            experience = experience_el.inner_text().strip() if experience_el else "N/A"

            if salary == experience: salary = 'N/A'

            results.append( {
                "Company name" : company_name, 
                "vacancy name" : vacancy_name,
                "expirience" : experience, 
                "salary" : salary
            })
        
        next_page_number = str(pg + 2)
        next_button = page.locator(f'a[data-qa="pager-page"]:has-text("{next_page_number}")')
        if next_button.count() > 0:
            next_button.click()
            page.wait_for_load_state("networkidle")
        else:
            print("Страницы кончились")
            break
    return results

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless = False)
        context = browser.new_context()
        page = context.new_page()

        register(page, login, password)
        set_search_parameters(page, city, vacancy)
        parsed_data = parse_vacancies(page, page_to_parse)
        save_to_csv(parsed_data)

if __name__ == "__main__":
    main()