#ifndef NAIVESUFFIXTREE_H

#define NAIVESUFFIXTREE_H
#include "patterns.h"
#include <string>

class NaiveSuffixTree : public AbstractTree {
    public:
        NaiveSuffixTree(std::string str);
        void display();

        Node* root();
        const std::string text();
        Node *root_;
        std::string str;
    private:
        void display(Node *tmp_node, int depth);
        void build();
        void insert_suffix(int start, int end);
};

#endif /* end of include guard: NAIVESUFFIXTREE_H */
