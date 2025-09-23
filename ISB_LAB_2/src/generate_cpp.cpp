#include <iostream>
#include <fstream>
#include <string>

using namespace std;

string getInputFileCpp(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open " << filename << "!" << endl;
        return "";
    }

    string line;
    while (getline(file, line)) {
        // Удаляем пробелы и табы для упрощения поиска
        string cleaned_line;
        for (char c : line) {
            if (c != ' ' && c != '\t') {
                cleaned_line += c;
            }
        }

        // Ищем ключ input_file_cpp
        size_t pos = cleaned_line.find("\"input_file_cpp\":\"");
        if (pos != string::npos) {
            size_t start = pos + 16; // Длина "\"input_file_cpp\":\""
            size_t end = cleaned_line.find("\"", start);
            if (end != string::npos) {
                file.close();
                return cleaned_line.substr(start, end - start);
            }
        }
    }

    file.close();
    cerr << "Error: 'input_file_cpp' not found or has invalid format in " << filename << "!" << endl;
    return "";
}
