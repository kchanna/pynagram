//
// Created by Keshav Channa on 22/07/16.
//

#ifndef GENERATEWORDS_DICTIONARY_H
#define GENERATEWORDS_DICTIONARY_H

#include <iostream>     // std::cout
#include <algorithm>    // std::sort
#include <vector>       // std::vector

struct DictEntry
{
		char*     pszStr;
		char*     pszStrProcessed;
		int       len;  // string length
public:

		void Zero()
		{
			pszStr = NULL;
			pszStrProcessed = NULL;
			len = 0;
		}
		void Assign(const char* psz, const char* _pszProcessed_, int wlen)
		{
			pszStr = new char[wlen+1];
			pszStrProcessed = new char[wlen+1];
			len = wlen;

			strcpy(pszStr, psz);
			strcpy(pszStrProcessed, _pszProcessed_);
		}

		DictEntry()
		{
			pszStr = NULL;
			pszStrProcessed = NULL;
			len = 0;
		}
};

struct DictNode
{
		DictEntry*  pEntries;
		int         len;

public:

		DictNode()
		{
			pEntries = NULL;
			len = 0;
		}
};

struct Dictionary
{
	DictNode*     pNodes; // array
	int           len;

public:

	Dictionary()
	{
		pNodes = NULL;
		len = 0;
	}
};


int processDictionary(const char* pszFilename);

#endif //GENERATEWORDS_DICTIONARY_H
