/**
 * Извлекает значение поля input_file_java из JSON-файла настроек
 *
 * Функция выполняет поиск значения по ключу "input_file_java" в файле settings.json.
 * Обрабатывает исключения ввода-вывода и случаи отсутствия требуемого поля.
 * В случае ошибки выводит сообщение в stderr и возвращает пустую строку.
 *
 * @param filename путь к файлу settings.json
 * @return значение поля input_file_java или пустая строка в случае ошибки
 */
public static String getInputFileJava(String filename) {
    try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
        String line;
        while ((line = reader.readLine()) != null) {
            // Ищем строку содержащую input_file_java
            if (line.contains("input_file_java")) {
                // Извлекаем значение между кавычками
                String[] parts = line.split("\"");
                for (int i = 0; i < parts.length - 1; i++) {
                    if (parts[i].contains("input_file_java")) {
                        return parts[i + 2]; // Значение после ключа
                    }
                }
            }
        }

        System.err.println("Error: 'input_file_java' not found in " + filename + "!");
        return "";

    } catch (IOException e) {
        System.err.println("Error: Could not read " + filename + "! " + e.getMessage());
        return "";
    }
}