#include "SuffixTreeQuerier.h"
SuffixTreeQuerier::SuffixTreeQuerier(AbstractTree& tree) 
    : tree(tree) {

    }
SuffixTreeQuerier::location SuffixTreeQuerier::find(std::string str) {
    const std::string text = tree.text();
    Node *parent = tree.root();
    Node *next_node = tree.root();

    SuffixTreeQuerier::location loc(-2,-2);
    int matches = 0;
    int i = 0;
    while (parent->children.size() > 0) {
        for (auto it = parent->children.begin(); 
                it != parent->children.end(); ++it) {
            Node *child = *it;
            i = 0;
            while (matches + i < str.size()
                    && child->start+i <= child->end 
                    && str[matches + i] == text[child->start+i]) {
                i++;
            }
            matches += i;
            // Matched nodes with further children exactly
            if (matches == str.size()) {
                return SuffixTreeQuerier::location(child->value,child->value-1+str.size());
            }
            if (i > 0) {
                next_node = child;
                break;
            }
        }
        // Nothing found
        if (parent == next_node) {
            return SuffixTreeQuerier::location(-1,-1);
        }
        parent = next_node;
    }
    return loc;
}
