def analyze_stock(data):
    if not data:
        return "Нет данных для анализа."
    
    result = "📊 Анализ остатков:\n"
    for item in data[:10]:  # Показываем первые 10 товаров
        name = item.get("nm", "Без названия")
        size = item.get("size", "N/A")
        qty = item.get("quantity", 0)
        result += f"{name} | Размер: {size} | Остаток: {qty}\n"
    return result
