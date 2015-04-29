#include <string>
#include <iostream>
#include <cstdlib>
#include <cstdio>
#include "NaiveSuffixTree.h"
#include "SuffixTreeQuerier.h"

#include <chrono>


int main(int argc, const char *argv[]) {
    NaiveSuffixTree t("bananas$");
    t.display();

    SuffixTreeQuerier stq(t);
    SuffixTreeQuerier::location loc = stq.find("an");

    std::cout << loc.first << "," << loc.second << std::endl;

    //std::string s("AdsjakdjsakjdKASJDkasjdkjaskdjKASJdkasJDkajskdjaSKdjkasjdkASJdkajsdkjASKdjaksjdkasjdkajsdkjaskdjaksdjiweqjdioajwdisajdkasjkdasjk$");

    //auto start = std::chrono::steady_clock::now();
    //for (int i = 0; i < 1; i++) {
        //NaiveSuffixTree t(s);
    //}
    //auto end = std::chrono::steady_clock::now();

    //std::cout << std::chrono::duration<double, std::milli>(end-start).count() 
        //<< " ms" << std::endl;

    return 0;
}
