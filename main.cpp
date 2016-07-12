// C program to print all permutations with duplicates allowed
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include <ostream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <future>
#include <ctime>
#include <ratio>
#include <chrono>

struct Anagram
{
    int         r;
    int         nPr;

    std::chrono::high_resolution_clock::time_point      start_time, end_time;

    std::vector<std::string>    theStrings;

    Anagram()
    {
        r = nPr = -1;
    }
};


Anagram*     g_anagramData = NULL;

/* Function to swap values at two pointers */
inline void swap(char *x, char *y)
{
    char temp;
    temp = *x;
    *x = *y;
    *y = temp;
}

#define DO_SWAP(xx,yy)  {   char temp; temp = (*(xx));  (*(xx)) = (*(yy));   (*(yy)) = temp;  }

int g_found = 0;

/* Function to print permutations of string
   This function takes three parameters:
   1. String
   2. Starting index of the string
   3. Ending index of the string. */
void permute(const int theIndex, char *a, int n, int l, int r, int depth)
{
    int i;

		//printf("DEBUG: depth = %d, a = %s, l = %d, r = %d, \n", depth, a, l, r);
    if (l == r)
    {
	    char szCopy[512];

	    strncpy(szCopy, a, r);
	    szCopy[r] = 0;
	    //printf("%d. %s\n", ++g_found, szCopy);
        g_anagramData[theIndex].theStrings.push_back(szCopy);
    }
    else
    {
        for (i = l; i < n; i++)
        {
	        // do the swap
	        //printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            //swap((a+l), (a+i));
            DO_SWAP((a+l), (a+i));

            permute(theIndex, a, n, l+1, r, depth+1);

	        // undo the swap
	        //printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            //swap((a+l), (a+i)); //backtrack
            DO_SWAP((a+l), (a+i)); //backtrack
        }
    }

    if(0 == depth)
    {
        g_anagramData[theIndex].end_time = std::chrono::high_resolution_clock::now();
    }
}

// Takes the input string and removes special characters and spaces
void prepareString(char* in_str, int str_len)
{
    int i;

    for(i=0;i<str_len;i++)
    {
        int _ch = in_str[i];

        if(0 == _ch)    break;

        if(isupper(_ch))
        {
            _ch = tolower(_ch);
        }

        if(!((_ch >= 'a') && (_ch <= 'z')))
        {
            memcpy(&in_str[i], &in_str[i+1], str_len - i);
            in_str[str_len - 1] = 0;
            i--;
            continue;
        }
        else
        {
            in_str[i] = (char)_ch;
        }
    }
}

static int factorial(int number) {
    int temp;

    if(number <= 1) return 1;

    temp = number * factorial(number - 1);
    return temp;
}


bool canCreateNewThreads(const std::future<void>* threads, int nMaxIndex)
{
    int     i, nRunning = 0;
    const int nMaxThreadsToRunAtOnce = 4;

    for(i=0;i<nMaxIndex;i++)
    {
        auto ret = threads[i].wait_for(std::chrono::milliseconds(100));
        if(std::future_status::ready != ret)
        {
            nRunning++;

            if(nRunning > nMaxThreadsToRunAtOnce) {
                break;  // No need to check further...
            }
        }
    }

    // Run a maximum of "n" threads at a time..
    if(nRunning > nMaxThreadsToRunAtOnce) {
        return false;
    }

    return true;
}

void formWords(const char* in_str, int slen)
{
    auto                t1 = std::chrono::high_resolution_clock::now();
    int                 iLen = 0;
    std::future<void>*  threads = new std::future<void>[slen + 1];

    while(iLen < slen)
    {
        iLen++;

        g_anagramData[iLen - 1].r = iLen;
        g_anagramData[iLen - 1].nPr = factorial(slen) / factorial(slen - iLen);

        g_anagramData[iLen - 1].start_time = std::chrono::high_resolution_clock::now();

        char* str = new char[slen+1];
        strcpy(str, in_str);
        threads[iLen-1] = std::async(std::launch::async, permute, iLen-1, str, slen, 0, iLen, 0);

        while(true) {
            if(!canCreateNewThreads(threads, iLen-1))
            {
                std::this_thread::sleep_for(std::chrono::seconds(1));
            }
            else
            {
                break;
            }
        }
    }

    iLen = 0;
    while(iLen < slen)
    {
        iLen++;

        threads[iLen-1].get();

        std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(g_anagramData[iLen - 1].end_time - g_anagramData[iLen - 1].start_time);

        std::cout << "Time taken for generating words of (nPr) " << slen << "P" << iLen << " of " <<
                g_anagramData[iLen - 1].nPr << " words, is " << time_span.count() << " seconds" << std::endl;
    }

    auto t2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);

    std::cout << std::endl << "      Total Time taken for generating all words is " << time_span.count() << " seconds" << std::endl;
}


/* Driver program to test above functions */
int main()
{
    char str[] = "ABCD__*&EFGH345IJK";
    //char str[] = "ABCDEFG";
    int n = strlen(str);

    std::cout << "String before preparing: " << str << std::endl;
    prepareString(str, n);
    std::cout << "String after preparing: " << str << std::endl;
    n = strlen(str);

    g_anagramData = new Anagram[n+1];



    formWords(str, n);



    //permute(str, n, 0, 3, 0);
    return 0;
}