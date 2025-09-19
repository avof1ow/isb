#include <iostream>
#include <random>
#include <bitset>
#include <fstream>
#include <string>

using namespace std;

string getInputFileCpp(const string& filename) {
	// парсер для извлечения значения поля input_file_cpp из settings.json
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open " << filename << "!" << endl;
        return "";
    }

    string content((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();

    // Ищем "input_file_cpp": "путь"
    string key = "\"input_file_cpp\": \"";
    size_t start = content.find(key);
    if (start == string::npos) {
        cerr << "Error: 'input_file_cpp' not found in " << filename << "!" << endl;
        return "";
    }

    start += key.length();
    size_t end = content.find("\"", start);
    if (end == string::npos) {
        cerr << "Error: Invalid format of 'input_file_cpp' in " << filename << "!" << endl;
        return "";
    }

    return content.substr(start, end - start);
}

void generateRandomSequenceCpp(const string& output_file) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);
	
    bitset<128> sequence;
    for (int i = 0; i < 128; ++i) {
        sequence[i] = dis(gen);
    }
	
    cout << "C++ Random Sequence: " << sequence << endl;
	
    ofstream out(output_file);
    if (out.is_open()) {
        out << sequence;
        out.close();
        cout << "Sequence saved to " << output_file << endl;
    } else {
        cerr << "Error: Could not save sequence to " << output_file << "!" << endl;
    }
}

int main() {
    string output_file = getInputFileCpp("settings.json");
    if (output_file.empty()) {
        return 1;
    }
    generateRandomSequenceCpp(output_file);
    return 0;
}