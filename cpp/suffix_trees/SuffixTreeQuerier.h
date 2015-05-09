#ifndef SUFFIXTREEQUERIER_H

#define SUFFIXTREEQUERIER_H

#include "patterns.h"

class SuffixTreeQuerier {
    public:
        typedef std::pair<int,int> location;
        SuffixTreeQuerier(AbstractTree &tree);
        location find(std::string str);

    private:
        AbstractTree &tree;
};

#endif /* end of include guard: SUFFIXTREEQUERIER_H */
