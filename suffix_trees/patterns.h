#include <vector>
#ifndef PATTERNS_H
#define PATTERNS_H
#include <string>

/* Tree */
typedef struct node_ {
    std::vector<struct node_*> children;
    int start, end;
    int value;
} Node;


class AbstractTree {
    public:
        virtual Node* root() = 0;
        virtual const std::string text() = 0;
        virtual void display() = 0;
};


#endif /* end of include guard: PATTERNS_H */
