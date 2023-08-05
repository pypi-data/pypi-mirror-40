#include <Python.h>
#include <bits/stdc++.h>
#include "utils.h"

using namespace std;

wstring replace_persian_number_string_with_english_number(wstring str) {
	vector<wstring> words = split(strip(str));
	vector<wstring> words_trimmed;
	for(wstring w: words)
		words_trimmed.push_back(remove_tail(w));

	vector<wstring> result;

	int total_sum = 0;
	int index = 0;
	int summation = 0;
	bool inside_a_number = false;
	int SADed = 0;
	while (index < words.size()){

		wstring input_word = words[index];
		wstring input_word_trimmed = words_trimmed[index];

		// Handle the exception word 'sevvom'
		if (input_word == normalize_characters(L"سوم")) {
			input_word = normalize_characters(L"سهم");  // "seh'om"
			input_word_trimmed = normalize_characters(L"سه");
		}

		// Check to see if the word is a number attach to word "hezar"
		if (is_a_number_with_hezar(input_word)) {
			wstring new_word = input_word.substr(0, input_word.size() - _hezar.size());

			// split hezar and number سبصدهزار => سیصد هزار
			// insert hezar
			words.insert(words.begin() + index + 1, _hezar);
			words_trimmed.insert(words_trimmed.begin() + index + 1, _hezar);

			// remove hezar from current word
			words[index] = new_word;

			// Update current inputs
			input_word = new_word;
			input_word_trimmed = remove_tail(input_word);
		}

		// Check to see if the word is a number attach to a persian "and"
		if (is_a_number_with_persian_and(input_word)) {
			wstring new_word = input_word.substr(0, input_word.size() - 1);

			// Insert a persian "and" in the lists
			words.insert(words.begin() + index + 1, _PERSIAN_AND);
			words_trimmed.insert(words_trimmed.begin() + index + 1, _PERSIAN_AND);

			// Update current inputs
			input_word = new_word;
			input_word_trimmed = remove_tail(input_word);
		}
		if (is_a_number_with_persian_and_at_first(input_word)) {
			wstring new_word = input_word.substr(1);
			wstring next_word_trimmed = remove_tail(input_word.substr(1));

			// Insert a persian "and" in the lists
			words.insert(words.begin() + index + 1, new_word);
			words[index] = _PERSIAN_AND;

			words_trimmed.insert(words_trimmed.begin() + index + 1, next_word_trimmed);
			words_trimmed[index] = _PERSIAN_AND;

			// Update current inputs
			input_word = words_trimmed[index];
			input_word_trimmed = remove_tail(input_word);
		}
		// Set the next words
		wstring next_word, next_word_trimmed;
		if (index != (int)words.size() - 1) {
			next_word = words[index + 1];
			next_word_trimmed = words_trimmed[index + 1];
		}

		// Check to see if the word is a number before "صد" like نه صد => نهصد
		if (_SMALL_NUMBER_MAP.find(input_word) != _SMALL_NUMBER_MAP.end() && _SAD.find(next_word_trimmed) != -1 && next_word_trimmed != L"") {
			next_word = input_word + next_word;
			next_word_trimmed = remove_tail(next_word);

			input_word = L"";
			input_word_trimmed = L"";
			if (index != words.size() - 1) {
				words[index + 1] = next_word;
				words_trimmed[index + 1] = next_word_trimmed;
				words[index] = L"";
				words_trimmed[index] = L"";
			}
			SADed = 1;
		}
		bool inside_a_number;

		if (find(_EXCEPTIONS.begin(), _EXCEPTIONS.end(), input_word) != _EXCEPTIONS.end()) {
			inside_a_number = false;
			index += 1;
		}

		else if (_SEPARATORS.find(input_word) != _SEPARATORS.end()) {
			inside_a_number = true;

			if (summation == 0)  // for cases like 'hezar o yek'
				summation = 1;

			int multiplier = _SEPARATORS[input_word];

			// Handle 'سی صد'
			if (summation == 30 && multiplier == 100)
				multiplier = 10;

			summation *= multiplier;
			total_sum += summation;
			summation = 0;
			index ++;
		}

		else if (_WORD_NUMBER_MAP.find(input_word_trimmed) != _WORD_NUMBER_MAP.end()) {
			inside_a_number = true;
			summation += _WORD_NUMBER_MAP[input_word_trimmed];
			index += 1;
		}

		else if (input_word == _PERSIAN_AND){
			// Handle cases like these:
			//    'panj va do' --> '5 va 2'
			//    'panjah va do' --> '52'
			if (_WORD_NUMBER_MAP.find(next_word_trimmed) != _WORD_NUMBER_MAP.end()) {
				int next_int = _WORD_NUMBER_MAP[next_word_trimmed];
				if (summation > 0 && to_str(summation).size() <= to_str(next_int).size())
					inside_a_number = false;
			}

			index += 1;
		}

		else if (words[index].empty() && SADed == 1) {
			inside_a_number = true;
			index += 1;
		}

		else {
			inside_a_number = false;
			index += 1;
		}

		bool can_append_word = true;

		if (inside_a_number && (input_word != input_word_trimmed || find(_PERSIAN_OMS.begin(), _PERSIAN_OMS.end(), next_word) != _PERSIAN_OMS.end())){
			if (find(_PERSIAN_OMS.begin(), _PERSIAN_OMS.end(), next_word) != _PERSIAN_OMS.end())
				index += 1;  // Bypass the persian OM

			inside_a_number = false;
			can_append_word = false;
		}

		// Decide what to add to the result
		if (!inside_a_number or index > (int)words.size() - 1) {
			total_sum += summation;
			if (total_sum > 0) {
				result.push_back(to_wstr(total_sum));
				total_sum = 0;
				summation = 0;
			}

			if (!inside_a_number && can_append_word)
				result.push_back(input_word);
		}
	}

	return strip(join(L' ', result));
}

