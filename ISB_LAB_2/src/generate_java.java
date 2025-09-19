import java.util.Random;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.io.File;
import java.io.IOException;

public class RandomSequenceJava {
    // Простой парсер для извлечения значения поля input_file_java из settings.json
    public static String getInputFileJava(String filename) {
        try {
            // Читаем весь файл в строку
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            StringBuilder content = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line.trim()); // Удаляем лишние пробелы и переносы строк
            }
            reader.close();

            // Ищем "input_file_java": "путь"
            String key = "\"input_file_java\": \"";
            int start = content.indexOf(key);
            if (start == -1) {
                System.err.println("Error: 'input_file_java' not found in " + filename + "!");
                return "";
            }

            start += key.length();
            int end = content.indexOf("\"", start);
            if (end == -1) {
                System.err.println("Error: Invalid format of 'input_file_java' in " + filename + "!");
                return "";
            }

            // Извлекаем путь и заменяем слэши для Windows
            String path = content.substring(start, end);
            return path.replace("/", "\\"); // Для совместимости с Windows
        } catch (IOException e) {
            System.err.println("Error: Could not read " + filename + "! " + e.getMessage());
            return "";
        }
    }

    public static void generateRandomSequenceJava(String outputFile) {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        // Генерация 128 бит
        for (int i = 0; i < 128; i++) {
            sequence.append(rand.nextInt(2)); // 0 или 1
        }

        // Вывод в консоль
        System.out.println("Java Random Sequence: " + sequence);

        // Создаем директорию, если она не существует
        File file = new File(outputFile);
        File parentDir = file.getParentFile();
        if (parentDir != null && !parentDir.exists()) {
            parentDir.mkdirs(); // Создаем папку output/, если нужно
        }

        // Сохранение в файл
        try {
            PrintWriter out = new PrintWriter(file);
            out.println(sequence);
            out.close();
            System.out.println("Sequence saved to " + outputFile);
        } catch (IOException e) {
            System.err.println("Error: Could not save sequence to " + outputFile + "! " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        // Читаем путь из settings.json
        String outputFile = getInputFileJava("settings.json");
        if (outputFile.isEmpty()) {
            System.exit(1);
        }

        generateRandomSequenceJava(outputFile);
    }
}