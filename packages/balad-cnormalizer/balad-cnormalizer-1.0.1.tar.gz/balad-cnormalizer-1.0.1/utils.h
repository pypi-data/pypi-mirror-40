//
// Created by amir on 12/25/18.
//

#ifndef NORMALIZER_UTILS_H
#define NORMALIZER_UTILS_H

#include <bits/stdc++.h>
using namespace std;

map<wchar_t, wchar_t> CHARACTER_REPLACE_DICT = {
	{wchar_t(8204), wchar_t(32)},  // half-space -> space
	{wchar_t(8205), wchar_t(0)},  // half-space -> space
	{wchar_t(1571), wchar_t(1575)},  // أ -> ا
	{wchar_t(1573), wchar_t(1575)},  // إ -> ا
	{wchar_t(1577), wchar_t(1607)},  // ة -> ه
	{wchar_t(1603), wchar_t(1705)},  // ك -> ک
	{wchar_t(1609), wchar_t(1740)},  // ى -> ی
	{wchar_t(1610), wchar_t(1740)},  // ي -> ی
	{wchar_t(1726), wchar_t(1607)},  // ھ -> ه
	{wchar_t(233), wchar_t(101)},  // e <- é
	{L'1', L'۱'},
	{L'2', L'۲'},
	{L'3', L'۳'},
	{L'4', L'۴'},
	{L'5', L'۵'},
	{L'6', L'۶'},
	{L'7', L'۷'},
	{L'8', L'۸'},
	{L'9', L'۹'},
	{L'0', L'۰'},
};

inline wstring normalize_characters(wstring raw_string) {
	wstring normalized_string;
	if (!raw_string.empty()) 
		for(wchar_t character: raw_string) {
			if (CHARACTER_REPLACE_DICT.find(character) != CHARACTER_REPLACE_DICT.end()) {
				if(int(CHARACTER_REPLACE_DICT[character]))
					normalized_string += CHARACTER_REPLACE_DICT[character];
			}
			else
				normalized_string += character;
		}
	return normalized_string;
}

inline wchar_t normalize_characters(wchar_t raw_char) {
	wstring raw_string;
	raw_string  += raw_char;
	return normalize_characters(raw_string)[0];
}

map<wstring, int> _WORD_NUMBER_MAP = {
	{normalize_characters(L"صفر"), 0},
	{normalize_characters(L"یک"), 1},
	{normalize_characters(L"اول"), 1},
	{normalize_characters(L"دو"), 2},
	{normalize_characters(L"سه"), 3},
	{normalize_characters(L"سوم"), 3},
	{normalize_characters(L"چهار"), 4},
	{normalize_characters(L"پنج"), 5},
	{normalize_characters(L"شش"), 6},
	{normalize_characters(L"شیش"), 6},
	{normalize_characters(L"هفت"), 7},
	{normalize_characters(L"هف"), 7},
	{normalize_characters(L"هشت"), 8},
	{normalize_characters(L"هش"), 8},
	{normalize_characters(L"نه"), 9},
	{normalize_characters(L"ده"), 10},
	{normalize_characters(L"یازده"), 11},
	{normalize_characters(L"دوازده"), 12},
	{normalize_characters(L"سیزده"), 13},
	{normalize_characters(L"سینزده"), 13},
	{normalize_characters(L"سینزه"), 13},
	{normalize_characters(L"چهارده"), 14},
	{normalize_characters(L"چارده"), 14},
	{normalize_characters(L"پانزده"), 15},
	{normalize_characters(L"پونزده"), 15},
	{normalize_characters(L"پانزه"), 15},
	{normalize_characters(L"پونزه"), 15},
	{normalize_characters(L"شانزده"), 16},
	{normalize_characters(L"شونزده"), 16},
	{normalize_characters(L"شانزه"), 16},
	{normalize_characters(L"شونزه"), 16},
	{normalize_characters(L"هفده"), 17},
	{normalize_characters(L"هیفده"), 17},
	{normalize_characters(L"هیوده"), 17},
	{normalize_characters(L"هوده"), 17},
	{normalize_characters(L"هجده"), 18},
	{normalize_characters(L"هیجده"), 18},
	{normalize_characters(L"هژده"), 18},
	{normalize_characters(L"هیژده"), 18},
	{normalize_characters(L"نوزده"), 19},
	{normalize_characters(L"نونزده"), 19},
	{normalize_characters(L"نوزه"), 19},
	{normalize_characters(L"بیست"), 20},
	{normalize_characters(L"سی"), 30},
	{normalize_characters(L"چهل"), 40},
	{normalize_characters(L"پنجاه"), 50},
	{normalize_characters(L"شست"), 60},
	{normalize_characters(L"شصت"), 60},
	{normalize_characters(L"هفتاد"), 70},
	{normalize_characters(L"هشتاد"), 80},
	{normalize_characters(L"نود"), 90},
	{normalize_characters(L"صد"), 100},
	{normalize_characters(L"یکصد"), 100},
	{normalize_characters(L"دویست"), 200},
	{normalize_characters(L"سیصد"), 300},
	{normalize_characters(L"چهارصد"), 400},
	{normalize_characters(L"پانصد"), 500},
	{normalize_characters(L"پونصد"), 500},
	{normalize_characters(L"ششصد"), 600},
	{normalize_characters(L"شیشصد"), 600},
	{normalize_characters(L"شونصد"), 600},
	{normalize_characters(L"هفتصد"), 700},
	{normalize_characters(L"هفصد"), 700},
	{normalize_characters(L"هشتصد"), 800},
	{normalize_characters(L"هشصد"), 800},
	{normalize_characters(L"نهصد"), 900},
	{normalize_characters(L"هزار"), 1000},
	{normalize_characters(L"یکهزار"), 1000},
};
map<wstring, int> _SMALL_NUMBER_MAP = {
	{normalize_characters(L"یک"), 1},
	{normalize_characters(L"دو"), 2},
	{normalize_characters(L"سه"), 3},
	{normalize_characters(L"سوم"), 3},
	{normalize_characters(L"چهار"), 4},
	{normalize_characters(L"چار"), 4},
	{normalize_characters(L"پنج"), 5},
	{normalize_characters(L"شش"), 6},
	{normalize_characters(L"شیش"), 6},
	{normalize_characters(L"هفت"), 7},
	{normalize_characters(L"هف"), 7},
	{normalize_characters(L"هشت"), 8},
	{normalize_characters(L"هش"), 8},
	{normalize_characters(L"نه"), 9}
};
vector<wstring> _EXCEPTIONS = {normalize_characters(L"سیم"),
	normalize_characters(L"سیمین"),
	normalize_characters(L"اولم"),
	normalize_characters(L"اولمین"),
};
map<wstring, int> _SEPARATORS = {
	{normalize_characters(L"صد"), 100},
	{normalize_characters(L"هزار"), 1000},
	{normalize_characters(L"میلیون"), 1000000}
};
wstring _SAD = normalize_characters(L"صد");
vector<wstring> _PERSIAN_OMS = {normalize_characters(L"ام"), normalize_characters(L"امین")};
wstring _PERSIAN_AND = normalize_characters(L"و");
wstring _hezar = normalize_characters(L"هزار");

