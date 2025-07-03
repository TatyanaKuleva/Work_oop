

def get_top_n_vacancies(vacancies, attribute, n=5, reverse=True):
    if not vacancies:
        return []

    if not hasattr(vacancies[0], attribute):
        raise AttributeError(f'{attribute} не найден')

    sorted_vacancies = sorted(vacancies, key=lambda x: getattr(x, attribute), reverse=reverse)
    return sorted_vacancies[:n]