static PyObject * rpnswen_wrapper(PyObject * self, PyObject * args) {
	Py_UNICODE * input;
	wstring result;
	PyObject * ret;

	// parse arguments
	if (!PyArg_ParseTuple(args, "u", &input)) {
		return NULL;
	}

	// run the actual function
	result = replace_persian_number_string_with_english_number((wstring)input);
	// build the resulting string into a Python object.
	ret = PyUnicode_FromWideChar(result.c_str(), wcslen(result.c_str()));

	return ret;
}

static PyMethodDef NormMethods[] = {
	{ "replace_persian_number_string_with_english_number", rpnswen_wrapper, METH_VARARGS, "replace persian number string with digits" },
	{ NULL, NULL, 0, NULL }
};
static struct PyModuleDef cnormalizer_module = {
    PyModuleDef_HEAD_INIT,
    "cnormalizer",
    "C Normalizer", 
    -1,       
    NormMethods
};
PyMODINIT_FUNC PyInit_cnormalizer(void) {
	PyModule_Create(&cnormalizer_module);
}



int main(){
	wcout << replace_persian_number_string_with_english_number(L"آرین") << endl;
	/*wstring text = L"هفت هزار و هشتصد و نود و سوم هفت هزار و هشتصد و نود و سوم هفت هزار و هشتصد و نود و سوم هفت هزار و هشتصد و نود و سوم هفت هزار و هشتصد و نود و سوم شعشع رشذرشس ضص شراسی هفت هزار و هشتصد و نود و سوم تسیرتنذری سیرانذرسیرذسی رسیتنرذسیتنرذسیتنر سیرتنسیذرتنضذ۳ب رلعرضصنذترنضص ضاغیضصانذ یرمسیکرسیرنمکسی رسینمرادسردسیر سیتنمرسیتنمرسیتنمذرسی رسیتنرسیتنرذستنیرگ رسیهحرسیاهخرسهخیحراهخصثرخ صثخحرصثخحرتصثخحرس یرتمسیارتنمسیرنمسیر ضصباهخرضتذرمذثرخمصثر صرتنمسیرتنمسیتنرسی رضهخصرذضخذرضصر هفت هزار و هشتصد و نود و سوم هفت هزار و هشتصد و نود و سومتصرعخصثذعرصثذهخر هفت هزار و هشتصد و نود و سومهخراقثذتنصث رصثپدر ص ثر هصت ذهصثبرهصرذصثهذعرذصثذعهرصثذعه هزار صثرعخرذعهصثذعخرصثعهخلرذعخصثذعخرصثذعخرعخصثذعهخرذصعخثذعخرصثذعخرهخصثاهحبضحصخبذهرذخسیرذهخیذهخرسیخذرذهخسی";
	  wstringstream ss;
	  ss << text;
	  wstring word;
	  vector<wstring> words;
	  while(ss >> word)
	  words.push_back(word);
	  clock_t beg = clock();
	  for(int i = 0; i < 1000; ++ i) {
	  for(wstring word: words)
	  remove_tail(word);
	  }
	  clock_t end = clock();
	  cout << (double)(end - beg) / CLOCKS_PER_SEC << endl;*/
	


}