template<class T>
inline string to_str(T x) {
	stringstream ss;
	ss << x;
	string s;
	ss >> s;
	return s;
}

template<class T>
inline wstring to_wstr(T x) {
	wstringstream ss;
	ss << x;
	wstring s;
	ss >> s;
	return s;
}


inline wstring strip(wstring s) {
	int h = 0, t = (int)s.size();
	while(h < t && s[h] == L' ')
		++ h;
	while(t > h && s[t-1] == L' ')
		-- t;
	return s.substr(h, t-h);
}

inline vector<wstring> split(wstring s, wchar_t d = L' ', bool ignore_empty=true) {
	vector<wstring> v;
	wstring cur = L"";
	s += d;
	for(wchar_t c: s) {
		if(c != d)
			cur += c;
		else {
			if(!cur.empty() || !ignore_empty)
				v.push_back(cur);
			cur = L"";
		}
	}
	return v;
}

inline bool startswith(wstring s, wstring t) {
	return s.find(t) == 0;
}

inline bool endswith(wstring s, wstring t) {
	wstring rs = s, rt = t;
	reverse(rs.begin(), rs.end());
	reverse(rt.begin(), rt.end());
	return startswith(rs, rt);
}

inline wstring join(wchar_t d, vector<wstring> list) {
	wstring res = L"";
	for(int i = 0; i < list.size(); ++ i) {
		if (i)
			res += d;
		res += list[i];
	}
	return res;
}



wchar_t _MIM = L'م', _ALEF = L'ا', _NUN = L'ن', _YE = normalize_characters(L'ی');
wstring remove_tail(wstring word) {
	int len = word.size();
	if (len >= 4 and word[len-1] == _NUN and word[len-2] == _YE and word[len-3] == _MIM and word[len-4] == _ALEF)
		return word.substr(0, len-4);
	if (len >= 3 and word[len - 1] == _NUN and word[len - 2] == _YE and word[
			len - 3] == _MIM)
		return word.substr(0, len - 3);
	if (len >= 2 and word[len-1] == _MIM and word[len-2] == _ALEF)
		return word.substr(0, len-2);
	if (len >= 1 and word[len-1] == _MIM)
		return word.substr(0, len-1);

	return word;
}

wstring endings[] = {normalize_characters(L"امین"), normalize_characters(L"ام"), normalize_characters(L"م"), normalize_characters(L"مین")};

wstring remove_tail_old(wstring input_word){
	wstring rw = input_word;
	reverse(rw.begin(), rw.end());
	for(wstring e: endings) {
		wstring re = e;
		reverse(re.begin(), re.end());
		if (rw.find(re) == 0)
			return input_word.substr(0, input_word.size() - e.size());
	}

	return input_word;
}

bool is_a_number_with_hezar(wstring word) {
	if (word.size() > 1 && endswith(word, _hezar)) {
		wstring word_trimmed = word.substr(0, word.size() - _hezar.size());
		return _WORD_NUMBER_MAP.find(word_trimmed) != _WORD_NUMBER_MAP.end();
	}
	return false;
}

bool is_a_number_with_persian_and(wstring word) {
	if (word.size() > 1 && endswith(word, _PERSIAN_AND)) {
		wstring word_trimmed = word.substr(0, word.size() - 1);
		return _WORD_NUMBER_MAP.find(word_trimmed) != _WORD_NUMBER_MAP.end();
	}
	return false;
}

bool is_a_number_with_persian_and_at_first(wstring word) {
	if (word.size() > 1 && startswith(word, _PERSIAN_AND)) {
		wstring word_trimmed = remove_tail(word.substr(1));
		return _WORD_NUMBER_MAP.find(word_trimmed) != _WORD_NUMBER_MAP.end();
	}

	return false;
}


#endif //NORMALIZER_UTILS_H
