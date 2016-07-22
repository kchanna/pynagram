//
// Created by Keshav Channa on 22/07/16.
//

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include <ostream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <future>
#include <ctime>
#include <ratio>
#include <chrono>

#include "dictionary.h"

Dictionary*     g_dictionary = new Dictionary();

int readLine(FILE* file, char* pszLine, int buffer)
{
	int   iRead = 0;

	pszLine[0] = 0;

	if(feof(file))
	{
		return -2;
	}

	do {
		if(feof(file))
		{
			break;
		}

		size_t result = fread(&pszLine[iRead], 1, sizeof(char), file);
		if (result != 1) {
			if(feof(file))
			{
				return -1000;
			}
			std::cout << ("Read file error") << std::endl;
			break;
		}
		if('\r' == pszLine[iRead])
			continue;
		if('\n' == pszLine[iRead])  // end of line
			break;

		iRead++;
		if(iRead >= buffer) {
			break;
		}
	} while(1);

	pszLine[iRead] = 0;
	return iRead;
}


static void getProcessedWord(const char* pszStr, int wlen, char* pszStrProcessed)
{
	int   i;

	pszStrProcessed[0] = 0;
	std::vector<char> myvector (pszStr, pszStr+wlen);

	// using default comparison (operator <):
	std::sort (myvector.begin(), myvector.begin()+wlen);

	for(i=0;i<wlen;i++) {
		pszStrProcessed[i] = myvector[i];
	}
	pszStrProcessed[i] = 0;

	for(i=0;i<wlen;i++)
	{
		int _ch = pszStrProcessed[i];

		if(0 == _ch)    break;

		if(!((_ch >= 'a') && (_ch <= 'z')))
		{
			memcpy(&pszStrProcessed[i], &pszStrProcessed[i+1], wlen - i);
			pszStrProcessed[wlen - 1] = 0;
			i--;
			continue;
		}
		else
		{
			pszStrProcessed[i] = (char)_ch;
		}
	}
	pszStrProcessed[i] = 0;
}

static int validateWordEn(char* pszWord, int wlen)
{
	int i;

	for(i=0;i<wlen;i++)
	{
		int _ch = pszWord[i];

		if(0 == _ch)    break;

		if(isupper(_ch))
		{
			_ch = tolower(_ch);
		}

		if(((_ch >= 'a') && (_ch <= 'z')))
		{
			pszWord[i] = (char)_ch;
		}
		else
		{
			// ' is okay...
			if((_ch >= '\''))
			{
				pszWord[i] = (char)_ch;
			}
			else
			{
				break;
			}
		}
	}

	return (i >= wlen);
}

static int addToDictionaryEn(char* pszWord, int wlen)
{
	if(NULL == g_dictionary->pNodes)
	{
		g_dictionary->len = 26;
		g_dictionary->pNodes = new DictNode[g_dictionary->len];
		if(NULL == g_dictionary->pNodes)
		{
			return -3;
		}
	}
	// Validate word...
	if(1 != validateWordEn(pszWord, wlen)) {
		std::cout << "Failed to validate word (" << pszWord << ")" << std::endl;
		return -10;
	}

	int   i;
	int   index = pszWord[0] - 'a';
	DictEntry*  pOldEntries = g_dictionary->pNodes[index].pEntries;
	char  szProcessed[1024];

	getProcessedWord(pszWord, wlen, szProcessed);

	if(NULL != g_dictionary->pNodes[index].pEntries)
	{
		// New array..
		g_dictionary->pNodes[index].pEntries = new DictEntry[g_dictionary->pNodes[index].len + 1];
		// Copy over the previous array...
		for(i=0;i<g_dictionary->pNodes[index].len;i++)
		{
			g_dictionary->pNodes[index].pEntries[i] = pOldEntries[i];
			// We've copied over the pointer, we shouldn't release both..
			pOldEntries[i].Zero();
		}

		g_dictionary->pNodes[index].len = g_dictionary->pNodes[index].len + 1;
	}
	else {
		g_dictionary->pNodes[index].len = 1;
		g_dictionary->pNodes[index].pEntries = new DictEntry[g_dictionary->pNodes[index].len];
	}

	g_dictionary->pNodes[index].pEntries[g_dictionary->pNodes[index].len - 1].Assign(pszWord, szProcessed, wlen);

	if(pOldEntries) {
		delete []pOldEntries;
		pOldEntries = NULL;
	}
	return 0;
}

static int addToDictionary(const char* pszLang, char* pszWord, int wlen)
{
	return addToDictionaryEn(pszWord, wlen);
}


int processDictionary(const char* pszFilename)
{
	auto                t1 = std::chrono::high_resolution_clock::now();

	FILE*   file = fopen(pszFilename, "rb");
	if(NULL == file)
	{
		std::cout << "Failed to open dictionary file (" << pszFilename << ") for reading. " << std::endl;
		return -1;
	}

	do {
		char sz[1024];

		int ret = readLine(file, sz, sizeof(sz)/sizeof(sz[0]));
		if(-1000 == ret)  break;  // end of file
		if(ret < 0)       break;

		if(0 != addToDictionary("en-us", sz, ret))
		{
			std::cout << "Failed to add word (" << sz << ") from dictionary. " << std::endl;
			return -2;
		}
	} while(1);

	fclose(file);
	file = NULL;

	auto                t2 = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);

	std::cout << "Time taken for processing dictionary " << time_span.count() << " seconds" << std::endl;

	return 0;
}